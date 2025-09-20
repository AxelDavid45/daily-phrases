# Daily Phrase API (VibeCoded)

A lightweight FastAPI service that provides daily inspirational phrases in Spanish via REST API and RSS feed.

## ✨ Features

- 🇪🇸 **Spanish phrases** with author attribution
- ⏰ **12-hour rotation** (00:00-11:59 and 12:00-23:59)
- 📚 **1M+ phrases** stored in SQLite database
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

# 1440 rotations (every minute - for testing)
docker build --build-arg ROTATIONS_PER_DAY=1440 -t daily-phrase-api .
```

## 🧮 How the Algorithm Works

The phrase selection uses **deterministic randomness** to ensure the same phrase appears globally at the same time:

### Step-by-Step Process

1. **Time Period Calculation**
   ```python
   # Example: ROTATIONS_PER_DAY = 1440 (every minute)
   minutes_per_period = (24 * 60) / 1440 = 1.0 minute per period
   
   # At 20:08 → current_minute_of_day = 20*60 + 8 = 1208
   period = int(1208 / 1.0) = 1208
   ```

2. **Hash Input Creation**
   ```python
   # Combines date + period for uniqueness
   hash_input = "2025-09-20-1208"
   ```

3. **Deterministic Index Generation**
   ```python
   # MD5 hash → large number → modulo to fit phrase count
   phrase_index = int(hashlib.md5(hash_input.encode()).hexdigest(), 16) % total_phrases
   ```

### Common Rotation Values

| `ROTATIONS_PER_DAY` | Minutes per Period | Description |
|---------------------|-------------------|-------------|
| `1` | 1440 minutes | Once per day |
| `2` | 720 minutes | Every 12 hours |
| `4` | 360 minutes | Every 6 hours |
| `24` | 60 minutes | Every hour |
| `1440` | 1 minute | Every minute (testing) |

**Why 1440?** There are exactly **1440 minutes in a day** (24 × 60), so `ROTATIONS_PER_DAY=1440` means one rotation per minute.

### Key Properties

✅ **Global Sync**: Everyone gets the same phrase at the same time  
✅ **No Coordination**: No shared state needed between instances  
✅ **Even Distribution**: Hash function spreads selections across all phrases  
✅ **Time-Based**: Automatically changes based on configured frequency

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

- **Image size**: ~314MB (includes SQLite database)
- **Base**: Python 3.11-slim
- **Dependencies**: FastAPI, Uvicorn, FeedGen, SQLite
- **Database**: 104MB SQLite with 1M+ phrases
- **Performance**: ~0.013-0.021s response time
- **Security**: Non-root user, health checks

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
http://daily-phrase.ademapps.dev/rss
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