from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check_evaluation():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict_valid_evaluation():
    # Use context manager to trigger the lifespan startup (model load)
    with TestClient(app) as client:
        payload = {"feature1": 10.0, "feature2": 20.0}
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        # Model is trained on y = (x1 * 2.0) + (x2 * 3.0)
        # For [10.0, 20.0]: (10 * 2) + (20 * 3) = 20 + 60 = 80
        assert response.json() == {"prediction": 80.0}


def test_predict_invalid_schema_evaluation():
    response = client.post("/predict", json={"feature1": "invalid_string"})
    assert response.status_code == 422  # Pydantic validation rejection
