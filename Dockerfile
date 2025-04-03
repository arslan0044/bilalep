# ===========================
# STAGE 1: Build dependencies
# ===========================
FROM python:alpine AS builder

WORKDIR /app

# Set environment variables for Python optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VENV_PATH="/opt/venv"

# Install system dependencies (Alpine-compatible packages)
RUN apk update && \
    apk add --no-cache \
    build-base \
    postgresql-dev \
    && rm -rf /var/cache/apk/*

# Create and activate a virtual environment
RUN python -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ===========================
# STAGE 2: Final runtime image
# ===========================
FROM python:alpine

WORKDIR /app

# Environment variable for virtual environment
ENV VENV_PATH="/opt/venv" \
    PATH="/opt/venv/bin:$PATH"

# Install necessary system packages
RUN apk update && \
    apk add --no-cache \
    build-base \
    postgresql-dev \
    && rm -rf /var/cache/apk/*

# Copy virtual environment from builder stage
COPY --from=builder $VENV_PATH $VENV_PATH

# Copy project files
COPY . /app

# Create non-root user (Alpine-compatible)
RUN adduser -D appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose the application port
EXPOSE 8000

# Start the Django application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bilalep.wsgi:application", "--workers", "3"]