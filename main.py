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
    return {"message": "Welcome to Daily Phrase API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

def get_daily_phrase():
    phrases = [
        "Today is a great day to learn something new!",
        "Every moment is a fresh beginning.",
        "Believe you can and you're halfway there.",
        "The best time to plant a tree was 20 years ago. The second best time is now.",
        "Your limitation—it's only your imagination.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
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
    fg.id('https://daily-phrase-api.com/rss')
    fg.title('Daily Phrase')
    fg.link(href='https://daily-phrase-api.com', rel='alternate')
    fg.link(href='https://daily-phrase-api.com/rss', rel='self')
    fg.description('Daily inspirational phrases to brighten your day')
    fg.language('en')
    fg.author(name='Daily Phrase API', email='noreply@daily-phrase-api.com')
    fg.managingEditor('noreply@daily-phrase-api.com (Daily Phrase API)')
    fg.webMaster('noreply@daily-phrase-api.com (Daily Phrase API)')
    
    today = datetime.now(timezone.utc)
    phrase = get_daily_phrase()
    
    fe = fg.add_entry()
    fe.id(f'phrase-{today.strftime("%Y-%m-%d")}-{hash(phrase) % 10000}')
    fe.title(f'Daily Phrase - {today.strftime("%B %d, %Y")}')
    fe.link(href=f'https://daily-phrase-api.com/phrase/{today.strftime("%Y-%m-%d")}')
    fe.description(phrase)
    fe.pubDate(today)
    
    rss_str = fg.rss_str(pretty=True)
    return Response(content=rss_str, media_type="application/rss+xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)