
# Lesson 13: The Quiz Bot — Variables, if/else, Exit Codes & Failing Loudly

## The goal

Build `quiz-bot.sh` on your own Mac: it fetches the class decks from GitHub, then fires a Claude call that reads the newest session and sends a quiz question to your Telegram channel. The news bot is done on the server — this is a new product, a new file, built locally first. Same machinery you already know; three new moves: a variable, an `if`, and `exit 1`.

**The pipeline:**
```
bash fetches the class → (something writes the quiz) → bash sends it
```
The middle piece comes later — today, the two ends.

---

## Pre-flight — four things must be working

```bash
git --version                                         # answers? good.
mkdir ~/code/quiz-bot && cd ~/code/quiz-bot           # the home for today's bot
claude -p "say hi"                                    # ✓ nothing back? sign in (next)
git ls-remote git@github.com:312school/26a.312school.com.git  # "permission denied"? fix SSH key (S6/7)
```

If Claude didn't answer: open `claude` → sign in with your school account → or type `/login` if already inside → then `claude -p "say hi"` answers again. One sign-in and Claude remembers you.

---

## The decks repo

All class slides live in one GitHub repo — a `session-N` folder per class, each with `deck.html`. The same slides you read in class — the bot reads the same pages.

```
github.com/312school/26a.312school.com
├── session-1/deck.html
├── session-2/deck.html
└── … session-14/deck.html    # one folder per class, newest at the end
```

You can clone it once your SSH key is set up (Session 6/7). `permission denied`? Redo that SSH step (or clone over `https://`, which works but asks you to sign in every time).

---

## Variables — a name for a value

A **variable** is a name you give a value so you write it once and reuse it.

```bash
MY_NAME=Amina      # set it — NO dollar sign
echo $MY_NAME      # read it — dollar sign in front
Amina
```

- **To set:** `NAME=value` — no `$`
- **To read:** `$NAME` — dollar sign in front

A variable lives in **this terminal only** — close it and it's gone. `export` is what hands it to a child script (same idea as your news-bot notes).

**Gotcha — use `$HOME`, not `~` in variables.** In a variable, `~` doesn't always expand. If `echo $REPO_DIR` comes back empty, that's why.

```bash
REPO_DIR=$HOME/code/quiz-bot/decks    # top of quiz-bot.sh
echo $REPO_DIR
/Users/you/code/quiz-bot/decks        # ✓
```

Write the path once, fix it once — every line after this says `$REPO_DIR`.

---

## Clone the decks — and the problem

First clone works. Second clone breaks:

```bash
git clone git@github.com:312school/26a.312school.com.git decks
# first time: Cloning into 'decks'... done.

git clone git@github.com:312school/26a.312school.com.git decks
# second time: fatal: destination path 'decks' already exists and is not an empty directory.
```

A fetch you run every day can't always be `clone` — the folder's already there the second time. The script has to **decide**.

### git pull — update what you already have

```bash
# git clone  = download the first time
# git pull   = update a copy you already have

cd ~/code/quiz-bot/decks && git pull
Already up to date.    # nothing new — or it pulls in the newest class
```

Two moves: **clone** to get it, **pull** to refresh it.

---

## `if` / `else` / `fi` — a script that can decide

Until now your script runs every line, top to bottom. An `if` (**conditional**) lets it choose.

```bash
if [ … ]; then    # if the answer is yes…
  …do one thing…
else              # otherwise…
  …do the other…
fi                # "if" spelled backwards — it ends the if
```

Four words: `if` · `then` · `else` · `fi`. The question goes in `[ … ]`.

### The question in the brackets

```bash
[ -d "$REPO_DIR" ]
```

- `[ … ]` — a **test**: asks one yes/no question. (The brackets really are a small command.)
- `-d` — the question: **"is this a folder?"** (d = directory = folder)
- `"$REPO_DIR"` — what to check

**The spaces inside `[ ]` are required** — because `[` is a command, each piece must be its own word. This is the first thing that bites.

### Try it on a throwaway folder

```bash
mkdir /tmp/x
if [ -d /tmp/x ]; then echo "here"; else echo "nope"; fi
here       # the folder exists → first branch

rmdir /tmp/x
if [ -d /tmp/x ]; then echo "here"; else echo "nope"; fi
nope       # gone now → other branch
```

Every `if` today is this exact shape.

### Clone or pull — fill in the real decision

```bash
if [ -d "$REPO_DIR" ]; then
  cd "$REPO_DIR" && git pull          # it's here → refresh it
else
  git clone git@github.com:312school/26a.312school.com.git "$REPO_DIR"   # not here → download
fi
```

```bash
chmod +x quiz-bot.sh    # make it runnable — once
./quiz-bot.sh           # decks not there yet → CLONES
Cloning into '…/decks'... done.
./quiz-bot.sh           # decks ARE there → PULLS
Already up to date.
```

