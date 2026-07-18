#!/usr/bin/env python3
"""
study_db.py

A lightweight, dependency-free SQLite database for everything you've studied.
Designed to plug into update_recap.py: every time that script appends new
content to recap.md / lesson1.md / lesson1.html / quiz.html, it can also call
insert_session() here so the content becomes searchable forever.

Usage as a library:
    from study_db import init_db, insert_session, search

    init_db()
    insert_session(
        session_number=25,
        file_type="notes",          # "recap" | "notes" | "quiz"
        title="IAM Roles vs Policies",
        body_text="...the full markdown/text content that was appended...",
        tags="AWS, IAM, security"    # optional, comma-separated
    )

    results = search("IAM policy")
    for r in results:
        print(r["session_number"], r["file_type"], r["title"])

Usage from the command line:
    python3 study_db.py search "IAM policy"
    python3 study_db.py stats
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent / "study.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_number  INTEGER NOT NULL,
    file_type       TEXT NOT NULL,          -- 'recap' | 'notes' | 'quiz'
    title           TEXT,
    tags            TEXT,
    added_at        TEXT NOT NULL,
    UNIQUE(session_number, file_type)
);

CREATE TABLE IF NOT EXISTS content (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    body_text       TEXT NOT NULL
);

-- Full-text search index over titles, tags, and body text
CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(
    title,
    tags,
    body_text,
    tokenize='porter'
);
"""


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"Database ready at {DB_PATH}")


def insert_session(session_number: int, file_type: str, body_text: str,
                    title: str = "", tags: str = ""):
    """
    Insert (or update, if this session/file_type combo already exists)
    one chunk of studied content into the database.
    """
    conn = get_conn()
    cur = conn.cursor()

    now = datetime.now(timezone.utc).isoformat()

    # Upsert the session row
    cur.execute("""
        INSERT INTO sessions (session_number, file_type, title, tags, added_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(session_number, file_type) DO UPDATE SET
            title=excluded.title,
            tags=excluded.tags,
            added_at=excluded.added_at
    """, (session_number, file_type, title, tags, now))

    # Get the session id (works whether it was inserted or updated)
    cur.execute("""
        SELECT id FROM sessions WHERE session_number=? AND file_type=?
    """, (session_number, file_type))
    session_id = cur.fetchone()["id"]

    # Replace any existing content + FTS entry for this session
    cur.execute("DELETE FROM content WHERE session_id=?", (session_id,))
    cur.execute("DELETE FROM content_fts WHERE rowid=?", (session_id,))

    cur.execute("""
        INSERT INTO content (session_id, body_text) VALUES (?, ?)
    """, (session_id, body_text))

    cur.execute("""
        INSERT INTO content_fts (rowid, title, tags, body_text)
        VALUES (?, ?, ?, ?)
    """, (session_id, title, tags, body_text))

    conn.commit()
    conn.close()


def search(query: str, limit: int = 15):
    """
    Full-text search across everything you've studied.
    Returns a list of dict-like rows: session_number, file_type, title,
    tags, added_at, and a short snippet of matching text.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.session_number, s.file_type, s.title, s.tags, s.added_at,
               snippet(content_fts, 2, '[', ']', '...', 12) AS snippet
        FROM content_fts
        JOIN sessions s ON s.id = content_fts.rowid
        WHERE content_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """, (query, limit))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def stats():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS n FROM sessions")
    total = cur.fetchone()["n"]
    cur.execute("""
        SELECT MIN(session_number) AS lo, MAX(session_number) AS hi
        FROM sessions
    """)
    row = cur.fetchone()
    conn.close()
    return {"total_entries": total, "session_range": (row["lo"], row["hi"])}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 study_db.py [init|search <query>|stats]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "init":
        init_db()

    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: python3 study_db.py search <query>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        results = search(query)
        if not results:
            print(f"No matches for '{query}'.")
        for r in results:
            print(f"\n[session-{r['session_number']}] {r['file_type']} — {r['title']}")
            if r["tags"]:
                print(f"  tags: {r['tags']}")
            print(f"  {r['snippet']}")

    elif cmd == "stats":
        s = stats()
        print(f"Total entries: {s['total_entries']}")
        print(f"Session range: {s['session_range'][0]} → {s['session_range'][1]}")

    else:
        print(f"Unknown command: {cmd}")
