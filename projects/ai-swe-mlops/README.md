# ai-swe-mlops-project

## 1. Problem and Business Metric

**What the model solves:** an MLOps pipeline for classification tasks, covering data versioning with DVC, experiment tracking with MLflow, and a reproducible training/evaluation workflow.

**Business metric:** _to be defined per use case_ (e.g., false-positive reduction, precision uplift in automated decisions).

**Technical metric used as a proxy:** standard classification metrics (accuracy, F1, ROC-AUC) logged to MLflow on every run.

---

## 2. Architecture

Data flow and pipeline stages:

```
Ingestion  →  Processing  →  Training  →  Evaluation
  (raw)       (processed)    (models)     (reports)
```

- **Ingestion** — raw data in `data/raw/` (immutable, DVC-tracked).
- **Processing** — `src/preprocess.py` handles cleaning and feature engineering → `data/processed/`.
- **Training** — `src/train.py` trains the model, logs parameters/metrics/artifacts to MLflow, and saves the binary to `models/`.
- **Evaluation** — `src/evaluate.py` loads the model and emits metrics to `reports/`.

Orchestration: `dvc.yaml` + `params.yaml` make the pipeline reproducible via `dvc repro`. Experiments are tracked in `mlruns/` (MLflow local by default).

---

## 3. Prerequisites

- **Python** 3.10+
- **Git**
- **DVC** 3.x
- **MLflow** (installed via `requirements.txt` / `pyproject.toml`)

---

## 4. Installation and Setup

Explicit, reproducible instructions — do not skip any step:

```bash
# 1. Clone the repository
git clone https://github.com/<your-user>/neural-forge.git
cd neural-forge/projects/ai-swe-mlops

# 2. Install the project in editable mode with dev dependencies
pip install -e ".[dev]"

# 3. Pull DVC-versioned data
#    ESSENTIAL: without this step the project has no data.
dvc pull

# 4. Reproduce the full pipeline (preprocess → train → evaluate)
dvc repro
```

Useful additional commands:

```bash
# Run training manually (outside DVC)
python -m src.train --config configs/train_config.yaml

# Evaluate
python -m src.evaluate --config configs/train_config.yaml

# Launch MLflow UI
mlflow ui
```

---

## 5. Results

Current model performance on the test set:

| Metric | Value | Baseline | Δ |
|---|---|---|---|
| Accuracy | _TBD_ | _TBD_ | _TBD_ |
| F1       | _TBD_ | _TBD_ | _TBD_ |
| ROC-AUC  | _TBD_ | _TBD_ | _TBD_ |

Per-run metrics are available in the MLflow UI (`mlflow ui`) and exported reports live in `reports/`.

---

## Running Tests

```bash
pytest
```

## Configuration

All hyperparameters and pipeline settings live in `configs/train_config.yaml`. Values can be overridden via CLI args when invoking `src.train` or `src.evaluate`.

## Experiment Tracking

MLflow is configured locally by default (`mlruns/`). To use a remote server, set `MLFLOW_TRACKING_URI`.

## Data Versioning

Raw data is versioned with DVC. The DVC remote is an in-repo committed folder at `.dvc-store/ai-swe-mlops/` at the monorepo root — no credentials, no per-machine setup, CI works out of the box. See `docs/adr/0001-dvc-remote-strategy.md` for rationale and size budget.

When adding new data:

```bash
dvc add data/raw/<file>
git add data/raw/<file>.dvc .gitignore
dvc push
git add ../../.dvc-store/ai-swe-mlops
git commit -m "data: add new raw file"
```
