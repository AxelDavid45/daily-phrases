# Daily Phrase API (VibeCoded)

A lightweight FastAPI service that provides daily inspirational phrases in Spanish via REST API and RSS feed.

## ✨ Features

- 🇪🇸 **Spanish phrases** with author attribution
- ⏰ **12-hour rotation** (00:00-11:59 and 12:00-23:59)
- 📚 **1M+ phrases** loaded from text file
- 📡 **RSS feed** with standards compliance
- 🐋 **Dockerized** for easy deployment
- 🔄 **Updatable** by simply replacing `phrases.txt`

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

### Docker (Recommended)

```bash
# With Docker Compose
docker-compose up --build

# Or manually
docker build -t daily-phrase-api .
docker run -p 8000:8000 daily-phrase-api

# Configure phrase rotation frequency during build
docker build --build-arg ROTATIONS_PER_DAY=4 -t daily-phrase-api .  # Changes every 6 hours
docker build --build-arg ROTATIONS_PER_DAY=1 -t daily-phrase-api .  # Changes once per day
docker build --build-arg ROTATIONS_PER_DAY=24 -t daily-phrase-api . # Changes every hour
```

## 📡 API Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Welcome message | JSON |
| `/health` | GET | Health check | JSON |
| `/api/phrase` | GET | Current phrase with author | JSON |
| `/stats` | GET | Rotation configuration and stats | JSON |
| `/rss` | GET | RSS feed | XML |

### Example Response `/api/phrase`

```json
{
  "phrase": "El tiempo es el arma del astuto y la perdición del indeciso.",
  "author": "Coronel Vornak"
}
```

## 📝 Phrase Format

The `phrases.txt` file supports multiple formats:

```text
"Inspirational phrase" - Author
Simple phrase | Author  
Phrase without author
```

### Updating Phrases

1. Edit the `phrases.txt` file
2. Restart the container/service
3. New phrases will be available immediately

## ⏰ Configurable Rotation

You can configure how many times per day phrases change during Docker build:

```bash
# Default: 2 rotations (every 12 hours)
docker build -t daily-phrase-api .

# 4 rotations (every 6 hours)  
docker build --build-arg ROTATIONS_PER_DAY=4 -t daily-phrase-api .

# 1 rotation (once per day)
docker build --build-arg ROTATIONS_PER_DAY=1 -t daily-phrase-api .

# 24 rotations (every hour)
docker build --build-arg ROTATIONS_PER_DAY=24 -t daily-phrase-api .
```

**How it works:**
- **Deterministic**: Same phrase during each period
- **Hash-based**: Uses date + period for consistent selection
- **Configurable**: Set `ROTATIONS_PER_DAY` from 1 to 24

## 🐋 Production Deployment

### Docker Compose

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    restart: unless-stopped
```

### Environment Variables

```bash
ENV=production  # Execution mode
```

## 📊 Technical Specifications

- **Image size**: ~214MB (optimized)
- **Base**: Python 3.11-slim
- **Dependencies**: FastAPI, Uvicorn, FeedGen
- **Capacity**: 1M+ phrases
- **Memory**: Efficient on-demand loading

## 🔧 Development

### Project Structure

```
daily-phrase/
├── main.py           # Main application
├── phrases.txt       # Phrase database
├── requirements.txt  # Python dependencies
├── Dockerfile        # Docker configuration
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Ensure tests pass
5. Submit a Pull Request

## 📱 RSS Feed Usage

Subscribe to the RSS feed in your favorite reader:

```
http://your-domain.com/rss
```

The feed includes:
- Title with phrase and author
- Complete description
- Spanish metadata
- Automatic updates every 12 hours

## 🚀 Demo

The API will be available at `http://localhost:8000`

Usage examples:
- RSS Feed: `http://localhost:8000/rss`
- JSON API: `http://localhost:8000/api/phrase`
- Health: `http://localhost:8000/health`

# Notes

This project was made as a proof of concept using claudecode.