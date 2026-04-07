# Contributing

## Commit messages

This repository follows the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification. Every commit message must match:

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

**Allowed types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

**Examples:**

- `feat(training): add mixed-precision support`
- `fix: handle empty config path`
- `docs: add CONTRIBUTING guide`
- `refactor(data)!: drop legacy loader`

Breaking changes are indicated with `!` after the type/scope and/or a `BREAKING CHANGE:` footer.

### Enforcement

- **Locally** — a POSIX `commit-msg` hook lives in `.githooks/`. Enable it once per clone:

  ```bash
  git config core.hooksPath .githooks
  ```

  No Node or external dependencies required.

- **In CI** — [`commitlint`](https://commitlint.js.org/) runs on every push and pull request via `.github/workflows/commitlint.yml`, using the config in `commitlint.config.mjs`. Non-conforming commits will fail the check.

Keeping messages structured lets us auto-generate changelogs and drive semantic versioning from history alone.
