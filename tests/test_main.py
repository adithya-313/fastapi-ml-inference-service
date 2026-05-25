from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check_evaluation():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict_valid_evaluation():
    payload = {"feature1": 10.0, "feature2": 20.0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    # Evaluates the mock logic: (10.0 * 0.5) + (20.0 * 0.5) = 15.0
    assert response.json() == {"prediction": 15.0}


def test_predict_invalid_schema_evaluation():
    payload = {"feature1": "invalid_string"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Pydantic validation rejection
