from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import hashlib
from pathlib import Path

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

def load_phrases():
    """Load phrases from file with format: 'phrase | author'"""
    phrases_file = Path(__file__).parent / "phrases.txt"
    
    if not phrases_file.exists():
        # Fallback phrases if file doesn't exist
        return [
            {"phrase": "¡Hoy es un gran día para aprender algo nuevo!", "author": "Anónimo"},
            {"phrase": "Cada momento es un nuevo comienzo.", "author": "Anónimo"},
            {"phrase": "Cree que puedes y ya estás a la mitad del camino.", "author": "Anónimo"},
        ]
    
    try:
        phrases = []
        with open(phrases_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # Support multiple formats: "phrase" - author, phrase | author, or just phrase
                    if '" - ' in line and line.startswith('"'):
                        # Format: "phrase" - author
                        quote_end = line.rfind('" - ')
                        if quote_end > 0:
                            phrase_text = line[1:quote_end]  # Remove opening quote
                            author = line[quote_end + 4:].strip()
                            # Remove any trailing emojis or special characters from author
                            author = author.split(' ⚔️')[0].split(' 🏛️')[0].split(' 📚')[0]
                            phrases.append({
                                "phrase": phrase_text,
                                "author": author
                            })
                        else:
                            # Fallback if parsing fails
                            phrases.append({
                                "phrase": line.strip(),
                                "author": "Anónimo"
                            })
                    elif '|' in line:
                        # Old format: phrase | author
                        phrase_text, author = line.split('|', 1)
                        phrases.append({
                            "phrase": phrase_text.strip(),
                            "author": author.strip()
                        })
                    else:
                        # Just phrase without author
                        phrases.append({
                            "phrase": line.strip(),
                            "author": "Anónimo"
                        })
        return phrases if phrases else [{"phrase": "No se encontraron frases.", "author": "Sistema"}]
    except Exception:
        # Fallback if file can't be read
        return [{"phrase": "Error al cargar frases. Intenta más tarde.", "author": "Sistema"}]

def get_daily_phrase():
    phrases = load_phrases()
    now = datetime.now()
    
    # Create 12-hour intervals: 00:00-11:59 (period 0) and 12:00-23:59 (period 1)
    period = 0 if now.hour < 12 else 1
    date_str = now.strftime("%Y-%m-%d")
    hash_input = f"{date_str}-{period}"
    
    phrase_index = int(hashlib.md5(hash_input.encode()).hexdigest(), 16) % len(phrases)
    return phrases[phrase_index]

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
