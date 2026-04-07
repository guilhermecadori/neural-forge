# ADR 0002: Mandatory .gitignore baseline for every project

- **Status:** Accepted
- **Date:** 2026-04-07
- **Scope:** `neural-forge` monorepo — the monorepo root and every
  subdirectory under `projects/`

## Context

The monorepo hosts multiple ML projects. Each project keeps its own
`.gitignore`, which is the right default (project-specific patterns differ:
framework caches, tool caches, experiment outputs). The wrong default is
**relying on every project to remember the same handful of patterns that
protect the repo from catastrophic mistakes**:

- committing secrets (`.env`, API keys, credentials);
- committing large binary datasets (GitHub rejects files > 100 MB and degrades
  badly on binary blobs long before that);
- committing local virtualenvs or `__pycache__` noise that ruins diffs.

Drift between project `.gitignore` files is almost guaranteed without
enforcement. A pattern missed once, in one project, can leak a credential
into git history — and rewriting history on a pushed public repo is
expensive and error-prone.

## Decision

### 1. A single baseline file is the source of truth

`templates/.gitignore-baseline` lists the non-negotiable patterns that every
`.gitignore` in the monorepo **must** contain. It is versioned alongside
the code. Changes to it go through a normal PR and should update this ADR if
the rationale shifts.

### 2. Scope of the requirement

The baseline patterns must appear verbatim in:

- the monorepo root `.gitignore`;
- every `projects/<name>/.gitignore`.

"Verbatim" means the exact string (one pattern per line) appears somewhere in
the target file. Targets are free to add **more** patterns — they just cannot
omit baseline ones. Order does not matter. Comments and blank lines in the
baseline are ignored for comparison purposes.

A project directory that exists but has no `.gitignore` at all is treated
as a baseline violation.

### 3. Enforcement is automated

Two layers:

1. **CI workflow** at `.github/workflows/gitignore-baseline.yml`. Runs on
   every push and pull request, fails the job if any target `.gitignore`
   is missing a baseline pattern, and prints exactly which patterns are
   missing from which files. This is the authoritative gate.
2. **Local pre-commit hook** (future addition). Same check, running before
   commit, so violations are caught before they reach CI.

Developers are not expected to run the check manually. CI is the backstop.

## Rationale

### Why a baseline instead of a shared ignore file

DVC, git, and most tools do support cascading / root-level ignore files. A
single root `.gitignore` would technically cover everything in the repo.
It was rejected because:

- **Per-project autonomy.** Each project already has project-specific ignore
  patterns (framework caches, MLflow runs, notebook checkpoints, model
  binaries unique to that stack). Those belong next to the project, not in a
  monorepo-global file.
- **Copyability.** Projects occasionally get extracted to standalone repos.
  A project-local `.gitignore` travels with them; a root-only one doesn't.
- **Explicitness beats inheritance.** Reading a project's `.gitignore` should
  tell you what's ignored, without having to remember a parent file exists.

### Why enforce via CI rather than trust convention

- **Drift is silent.** Missing a single line in a single file can leak a
  `.env` or a 200 MB CSV. The cost of the check is seconds; the cost of the
  mistake is rewriting history or rotating credentials.
- **Mechanical rule, mechanical check.** "File X contains string Y" is the
  simplest possible test. No judgment involved.

### Why "superset", not "exact match"

Projects legitimately need to ignore patterns the baseline doesn't care about
(MLflow runs, torch checkpoints, ruff caches, etc.). The baseline is a
**floor**, not a contract. Enforcing equality would punish normal project
hygiene.

## Consequences

### Positive

- Every project is guaranteed to ignore secrets, large binaries, venvs, and
  Python/Jupyter noise before CI ever runs.
- Adding a new protected pattern is a one-line edit to the baseline plus a
  one-line edit to each project's `.gitignore` — CI tells you exactly where.
- Onboarding a new project is a single copy of the baseline into the new
  project's `.gitignore`, plus whatever project-specific additions it needs.

### Negative / accepted trade-offs

- **Duplication.** The same patterns live in N+1 places. Deliberate: see
  "Why a baseline instead of a shared ignore file" above.
- **Baseline updates touch many files.** Adding a pattern means editing the
  root and every project. Acceptable because it is rare and CI flags any
  missed file.
- **CI can still only see patterns that are written down.** If a pattern
  needs to exist but isn't in the baseline yet, this ADR doesn't help. The
  mitigation is: when a new class of sensitive/large file is encountered,
  add it to the baseline *first*, then let CI propagate the requirement.

## How to apply this decision

### Adding a new project

1. Copy `templates/.gitignore-baseline` into
   `projects/<new-project>/.gitignore`.
2. Append any project-specific patterns below the baseline block.
3. Commit. CI verifies the baseline is intact.

### Updating the baseline

1. Edit `templates/.gitignore-baseline` with the new pattern.
2. Add the same pattern to the monorepo root `.gitignore` and every
   `projects/*/.gitignore`.
3. Update this ADR if the rationale for the new pattern is non-obvious.
4. Open a single PR containing all the file edits. CI will refuse to merge
   until every file is in sync.

## References

- Baseline file: `templates/.gitignore-baseline`
- Enforcement workflow: `.github/workflows/gitignore-baseline.yml`
- Related: `docs/adr/0001-dvc-remote-strategy.md` — why `data/` and model
  binaries go through DVC rather than git.
