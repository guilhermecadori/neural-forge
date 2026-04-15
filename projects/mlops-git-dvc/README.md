# mlops-git-dvc

---

## 1. Problem and Business Metric

**What the project solves:** provides a reference scaffold for managing ML projects with Git and DVC, enforcing reproducible data versioning, experiment tracking, and a clean separation of concerns (source, tests, configs, notebooks, scripts, docs).

**Business metric:** N/A — this is a learning/reference project, not a production model.

**Technical metric used as a proxy:** N/A.

---

## 2. Architecture

Project layout (numbered directories enforce a canonical ordering):

```
1-src/project-1/   →  core logic (data, features, models, training, inference, evaluation, api)
2-tests/            →  unit, integration, smoke, regression
3-configs/          →  versioned hyperparameters and pipeline settings
4-notebooks/        →  exploration and inspection (not production logic)
5-scripts/          →  thin CLI entry points
6-docs/             →  design docs and ADRs
```

Guiding rules (from `1-RULES.md`):

- Core logic goes in `1-src/`, not notebooks.
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
