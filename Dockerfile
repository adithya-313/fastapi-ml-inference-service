# =============================================================================
# STAGE 1: BUILDER (Dependency Compilation)
# =============================================================================
# Use slim Python image as the foundation for building dependencies
FROM python:3.11-slim AS builder

# Prevent Python from writing .pyc files to disk and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /build

# Create a virtual environment to isolate dependencies cleanly
RUN python -m venv /opt/venv
# Make sure we use the virtual environment's binaries
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install them securely
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# STAGE 2: RUNTIME (Production Execution)
# =============================================================================
# Start fresh with a new slim image to discard build tools and caches
FROM python:3.11-slim AS runtime

# SECURITY: Create a non-root user and group to run the application
# This prevents the container process from having root privileges on the host
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Copy ONLY the compiled virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Ensure the runtime uses the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy the application code and assign ownership to the non-root user
COPY --chown=appuser:appgroup . .

# SECURITY: Switch execution context from root to our custom user
USER appuser

# Expose port for documentation and runtime mapping
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
