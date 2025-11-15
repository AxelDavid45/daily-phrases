"""Application configuration settings."""
import os
from pathlib import Path


class Settings:
    """Application settings."""

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # API settings
    TITLE: str = "Daily Phrase API"
    VERSION: str = "1.0.0"

    # Phrase rotation settings
    ROTATIONS_PER_DAY: int = int(os.getenv('ROTATIONS_PER_DAY', '2'))

    # Database settings
    BASE_DIR: Path = Path(__file__).parent.parent
    DB_PATH: Path = BASE_DIR / "phrases.db"

    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]

    # RSS Feed settings
    RSS_ID: str = "https://daily-phrase.ademapps.dev/rss"
    RSS_LINK: str = "https://daily-phrase.ademapps.dev"
    RSS_TITLE: str = "Frase Diaria"
    RSS_DESCRIPTION: str = "Frases diarias inspiradoras para alegrar tu día"
    RSS_LANGUAGE: str = "es"
    RSS_AUTHOR_NAME: str = "Daily Phrase API"
    RSS_AUTHOR_EMAIL: str = "noreply@ademapps.dev"


settings = Settings()