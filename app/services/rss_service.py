"""Service for RSS feed generation."""
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator

from app.config import settings
from app.models.schemas import PhraseData


class RSSService:
    """Handles RSS feed generation."""

    def generate_feed(self, phrase_data: PhraseData) -> str:
        """Generate RSS feed with the given phrase."""
        fg = FeedGenerator()
        fg.id(settings.RSS_ID)
        fg.title(settings.RSS_TITLE)
        fg.link(href=settings.RSS_LINK, rel="alternate")
        fg.link(href=settings.RSS_ID, rel="self")
        fg.description(settings.RSS_DESCRIPTION)
        fg.language(settings.RSS_LANGUAGE)
        fg.author(name=settings.RSS_AUTHOR_NAME, email=settings.RSS_AUTHOR_EMAIL)
        fg.managingEditor(f"{settings.RSS_AUTHOR_EMAIL} ({settings.RSS_AUTHOR_NAME})")
        fg.webMaster(f"{settings.RSS_AUTHOR_EMAIL} ({settings.RSS_AUTHOR_NAME})")

        # Add current phrase as entry
        today = datetime.now(timezone.utc)
        phrase_text = phrase_data.phrase
        phrase_author = phrase_data.author

        fe = fg.add_entry()
        fe.id(f'phrase-{today.strftime("%Y-%m-%d")}-{hash(phrase_text) % 10000}')
        fe.title(f'"{phrase_text}" - {phrase_author}')
        fe.link(href=f'{settings.RSS_LINK}/phrase/{today.strftime("%Y-%m-%d")}')
        fe.description(f'"{phrase_text}" - {phrase_author}')
        fe.pubDate(today)

        return fg.rss_str(pretty=True)