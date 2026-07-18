#!/usr/bin/env python3
"""
backfill.py

One-time import: reads your EXISTING recap.md, lesson1.md, and quiz.html
(sessions 1-24, already written) and loads them into study.db so your
search history starts complete, not just from today forward.

Run this once from ~/code/class_recap/, after copying study_db.py there:
    python3 backfill.py

Safe to re-run — insert_session() overwrites by (session_number, file_type),
so running it twice won't create duplicates.
"""

import re
import json
from pathlib import Path
from study_db import init_db, insert_session

BASE = Path(__file__).parent

RECAP_MD = BASE / "recap.md"
NOTES_MD = BASE / "lesson1.md"
QUIZ_HTML = BASE / "quiz.html"


def split_by_session_headers(text: str, pattern: str):
    """
    Splits markdown text into (session_number, title, body) chunks based on
    a heading pattern like '## Session 12: ...' or '## Lesson 12: ...'.
    Adjust `pattern` if your headers look different.
    """
    matches = list(re.finditer(pattern, text))
    chunks = []
    for i, m in enumerate(matches):
        session_num = int(m.group(1))
        title = m.group(2).strip() if m.lastindex and m.lastindex >= 2 else ""
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        chunks.append((session_num, title, body))
    return chunks


def backfill_recap():
    if not RECAP_MD.exists():
        print(f"Skipping recap: {RECAP_MD} not found")
        return
    text = RECAP_MD.read_text(encoding="utf-8")
    # Adjust this regex to match your actual recap.md header style
    chunks = split_by_session_headers(
        text, r"#+\s*Lesson\s+(\d+)[:\-]?\s*(.*)"
    )
    for session_num, title, body in chunks:
        insert_session(session_num, "recap", body, title=title)
    print(f"Backfilled {len(chunks)} recap entries")


def backfill_notes():
    if not NOTES_MD.exists():
        print(f"Skipping notes: {NOTES_MD} not found")
        return
    text = NOTES_MD.read_text(encoding="utf-8")
    chunks = split_by_session_headers(
        text, r"#+\s*Lesson\s+(\d+)[:\-]?\s*(.*)"
    )
    for session_num, title, body in chunks:
        insert_session(session_num, "notes", body, title=title)
    print(f"Backfilled {len(chunks)} notes entries")


def backfill_quiz():
    if not QUIZ_HTML.exists():
        print(f"Skipping quiz: {QUIZ_HTML} not found")
        return
    text = QUIZ_HTML.read_text(encoding="utf-8")

    # Split on the '// ── Lesson N: Title ──' comments your script inserts
    pattern = r"//\s*──\s*Lesson\s+(\d+):\s*(.*?)\s*──"
    matches = list(re.finditer(pattern, text))
    count = 0
    for i, m in enumerate(matches):
        session_num = int(m.group(1))
        title = m.group(2).strip()
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        insert_session(session_num, "quiz", body, title=title)
        count += 1
    print(f"Backfilled {count} quiz entries")


if __name__ == "__main__":
    init_db()
    backfill_recap()
    backfill_notes()
    backfill_quiz()
    print("\nBackfill complete. Try: python3 study_db.py stats")
