# Build Commands
- python -m pytest tests/ -v: Run tests
- python -m pip install -e .: Install package in editable mode
- dvc repro: Reproduce the full pipeline
- mlflow ui --port 5000: Start the MLflow UI

# Code Style
- Use type hints on all functions
- Follow PEP 8 conventions
- Use dataclasses or Pydantic for data models
- Docstrings in Google format

# Architecture
- MLflow for experiment tracking
- DVC for data and pipeline versioning
- pytest for unit tests
- Hydra or YAML for configuration

# Workflow
- Always run tests after code changes
- Commit frequently with descriptive messages
- Use dvc add for new datasets
