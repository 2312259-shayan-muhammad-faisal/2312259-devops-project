# Use slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy and install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
