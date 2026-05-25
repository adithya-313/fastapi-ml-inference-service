# FastAPI ML Inference Service

A production-ready, containerized FastAPI service for Machine Learning inference, demonstrating multi-stage Docker builds, non-root execution, health probing, and optional GPU passthrough.

## Architecture Highlights
- **Multi-stage Dockerfile:** Optimized build yielding minimal runtime footprints.
- **Security:** Enforced `appuser` non-root execution (Principle of Least Privilege).
- **Resilience:** Native Python healthchecks and Compose auto-restart policies.
- **Observability:** Centralized logging and Prometheus sidecar placeholder.

## Deployment Instructions

### Standard CPU Deployment (Default)
```bash
# Bring up the API and Prometheus placeholder in the background
docker compose up -d --build

# Verify container health state
docker inspect --format="{{json .State.Health.Status}}" ml-inference-api

# Check the health endpoint directly
curl http://localhost:8000/health

# Make a test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"feature1": 10.0, "feature2": 20.0}'

# Tear down
docker compose down
```

### GPU-Accelerated Deployment (Optional)
*Requires the NVIDIA Container Toolkit on the host.*

```bash
# Bring up the cluster using the GPU override configuration
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build

# Alternatively, via pure Docker:
docker run --gpus all -d -p 8000:8000 fastapi-ml-optimized:latest
```

## Endpoints
- `GET /health` — Verifies container liveness.
- `POST /predict` — Accepts inference requests.

## Storage
Models: ML model binaries are persisted in the Docker named volume `ml_model_volume`.
