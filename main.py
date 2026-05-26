# =============================================================================
# IMPORTS
# =============================================================================
# Import FastAPI to create our web application
from fastapi import FastAPI

# Import HTTPException to return structured error responses
from fastapi import HTTPException

# Import BaseModel from Pydantic to define request/response data schemas
from pydantic import BaseModel

# Import logging to track when endpoints are called (observability)
import logging

# Import uvicorn to run the server
import uvicorn

# Import joblib to load the trained ML model from disk
import joblib

# Import numpy to format input data for scikit-learn
import numpy as np

# Import asynccontextmanager to handle app startup/shutdown lifespan
from contextlib import asynccontextmanager

# Import AsyncGenerator to annotate the lifespan return type
from collections.abc import AsyncGenerator


# =============================================================================
# LOGGING SETUP
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# =============================================================================
# DATA MODELS
# =============================================================================

# Define the shape of data we expect from the client when they call /predict
class InferenceRequest(BaseModel):
    """
    Input schema for prediction requests.
    - feature1: a floating-point number (required)
    - feature2: a floating-point number (required)
    """
    feature1: float
    feature2: float


# Define the shape of data we will send back to the client
class InferenceResponse(BaseModel):
    """
    Output schema for prediction responses.
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
# APPLICATION LIFESPAN (Startup / Shutdown)
# =============================================================================
# The lifespan context manager runs code BEFORE the app accepts requests
# (on startup) and AFTER the app stops (on shutdown).
# This is where we load the trained ML model into memory.

# Global variable to hold the loaded model so all endpoints can access it
model = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    STEP 1: Load the trained model from disk before the app starts.
    STEP 2: Yield control to the application so it can handle requests.
    STEP 3: Clean up resources after the application shuts down.
    """
    # Allow the global model variable to be modified inside this function
    global model

    # --- STARTUP PHASE ---
    # Attempt to load the serialized model from the models/ directory
    try:
        # LOGGING: Inform the operator that model loading is starting
        logger.info("Loading ML model from models/model.joblib...")
        # Load the model file that was saved by train.py
        model = joblib.load("models/model.joblib")
        # LOGGING: Confirm the model loaded successfully
        logger.info("ML model loaded successfully")
    except Exception as e:
        # ERROR HANDLING: If the model file is missing or corrupt,
        # log the error and set model to None so /predict can respond gracefully
        logger.error("Failed to load ML model: %s", e)
        model = None

    # Yield control — the application runs here
    yield

    # --- SHUTDOWN PHASE ---
    # LOGGING: Inform the operator that the application is shutting down
    logger.info("Application shutting down. Model reference released.")


# =============================================================================
# APP INITIALIZATION
# =============================================================================
# Create the FastAPI application instance with the lifespan handler
app = FastAPI(
    title="ML Inference Service",
    description="A beginner-friendly API for making predictions with a real trained model",
    version="2.0.0",
    lifespan=lifespan,
)


# =============================================================================
# ENDPOINTS
# =============================================================================

# Health-check endpoint — lets clients know the service is running
@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Return {"status": "healthy"} to confirm the service is alive.
    """
    # LOGGING: Record that this endpoint was called (observability)
    logger.info("Health check endpoint was called")
    return HealthResponse(status="healthy")


# Prediction endpoint — accepts features and returns a real model prediction
@app.post("/predict", response_model=InferenceResponse)
async def predict(request_body: InferenceRequest) -> InferenceResponse:
    """
    Accept an InferenceRequest containing feature1 and feature2,
    then run the trained ML model and return the prediction.
    """
    # LOGGING: Record the incoming features for observability and debugging
    logger.info(
        "Prediction endpoint called with feature1=%s, feature2=%s",
        request_body.feature1,
        request_body.feature2,
    )

    # STEP 1: Verify that the model was loaded successfully during startup
    if model is None:
        # ERROR HANDLING: If the model failed to load, return a 503 error
        logger.error("Prediction request rejected: model is not loaded")
        raise HTTPException(
            status_code=503,
            detail="ML model is not available. Please try again later.",
        )

    # STEP 2: Convert the incoming features into a 2D numpy array
    # scikit-learn expects a 2D array where each row is one sample
    input_array = np.array([[request_body.feature1, request_body.feature2]])

    # STEP 3: Run the model's predict method inside a try/except block
    try:
        # Execute the prediction
        result = model.predict(input_array)
        # Extract the single scalar value from the result array
        prediction_value: float = float(result[0])
    except Exception as e:
        # ERROR HANDLING: If prediction fails, log and return a 500 error
        logger.error("Model prediction failed: %s", e)
        raise HTTPException(
            status_code=500,
            detail="Prediction computation failed.",
        )

    # LOGGING: Record the outgoing prediction for observability
    logger.info("Prediction result: %s", prediction_value)

    # Build and return the response
    return InferenceResponse(prediction=prediction_value)


# =============================================================================
# ENTRY POINT (for running directly with `python main.py`)
# =============================================================================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
