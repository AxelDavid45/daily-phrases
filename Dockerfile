FROM python:3.11-slim

# Build argument for rotation frequency
ARG ROTATIONS_PER_DAY=2

# Set environment variable from build arg
ENV ROTATIONS_PER_DAY=${ROTATIONS_PER_DAY}

# Set production environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files and migration script
COPY main.py phrases.txt migrate_to_sqlite.py .

# Build SQLite database from phrases.txt
RUN python migrate_to_sqlite.py && \
    echo "✅ Database built successfully" && \
    ls -lh phrases.db && \
    rm phrases.txt migrate_to_sqlite.py

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --uid 1001 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]