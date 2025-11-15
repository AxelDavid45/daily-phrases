"""RSS feed routes."""
from fastapi import APIRouter, Response, Depends

from app.services.phrase_service import PhraseService
from app.services.rss_service import RSSService
from app.dependencies import get_phrase_service, get_rss_service

router = APIRouter()


@router.get("/rss", response_class=Response)
async def get_rss_feed(
    phrase_service: PhraseService = Depends(get_phrase_service),
    rss_service: RSSService = Depends(get_rss_service)
):
    """Get RSS feed with current phrase."""
    phrase_data = phrase_service.get_current_phrase()
    rss_content = rss_service.generate_feed(phrase_data)
    return Response(content=rss_content, media_type="application/rss+xml")