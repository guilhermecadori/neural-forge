python-package



Use this for reusable libraries and modules



Examples:

* config loader package
* evaluation package
* experiment tracking helpers
* model registry client
* feature engineering utilities



python-package/

├─ src/

│  └─ package\_name/

│     ├─ \_\_init\_\_.py

│     ├─ api/

│     │  └─ \_\_init\_\_.py

│     ├─ core/

│     │  ├─ \_\_init\_\_.py

│     │  ├─ types.py

│     │  ├─ exceptions.py

│     │  └─ constants.py

│     ├─ services/

│     │  └─ \_\_init\_\_.py

│     ├─ adapters/

│     │  └─ \_\_init\_\_.py

│     └─ utils/

│        └─ \_\_init\_\_.py

├─ tests/

│  ├─ unit/

│  ├─ integration/

│  └─ fixtures/

├─ docs/

│  ├─ usage/

│  ├─ architecture/

│  └─ adr/

├─ examples/

│  ├─ basic\_usage.py

│  └─ advanced\_usage.py

├─ scripts/

│  └─ check\_package.sh

├─ .github/workflows/

│  └─ ci.yml

├─ .gitignore

├─ .pre-commit-config.yaml

├─ CHANGELOG.md

├─ LICENSE

├─ Makefile

├─ pyproject.toml

└─ README.md



**What each folder means**

* api/ public interfaces you want users to call
* core/ domain objects, types, errors, internal abstractions
* services/ main business logic
* adapters/ integrations with filesystem, databases, cloud, third-party tools
* utils/ only truly generic helpers, keep this small
* examples/ runnable usage examples
* docs/adr/ design decisions for architecture evolution



**Rules for this template**

* keep the public API explicit
* avoid huge utils.py
* prefer small focused modules
* do not mix project-specific code into the package
* package should solve one clear problem



**Good first packages for you**

* mlcfg or ml\_config
* evalkit
* artifact\_store
* experiment\_utils

