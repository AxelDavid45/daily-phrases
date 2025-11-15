"""Repository for phrase data access."""
import sqlite3
from pathlib import Path
from typing import Optional

from app.config import settings
from app.models.schemas import PhraseData


class PhraseRepository:
    """Handles database operations for phrases."""

    def __init__(self, db_path: Path = settings.DB_PATH):
        """Initialize repository with database path."""
        self.db_path = db_path
        self.fallback_phrases = [
            PhraseData(phrase="¡Hoy es un gran día para aprender algo nuevo!", author="Anónimo"),
            PhraseData(phrase="Cada momento es un nuevo comienzo.", author="Anónimo"),
            PhraseData(phrase="Cree que puedes y ya estás a la mitad del camino.", author="Anónimo"),
        ]

    def get_phrase_count(self) -> int:
        """Get total number of phrases in database."""
        if not self.db_path.exists():
            return len(self.fallback_phrases)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM phrases')
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            return len(self.fallback_phrases)

    def get_phrase_by_index(self, index: int) -> PhraseData:
        """Get a specific phrase by index from database."""
        if not self.db_path.exists():
            return self.fallback_phrases[index % len(self.fallback_phrases)]

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get phrase by ID (SQLite IDs start at 1)
            cursor.execute('SELECT phrase, author FROM phrases WHERE id = ?', (index + 1,))
            result = cursor.fetchone()

            if result:
                conn.close()
                return PhraseData(phrase=result[0], author=result[1])
            else:
                # If index is out of range, fallback to modulo
                cursor.execute('SELECT COUNT(*) FROM phrases')
                total_count = cursor.fetchone()[0]
                actual_index = (index % total_count) + 1
                cursor.execute('SELECT phrase, author FROM phrases WHERE id = ?', (actual_index,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    return PhraseData(phrase=result[0], author=result[1])
                return self.fallback_phrases[0]

        except Exception:
            # Fallback if database error
            return self.fallback_phrases[index % len(self.fallback_phrases)]