"""Business logic for phrase selection and rotation."""
import hashlib
from datetime import datetime

from app.config import settings
from app.models.schemas import PhraseData, DebugInfo, StatsResponse
from app.repositories.phrase_repository import PhraseRepository


class PhraseService:
    """Handles phrase selection and rotation logic."""

    def __init__(self, repository: PhraseRepository = None):
        """Initialize service with repository."""
        self.repository = repository or PhraseRepository()

    def get_current_phrase(self) -> PhraseData:
        """Get the current phrase based on time and rotation settings."""
        now = datetime.now()

        # Calculate period based on configurable rotations per day
        minutes_per_period = (24 * 60) / settings.ROTATIONS_PER_DAY
        current_minute_of_day = now.hour * 60 + now.minute
        period = int(current_minute_of_day / minutes_per_period)

        # Create deterministic hash input
        date_str = now.strftime("%Y-%m-%d")
        hash_input = f"{date_str}-{period}"

        # Calculate phrase index using hash
        total_phrases = self.repository.get_phrase_count()
        phrase_index = int(hashlib.md5(hash_input.encode()).hexdigest(), 16) % total_phrases

        # Get specific phrase by index
        return self.repository.get_phrase_by_index(phrase_index)

    def get_stats(self) -> StatsResponse:
        """Get statistics about phrase rotation and current state."""
        now = datetime.now()
        minutes_per_period = (24 * 60) / settings.ROTATIONS_PER_DAY
        current_minute_of_day = now.hour * 60 + now.minute
        period = int(current_minute_of_day / minutes_per_period)
        date_str = now.strftime("%Y-%m-%d")
        hash_input = f"{date_str}-{period}"
        total_phrases = self.repository.get_phrase_count()

        # Calculate next change time
        next_period_minute = (period + 1) * minutes_per_period
        next_change_hour = int(next_period_minute // 60)
        next_change_minute = int(next_period_minute % 60)

        debug = DebugInfo(
            current_time=now.strftime("%H:%M:%S"),
            current_minute_of_day=current_minute_of_day,
            current_period=period,
            hash_input=hash_input,
            next_change_time=f"{next_change_hour:02d}:{next_change_minute:02d}"
        )

        return StatsResponse(
            rotations_per_day=settings.ROTATIONS_PER_DAY,
            minutes_per_rotation=minutes_per_period,
            total_phrases=total_phrases,
            language="Spanish",
            debug=debug
        )