# neural-forge

A personal monorepo for exploring and experimenting with AI/ML software engineering at a systems level. It consolidates reusable packages, project scaffolds, and architectural references used to prototype, benchmark, and iterate on production-oriented ML workflows.

## Layout

- **projects/** — self-contained explorations
  - `ai-swe-mlops` — reference MLOps pipeline with DVC data versioning and MLflow experiment tracking
  - `automotive-performance` — architecture notes for an AI diagnostic and tuning assistant over FuelTech ECUs
  - `churn-prediction` — bank customer churn prediction with a DVC pipeline
  - `diesel-performance` — architecture notes for AURA, an edge AI diagnostic agent for diesel vehicles
  - `linux-docker-kubernetes` — Docker/Kubernetes course labs for deploying ML models
  - `mlops-git-dvc` — reference scaffold for a Git + DVC MLOps workflow
  - `template-project-structure` — mandatory scaffold to copy into new projects
- **templates/** — opinionated starters and shared conventions for ML projects, Python packages, service APIs, and benchmarking harnesses
- **experiments/** — sandbox for focused, short-lived investigations
- **docs/** — `architecture`, `adr` (architecture decision records), `notes`, and `study-plan`
- **scripts/** — repository-wide automation
- **tools/** — developer tooling

## Philosophy

The repo is organized around the idea that ML systems benefit from the same rigor as traditional software: clear boundaries between components, reproducible environments, explicit architectural decisions, and tight feedback loops between prototyping and production. Each subtree is designed to be explored independently while sharing conventions across the whole.

## Usage

```bash
git clone https://github.com/guilhermecadori/neural-forge.git
cd neural-forge
```

Individual projects and templates carry their own setup instructions.
