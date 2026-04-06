ml-project



Use this for end-to-end ML / DL work



Examples:

* tabular training pipeline
* image classification project
* LLM finetuning / evaluation repo
* feature store experiment
* drift monitoring prototype



ml-project/

├─ src/

│  └─ project\_name/

│     ├─ \_\_init\_\_.py

│     ├─ data/

│     │  ├─ datasets.py

│     │  ├─ loaders.py

│     │  ├─ schemas.py

│     │  └─ splits.py

│     ├─ features/

│     │  ├─ builders.py

│     │  ├─ transforms.py

│     │  └─ validators.py

│     ├─ models/

│     │  ├─ registry.py

│     │  ├─ base.py

│     │  └─ factories.py

│     ├─ training/

│     │  ├─ trainer.py

│     │  ├─ losses.py

│     │  ├─ optimizers.py

│     │  └─ callbacks.py

│     ├─ evaluation/

│     │  ├─ metrics.py

│     │  ├─ reports.py

│     │  ├─ plots.py

│     │  └─ validators.py

│     ├─ inference/

│     │  ├─ predictor.py

│     │  ├─ preprocess.py

│     │  └─ postprocess.py

│     ├─ pipelines/

│     │  ├─ train\_pipeline.py

│     │  ├─ eval\_pipeline.py

│     │  └─ batch\_inference\_pipeline.py

│     ├─ monitoring/

│     │  ├─ drift.py

│     │  ├─ data\_quality.py

│     │  └─ performance.py

│     ├─ config/

│     │  ├─ settings.py

│     │  └─ loader.py

│     └─ common/

│        ├─ io.py

│        ├─ logging.py

│        └─ seed.py

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

├─ notebooks/

│  ├─ 01\_eda.ipynb

│  ├─ 02\_baseline.ipynb

│  └─ 03\_error\_analysis.ipynb

├─ scripts/

│  ├─ run\_train.py

│  ├─ run\_eval.py

│  ├─ run\_batch\_inference.py

│  └─ export\_artifacts.py

├─ data/

│  ├─ raw/

│  ├─ interim/

│  ├─ processed/

│  └─ external/

├─ artifacts/

│  ├─ models/

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

* data/, training/, evaluation/, inference/ are separate on purpose
* pipelines/ wires the stages together
* configs/ keeps experiments reproducible
* artifacts/ stores outputs from runs
* notebooks/ are exploratory only, not core pipeline logic
* monitoring/ lets you practice production-oriented MLE thinking early



**Rules for this template**

* all meaningful logic must live in src/
* scripts should call code from src/, not reimplement it
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

