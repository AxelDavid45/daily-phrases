"""Phrase API routes."""
from fastapi import APIRouter, Depends

from app.models.schemas import PhraseResponse
from app.services.phrase_service import PhraseService
from app.dependencies import get_phrase_service

router = APIRouter(prefix="/api")


@router.get("/phrase", response_model=PhraseResponse)
async def get_phrase(
    phrase_service: PhraseService = Depends(get_phrase_service)
):
    """Get current daily phrase."""
    phrase_data = phrase_service.get_current_phrase()
    return PhraseResponse(
        phrase=phrase_data.phrase,
        author=phrase_data.author
    )