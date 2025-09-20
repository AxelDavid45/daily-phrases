# Daily Phrase API (vibe coded)

A lightweight FastAPI service that provides daily inspirational phrases via REST API and RSS feed.

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t daily-phrase-api .
docker run -p 8000:8000 daily-phrase-api
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/phrase` - Get today's phrase as JSON
- `GET /rss` - RSS feed with daily phrase

## Usage

The API will be available at `http://localhost:8000`

Example RSS feed subscription: `http://localhost:8000/rss`