#!/usr/bin/env python3
"""
Pulls new sessions from the 312school decks repo and uses Claude to
append matching content to recap.md, lesson1.md + lesson1.html, and quiz.html.
Also records each new session into study.db so it's searchable.
Run from inside ~/code/class_recap.
"""

import glob, os, re, subprocess, json, sys

from study_db import insert_session

BASE = os.path.dirname(os.path.abspath(__file__))
DECKS_DIR = os.path.join(BASE, "decks")
STATE_FILE = os.path.join(BASE, ".session_state.json")
AUTO_PUSH = False   # set True once you trust the output; False lets you review first

DEFAULT_STATE = {"recap": 0, "notes": 0, "quiz": 0}


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return dict(DEFAULT_STATE)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def session_number(path):
    return int(os.path.basename(path.rstrip("/")).split("-")[-1])


def list_sessions():
    folders = glob.glob(os.path.join(DECKS_DIR, "session-*"))
    folders = [f for f in folders if os.path.isfile(os.path.join(f, "deck.html"))]
    return sorted(folders, key=session_number)


def run_claude(prompt):
    cmd = [
        "claude", "--model", "sonnet", "-p", prompt,
        "--allowedTools", "Bash",
        "--dangerously-skip-permissions",
    ]
    result = subprocess.run(cmd)
    return result.returncode == 0


def pending_sessions(sessions, last_done):
    return [s for s in sessions if session_number(s) > last_done]


# ---------------------------------------------------------------------------
# study.db recording helpers
# ---------------------------------------------------------------------------

def extract_section(text, pattern, n):
    """
    Finds the chunk of `text` belonging to lesson/session number `n`, using
    `pattern` to locate headers. Returns (title, body) or ("", "") if not found.
    """
    matches = list(re.finditer(pattern, text))
    for i, m in enumerate(matches):
        if int(m.group(1)) == n:
            title = m.group(2).strip() if m.lastindex and m.lastindex >= 2 else ""
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            return title, text[start:end].strip()
    return "", ""


def record_recap(n):
    path = os.path.join(BASE, "recap.md")
    if not os.path.exists(path):
        return
    text = open(path, encoding="utf-8").read()
    title, body = extract_section(text, r"#+\s*Lesson\s+(\d+)[:\-]?\s*(.*)", n)
    if body:
        insert_session(n, "recap", body, title=title)
        print(f"[recap] session-{n} recorded in study.db")


def record_notes(n):
    path = os.path.join(BASE, "lesson1.md")
    if not os.path.exists(path):
        return
    text = open(path, encoding="utf-8").read()
    title, body = extract_section(text, r"#+\s*Lesson\s+(\d+)[:\-]?\s*(.*)", n)
    if body:
        insert_session(n, "notes", body, title=title)
        print(f"[notes] session-{n} recorded in study.db")


def record_quiz(n):
    path = os.path.join(BASE, "quiz.html")
    if not os.path.exists(path):
        return
    text = open(path, encoding="utf-8").read()
    title, body = extract_section(text, r"//\s*──\s*Lesson\s+(\d+):\s*(.*?)\s*──", n)
    if body:
        insert_session(n, "quiz", body, title=title)
        print(f"[quiz] session-{n} recorded in study.db")


DB_RECORDERS = {
    "recap": record_recap,
    "notes": record_notes,
    "quiz": record_quiz,
}


def process_target(name, sessions, state, build_prompt):
    for folder in pending_sessions(sessions, state[name]):
        n = session_number(folder)
        print(f"[{name}] processing session-{n} ...")
        if not run_claude(build_prompt(folder, n)):
            print(f"[{name}] FAILED on session-{n} — stopping this target, will retry next run")
            return
        state[name] = n
        save_state(state)
        print(f"[{name}] session-{n} done")

        # Record the newly written section into study.db
        DB_RECORDERS[name](n)


def recap_prompt(folder, n):
    return (
        f"Read {folder}/deck.html. Write a short, travel-friendly recap of this lesson "
        f"in the exact same style as the existing entries in recap.md (short prose + "
        f"key commands in fenced code blocks, no fluff). "
        f"Append it to the end of recap.md as a new '## Lesson <N>: <Title>' section "
        f"(pick <N> by counting existing '## Lesson' headers in recap.md and adding 1), "
        f"preceded by a '---' separator, matching the formatting already there. "
        f"Only edit recap.md — do not touch any other file."
    )


def notes_prompt(folder, n):
    return (
        f"Read {folder}/deck.html and {folder}/after-class.html if it exists. "
        f"Write a detailed lesson section in the exact style of lesson1.md's existing entries "
        f"(##/### headers, tables, fenced code blocks). Append it as a new "
        f"'# Lesson <N>: <Title>' section preceded by '---' "
        f"(pick <N> by counting existing top-level '# Lesson' headers in lesson1.md and adding 1). "
        f"Then update lesson1.html to match: add a new <li><a href=\"#slug\">Lesson <N>: <Title></a></li> "
        f"to the nav <ul>, and add the corresponding <h1 id=\"slug\">...</h1> section in the same HTML "
        f"style as the other sections, inserted right before </main>. "
        f"Only edit lesson1.md and lesson1.html — do not touch any other file."
    )


def quiz_prompt(folder, n):
    return (
        f"Read {folder}/deck.html. Write 2-3 multiple-choice quiz questions about it, in the exact "
        f"JS object format already used in quiz.html's ALL_QUESTIONS array "
        f"(fields: lesson, q, answers, correct, explain). Use lesson: \"Lesson <N>\" "
        f"(pick <N> by finding the highest existing lesson number in ALL_QUESTIONS and adding 1). "
        f"Insert a '// ── Lesson <N>: <Title> ──' comment followed by the new question objects, "
        f"right before the closing '];' of ALL_QUESTIONS. "
        f"Then update the header text near the top of the file: the '<p>Study Quiz — Lessons 1 – X</p>' "
        f"line and the '<p>N questions across all X lessons...' line — recalculate both to match the "
        f"new highest lesson number and new total question count. "
        f"Only edit quiz.html — do not change any existing questions."
    )


def main():
    os.chdir(BASE)

    print("Pulling latest sessions...")
    subprocess.run(["git", "-C", DECKS_DIR, "pull"], check=False)

    sessions = list_sessions()
    if not sessions:
        print("No session folders found — check the decks/ path.")
        sys.exit(1)

    state = load_state()

    process_target("recap", sessions, state, recap_prompt)
    process_target("notes", sessions, state, notes_prompt)
    process_target("quiz", sessions, state, quiz_prompt)

    if AUTO_PUSH:
        subprocess.run(["git", "add", "-A"], cwd=BASE)
        subprocess.run(["git", "commit", "-m", "Auto-update recap/notes/quiz"], cwd=BASE)
        subprocess.run(["git", "push"], cwd=BASE)
        print("Pushed.")
    else:
        print("AUTO_PUSH is off — review with `git diff`, then commit/push manually.")


if __name__ == "__main__":
    main()
