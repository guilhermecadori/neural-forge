ml-project



Use this for end-to-end ML / DL work



Examples:

* tabular training pipeline
* image classification project
* LLM finetuning / evaluation repo
* feature store experiment
* drift monitoring prototype



ml-project/

├─ src/                            # flat scripts — add prepare.py, train.py, evaluate.py etc. as needed

├─ configs/

│  ├─ data/

│  ├─ model/

│  ├─ training/

│  ├─ evaluation/

│  └─ experiments/

├─ tests/

│  ├─ unit/

│  ├─ integration/

│  ├─ smoke/

│  ├─ regression/

│  └─ fixtures/

├─ notebooks/                      # exploratory only; numbered <stage>.<step>-<slug>.ipynb

│  ├─ 1.0-eda-inicial.ipynb

│  ├─ 2.0-baseline.ipynb

│  └─ 3.0-error-analysis.ipynb

├─ scripts/                        # one-off utilities — add as needed

├─ data/                           # DVC-tracked; never committed to git

│  ├─ raw/                         # immutable source data — read-only, never edited in place

│  ├─ processed/                   # cleaned, validated, feature-engineered intermediates

│  └─ final/                       # model-ready splits (train/val/test) consumed by training

├─ models/                         # DVC-tracked; trained model binaries (.pkl, .pt, .h5, .onnx)

├─ artifacts/                      # run outputs; small files may be git-tracked, large ones DVC

│  ├─ reports/

│  ├─ figures/

│  └─ logs/

├─ docs/

│  ├─ architecture/

│  ├─ experiments/

│  ├─ model\_cards/

│  └─ adr/

├─ .github/workflows/

│  └─ ci.yml

├─ .gitignore

├─ .pre-commit-config.yaml

├─ Makefile

├─ pyproject.toml

├─ README.md

└─ docker-compose.yml



**What matters most here**

* src/ holds flat pipeline scripts (prepare.py, train.py, evaluate.py, etc.)
* DVC wires the stages together via dvc.yaml
* configs/ keeps experiments reproducible
* artifacts/ stores outputs from runs
* notebooks/ are exploratory only, not core pipeline logic
* monitoring/ lets you practice production-oriented MLE thinking early



**Data layout convention**

* `data/raw/` — source data, **immutable**. Never edit in place, never overwrite. If the source changes, version it as a new file.
* `data/processed/` — cleaned, validated, feature-engineered outputs of deterministic transforms over `raw/`. Reproducible from `raw/` + code.
* `data/final/` — model-ready train/val/test splits consumed directly by training code. Reproducible from `processed/` + code.
* All three directories are DVC-tracked, never committed to git. Only `.dvc` pointer files and pipeline metadata (`dvc.yaml`, `dvc.lock`, `params.yaml`) are committed.



**Notebook convention**

* Name notebooks `<stage>.<step>-<slug>.ipynb`, e.g. `1.0-eda-inicial.ipynb`, `2.1-feature-exploration.ipynb`.
* `<stage>` groups notebooks by phase (1 = EDA, 2 = features, 3 = modeling, 4 = evaluation, 5 = error analysis). `<step>` is a minor iteration within the stage.
* Notebooks are for exploration and communication only. Any logic worth keeping must be promoted into `src/<project>/` and imported back into the notebook.



**Data & model versioning (DVC)**

* `data/` and `models/` are tracked with DVC, not git.
* Each project owns its own `dvc.yaml` pipeline wiring `raw → processed → final → train → evaluate`.
* Model binaries (`.pkl`, `.pt`, `.h5`, `.onnx`, etc.) live under `models/` and are produced by pipeline stages — never manually dropped in.
* Remotes, caching, and the monorepo-wide DVC strategy are documented in the monorepo's ADR on DVC (`docs/adr/`). Do not hardcode personal paths in a project's `.dvc/config`.



**Rules for this template**

* all meaningful logic must live in src/ as flat scripts (prepare.py, train.py, evaluate.py, etc.)
* scripts/ is for one-off utilities that call code from src/, not reimplement it
* config must be explicit and versioned
* every model experiment should be reproducible
* evaluation should be first-class, not an afterthought
* This template is the most important one for you



**Because it is where you combine:**

* SWE structure
* MLE workflows
* DL training
* inference thinking
* monitoring thinking

