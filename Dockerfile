FROM python:3.11-slim

# Build argument for rotation frequency
ARG ROTATIONS_PER_DAY=2

# Set environment variable from build arg
ENV ROTATIONS_PER_DAY=${ROTATIONS_PER_DAY}

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py phrases.txt .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]