Both branches, one script. The "already exists" error? Gone.

---

## Exit codes — every command leaves a number

### The silent failure

Typo the repo URL:
```bash
./quiz-bot.sh
fatal: repository '…' does not exist
# …and the script keeps going, as if nothing happened.
```

The fetch failed — but the script **marched on**: no buzz, no clue. **A failure you can't see is the dangerous one.**

### Every command leaves an exit code

```bash
ls           # works
echo $?   →  0

ls /nope     # fails
echo $?   →  1    # a different number
```

Every command leaves a number when it finishes — its **exit code** (plain name: the error number). `$?` reads it. A failed `git clone` leaves `128`.

**Why 0 is the good number:** everywhere else, 0 is a bad score. Here it's backwards.
- `0` = "no error to report" — nothing went wrong
- `≠ 0` = a specific failure (1, 128, etc. — each names what broke)

Read `$?` on the **very next line** after the command — it changes with every command.

### `exit 1` — stop and say so

```bash
if [ $? -ne 0 ]; then          # -ne = "not equal": is the exit code not 0?
  echo "could not fetch the decks — check the repo URL"
  exit 1                        # stop the script, leave exit code 1 (I failed)
fi
```

`-ne` = "not equal." The same `if` shape as clone-or-pull — only the question changed. **A script that can't do its job should say so and stop, not continue broken.**

### Now the broken fetch halts loudly

```bash
./quiz-bot.sh
could not fetch the decks — check the repo URL
# …STOPS — exit code 1 — doesn't march on this time.

# fix the URL:
./quiz-bot.sh  →  Already up to date.   # exit code 0 → no stop, keeps going
```

Loud-and-stopped when it fails; quiet-and-onward when it works. **That's failing loudly.**

---

## The Telegram notes + the Claude call

```bash
export TELEGRAM_BOT_TOKEN=8123456789:AAH…   # note 1 — bot's key (from the news bot)
export TELEGRAM_CHAT_ID=@your_quiz_channel   # note 2 — the public channel it posts to
```

- **Token** — proves it's your bot
- **Chat id** — where it posts; for a public channel that's `@channel_name`
- The bot must be an **admin** of the channel to post — add it in the channel's settings

### The Claude call — one line per flag

```bash
claude --model sonnet -p --allowedTools "WebSearch" "Bash" --verbose "…"
#  --model sonnet  : which Claude model answers
#  -p              : answer once and stop — no chat window
#  --allowedTools  : the tools it may use this run
#  --verbose       : show the work as it goes
```

Use `"Bash"`, **not** `"Bash(curl:*)"` — the narrow form silently skips the Telegram send. Sonnet: Haiku pauses, Opus costs more.

### The payoff — your phone buzzes

```bash
claude --model sonnet -p --allowedTools "WebSearch" "Bash" --verbose \
  "Read $REPO_DIR/session-14/deck.html, write one quiz question, and send it on
   Telegram with curl — token in $TELEGRAM_BOT_TOKEN, chat id in $TELEGRAM_CHAT_ID."
# buzz — a real quiz question on the newest class, posted to your channel
```

A real quiz, posted to your channel — fired from your own Mac, by hand. The two ends of the pipeline, working.

---

## Why we don't schedule it yet

You already know how to `cron` this — but your laptop sleeps, closes, goes offline. A bot that buzzes every morning has to live on a machine that's **always on** — your server. Moving it there is the last thing we do in this run. Not today.

---

## What's still thin — and what's next

The bot works, but:
- **Only the newest class** — quizzes one class, not every class you've covered
- **Only one question** — real practice needs a set, not just one
- **Re-sends what you've seen** — can't yet skip classes it already quizzed you on

Every-class, real question sets, and skipping what's done all need **looping** and **deciding** — the next language in the arc.

**Take-home:** run your bot a few more times; break the fetch on purpose and confirm it now stops loudly.

# Lesson 14: Python — Programs, Variables, Types, Lists & Loops

## What is software?
Software is just instructions. Every app you use — Telegram, a website, Maps — is a list of instructions a computer follows, in order. The computer does **exactly** what it's told, step by step. No magic underneath.

## What is a program?
So far you've typed commands by hand, one at a time (`git status`, `ls`, `cd code`). A program is those same instructions **written down once** in a file — and the computer runs all of them, in order, by itself.

## The language: Python
Programs are written in a language the computer understands. The language used here is **Python**. Example:
```python
print("hello")
```
Read it out loud: "print hello" — it says hello on the screen. You'll be able to read a lot of Python before you can write it.

## The editor: VSCode
Writing real code in the bare terminal is painful. VSCode shows your whole file, colors it, and keeps the terminal you already know right inside it.

