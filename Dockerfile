# ── Stage 1: Base image ──────────────────────────────────────────────────────
FROM python:3.11-slim

# Security: run as non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set working directory
WORKDIR /app

# Copy dependency manifest first (layer-caching optimisation)
COPY requirements.txt .

# Install dependencies (no cache to keep image lean)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app.py .
COPY tests/ ./tests/

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Run application
CMD ["python", "app.py"]
