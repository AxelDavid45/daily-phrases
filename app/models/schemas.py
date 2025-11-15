"""Pydantic models for request/response validation."""
from pydantic import BaseModel


class PhraseResponse(BaseModel):
    """Response model for phrase endpoint."""
    phrase: str
    author: str


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str


class WelcomeResponse(BaseModel):
    """Response model for root endpoint."""
    message: str


class DebugInfo(BaseModel):
    """Debug information for stats endpoint."""
    current_time: str
    current_minute_of_day: int
    current_period: int
    hash_input: str
    next_change_time: str


class StatsResponse(BaseModel):
    """Response model for stats endpoint."""
    rotations_per_day: int
    minutes_per_rotation: float
    total_phrases: int
    language: str
    debug: DebugInfo


class PhraseData(BaseModel):
    """Internal model for phrase data."""
    phrase: str
    author: str