Setup:
```
1. open VSCode
2. File → Open Folder → ~/code/quiz-bot   # point it at where you work
3. Terminal → New Terminal                 # same terminal, now inside the editor
python3 --version  →  Python 3.x          # ✓ Python is here
```
Don't have the folder yet? `mkdir -p ~/code/quiz-bot` first.

## Your first program
New file → save as `hello.py`:
```python
print("Hello from my first program")
```
The `.py` on the filename tells the computer it's a Python program. Saved — not run yet.

Run it in the terminal:
```
python3 hello.py
Hello from my first program
```
`python3` is the thing that runs your file. You wrote instructions; the computer ran them. **That's a program.**

**No output?** Your file isn't saved — a white dot by the filename means unsaved; press ⌘S, or turn on Auto Save (File → Auto Save). `cat hello.py` only *shows* the text — `python3 hello.py` *runs* it.

Change a line, get a new result:
```python
print("Hello from Amina")   # your own name
```
You change the instructions, the computer does the new thing. That's all programming is, underneath.

## Variables
A variable is a name that holds a value. Set it once, use it by that name — the program remembers.
```python
topic = "git"
print(topic)    →   git
topic = "linux"
print(topic)    →   linux
```
`=` **sets** a value. `==` **asks** a question (true or false). Easy to mix up — this is the one to remember.

## Text & numbers: + does two different things
```python
"cat" + "dog"   →   "catdog"    # text: + glues (concatenation)
2 + 2           →   4           # numbers: + adds
"2" + "2"       →   "22"        # still text — glues, doesn't add
```
The quotes make the difference.

## Three kinds of values (types)
| Type    | What it is                    | Examples           |
|---------|-------------------------------|--------------------|
| string  | text — always in quotes       | `"git"`, `"hello"` |
| integer | whole number, no decimal      | `42`, `0`, `-3`    |
| float   | number with a decimal point   | `3.14`, `0.5`      |

Python treats each type differently — that's why `"2" + "2"` glued instead of adding.

## Lists
A list holds things in order, using square brackets:
```python
classes = ["git", "linux", "networking"]
```
Reach in by position — Python counts from **0**:
```python
classes[0]   →   "git"
classes[1]   →   "linux"
```
`[0]` is the first item. This trips everyone once; that's normal.

## The for loop
Instead of writing `print` three times, say it once:
```python
for c in classes:
    print(c)
```
`c` isn't a fixed name — each time around the loop it **becomes the next item**, and the indented line runs again. Three items → three passes → `git` · `linux` · `networking`.

**Why Python here vs bash:**
| Bash | Python |
|------|--------|
| `for c in git linux networking; do` | `for c in classes:` |
| `  echo "$c"` | `    print(c)` |
| `done` | |

Both can do it. Python reads closer to plain English, so it's easier to get right. This is the first loop you've written in either language.

## The one trap: indentation
Python cares about the spaces at the start of a line, and they're **invisible**:
```python
for c in classes:
    print(c)        # ✓ indented — runs

for c in classes:
print(c)            # IndentationError — not indented
```
The fix is always the same: line them up.

## if — a program that chooses
Until now every line runs no matter what. An `if` lets the program **choose**:
```python
if c == "git":
    print("← let's review git")
# if false: skip it — do nothing
```
bash has an `if` too — same idea; Python just writes it with a colon and indented lines.

## Putting it all together
```python
classes = ["git", "linux", "networking"]
for c in classes:
    if c == "networking":
        print(c, "— the tricky one!")
    else:
        print(c)
```
Output:
```
git
linux
networking — the tricky one!
```
A list, a loop, and a decision — a real little program, written and run by you.

## Summary: what you can now do
```python
print("hi")                      # say something
topic = "git"                    # a name holds a value
classes = ["git", "linux"]       # a list, in order
for c in classes:                # do it for every item
    if c == "git": print(c)      # ...only when true
```
From "what is a program" to a loop with a decision — in one sitting, in the editor real engineers use.

# Lesson 15: Write the Real Quizzes — List, Loop, Skip, Run

**Goal:** Python lists your classes, skips the ones already done, and runs the command that buzzes your phone.

## The finished bot (what we're building toward)
```
python3 quiz_bot.py
decks/session-1: writing and sending…   # 📱 buzz
decks/session-2: writing and sending…   # 📱 buzz

python3 quiz_bot.py                     # run it a second time
decks/session-1: already done, skipping
decks/session-2: already done, skipping
```
First run: every class buzzes. Second run: nothing sends. That's the whole goal.

## Pre-flight: three checks
```bash
cd ~/code/quiz-bot
ls decks              # → session-1 session-2 … (your real classes)
claude -p "say hi"    # → a reply
```
No `decks` folder? Clone it (same fetch from last session). `claude -p` silent? Re-do the login from the cheat-sheet. Telegram token goes in the environment: `export TELEGRAM_BOT_TOKEN=…` in your shell — not hard-coded in the script.

