repo-name/

├─ src/

├─ tests/

├─ docs/

├─ scripts/

├─ .github/workflows/ci.yml

├─ .gitignore

├─ .pre-commit-config.yaml

├─ pyproject.toml

├─ README.md

└─ Makefile



**Shared rules**

* src/ holds real code
* tests/ holds automated tests
* scripts/ holds thin command entry points only
* docs/ holds design notes, usage docs, ADRs, diagrams
* README.md explains purpose, setup, usage, status
* pyproject.toml manages packaging, tooling, dependencies
* Makefile gives standard commands like make test, make lint, make run
* .github/workflows/ci.yml runs lint, type checks, tests
* .pre-commit-config.yaml enforces formatting and quality before commits



**Shared engineering baseline**

I would standardize on:

* ruff for lint + formatting
* mypy or pyright for typing
* pytest for tests
* pydantic where typed config / schemas are useful
* uv or poetry for dependency management
* pre-commit hooks from day one

