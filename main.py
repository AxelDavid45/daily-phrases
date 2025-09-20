from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import hashlib

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

def get_daily_phrase():
    phrases = [
        "¡Hoy es un gran día para aprender algo nuevo!",
        "Cada momento es un nuevo comienzo.",
        "Cree que puedes y ya estás a la mitad del camino.",
        "El mejor momento para plantar un árbol fue hace 20 años. El segundo mejor momento es ahora.",
        "Tu limitación, es solo tu imaginación.",
        "Empújate a ti mismo, porque nadie más lo hará por ti.",
        "Las grandes cosas nunca vienen de las zonas de confort.",
    ]
    today = datetime.now().date()
    phrase_index = int(hashlib.md5(str(today).encode()).hexdigest(), 16) % len(phrases)
    return phrases[phrase_index]

@app.get("/api/phrase")
async def get_phrase():
    return {"phrase": get_daily_phrase()}

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
    phrase = get_daily_phrase()

    fe = fg.add_entry()
    fe.id(f'phrase-{today.strftime("%Y-%m-%d")}-{hash(phrase) % 10000}')
    fe.title(f"{phrase}")
    fe.link(href=f'https://daily-phrase.ademapps.dev/phrase/{today.strftime("%Y-%m-%d")}')
    fe.description(phrase)
    fe.pubDate(today)

    rss_str = fg.rss_str(pretty=True)
    return Response(content=rss_str, media_type="application/rss+xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
