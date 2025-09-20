#!/usr/bin/env python3
"""
Script to migrate phrases.txt to SQLite database for better performance
"""

import sqlite3
import sys
from pathlib import Path

def create_database():
    """Create SQLite database with phrases table"""
    conn = sqlite3.connect('phrases.db')
    cursor = conn.cursor()
    
    # Create phrases table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phrases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phrase TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')
    
    # Create index for faster lookups
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_id ON phrases(id)')
    
    conn.commit()
    return conn

def parse_phrase_line(line):
    """Parse a line from phrases.txt and extract phrase and author"""
    line = line.strip()
    if not line:
        return None, None
    
    # Support multiple formats: "phrase" - author, phrase | author, or just phrase
    if '" - ' in line and line.startswith('"'):
        # Format: "phrase" - author
        quote_end = line.rfind('" - ')
        if quote_end > 0:
            phrase_text = line[1:quote_end]  # Remove opening quote
            author = line[quote_end + 4:].strip()
            # Remove any trailing emojis or special characters from author
            author = author.split(' ⚔️')[0].split(' 🏛️')[0].split(' 📚')[0]
            return phrase_text, author
    elif '|' in line:
        # Old format: phrase | author
        phrase_text, author = line.split('|', 1)
        return phrase_text.strip(), author.strip()
    else:
        # Just phrase without author
        return line.strip(), "Anónimo"
    
    return None, None

def migrate_phrases():
    """Migrate phrases from phrases.txt to SQLite database"""
    phrases_file = Path(__file__).parent / "phrases.txt"
    
    if not phrases_file.exists():
        print("❌ phrases.txt not found")
        sys.exit(1)
    
    print("🚀 Starting migration from phrases.txt to SQLite...")
    
    # Create database
    conn = create_database()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM phrases')
    
    # Read and insert phrases
    inserted_count = 0
    skipped_count = 0
    
    try:
        with open(phrases_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                phrase, author = parse_phrase_line(line)
                
                if phrase and author:
                    cursor.execute(
                        'INSERT INTO phrases (phrase, author) VALUES (?, ?)',
                        (phrase, author)
                    )
                    inserted_count += 1
                else:
                    skipped_count += 1
                
                # Progress indicator
                if line_num % 50000 == 0:
                    print(f"  Processed {line_num:,} lines...")
                    conn.commit()  # Commit in batches
        
        # Final commit
        conn.commit()
        
        # Get total count
        cursor.execute('SELECT COUNT(*) FROM phrases')
        total_phrases = cursor.fetchone()[0]
        
        print(f"✅ Migration completed!")
        print(f"   - Total lines processed: {line_num:,}")
        print(f"   - Phrases inserted: {inserted_count:,}")
        print(f"   - Lines skipped: {skipped_count:,}")
        print(f"   - Database phrases: {total_phrases:,}")
        
        # Database file size
        db_path = Path("phrases.db")
        if db_path.exists():
            db_size_mb = db_path.stat().st_size / (1024 * 1024)
            print(f"   - Database size: {db_size_mb:.1f} MB")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_phrases()