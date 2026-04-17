# mlops-git-dvc

---

## 1. Problem and Business Metric

**What the project solves:** provides a reference scaffold for managing ML projects with Git and DVC, enforcing reproducible data versioning, experiment tracking, and a clean separation of concerns (source, tests, configs, notebooks, scripts, docs).

**Business metric:** N/A — this is a learning/reference project, not a production model.

**Technical metric used as a proxy:** N/A.

---

## 2. Architecture

Project layout:

```
src/                →  core logic (data, features, models, training, inference, evaluation, api)
tests/              →  unit, integration, smoke, regression
configs/            →  versioned hyperparameters and pipeline settings
notebooks/          →  exploration and inspection (not production logic)
scripts/            →  thin CLI entry points
docs/               →  design docs and ADRs
```

Guiding rules (from `RULES.md`):

- Core logic goes in `src/`, not notebooks.
- Notebooks are for exploration, inspection, and explanation.
- Scripts are thin entry points, not where real logic lives.
- Configs are explicit and versioned.

---

## 3. Prerequisites

- **Git**
- **DVC** 3.x
- **Python** 3.11+

---

## 4. Installation and Setup

```bash
# 1. Clone the repository
git clone https://github.com/guilhermecadori/neural-forge.git
cd neural-forge/projects/mlops-git-dvc

# 2. Install the project and its dependencies
pip install -e .

# 3. Pull DVC-versioned data (if any stages are tracked)
#    ESSENTIAL: without this step DVC-tracked files stay as pointer stubs.
dvc pull

# 4. Reproduce the pipeline
dvc repro
```

---

## 5. Results

| Metric | Value | Baseline | Delta |
|---|---|---|---|
| N/A | N/A | N/A | N/A |

This project is a structural scaffold and learning reference — there are no model metrics to report.
