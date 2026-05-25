# FastAPI ML Inference Service

A beginner-friendly FastAPI service for ML inference with Docker containerization.

## Quick Start

### Build and Run with Docker

```bash
# Build the optimized multi-stage image
docker build -t fastapi-ml-optimized:latest .

# Run the container
docker run -d -p 8000:8000 --name ml-api fastapi-ml-optimized:latest

# Verify health
curl http://localhost:8000/health

# Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"feature1": 10.0, "feature2": 20.0}'

# Stop and remove
docker stop ml-api && docker rm ml-api
```

### Run Locally (without Docker)

```bash
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
.\venv\Scripts\python main.py
```

## Endpoints

- `GET /health` — Returns `{"status": "healthy"}`
- `POST /predict` — Accepts `{"feature1": float, "feature2": float}`, returns `{"prediction": float}`

## Image Size Comparison

| Image | Size (bytes) |
|---|---|
| `fastapi-ml-basic` (single-stage) | 54,621,222 |
| `fastapi-ml-optimized` (multi-stage + non-root) | 58,258,015 |

The multi-stage build isolates dependencies in a virtual environment and enforces non-root execution for improved security. The slight size increase is due to the bundled venv structure — significant savings appear when compiling native extensions (e.g., numpy, scikit-learn) where build tools can be discarded entirely in the runtime stage.
