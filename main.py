from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import hashlib
import os
import sqlite3
from pathlib import Path

# Get rotation frequency from environment variable (set during build)
ROTATIONS_PER_DAY = int(os.getenv('ROTATIONS_PER_DAY', '2'))  # Default: 2 (every 12 hours)

app = FastAPI(title="Daily Phrase API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Frases Diarias"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/stats")
async def get_stats():
    now = datetime.now()
    minutes_per_period = (24 * 60) / ROTATIONS_PER_DAY
    current_minute_of_day = now.hour * 60 + now.minute
    period = int(current_minute_of_day / minutes_per_period)
    date_str = now.strftime("%Y-%m-%d")
    hash_input = f"{date_str}-{period}"
    total_phrases = get_phrase_count()
    
    # Calculate next change time
    next_period_minute = (period + 1) * minutes_per_period
    next_change_hour = int(next_period_minute // 60)
    next_change_minute = int(next_period_minute % 60)
    
    return {
        "rotations_per_day": ROTATIONS_PER_DAY,
        "minutes_per_rotation": minutes_per_period,
        "total_phrases": total_phrases,
        "language": "Spanish",
        "debug": {
            "current_time": now.strftime("%H:%M:%S"),
            "current_minute_of_day": current_minute_of_day,
            "current_period": period,
            "hash_input": hash_input,
            "next_change_time": f"{next_change_hour:02d}:{next_change_minute:02d}"
        }
    }

def get_phrase_count():
    """Get total number of phrases in database"""
    db_path = Path(__file__).parent / "phrases.db"
    
    if not db_path.exists():
        return 3  # Fallback count
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM phrases')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception:
        return 3  # Fallback count

def get_phrase_by_index(index):
    """Get a specific phrase by index from database"""
    db_path = Path(__file__).parent / "phrases.db"
    
    # Fallback phrases if database doesn't exist
    fallback_phrases = [
        {"phrase": "¡Hoy es un gran día para aprender algo nuevo!", "author": "Anónimo"},
        {"phrase": "Cada momento es un nuevo comienzo.", "author": "Anónimo"},
        {"phrase": "Cree que puedes y ya estás a la mitad del camino.", "author": "Anónimo"},
    ]
    
    if not db_path.exists():
        return fallback_phrases[index % len(fallback_phrases)]
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get phrase by ID (SQLite IDs start at 1)
        cursor.execute('SELECT phrase, author FROM phrases WHERE id = ?', (index + 1,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {"phrase": result[0], "author": result[1]}
        else:
            # If index is out of range, fallback to modulo
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM phrases')
            total_count = cursor.fetchone()[0]
            actual_index = (index % total_count) + 1
            cursor.execute('SELECT phrase, author FROM phrases WHERE id = ?', (actual_index,))
            result = cursor.fetchone()
            conn.close()
            return {"phrase": result[0], "author": result[1]} if result else fallback_phrases[0]
            
    except Exception:
        # Fallback if database error
        return fallback_phrases[index % len(fallback_phrases)]

def get_daily_phrase():
    now = datetime.now()
    
    # Calculate period based on configurable rotations per day
    # Use minutes for better precision with high-frequency rotations
    minutes_per_period = (24 * 60) / ROTATIONS_PER_DAY
    current_minute_of_day = now.hour * 60 + now.minute
    period = int(current_minute_of_day / minutes_per_period)
    
    date_str = now.strftime("%Y-%m-%d")
    hash_input = f"{date_str}-{period}"
    
    # Get total phrase count and calculate index
    total_phrases = get_phrase_count()
    phrase_index = int(hashlib.md5(hash_input.encode()).hexdigest(), 16) % total_phrases
    
    # Get specific phrase by index
    return get_phrase_by_index(phrase_index)

@app.get("/api/phrase")
async def get_phrase():
    phrase_data = get_daily_phrase()
    return {
        "phrase": phrase_data["phrase"],
        "author": phrase_data["author"]
    }

@app.get("/rss", response_class=Response)
async def get_rss_feed():
    fg = FeedGenerator()
    fg.id("https://daily-phrase.ademapps.dev/rss")
    fg.title('Frase Diaria')
    fg.link(href="https://daily-phrase.ademapps.dev", rel="alternate")
    fg.link(href="https://daily-phrase.ademapps.dev/rss", rel="self")
    fg.description('Frases diarias inspiradoras para alegrar tu día')
    fg.language('es')
    fg.author(name='Daily Phrase API', email='noreply@ademapps.dev')
    fg.managingEditor("noreply@ademapps.dev (Daily Phrase API)")
    fg.webMaster("noreply@ademapps.dev (Daily Phrase API)")

    today = datetime.now(timezone.utc)
    phrase_data = get_daily_phrase()
    phrase_text = phrase_data["phrase"]
    phrase_author = phrase_data["author"]

    fe = fg.add_entry()
    fe.id(f'phrase-{today.strftime("%Y-%m-%d")}-{hash(phrase_text) % 10000}')
    fe.title(f'"{phrase_text}" - {phrase_author}')
    fe.link(href=f'https://daily-phrase.ademapps.dev/phrase/{today.strftime("%Y-%m-%d")}')
    fe.description(f'"{phrase_text}" - {phrase_author}')
    fe.pubDate(today)

    rss_str = fg.rss_str(pretty=True)
    return Response(content=rss_str, media_type="application/rss+xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
