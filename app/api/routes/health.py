"""Health check and statistics routes."""
from fastapi import APIRouter, Depends

from app.models.schemas import WelcomeResponse, HealthResponse, StatsResponse
from app.services.phrase_service import PhraseService
from app.dependencies import get_phrase_service

router = APIRouter()


@router.get("/", response_model=WelcomeResponse)
async def root():
    """Welcome endpoint."""
    return WelcomeResponse(message="Bienvenido a la API de Frases Diarias")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy")


@router.get("/stats", response_model=StatsResponse)
async def get_stats(
    phrase_service: PhraseService = Depends(get_phrase_service)
):
    """Get statistics about phrase rotation."""
    return phrase_service.get_stats()