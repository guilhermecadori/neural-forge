# churn-prediction

---

## 1. Problem and Business Metric

**What the model solves:** predicts whether a bank customer will churn, enabling proactive retention campaigns that reduce revenue loss from attrition.

**Business metric:** churn reduction rate — percentage of at-risk customers retained through targeted intervention.

**Technical metric used as a proxy:** accuracy (classification correctness on the held-out test set). Accuracy is a reasonable starting proxy given balanced-class assumptions; future iterations may switch to F1 or ROC-AUC for imbalanced scenarios.

---

## 2. Architecture

Data flow and pipeline stages (orchestrated by `dvc.yaml`):

```
Ingestion  →  Prepare  →  Train  →  Evaluate
  (raw)      (processed)  (model)   (metrics)
```

- **Ingestion** — raw churn dataset in `data/raw/churn.csv` (DVC-tracked).
- **Prepare** — `src/prepare.py` fills missing values (median imputation) and splits into train/test sets → `data/processed/`.
- **Train** — `src/train.py` fits a `RandomForestClassifier` (n_estimators=50), saves `models/model.pkl`, and writes `metrics.json`.

Reproducible via `dvc repro`.

---

## 3. Prerequisites

- **Python** 3.11+
- **Git**
- **DVC** 3.x
- **scikit-learn**, **pandas** (installed via requirements or pyproject.toml)

---

## 4. Installation and Setup

```bash
# 1. Clone the repository
git clone https://github.com/guilhermecadori/neural-forge.git
cd neural-forge/projects/churn-prediction

# 2. Install dependencies
pip install -e ".[dev]"

# 3. Pull DVC-versioned data
#    ESSENTIAL: without this step the project has no data.
dvc pull

# 4. Reproduce the full pipeline (prepare → train)
dvc repro
```

> **Why `dvc pull` matters:** without it, `data/` and `models/` stay empty — the git repo only contains the `.dvc` pointer files.

---

## 5. Results

Current model performance on the test set:

| Metric | Value | Baseline | Delta |
|---|---|---|---|
| Accuracy | 0.667 | N/A | N/A |

Model: `RandomForestClassifier(n_estimators=50, random_state=42)`.
