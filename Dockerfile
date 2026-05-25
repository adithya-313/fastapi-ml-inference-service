# =============================================================================
# BASE IMAGE
# =============================================================================
# Use Python 3.11 slim to get a lightweight Linux environment with Python installed
FROM python:3.11-slim

# =============================================================================
# WORKING DIRECTORY
# =============================================================================
# Set the directory inside the container where our application will live
WORKDIR /app

# =============================================================================
# DEPENDENCIES
# =============================================================================
# Copy only the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install the Python dependencies without storing pip cache to save space
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# APPLICATION CODE
# =============================================================================
# Copy the rest of our application code into the container
COPY . .

# =============================================================================
# EXECUTION
# =============================================================================
# Expose port 8000 so the host machine can talk to the container
EXPOSE 8000

# Command to run our FastAPI application using uvicorn when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
