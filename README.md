# Production FastAPI ML Inference Service

A rigorously engineered, production-ready FastAPI service for Machine Learning inference. This repository demonstrates the evolution from a basic script to a globally scalable, containerized architecture.

## 🏗️ System Architecture
- **API Layer:** FastAPI with strict Pydantic data contracts.
- **Containerization:** Multi-stage Docker build utilizing `python:3.11-slim`.
- **Security Context:** Enforced Principle of Least Privilege (Non-root `appuser` execution).
- **Resilience:** Native Python `HEALTHCHECK` probes and Compose auto-restart policies.
- **Hardware Abstraction:** Layered Compose architecture for optional NVIDIA GPU passthrough.
- **Continuous Integration:** Automated GitHub Actions pipeline for static analysis, type-safety, and unit testing.

## 🚀 Developer Experience (DX)
We use a `Makefile` to simplify operations.

**Local Development:**
```bash
make install    # Install all dependencies
make lint       # Run Ruff and Mypy
make test       # Run Pytest evaluation suite
make run        # Start the Uvicorn server locally
```

**Docker Orchestration:**
```bash
make docker-build # Build the optimized image
make docker-up    # Spin up the cluster in the background
make clean        # Tear down cluster, volumes, and cache files
```

## 🔌 API Endpoints

- `GET /health` — Verifies container liveness. Returns `{"status": "healthy"}`.
- `POST /predict` — Accepts inference requests.
  - Payload: `{"feature1": float, "feature2": float}`
  - Response: `{"prediction": float}`

## 🖥️ GPU-Accelerated Deployment (Optional)

If your host supports the NVIDIA Container Toolkit, you can bypass the standard CPU deployment and inject hardware acceleration:

```bash
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build
```
