# ADR 0001: DVC is per-project, with OneDrive as the personal remote

- **Status:** Accepted
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

## Decision

### 1. DVC is initialized per project, not at the monorepo root

Each project that needs data/model versioning runs `dvc init` in its own
subdirectory (e.g. `projects/ai-swe-mlops/`). The monorepo root has no
`.dvc/` directory and no top-level `dvc.yaml`.

### 2. The default personal remote is a folder inside the user's OneDrive

Projects declare a remote named `onedrive` pointing at
`<OneDrive>/DVCStore/neural-forge/<project-name>/`. OneDrive's desktop client
handles cloud sync transparently; DVC treats it as a plain local remote.

### 3. Machine-specific paths live in `.dvc/config.local`, not `.dvc/config`

The committed `.dvc/config` declares the `onedrive` remote as the default but
**does not** set its `url`. The absolute filesystem path is set in
`.dvc/config.local`, which DVC's `.dvc/.gitignore` excludes from version
control. This keeps personal paths, usernames, and drive letters out of the
public repo.

## Rationale

### Why per-project DVC

- **Blast radius.** A single root-level `.dvc/` would couple unrelated
  artifacts (tutorial data, real models, throwaway experiments) into one
  cache and one lock file. Failure in one project's pipeline would block
  others.
- **Remote flexibility.** Per-project config lets each project point at the
  storage that fits its data volume and sensitivity. One project can use
  OneDrive, another can later switch to S3 without affecting the rest.
- **Matches DVC's design.** DVC's pipeline, params, and lock mechanics are
  scoped to a working tree. Forcing a single root usually ends in an un-forcing
  migration later.
- **Experiments stay cheap.** Code in `experiments/` should not be dragged
  into DVC bookkeeping.

### Why OneDrive as the personal remote

- **Zero credentials, zero extras.** No `dvc[s3]`, `dvc[azure]`, no access
  keys in config, no risk of leaking secrets via a public `.dvc/config`.
- **Already paid for and already syncing.** No additional cost or
  infrastructure for personal work.
- **Cross-machine sync for free.** OneDrive syncs `DVCStore/` across the
  author's devices automatically.
- **Not suitable for CI or collaborators.** GitHub Actions runners have no
  OneDrive mount. This is acknowledged as a limitation, not a flaw — see
  Consequences.

### Why `.dvc/config.local` instead of an env-var interpolation

DVC's local-remote URLs do **not** expand environment variables like
`${ONEDRIVE_DVC}`. The CLI treats such strings as literal path segments. The
supported, documented mechanism for per-machine overrides is
`.dvc/config.local`, which DVC auto-excludes from git on `dvc init`. It is
the canonical solution and requires no workarounds.

## Consequences

### Positive

- The public `.dvc/config` contains no usernames, drive letters, or credentials.
- Each project can evolve its storage strategy independently.
- Onboarding a second machine is a matter of setting one value in
  `config.local` — no repo changes, no git churn.
- The decision is reversible: projects that outgrow OneDrive can add an S3
  or Azure remote alongside or instead, without affecting others.

### Negative / accepted trade-offs

- **CI cannot `dvc pull`** from the OneDrive remote. Any project that needs
  CI to reproduce pipelines end-to-end must add a second remote backed by
  object storage. This is accepted until a project actually needs CI
  reproduction.
- **Concurrent pushes from two machines before OneDrive finishes syncing**
  can cause sync conflicts. Acceptable for solo workflow; a real cloud
  remote would be required for multi-writer scenarios.
- **OneDrive Files-On-Demand** may mark rarely-used cache files as
  cloud-only, causing transparent re-downloads on access. Functional, but
  slower than a fully materialized local cache.
- **Each developer must set their own `config.local`** once per clone.
  Documented in the project README and in `scripts/dvc-bootstrap.sh`.

## How to apply this decision to a new project

```bash
cd projects/<new-project>
dvc init
# Commit the .dvc/ scaffolding DVC creates.

# Register the default remote (no URL — that lives in config.local).
dvc remote add -d onedrive placeholder
# Then edit .dvc/config to remove the url line, leaving only the remote
# declaration. Or use the bootstrap script:
../../scripts/dvc-bootstrap.sh <new-project>
```

The bootstrap script at `scripts/dvc-bootstrap.sh` automates the above.

## References

- DVC docs: [Remote storage](https://dvc.org/doc/user-guide/data-management/remote-storage)
- DVC docs: [`config.local`](https://dvc.org/doc/command-reference/config#local)
- Monorepo ML project template: `templates/ml-project.md`
