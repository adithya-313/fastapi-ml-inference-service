# FastAPI ML Inference Service

A rigorously engineered, containerized FastAPI microservice for Machine Learning inference. This repository prioritizes architectural resilience, security, and developer experience (DX) over naive implementations.

## 🏗️ System Architecture & Engineering Standards

* **Application Layer:** FastAPI with strict Pydantic data contracts. Model loading is decoupled from request execution via ASGI `lifespan` context managers to prevent blocking I/O on startup.
* **Containerization:** Multi-stage Docker build utilizing `python:3.11-slim`.
* **Security Context:** Enforced Principle of Least Privilege. The container drops root privileges and executes as a non-root `appuser`.
* **Resilience:** Zero-dependency cluster healing. Utilizes native Python `HEALTHCHECK` probes to prevent reliance on external binaries like `curl`.
* **Continuous Integration:** Automated GitHub Actions pipeline enforcing static analysis (Ruff), strict type-safety (Mypy), and unit testing (Pytest).

## Operations & Empirical Footprint

Integrating a functional `scikit-learn` model fundamentally alters the physics of the container due to heavy C-extensions (`numpy`, `scipy`). 

| Metric | System Reality | Architectural Choice |
| :--- | :--- | :--- |
| **Container Footprint** | **785.0 MB** | Represents the stable floor for Debian-slim + Scipy wheels. Alpine Linux was rejected to avoid `musl` libc compilation hazards. |
| **Boot Resilience** | **Fails Fast** | Model loads via ASGI Lifespan before the port binds. Corrupt or missing models crash the pod immediately, preventing runtime silent failures. |
| **Compute Constraints** | **CPU-Bound** | The current Scikit-Learn model executes strictly on CPU. The included `docker-compose.gpu.yml` passthrough configuration is infrastructure-ready for future tensor-based upgrades (PyTorch/TensorFlow). |

## 🚀 Developer Experience (DX)

A `Makefile` governs local operations to ensure frictionless onboarding.

```bash
make install      # Install all local dependencies (requirements.txt)
make lint         # Execute Ruff (linting) and Mypy (strict typing)
make test         # Run the Pytest evaluation suite with coverage
make run          # Start the Uvicorn ASGI server locally

make docker-build # Compile the multi-stage Docker image
make docker-up    # Spin up the Compose cluster in the background
make clean        # Tear down cluster, volumes, and clear cache files
```

## 🔌 API Contracts

**GET /health**
Liveness probe. Returns {"status": "healthy"}.

**POST /predict**
Accepts inference requests.

Payload: {"feature1": float, "feature2": float}

Response: {"prediction": float}
