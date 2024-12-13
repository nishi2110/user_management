# Build stage
FROM python:3.12-bookworm as base
WORKDIR /myapp

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim-bookworm as final
WORKDIR /myapp

# Install only necessary runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libc-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages and application code
COPY --from=base /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY . .

# Set environment variables
ENV PYTHONPATH=/myapp
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["uvicorn", "myapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
