import sqlite3
import json
import csv
from pathlib import Path


class LexiconCache:
    """
    Persistent storage for G2P results using SQLite.
    Also handles loading manual exceptions from a CSV file.
    """

    def __init__(self, db_name: str = "lexicon.db"):
        self.db_path = Path.cwd() / db_name
        self._init_db()
        self._load_exceptions()

    def _init_db(self):
        """Creates the table if it doesn't exist and ensures schema is up to date."""
        with sqlite3.connect(self.db_path) as conn:
            # 1. Create Base Table (If not exists - handles fresh install)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS words (
                    word TEXT PRIMARY KEY,
                    phonemes TEXT NOT NULL,
                    hit_count INTEGER DEFAULT 1
                )
            """)

            # 2. Schema Migration: Ensure 'is_exception' column exists
            # We try to select it; if it fails, we add it.
            # This is more robust than parsing PRAGMA output.
            try:
                conn.execute("SELECT is_exception FROM words LIMIT 1")
            except sqlite3.OperationalError:
                # Column doesn't exist, so add it
                try:
                    conn.execute("ALTER TABLE words ADD COLUMN is_exception BOOLEAN DEFAULT 0")
                except sqlite3.OperationalError:
                    pass  # Concurrent modification or other issue

    def _load_exceptions(self):
        """
        Loads exceptions from src/ckb_g2p/resources/exceptions.csv into the DB.
        This runs on init to ensure exceptions are always up to date.
        """
        # Locate the CSV relative to this file
        resource_path = Path(__file__).resolve().parents[1] / "resources" / "exceptions.csv"

        if not resource_path.exists():
            return

        try:
            with open(resource_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                to_insert = []
                for row in reader:
                    word = row.get("Word", "").strip()
                    ipa_str = row.get("IPA", "").strip()

                    if not word or not ipa_str:
                        continue

                    # Parse IPA string into list
                    if " " in ipa_str:
                        phonemes = [p for p in ipa_str.split(" ") if p and p not in [".", "ˈ"]]
                    else:
                        phonemes = list(ipa_str.replace(".", "").replace("ˈ", ""))

                    to_insert.append((word, json.dumps(phonemes), 1))

            if to_insert:
                with sqlite3.connect(self.db_path) as conn:
                    conn.executemany(
                        """
                        INSERT OR REPLACE INTO words (word, phonemes, is_exception) 
                        VALUES (?, ?, 1)
                        """,
                        to_insert
                    )
        except Exception as e:
            print(f"⚠️ Warning: Failed to load exceptions: {e}")

    def get(self, word: str) -> tuple:
        """Retrieves phonemes for a word if cached."""
        with sqlite3.connect(self.db_path) as conn:
            try:
                cursor = conn.execute("SELECT phonemes FROM words WHERE word=?", (word,))
                row = cursor.fetchone()
                if row:
                    return tuple(json.loads(row[0]))
            except sqlite3.OperationalError:
                # Schema might be outdated, try re-init
                self._init_db()
                # Retry once
                cursor = conn.execute("SELECT phonemes FROM words WHERE word=?", (word,))
                row = cursor.fetchone()
                if row:
                    return tuple(json.loads(row[0]))
        return None

    def set(self, word: str, phonemes: tuple):
        """Saves the result to the cache."""
        with sqlite3.connect(self.db_path) as conn:
            try:
                # Don't overwrite if it's an exception
                cursor = conn.execute("SELECT is_exception FROM words WHERE word=?", (word,))
                row = cursor.fetchone()
                if row and row[0] == 1:
                    return

                conn.execute(
                    "INSERT OR REPLACE INTO words (word, phonemes, is_exception) VALUES (?, ?, 0)",
                    (word, json.dumps(list(phonemes)))
                )
            except sqlite3.OperationalError:
                # Retry schema fix if column missing
                self._init_db()
                conn.execute(
                    "INSERT OR REPLACE INTO words (word, phonemes, is_exception) VALUES (?, ?, 0)",
                    (word, json.dumps(list(phonemes)))
                )