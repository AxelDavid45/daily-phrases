"""FastAPI dependencies for dependency injection."""
from app.services.phrase_service import PhraseService
from app.services.rss_service import RSSService


def get_phrase_service() -> PhraseService:
    """Get phrase service instance."""
    return PhraseService()


def get_rss_service() -> RSSService:
    """Get RSS service instance."""
    return RSSService()