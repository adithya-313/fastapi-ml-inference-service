# =============================================================================
# IMPORTS
# =============================================================================
# Import FastAPI to create our web application
from fastapi import FastAPI

# Import HTTPException to return custom error responses
from fastapi import HTTPException

# Import BaseModel from Pydantic to define request/response data schemas
from pydantic import BaseModel

# Import logging to track when endpoints are called (observability)
import logging

# Import uvicorn to run the server
import uvicorn


# =============================================================================
# LOGGING SETUP
# =============================================================================
# Configure logging so we can see timestamped messages in the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Create a logger instance for this module
logger = logging.getLogger(__name__)


# =============================================================================
# DATA MODELS
# =============================================================================
# Define the shape of data we expect from the client when they call /predict
class InferenceRequest(BaseModel):
    """
    This model tells FastAPI exactly what fields to expect in the request body.
    - feature1: a floating-point number (required)
    - feature2: a floating-point number (required)
    """
    feature1: float
    feature2: float


# Define the shape of data we will send back to the client
class InferenceResponse(BaseModel):
    """
    This model ensures the response always has a consistent structure.
    - prediction: the result our model computed
    """
    prediction: float


# Define a reusable health response structure
class HealthResponse(BaseModel):
    """
    Simple status field for the health-check endpoint.
    """
    status: str


# =============================================================================
# APP INITIALIZATION
# =============================================================================
# Create the FastAPI application instance
app = FastAPI(
    title="ML Inference Service",
    description="A beginner-friendly API for making predictions",
    version="1.0.0",
)


# =============================================================================
# ENDPOINTS
# =============================================================================
# Health-check endpoint — lets clients know the service is running
@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Return {"status": "healthy"} to confirm the service is alive.
    This is the first endpoint a client should call to verify connectivity.
    """
    # Log that someone hit this endpoint (observability)
    logger.info("Health check endpoint was called")

    # Build and return the response
    return HealthResponse(status="healthy")


# Prediction endpoint — accepts features and returns a mock prediction
@app.post("/predict", response_model=InferenceResponse)
async def predict(request_body: InferenceRequest) -> InferenceResponse:
    """
    Accept an InferenceRequest containing feature1 and feature2,
    then return a mock prediction value.
    In a real service this is where you would run your ML model.
    """
    # Log the incoming request for observability and debugging
    logger.info(
        "Prediction endpoint called with feature1=%s, feature2=%s",
        request_body.feature1,
        request_body.feature2,
    )

    # --- Mock model logic ---
    # Replace this block with your actual ML model inference code.
    # For now we simply compute: prediction = feature1 * 0.5 + feature2 * 0.5
    result: float = (request_body.feature1 * 0.5) + (request_body.feature2 * 0.5)
    # ------------------------

    # Build and return the response
    return InferenceResponse(prediction=result)


# =============================================================================
# ENTRY POINT (for running directly with `python main.py`)
# =============================================================================
# When this file is executed directly, start the Uvicorn development server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
