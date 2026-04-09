# <Project Name>

> **Template README for Git + DVC ML projects.**
> Copy this file into new projects and replace every `<...>` placeholder.
> All five sections below are **mandatory** — do not remove any of them.

---

## 1. Problem and Business Metric

**What the model solves:** <describe the problem in 1–3 sentences, in business vocabulary, not model vocabulary>.

**Business metric:** <e.g., churn reduction of X%, conversion uplift of Y bps, estimated savings of $Z/month>.

**Technical metric used as a proxy:** <e.g., ROC-AUC, F1, MAE> — justify why it reflects the business metric.

---

## 2. Architecture

Data flow and pipeline stages:

```
Ingestion  →  Processing  →  Features  →  Training  →  Evaluation  →  Inference
  (raw)       (processed)    (final)      (models)     (reports)      (predictor)
```

- **Ingestion** — `src/<project>/data/` loads raw sources into `data/raw/` (immutable, DVC-tracked).
- **Processing** — deterministically transforms `raw/` → `processed/`.
- **Features** — builds `data/final/` (train/val/test splits) from `processed/`.
- **Training** — `src/<project>/training/` produces artifacts in `models/` (DVC-tracked).
- **Evaluation** — `src/<project>/evaluation/` generates metrics and reports in `artifacts/reports/`.
- **Inference** — `src/<project>/inference/` packages the model for batch or online prediction.

Orchestration via `dvc.yaml` (reproducible) and/or `src/<project>/pipelines/`.

---

## 3. Prerequisites

- **Python** <version, e.g., 3.11+>
- **Git**
- **DVC** <version, e.g., 3.x>
- <other system dependencies, e.g., Docker, CUDA, make>

---

## 4. Installation and Setup

Explicit, reproducible instructions — do not skip any step:

```bash
# 1. Clone the repository
git clone https://github.com/<your-user>/<project>.git
cd <project>

# 2. Install dependencies
pip install -r requirements.txt
# or: pip install -e ".[dev]"

# 3. Pull DVC-versioned data
#    ESSENTIAL: without this step the project has no data.
dvc pull

# 4. Reproduce the full pipeline (raw → processed → final → train → evaluate)
dvc repro
```

> **Why `dvc pull` matters:** without it, `data/` and `models/` stay empty — the git repo only contains the `.dvc` pointer files. Including this step explicitly signals maturity in professional data management.

---

## 5. Results

Current model performance on the test set:

| Metric | Value | Baseline | Δ |
|---|---|---|---|
| <metric 1, e.g., ROC-AUC> | <0.00> | <0.00> | <+0.00> |
| <metric 2, e.g., F1>      | <0.00> | <0.00> | <+0.00> |
| <business metric>         | <0.00> | <0.00> | <+0.00> |

<Optional: figure in `artifacts/figures/` — ROC curve, confusion matrix, calibration plot, etc.>

Full report: [`artifacts/reports/<latest>.md`](artifacts/reports/)
