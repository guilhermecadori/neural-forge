# linux-docker-kubernetes

---

## 1. Problem and Business Metric

**What the project solves:** packages ML models as containerized microservices and deploys them to a Kubernetes cluster, enabling scalable, zero-downtime inference in production.

**Business metric:** deployment lead time (minutes from merged commit to live endpoint) and service availability (target 99.9% uptime).

**Technical metrics used as proxies:** container build time, pod startup latency, rolling-update success rate, and p95 inference latency.

---

## 2. Architecture

Deployment flow:

```
Source Code  ->  Docker Build  ->  Container Registry  ->  Kubernetes Cluster
  (src/)        (Dockerfile)       (ghcr.io / ECR)        (k8s manifests)
```

- **Docker Build** — multi-stage `Dockerfile` produces a minimal inference image with pinned dependencies.
- **Container Registry** — images are tagged by git SHA and pushed via CI.
- **Kubernetes Manifests** — `k8s/` contains Deployment, Service, Ingress, HPA, and ConfigMap resources.
- **Helm / Kustomize** — templated overlays for dev, staging, and production environments.
- **Health Checks** — liveness and readiness probes ensure only healthy pods receive traffic.
- **Scaling** — Horizontal Pod Autoscaler adjusts replicas based on CPU/memory or custom metrics.

---

## 3. Prerequisites

- **Linux** (Ubuntu 22.04+ or WSL2)
- **Docker** 24.x+
- **kubectl** 1.28+
- **Minikube** or a managed Kubernetes cluster (EKS, GKE, AKS)
- **Helm** 3.x (optional, for templated deployments)
- **Git**
- **Python** 3.11+

---

## 4. Installation and Setup

```bash
# 1. Clone the repository
git clone https://github.com/guilhermecadori/neural-forge.git
cd neural-forge/projects/linux-docker-kubernetes

# 2. Build the Docker image
docker build -t neural-forge-serve:latest .

# 3. Run locally
docker run -p 8080:8080 neural-forge-serve:latest

# 4. Deploy to Kubernetes (Minikube example)
minikube start
kubectl apply -f k8s/

# 5. Verify the deployment
kubectl get pods
kubectl get svc
```

> **Why containers matter:** packaging the model and its dependencies into an immutable image eliminates "works on my machine" issues and enables reproducible deployments across environments.

---

## 5. Results

| Metric | Target | Current | Status |
|---|---|---|---|
| Deployment lead time | < 5 min | N/A | N/A |
| p95 inference latency | < 200 ms | N/A | N/A |
| Service availability | 99.9% | N/A | N/A |
| Pod cold-start time | < 30 s | N/A | N/A |
