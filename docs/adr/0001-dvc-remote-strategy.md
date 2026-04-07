# ADR 0001: DVC is per-project, with an in-repo local store as the remote

- **Status:** Accepted (supersedes the OneDrive variant of this ADR)
- **Date:** 2026-04-07
- **Scope:** `neural-forge` monorepo

## Context

The `neural-forge` monorepo hosts multiple independent ML projects under
`projects/` that need to version datasets, pipelines, and model binaries. Git
alone is inadequate for these artifacts. DVC is the chosen tool.

Two orthogonal decisions had to be made:

1. **Where does DVC live in the monorepo?** Root-level (one `.dvc/` governing
   the whole repo) or per-project (each project under `projects/` is its own
   DVC repo)?
2. **What backs the remote?** Local filesystem, personal cloud (OneDrive,
   GDrive), or a proper object store (S3, Azure Blob, GCS)?

This monorepo is a solo learning environment. Datasets are small (sample-sized,
tutorial-sized), CI reproducibility matters more than cross-machine cloud sync,
and keeping credentials and machine-specific paths out of the public repo is a
hard constraint.

## Decision

### 1. DVC is initialized per project, not at the monorepo root

Each project that needs data/model versioning runs `dvc init` in its own
subdirectory (e.g. `projects/ai-swe-mlops/`). The monorepo root has no
`.dvc/` directory and no top-level `dvc.yaml`.

### 2. The default remote is a committed folder at the monorepo root

A single directory `.dvc-store/` lives at the monorepo root and is **committed
to git**. Each project declares a default remote named `local` pointing at
`.dvc-store/<project-name>/` via a repo-relative path. DVC resolves relative
remote URLs against the `.dvc/config` file that declares them, so the path
`../../../.dvc-store/<project-name>` resolves identically on every clone,
every machine, and every CI runner.

No `.dvc/config.local`. No environment variables. No per-machine setup. No
cloud credentials. `git clone` is all the setup any developer or CI job needs.

### 3. Small data only

Because the DVC store is committed to git, its contents count against repo
size. This strategy is explicitly scoped to learning-sized artifacts. Any
project whose `.dvc-store/` contribution passes roughly 100 MB should migrate
to object storage (S3 / Azure Blob / GCS) as a second, primary remote — see
"When to outgrow this" below.

## Rationale

### Why per-project DVC

- **Blast radius.** A single root-level `.dvc/` would couple unrelated
  artifacts into one cache and one lock file. Failure in one project's
  pipeline would block others.
- **Remote flexibility.** Per-project config lets each project point at the
  storage that fits its data volume. One project can use the in-repo store,
  another can later switch to S3 without affecting the rest.
- **Matches DVC's design.** DVC's pipeline, params, and lock mechanics are
  scoped to a working tree.

### Why an in-repo committed store

- **CI works out of the box.** GitHub Actions clones the repo and already has
  the data; `dvc pull` is either a no-op or a local-filesystem copy. No
  credentials to provision, no second remote to add later.
- **Zero credentials, zero extras.** No `dvc[s3]`, no access keys, no
  OneDrive path leakage, no sync conflicts.
- **Fully reproducible across clones.** The same commit always resolves to
  the same data on every machine — no "works on my laptop because OneDrive
  finished syncing."
- **Solo-friendly.** Single source of truth, no cross-machine sync
  coordination, no stale caches.
- **Reversible.** If any project outgrows the size budget, add an object-store
  remote and make it the default; leave the in-repo `local` remote alongside
  as a fallback or delete it.

### Why not OneDrive (previous decision)

An earlier version of this ADR used OneDrive as a personal remote via a
git-ignored `.dvc/config.local`. It was rejected because:

- **CI could not `dvc pull`** — GitHub runners have no OneDrive mount. The
  workflow had to manually stub data or skip reproducibility checks.
- **Machine-specific setup** — every clone required exporting `ONEDRIVE_DVC`
  and running a bootstrap script before DVC commands worked.
- **Sync-race hazards** — concurrent pushes from two machines before OneDrive
  finished syncing could corrupt the remote.

Given the data sizes involved here, those costs outweigh the "cloud-backed"
benefit OneDrive was supposed to provide.

## Consequences

### Positive

- `git clone` is the only setup. No bootstrap, no env vars, no credentials.
- CI reproduces pipelines end-to-end with no extra infrastructure.
- `.dvc/config` is fully committed and portable — no `config.local`.
- Each project can still evolve its storage strategy independently (add S3,
  switch defaults, etc.) without touching other projects.

### Negative / accepted trade-offs

- **Repo size grows with tracked data.** This is the core cost. Datasets
  measured in hundreds of MB or more do not belong in `.dvc-store/`.
- **No cross-machine sync beyond git.** Not relevant for solo workflow; a
  cloud remote would be required for multi-writer scenarios or very large
  datasets.
- **No deduplication across projects.** Each project's chunk of the store is
  independent. Acceptable because projects are independent by design.

## When to outgrow this

Migrate a project to object storage when **any** of the following is true:

- Its `.dvc-store/<project>/` folder approaches 100 MB or meaningfully slows
  down `git clone` / `git gc`.
- The project starts collaborating with non-local contributors who should not
  pull large binaries just to work on code.
- Sensitivity or licensing makes committing the data to a git history
  inappropriate.

Migration recipe:

```bash
cd projects/<name>
dvc remote add -d s3remote s3://<bucket>/<prefix>
dvc push -r s3remote
# Optionally keep the 'local' remote as a fallback, or remove it and purge
# .dvc-store/<name>/ from the repo via git filter-repo.
```

## How to apply this decision to a new project

Use the bootstrap script:

```bash
scripts/dvc-bootstrap.sh projects/<new-project>
```

It runs `dvc init`, writes a committed `.dvc/config` with the `local` remote
declared at `../../../.dvc-store/<new-project>`, and creates the matching
folder under `.dvc-store/`.

## References

- DVC docs: [Remote storage](https://dvc.org/doc/user-guide/data-management/remote-storage)
- Monorepo ML project template: `templates/ml-project.md`
