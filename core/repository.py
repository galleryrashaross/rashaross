"""Subscriber persistence. SQL details are private to this class."""
import re
import sqlite3
from pathlib import Path


class SubscriberRepository:
    __EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, db_path: str):
        self.__path = Path(db_path)
        self.__path.parent.mkdir(parents=True, exist_ok=True)
        with self.__connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS subscribers (
                email TEXT PRIMARY KEY,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")

    def __connect(self):
        return sqlite3.connect(self.__path)

    @classmethod
    def is_valid(cls, email: str) -> bool:
        return bool(email and len(email) <= 254 and cls.__EMAIL.match(email))

    def add(self, email: str) -> bool:
        """Returns True if newly added, False if it already existed."""
        email = email.strip().lower()
        with self.__connect() as db:
            cur = db.execute(
                "INSERT OR IGNORE INTO subscribers (email) VALUES (?)", (email,))
            return cur.rowcount == 1

    def all(self) -> list[tuple[str, str]]:
        with self.__connect() as db:
            return db.execute(
                "SELECT email, created_at FROM subscribers ORDER BY created_at"
            ).fetchall()
