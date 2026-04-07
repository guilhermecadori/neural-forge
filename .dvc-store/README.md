# .dvc-store

Committed, in-repo DVC remote for every project in this monorepo.

Each subfolder is the `local` remote for the project of the same name.
Project `.dvc/config` files reference this directory via the repo-relative
URL `../../../.dvc-store/<project-name>`, which DVC resolves against the
`.dvc/config` file itself — so it works on any clone, any machine, any CI
runner, with no per-machine setup.

**Do not put raw files here by hand.** Contents are managed by `dvc push` /
`dvc pull`. The store holds DVC-hashed chunks, not human-readable data.

**Size budget.** This directory is part of the git history. Keep each
project's slice well under ~100 MB. A project whose data outgrows that
budget should migrate to an object-store remote (S3, Azure Blob, GCS) —
see `docs/adr/0001-dvc-remote-strategy.md` for the migration recipe.