## One class, one command (the starting point)
```bash
claude --model sonnet -p "Read decks/session-1/deck.html, write one
  multiple-choice quiz question, save it to decks/session-1/quiz.md,
  and post it to my Telegram channel." \
  --allowedTools "Bash" --dangerously-skip-permissions
```
- `--allowedTools "Bash"` = which tools Claude may use (run commands — open the deck, save, post — not just answer)
- `--dangerously-skip-permissions` = don't pause before each step, so a Python run doesn't hang waiting
- `--model sonnet` = model for these demos

**Problem:** run it twice → same quiz sends twice. We want every class, once. That's the job for Python.

## Four verbs: List · Loop · Skip · Run

### Verb 1: List — get the real folders off disk
Last time the list was typed by hand. Now we want the actual folders:

| Bash | Python |
|------|--------|
| `ls decks/session-*` | `glob.glob("decks/session-*")` |

```python
import glob
glob.glob("decks/session-*")
# → ['decks/session-1', 'decks/session-2', 'decks/session-3']
```
`import glob` borrows the toolkit ("load this so I can use it"). `glob.glob(...)` finds folders by a pattern — same `*` idea as `ls *.pdf`.

### Verb 4: Run — Python can't run `claude` directly, it asks the terminal

Python doesn't know the `claude` command. The hand-off tool is called **subprocess**:
```python
import subprocess
subprocess.run(["echo", "hi"])   # → hi
```
Each piece of the command is its own list item. `subprocess` **waits** for the command to finish before the next line runs. The real `claude` call takes many seconds — quiet on screen = it's working, not broken:
```python
subprocess.run(["sleep", "2"])   # cursor sits for 2 seconds, then comes back
```

The real Claude call from Python:
```python
prompt = "Read decks/session-1/deck.html, write one quiz question, \
    save it to decks/session-1/quiz.md, and post it to my channel."
subprocess.run(["claude", "--model", "sonnet", "-p", prompt,
                "--allowedTools", "Bash", "--dangerously-skip-permissions"])
```
📱 Your phone buzzes. The bot works on one class. This is a fine stopping point if time is tight.

Building a path with `+`:
```python
print("decks/session-1" + "/quiz.md")   # → decks/session-1/quiz.md
```

### Verb 2: Loop — wrap the one-class command to cover all classes
```python
for folder in glob.glob("decks/session-*"):   # once per class
    # …the same claude command, with folder in place of "session-1"
```
`folder` is the current class each time around. Three items → three passes → three buzzes.

Use `sorted(...)` so classes always run in the same order:
```python
for folder in sorted(glob.glob("decks/session-*")):
```
**Backfill** = going back and quizzing every class not done yet. In class you run a few; the loop does the rest at home. If you hit a "rate-limit" message: stop, wait, re-run — the skip (next verb) means it picks up where it left off.

### Verb 3: Skip — don't re-send if the quiz already exists

`os.path.exists(...)` asks: does this path exist? Returns `True` or `False`:
```python
import os
os.path.exists("decks")    →   True
os.path.exists("nope")     →   False
```

`not` flips the answer — true becomes false, false becomes true:
```python
not os.path.exists("decks")    →   False
not os.path.exists("nope")     →   True
```

So `if not os.path.exists(...)` = **do the thing only when the file is NOT there yet**:
```python
if not os.path.exists(folder + "/quiz.md"):
    # write + send, then save quiz.md
else:
    print("already done, skipping")
```
When the command works (exit code `0`, like in bash), Python saves a tiny `quiz.md` next to the deck. `ls` the folder before and after — "done" is a file you can actually see. Run again → "skipping" for each, no buzz.

## The whole bot — about ten lines
```python
import glob, os, subprocess

for folder in sorted(glob.glob("decks/session-*")):    # LIST + LOOP
    if not os.path.exists(folder + "/quiz.md"):        # SKIP if done
        prompt = "Read " + folder + "/deck.html, write one quiz question, " \
                 "save it to " + folder + "/quiz.md, and post it to my channel."
        result = subprocess.run(["claude", "--model", "sonnet", "-p", prompt,
                                 "--allowedTools", "Bash",
                                 "--dangerously-skip-permissions"])    # RUN
        if result.returncode == 0:
            open(folder + "/quiz.md", "a").close()    # it worked → mark done
    else:
        print(folder, "already done, skipping")
```
Every line is one of the four verbs: **List** (glob), **Loop** (for), **Skip** (if not exists), **Run** (subprocess).

Claude could've done this whole loop from one prompt — you wrote the loop yourself, and that's the skill that carries into the app and the database. Later, in SQL, each question becomes a row in a table.
