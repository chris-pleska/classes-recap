# DTC School — Study Notes

# Lesson 1: The Terminal

## Why the Terminal

Engineers live in the terminal. Two reasons:

- **The browser is comfortable. The terminal is fast.** Ten clicks in a browser → one line in a terminal.
- **Real computers — the ones companies run — don't have buttons or a mouse.** Only the terminal.

Working through a browser is like talking through a translator. The terminal talks to the computer directly.

| | Terminal (Sports Car) | Browser (Minivan) |
|---|---|---|
| | Direct control, less weight | Comfortable, easy to use |
| | 10 browser clicks = 1 line | Good for everyday use |

> **Both work.** The terminal is what companies pay you to drive. Today is your first lap.

---

## Opening the Terminal

**Mac:**
1. Press `⌘ + space` — Spotlight opens.
2. Type `Terminal`
3. Press `Enter` — A black window opens. No mouse. Only keyboard.

**Windows:** Install WSL (Windows Subsystem for Linux) and open the WSL terminal. Same Linux commands run inside it.

---

## Navigation

Three commands. With these you can get anywhere.

| Command | What it does | Think of it as |
|---|---|---|
| `pwd` | Print working directory | "Where am I standing right now?" |
| `ls` | List files in this folder | "Look around the room" |
| `ls -a` | List files including hidden | "Look behind the curtains too" |
| `cd <folder>` | Change directory | "Walk into a room" |
| `cd ~` | Go to your home folder | "Go home" |
| `cd ..` | Go up one folder | "Step back into the hallway" |

**A path is an address.** Read `~/Downloads` from the right: a folder called `Downloads`, inside your home folder `~`.

**Two habits from day one:**
- **Tab autocompletes.** Start typing a path, press Tab — the terminal finishes it. Use it always.
- **Case matters.** `Desktop` ≠ `desktop`. The terminal is not the AI — typos are not forgiven.

---

## Create — Make a Folder. Make a File.

| Command | What it does | Think of it as |
|---|---|---|
| `mkdir <name>` | Make a new folder | "Build a new room" |
| `touch <file>` | Make an empty file | "Put a blank notebook on the shelf" |

**Chain with `&&`:** `mkdir code && cd code` — make the folder, walk into it. If the first fails, the second doesn't run.

**Filename starts with a dot = hidden:** `touch .secrets.txt` creates a hidden file. `ls` won't show it. `ls -a` will.

**No error = success.** If you don't see an error message, the command worked. Empty output is good news. Check with `ls` or `pwd`.

---

## Edit a File — The VI Round-Trip

Four keys, in order, every time.

| Command | What it does | Think of it as |
|---|---|---|
| `vi <file>` | Open to edit (creates it if missing) | "Sit down with the notebook and a pen" |
| `i` | Enter INSERT mode | "Pick up the pen" |
| `Esc` | Leave INSERT mode | "Put the pen down" |
| `:wq` | Save and quit | "Close the notebook and walk away" |

**The round-trip:** `i` → type → `Esc` → `:wq` → `Enter`

```bash
$ cd ~
$ mkdir code && cd code         # make folder, walk in
$ mkdir class1 && cd class1
$ touch notes.txt               # create an empty file
$ ls                            # see the file
$ cat notes.txt                 # empty — prints nothing

$ vi notes.txt                  # open in vi
  press i                       # enter INSERT mode — bottom shows -- INSERT --
  type your text
  press Esc                     # leave INSERT mode
  type :wq then Enter           # write and quit

$ ls && cat notes.txt           # your notes print to the terminal
```

---

## Look Inside a File

Three ways to look. Pick the smallest one.

| Command | What it does | Think of it as |
|---|---|---|
| `cat <file>` | Show the whole file | "Read the whole page out loud" |
| `head -n 1 <file>` | Show the first N lines | "Peek at the top" |
| `tail -n 1 <file>` | Show the last N lines | "Peek at the bottom" |

`head` shows the head of the file. `tail` shows the tail. A log file can be a **million lines** — `cat` floods the screen. `head` and `tail` are the polite versions.

---

## Move, Copy, Remove

Two friendly, one sharp.

| Command | What it does | Think of it as |
|---|---|---|
| `cp <from> <to>` | Copy a file. The original stays. | "Photocopy a notebook." |
| `mv <from> <to>` | Move or rename. Original is gone from old address. | "Carry it · or relabel it." |
| `rm <file>` | Remove. No confirmation. No Trash. | "Gone is gone." |

> ⚠️ **READ THIS CAREFULLY**
>
> `rm` does not ask. `rm` does not go to the Trash. **Gone is gone.**
> - Check `pwd` before every `rm`.
> - Run the command, then double-check with `ls` or `pwd`. Linux won't ask "are you sure?"
> - **Never type `rm -rf` right now.** We get to flags later — not now.

```bash
$ cd ~/code/class1 && ls        # notes.txt is here

# --- copy ---
$ cp notes.txt notes-backup.txt
$ ls                            # both files appear

# --- rename (mv in same folder) ---
$ mv notes-backup.txt class1-notes.txt
$ ls                            # old name gone

# --- move (mv across folders) ---
$ cd ~/code && mkdir archive
$ mv class1/class1-notes.txt archive/

# --- remove ---
$ cd ~/code/archive
$ pwd                           # READ THIS — in archive?
$ rm class1-notes.txt           # gone — no Trash
```

`cp` keeps. `mv` changes the address. `rm` erases. Always `pwd` before `rm`.

---

## When VI Traps You

Bail out, clean up, try again.

- **First fix — abandon and quit:** press `Esc`, then type `:q!` and Enter. Drops all unsaved changes, drops you back to the terminal. Most "stuck in vi" moments end here.
- **Computers don't forgive small mistakes** — an extra space, a semicolon instead of a colon, a wrong key.
- **If `:wq` didn't save and quit** — you probably forgot `Esc`, or you forgot `i` and never entered INSERT mode in the first place.
- **Swap file showing up?** vi leaves a hidden helper file when it crashes. Run `ls -a`. If you see `.notes.txt.swp`, delete it with `rm .notes.txt.swp` *before* running vi on that file again.

**Last resort — still stuck:**
1. `⌘ + Q` — quit Terminal
2. Reopen Terminal
3. `cd ~/code/class1`
4. `ls -a` — see a `.swp`?
5. If yes: `rm .notes.txt.swp`
6. Try the round-trip again

**You will probably mess this up the first time. That is fine. Repeat until it works.**

---

## Practice on Your Own

A sandbox in your browser — same commands, nothing to break.

Three exercises: **continent tour** · **build-your-own-world-map** · **clean-up-an-empire**

→ [26a.312school.com/filesystem-playground](https://26a.312school.com/filesystem-playground)

---

## Quick Reference — All Commands

| Command | What it does |
|---|---|
| `pwd` | Where am I? |
| `ls` / `ls -a` | List files / including hidden |
| `cd <folder>` / `cd ~` / `cd ..` | Navigate folders |
| `mkdir <name>` | Make a folder |
| `touch <file>` | Make an empty file |
| `vi <file>` → `i` → type → `Esc` → `:wq` | Edit and save a file |
| `cat` / `head -n N` / `tail -n N` | Read a file (all / top / bottom) |
| `cp <from> <to>` | Copy (original stays) |
| `mv <from> <to>` | Move or rename |
| `rm <file>` | Delete permanently — no Trash! |
| `cmd1 && cmd2` | Run two commands in sequence |

---

# Lesson 2: Compose — Commands Work Together

## Recap of Lesson 1

- Picked **Anthropic**, met **Opus / Sonnet / Haiku**, learned tokens and the 5-hour / weekly limits.
- Opened the terminal and learned to walk around — `pwd`, `cd`, `ls`.
- Made things — `mkdir`, `touch`, `vi` (the round-trip), `cat`, `head`, `tail`.
- Moved things — `cp`, `mv`, `rm`. *(pwd before every rm.)*
- Each command did one thing. Today we put them together.

---

## The Big Idea

Every command has an output. You can send it somewhere.

- **Send it into a file** — save the output, read it later, stack more on top of it.
- **Send it into another command** — hand the output to the next command and let it work on it. (`claude` is one of those commands too.)

Until today every command worked alone. From today, **commands work together** — and that is most of what real shell work is.

---

## Two Kinds of Paths

Look at the first character.

| Type | Examples | Rule |
|---|---|---|
| **Absolute** | `/Users/marsel/code/class1/notes.txt` · `~/code/class1/notes.txt` | Starts with `/` or `~` → works from **anywhere** on your computer |
| **Relative** | `notes.txt` · `class1/notes.txt` · `../class1/notes.txt` | Anything else → **depends on where you are**. Same path, different meaning in different folders. |

> **When in doubt — use absolute. Works every time.**

**Demo — Paths in Practice:**

```bash
$ cd ~/code → pwd          # anchor in code
$ ls class1                # relative path — works because class1 is right here
$ cat class1/notes.txt     # still relative — reads the file from class1

$ cd ~ → pwd               # jump home — now one folder higher
$ cat class1/notes.txt     # same command, now FAILS — no class1 here
$ cat ~/code/class1/notes.txt  # absolute path — works from anywhere
```

`~/...` always means the same place. Relative paths move with you.

---

## Claude Code

**Claude Code is Claude — in the terminal — that can read your files.**

| | Browser (`claude.ai`) | Terminal (Claude Code) |
|---|---|---|
| What it knows | What you type. Nothing else about your laptop. | What you type **and** what is on your laptop, in whatever folder you started from. |
| Best for | Questions, writing, thinking out loud. | Working with your files. |

### Install Claude Code

```bash
$ curl -fsSL claude.ai/install.sh | bash
```

- The installer puts `claude` on your `PATH` — you can run it from anywhere.
- Not `npm`. The npm install exists; the official one is `curl`.
- When it finishes, type `claude --version` to confirm.

### Sign In (First Time)

```bash
$ cd ~/code
$ claude           # a browser tab opens
```

1. Sign in with your 312School Claude Team account.
2. Browser says *"you can close this tab."* Terminal is ready.

### Three Prompts to Try

1. *Same as claude.ai:* "Explain what a **server** is, in one paragraph, for a beginner."
2. *Same as claude.ai:* "I want to learn the **terminal** — where should I start?"
3. *The new thing:* "What's in my **current folder**?" — Claude Code reads `~/code` and tells you.

Same Claude. New ability — **it can see your files now.**

### Claude Code Writes Files for You

Paste this into Claude Code:

```
Please create three sample files on my laptop for a class exercise:
- A friendly photo saved to ~/Desktop as sunset.jpg
- A short research paper (1-2 pages, any topic, with a few repeated
  keywords like climate, policy, data) saved to ~/Documents/research-paper.md
- A markdown notes file at ~/Downloads/my-notes.md with 5 lines.
Tell me the absolute path to each file when you're done.
```

---

## Three Streams

Every command takes in · gives back · and complains.

```
INPUT → [command: ls · grep · cat] → OUTPUT  (prints to screen by default)
                                   → ERRORS  (also prints to screen by default)
```

- **Output** goes to your screen — by default.
- **Errors** also go to your screen — by default.
- Today we send those two streams into **files** or **other commands**.

---

## Redirect Output — Overwrite or Add

| Operator | What it does | Think of it as |
|---|---|---|
| `cmd > file` | Send output to file — **overwrites** anything already there | "Empty cup, poured fresh" |
| `cmd >> file` | Send output to file — **appends** to the end | "Add a new line at the bottom" |

**One arrow replaces. Two arrows add.** If the file doesn't exist, both create it. No `<` — left to right only.

**Demo — Save Output to a File:**

```bash
$ cd ~/code/class1
$ ls > listing.txt          # pour the directory listing into a file
$ cat listing.txt           # see it
$ pwd >> listing.txt        # append the current folder
$ cat listing.txt           # now there are two pieces
$ ls > listing.txt          # overwrite — the pwd line is gone
$ cat listing.txt           # confirm
```

`>` is a fresh start. `>>` adds on. Same arrow, different count.

---

## Redirect Errors — `2>`

Output and errors are **two different rivers**. `>` catches one. `2>` catches the other.

```bash
$ ls does-not-exist              # error prints to your screen
$ ls does-not-exist 2> err.txt   # error goes into the file instead
$ cat err.txt                    # see the error
```

---

## Quick Reference — New Commands from Lesson 2

| Operator / Command | What it does |
|---|---|
| `cmd > file` | Redirect output to file (overwrite) |
| `cmd >> file` | Redirect output to file (append) |
| `cmd 2> file` | Redirect errors to file |
| `~/path` | Absolute path from home — works from anywhere |
| `claude` | Run Claude Code from the terminal |
| `claude --version` | Confirm Claude Code is installed |
| `curl -fsSL claude.ai/install.sh \| bash` | Install Claude Code |

---

# Lesson 3 (Session 04): Pipes, Search, and the Path Drill

## Recap of Last Session

- **Paths · absolute vs relative** — Starts with `/` or `~`? Absolute. Anything else? Relative.
- **Three streams · in · out · errors** — Output and errors both go to the screen by default.
- **`>` overwrites · `>>` appends** — One replaces. Two add to the end.
- **`2>` catches errors** — Sends errors to a file, leaves output alone.

Today we add `echo`, `|`, `grep`, `find`, and `less`.

> **Pace yourself.** Don't stop at "I think I got it." Type it. Break it. Explain it back. A 10% gap today = a giant gap in month 2. Everything next month builds on this month.

---

## echo — Print Text to the Screen

| Command | What it does | Think of it as |
|---|---|---|
| `echo "hello world"` | Prints `hello world` to the output | "Say it out loud." |
| `echo "What's the capital of Brazil?"` | Prints that text to the output | Same — just longer text |

Anything `echo` prints, we can hand to the next command. **Next up: the pipe.**

---

## Setup — questions.txt

Create this file for the next exercises:

```bash
$ mkdir -p ~/code/class4    # make the folder if you don't have it
$ cd ~/code/class4
$ vi questions.txt          # i → paste → Esc → :wq
$ cat questions.txt         # confirm 10 lines are there
```

**Paste this into questions.txt:**

```
What is the capital of Brazil?                   #geography
Which country has the largest population?        #geography
Who is the current Secretary-General of the UN? #politics
Name two countries that border Russia.           #geography
What is inflation, in one sentence?              #economy
Which currency does Japan use?                   #economy
What does GDP measure?                           #economy
Name one country that uses ranked-choice voting. #politics
What is the longest river in Africa?             #geography
What is a central bank?                          #economy
```

---

## grep — Search Inside Files

`grep` is a search bar for a file. Same idea as Cmd-F on a web page — but in the terminal.

| Command | What it does | Think of it as |
|---|---|---|
| `grep <text> <file>` | Print every line containing `<text>` | "Highlight the matching lines." |
| `grep <text> *.txt` | Same — across every `.txt` in this folder | "Highlight across all notebooks." |

**Don't read the file with your eyes. Ask `grep`.**

**Demo — pick lines by hashtag:**

```bash
$ cd ~/code/class4
$ grep "#politics" questions.txt    # two politics lines
$ grep "#economy" questions.txt     # four economy lines
$ grep "#geography" questions.txt   # four geography lines
```

Same file. Three filtered views — just with `grep`.

---

## The Pipe — `|`

`|` sends one command's output to the next. Until now, `grep` read a file. With `|`, it can read the **output of another command** instead — no file needed.

```
ls  →  | (all lines)  →  grep notes  →  your screen (just notes.txt)
```

```bash
$ ls | grep notes    # ls lists everything; grep keeps only lines with "notes"
```

Read it left to right: `ls` lists everything in this folder; `grep` reads that list and keeps only the lines mentioning `notes`.

---

## Chat Mode vs Print Mode

Two ways to talk to Claude Code:

| | `claude` | `claude -p "..."` |
|---|---|---|
| Mode | Chat · Interactive | Print · Headless |
| What happens | Opens a chat window inside your terminal. You type, Claude replies, you type again. | Claude reads, answers once, prints to screen, shell returns. No chat window. |
| Use for | Longer back-and-forth | **Piping. Always use this with pipes.** |

> **From a pipe, always `claude -p`.**

---

## Piping to Claude Code

**One question via echo:**

```bash
$ echo "What is the capital of France?" | claude -p   # one answer, shell returns
$ echo "Name three rivers in Africa." | claude -p
```

**A whole file:**

```bash
$ cat questions.txt | claude -p    # ten answers, shell returns
```

**Filter first, then ask Claude — this is the pattern:**

```bash
$ grep "#politics" questions.txt | claude -p    # two answers, not ten
$ grep "#economy" questions.txt | claude -p     # four answers, focused on economy
```

Filter with `grep`. Hand the result to Claude with `| claude -p`. **This is the pattern.**

---

## find — Find Files by Name

`grep` finds lines **inside** files. `find` finds the **files themselves** — by name, type, or location. Same idea as Finder's search bar — terminal version is faster and more precise.

**Anatomy of a `find` command:**

```
find   ~/Downloads   -name   "*.pdf"
 ↑         ↑           ↑        ↑
cmd    where to look  flag   pattern
```

| Command | What it does | Think of it as |
|---|---|---|
| `find ~ -name "research-paper.md"` | Search home folder, return absolute path | "Where does this file live?" |
| `find ~ -type f` | Every file under home | "List every notebook." |
| `find ~ -name "*.pdf"` | Exact match, case-sensitive | "Pull every PDF off the shelves." |
| `find ~ -iname "*RESEARCH*"` | Match anywhere in name, ignore case | "Shouted or whispered." |

**`-type f` = files. `-type d` = folders.**

**Where the `*` sits matters:** `"*.pdf"` = ends with .pdf · `"*pdf*"` = contains pdf anywhere · `"pdf*"` = starts with pdf.

**Silence the "permission denied" noise:**

```bash
$ find ~ -name "research-paper.md" 2> errors.txt   # errors go to file, matches print clean
```

---

## find + cat Demo — Read a File From Anywhere

```bash
# Step 1-2: find it, then cat via absolute path
$ find ~ -name "research-paper.md"          # prints /Users/<you>/Documents/research-paper.md
$ cat /Users/<you>/Documents/research-paper.md   # works — absolute path

# Step 3-4: cd to its folder — relative works
$ cd ~/Documents
$ cat research-paper.md                     # works — cwd contains the file

# Step 5-6: cd somewhere else — relative fails
$ cd ~/Desktop
$ cat research-paper.md                     # FAILS — no file in Desktop

# Step 7: absolute always wins
$ cat ~/Documents/research-paper.md         # works from anywhere
```

> **"Is the file in this folder?"** `ls | grep research-paper.md` — empty means no, a line means yes.

`~/...` always means the same place — **works from anywhere**. A bare filename means "in the folder you're standing in" — and that folder changes when you `cd`.

---

## less — Scroll a Long File

| Command | What it does |
|---|---|
| `less <file>` | Open file one screen at a time |
| `q` | Quit |
| Arrow keys | Scroll up/down |
| `/word` | Search inside |

`cat` dumps the whole file — `less` lets you scroll one screen at a time, like a pager. Use it for long files.

```bash
$ less ~/Documents/research-paper.md
```

---

## Quick Reference — Session 04 Commands

| Command | What it does | Think of it as |
|---|---|---|
| `echo "..."` | Print text to the output | "Say it out loud." |
| `\|` | Send output to another command | "Hand it along the assembly line." |
| `claude` | Chat mode — interactive | "Open a conversation." |
| `claude -p "..."` | Print mode — answer once, shell returns | "One question, one answer." |
| `echo "..." \| claude -p` | Ask Claude one question via pipe | "Say it, then ask." |
| `cat <file> \| claude -p` | Feed a whole file to Claude | "Whole file in, answers out." |
| `grep <text> <file>` | Print matching lines | "Highlight the lines with this word." |
| `grep <text> <file> \| claude -p` | Filter first, then ask Claude | "Filter, then ask." |
| `find ~ -name "..."` | Find file, return absolute path | "Where does this file live?" |
| `less <file>` | Read big file one screen at a time | "Pager. q to leave." |
| `find ~ … 2> errors.txt` | Silence permission-denied noise | "Filter the static." |
| `Tab · ↑ · Ctrl-L` | Autocomplete · previous command · clear screen | "The three shortcuts that pay back forever." |

## Take-Home Practice

1. **Ask Claude with echo.** Try three different one-line questions: `echo "What is an operating system?" | claude -p`, then `echo "What is a file?" | claude -p`, then one of your own. Notice the shell returns each time.

2. **Filter-first to Claude.** `grep "#economy" questions.txt | claude -p` and `grep "#geography" questions.txt | claude -p`. See the difference between asking 3 questions vs. asking 10.

3. **Find + path drill.** From anywhere, run `find ~ -name "research-paper.md"`. Copy the absolute path it prints. `cat` the file via that path — works. Then `cd ~/Documents` and `cat research-paper.md` — works. Then `cd ~/Desktop` and try `cat research-paper.md` — see it break. Switch back to the absolute path — works again.

> **There is no due date — the backlog grows if you skip.**

---

# Lesson 4: File Permissions, Users & Groups

**Session topic:** Why files on a shared Mac aren't automatically private — and how to control exactly who can read, write, or enter them.

---

## Why This Matters

Your Mac has more than one user. A shared computer — partner, sibling, child, a visiting relative — each can have their own login, their own home folder, their own files.

**Without controls:** Anyone with access to this Mac can poke at anyone else's stuff. No walls.  
**With permissions:** The OS keeps each user's stuff walled off. We get to decide who crosses.

File permissions are how a Mac keeps people walled off from each other. **That's the whole lesson.**

---

## Users

Every user has their own home folder. On a Mac, every account lives under `/Users/` — siblings, not nested.

```
/Users/
  ├── kurmanbek/       ← PRIMARY · INSTRUCTOR (your own username here)
  │   ├── Desktop/
  │   ├── Documents/
  │   └── Downloads/
  └── phoebe/          ← SECONDARY · STANDARD
      ├── Desktop/
      ├── Documents/
      └── Downloads/
```

- Two folders, two users — siblings, not nested.
- Neither user's home folder lives inside the other's.
- File permissions decide who can read across the gap.

---

## Groups

macOS gives you the groups you need. A group bundles users together so you grant access to many at once.

| Group | Who's in it |
|-------|-------------|
| `staff` | Every regular Mac user. The default. "All the normal people on this Mac." |
| `admin` | Users allowed to administer the machine — install software, change settings, override permissions. |

Two groups. Both already exist. No new groups to create.

---

## OS Context

macOS and Linux work the same way underneath — ~90% transfers when you meet servers later. Learning this the macOS way first.

---

## Setup: Two Tabs, Two Users

**Create a second user (GUI way):** System Settings → Users & Groups → Add User. Pick Standard (not Admin), name it `phoebe`, give it a password.

**Check who you are in the terminal:** `id` — tells you uid, gid, and groups.

```bash
# Tab 1 · kurmanbek (primary/admin)
$ id
uid=501(kurmanbek) gid=20(staff) groups=20(staff),101(admin),...
$ whoami
kurmanbek

# Tab 2 · switch to phoebe
$ su - phoebe
Password: ······
$ id
uid=502(phoebe) gid=20(staff) groups=20(staff),...
```

> **Note:** `kurmanbek` is the instructor's account. Yours will show your own username. The pattern is what to copy, not the name.

---

## The Surprise: Default Files Are Readable By Everyone

**Setup (Tab 1 · kurmanbek):**
```bash
cd ~/code/class5
claude -p "answer this in one short sentence and nothing else: what is the first iPhone chip?" > secret.txt
```

**Phoebe reads it (Tab 2):**
```bash
$ cat /Users/kurmanbek/code/class5/secret.txt
Samsung APL0098 (ARM11)     # phoebe reads it — no permission needed
```

**Why?** Check the permissions:
```bash
$ ls -l secret.txt
-rw-r--r--  1 kurmanbek  staff  ...  secret.txt
```

phoebe is in `staff` (group `r` works) AND she's "others" (`o` also has `r`). Either path lets her read.

**By default, files you create on a Mac are readable by every other user on this Mac.**

---

## The Permissions Model: ugo · rwx

Three classes × three actions — nine bits total.

```
3×3 MATRIX                  ls -l STRING
u · user (owner)    r w -   ┐
g · group (staff)   r - -   ├─ = -rw-r--r--
o · others          r - -   ┘     type|user|group|others
```

- The **matrix** is how you reason.
- The **string** (`-rw-r--r--`) is how the OS prints it.

**macOS default for a new file: `-rw-r--r--`** → owner reads + writes; group reads; others read. That's why phoebe walked right through.

---

## chmod — Change Permissions

### Symbolic form: `chmod WHO OP PERMS FILE`

| Part | Options | Meaning |
|------|---------|---------|
| **WHO** | `u` `g` `o` `a` | user/owner, group, others, all three |
| **OP** | `+` `-` `=` | add, remove, set exactly |
| **PERMS** | `r` `w` `x` | read, write, run/enter |

**Examples:**
```bash
chmod o+w secret.txt      # others can now write
chmod g-r secret.txt      # group loses read
chmod g=r script.sh       # group set exactly to read only (no w, no x)
chmod a+x script.sh       # all three classes get execute

# Comma form — multiple flips in one call, no spaces:
chmod g-r,o-r secret.txt  # group AND others lose read
```

### Numeric form: `chmod NNN FILE`

Each digit = sum of `r=4, w=2, x=1`. One digit per class (u, g, o).

| Number | String | Meaning |
|--------|--------|---------|
| `644` | `-rw-r--r--` | text-file default |
| `600` | `-rw-------` | owner only |
| `755` | `-rwxr-xr-x` | runnable + readable by all |
| `700` | `-rwx------` | owner-only script |
| `777` | `-rwxrwxrwx` | everyone-everything (avoid) |
| `640` | `-rw-r-----` | owner + group read, others none |
| `000` | `----------` | nobody (you can still chmod back) |

Same outcome as symbolic — just shorter.

---

## Demo: Tighten, Then Revert

```bash
# Tab 1 (kurmanbek) · TIGHTEN
$ chmod g-r,o-r secret.txt
$ ls -l secret.txt
-rw-------  1 kurmanbek  staff  ...  secret.txt   # owner only

# Tab 2 (phoebe) · BLOCKED
$ cat /Users/kurmanbek/.../secret.txt
cat: secret.txt: Permission denied

# Tab 1 (kurmanbek) · REVERT
$ chmod g+r,o+r secret.txt
$ ls -l secret.txt
-rw-r--r--  1 kurmanbek  staff  ...  secret.txt

# Tab 2 (phoebe) · READS AGAIN
$ cat /Users/kurmanbek/.../secret.txt
Samsung APL0098 (ARM11)
```

---

## Demo: Reading Isn't Writing

```bash
# Tab 2 (phoebe) · TRIES TO EDIT (default perms — no write)
$ vi /Users/kurmanbek/.../secret.txt
# edit, :wq
E212: Can't open file for writing

# Tab 1 (kurmanbek) · GRANT GROUP WRITE
$ chmod g+w secret.txt
$ ls -l secret.txt
-rw-rw-r--  1 kurmanbek  staff  ...  secret.txt

# Tab 2 (phoebe) · SAVES CLEANLY
$ vi /Users/kurmanbek/.../secret.txt
# edit, :wq — saves
$ cat /Users/kurmanbek/.../secret.txt
phoebe was here
```

> **Why `g+w`, not `o+w`?** phoebe is in `staff` — sharing via the group keeps it scoped. `o+w` would let any user on the Mac write.

---

## x on Folders: The Gatekeeper

`x` means different things depending on what it's on:

| Target | `x` means |
|--------|-----------|
| **File** | "This file is a program that can be run." Without `x`, even the owner can't execute it. |
| **Folder** | "You can enter / traverse into it." Without folder-`x`, even a readable file inside is unreachable. |

**Demo:**
```bash
# Tab 1 · SETUP
$ mkdir private-stuff
$ echo "do not read" > private-stuff/inside.txt
$ ls -ld private-stuff
drwxr-xr-x  kurmanbek  staff  ...  private-stuff

# Tab 2 (phoebe) · ENTERS FINE
$ cd /Users/kurmanbek/.../private-stuff
$ cat inside.txt
do not read

# Tab 1 · REMOVE x FOR GROUP + OTHERS
$ chmod g-x,o-x private-stuff
$ ls -ld private-stuff
drw-r--r--  kurmanbek  staff  ...   # no x on the folder

# Tab 2 (phoebe) · LOCKED OUT
$ cd /Users/kurmanbek/.../private-stuff
cd: permission denied
$ cat .../inside.txt
cat: permission denied    # file unchanged — just unreachable
```

**Folder-x is the gatekeeper. Whatever's inside, you can't get to it.**

---

## The "others" Class

`o` = everyone who isn't the owner and isn't in the group.

- **Default:** macOS makes every file you create readable by others (`-rw-r--r--`).
- **Fix for sensitive files:** `chmod go-r file` → owner-only.

---

## Admin Users & sudo

Some users are **admins** — they can install software, change system settings, and override file permissions.

**How macOS marks an admin:** System Settings → Users & Groups → "Allow this user to administer this computer." That toggle puts the user in the `admin` group. There's no separate "administrator account" — it's just group membership.

**`sudo` — run one command as admin:**
```bash
sudo <any command>   # runs with admin privileges; asks for YOUR own password
```

- Only admins (users in the `admin` group) can use `sudo`. Standard users get refused.
- What sudo lets admins do: install software (`brew install …`), create other users (`sysadminctl`), change permissions or ownership on any file.

---

## sysadminctl — Create Users from the Terminal

The modern macOS-recommended way to manage users from the terminal. Needs admin → use with `sudo`.

```bash
sudo sysadminctl -addUser NAME -fullName "Full Name" -password PASSWORD

# Example:
sudo sysadminctl -addUser rachel -fullName "Rachel Green" -password seekrit

# Make an admin from the start:
sudo sysadminctl -addUser rachel -fullName "Rachel Green" -password seekrit -admin
```

Same task as the System Settings demo (slide 6) — different surface.

---

## chown — Change Ownership

`chmod` changes **what** (permissions). `chown` changes **who** (owner/group).

```bash
sudo chown USER:GROUP FILE

# Example:
sudo chown rachel:staff tax.sh    # now rachel owns tax.sh
```

When you'll use it: a file ended up owned by the wrong user. `chown` fixes that. Requires `sudo`.

---

## Lesson 4 Cheat Sheet

| Command | What it does | Mental note |
|---------|-------------|-------------|
| `id` | See which user this terminal is | "Who am I?" |
| `whoami` | Short version of id | Just the username |
| `su - phoebe` | Switch to phoebe (needs phoebe's password) | "Become someone else." |
| `ls -l` | See permissions + ownership on each file | First column tells the whole story |
| `ls -ld folder` | See permissions on the folder itself (not its contents) | `-d` = directory itself |
| `chmod u+r file` | Symbolic — WHO + OP + PERMS | u/g/o + +/-/= + r/w/x |
| `chmod 644 file` | Numeric — same outcome, shorter | r=4, w=2, x=1, one digit per class |
| `chmod g-r,o-r file` | Multiple flips in one command (comma form) | Tighten sensitive files |
| `sudo chown user:group file` | Change a file's owner / group | Needs admin |
| `sudo <cmd>` | Run one command as admin | Admins only |
| `sudo sysadminctl -addUser …` | Make a user from the terminal | Modern macOS way |

**macOS default for new files:** `-rw-r--r--`. **Sensitive file?** `chmod go-r file`.

---

## What Was Deliberately Skipped (Linux variants)

These exist on Linux but weren't covered — we're on macOS. The concepts transfer; the syntax doesn't have to. AI can fill these in when you meet them:
- `useradd` · `groupadd` · `userdel`
- `/etc/passwd` · `/etc/shadow` · `/etc/group`
- the `wheel` group


---

# Lesson 5: Git & GitHub — Never Losing Your Files

**Session topic:** Version control — keeping a history of every change you make, backed up online. Two tools: Git (local, terminal) and GitHub (online copy).

---

## Why This Matters

Your files live in one place. The photos on your phone live on the phone — iCloud keeps another copy online. That second copy gives you: a backup (lose the phone, not the photos), reach from anywhere, and the ability to share.

Almost everything on a computer is a file — photos, documents, code. We all have files we don't want to lose.

**Two things we want for our files:**
1. **A safe place** — somewhere to keep them so we don't lose them.
2. **A history** — a way to see what changed, when, and how many times.

A safe place you might know. **The history part is the new idea.**

You've already seen history in Google Docs: File → Version history → See version history. Git gives you the same thing, but for any file on your computer.

---

## Meet Git

Git is the most popular tool in the world for keeping a history of your files.

- **Who made it:** Linus Torvalds, 2005 — the same person who made Linux.
- **How you use it:** You type commands (no app to click). It works on a whole **folder**, not one file at a time.

Git vs GitHub — two different things:

| | What it is |
|-|-----------|
| **Git** | The tool you run in the terminal. Keeps history locally. |
| **GitHub** | A website that holds a copy of your history online. |

---

## Installing Git

Git isn't on a Mac by default. Commands to install (do this with your instructor after class):

```bash
$ git --version          # is it already installed?
$ xcode-select --install  # Apple's version — the quick way
$ brew install git        # newest version, with Homebrew
```

---

## Setup: The Notebook Folder

This folder is yours — you'll keep adding to it all program long.

```bash
$ mkdir ~/code/notebook
$ cd ~/code/notebook
$ vi scifi-shows.txt     # type three shows, then save (Esc → :wq)
Silo
Foundation
Severance
```

---

## The One Big Idea: Git Only Remembers When You Tell It To

| Your phone / Google Docs | Git |
|--------------------------|-----|
| Saves by itself. You never decide — it just happens. | The opposite. Nothing is saved until you say so. |

Everything from here is just how to tell Git to remember.

---

## The Flow: Four Zones

```
YOUR FOLDER         PRE-LOADING AREA      MEMORY (.git)       GITHUB
(edit files)  →    (lined up, ready,  →  (saved for good,  → (online copy,
               git add   not saved yet)  git commit  won't forget)  git push  safe if laptop dies)
```

**Why two stops (add then commit)?** So you choose exactly what to save. Changed two files but only want to save one? Load just that one.

---

## git init — Start Keeping History

```bash
$ git init
Initialized empty Git repository in ~/code/notebook/.git/
$ ls -a
.    ..    .git    scifi-shows.txt
```

`git init` gets things ready so Git can start remembering this folder. **It does not save your files yet.** The hidden `.git` folder is where Git keeps its memory. Don't open it — just know it's there.

---

## git status — What Does Git See Right Now?

```bash
$ git status
On branch main
No commits yet
Untracked files:
  scifi-shows.txt
  (use "git add" to include in what will be committed)
```

**Untracked** = "in the folder, but not in Git's memory." You'll run `git status` all the time.

---

## git add — Load Into the Pre-Loading Area

```bash
git add FILE

$ git add scifi-shows.txt
$ git status
Changes to be committed:
  new file:   scifi-shows.txt
```

Loaded and ready — **but not in memory yet.** Loading is not the same as saving.

---

## git commit — Save Into Memory

```bash
git commit -m "MESSAGE"

$ git commit -m "Add my sci-fi shows list"
[main (root-commit) a1b2c3d] Add my sci-fi shows list
 1 file changed, 3 insertions(+)
```

This is the step that **actually puts it into memory.** The `-m` message is your label — you'll recognize it later.

---

## git log — See What You've Saved

```bash
$ git log
commit a1b2c3d  (HEAD -> main)
Author: Marsel <marsel@312school.com>
Date:   today

    Add my sci-fi shows list

# Compact version:
$ git log --oneline
a1b2c3d Add my sci-fi shows list
```

Your history, right there in the terminal — the same idea as the Google Docs history panel.

---

## git diff — See Exactly What Changed

After editing a file but before committing:

```bash
$ git diff
--- a/scifi-shows.txt
+++ b/scifi-shows.txt
 Silo
 Foundation
-Severance
```

`diff` = the difference between **right now** and the **last time you saved**. Removed lines marked `-`, added lines marked `+`. Check here before saving.

---

## The Everyday Git Loop

Every single time — same three steps:

```
git status       → What's changed?
git add FILE     → Load what you want to save.
git commit -m    → Save it, with a label.
git log          → Check the history.
```

Change something → check → load → save → look back. **You'll do this over and over.**

**Full example (second commit):**
```bash
$ vi scifi-shows.txt           # remove Severance
$ git status                   # shows: modified scifi-shows.txt
$ git diff                     # shows what changed
$ git add scifi-shows.txt
$ git commit -m "Remove Severance"
$ git log --oneline
b2c3d4e Remove Severance
a1b2c3d Add my sci-fi shows list
```

Two saved versions. Same rhythm every time.

---

## Enter GitHub — Put a Copy Online

So far everything is only on your laptop. If the laptop breaks, the history is gone. GitHub keeps a copy online.

**GitHub** is a website (owned by Microsoft) that holds a copy of your Git history. 312School uses it for your classes too.

### Create a Repo on GitHub

In the 312school org → New repository:
- Owner: `312school`
- Name: `your-name-notebook`
- Description: "My learning notes."
- **Visibility: Private ✓** — Always pick this unless you mean otherwise. (Public = the entire internet can read your files.)

Leave template / README / license at their defaults. The new repo starts empty.

---

## SSH Keys — How the Terminal Logs Into GitHub

| In a browser | In the terminal |
|---|---|
| Username + password | SSH key — a strong password your computer makes and shows GitHub automatically |

**Make your key and add it to GitHub:**

```bash
# In the terminal:
$ ssh-keygen              # press Enter at every prompt
$ cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAA... yourname@laptop
```

Then on GitHub:
- Settings → SSH and GPG keys → New SSH key
- Name it "My laptop key"
- Paste the line you copied → Add SSH key

SSH keygen makes two files: a **private** one (stays secret on your machine) and a **public** one (`.pub` — safe to share). **You only ever paste the public one.**

---

## git remote add — Connect Your Folder to the Online Copy

```bash
git remote add origin SSH-URL

$ git remote add origin git@github.com:312school/your-name-notebook.git
$ git branch -M main      # names the main line "main"
```

After this, `.git/config` will show a `[remote "origin"]` section pointing to GitHub.

---

## git push — Send Your History Online

```bash
git push -u origin main

$ git push -u origin main
# first time: may ask "are you sure?" — answer yes
To github.com:312school/your-name-notebook.git
 * [new branch]    main -> main
```

Refresh the GitHub page — **your file and its history are now online.** After the first push, future pushes are just `git push`.

---

## Looking at History on GitHub

- **Commits view** — your `git log`, on the website. Every saved version, in order.
- **Click any commit** — GitHub shows exactly what changed (that's `git diff` in the browser, with lines highlighted).

Two ways to read the same history: in the terminal, or on the website. Same saves, either place.

---

## Stuck? Ask Claude to Look — Not to Fix

Putting things online is where errors happen (a typo, a login issue). Right now you're learning the basics by hand. Use this prompt pattern:

```
I'm trying to push my changes to my GitHub repository and it's not
working. Here's the repo link: github.com/312school/your-name-notebook

Can you investigate and explain what's wrong — but DON'T fix it for
me. Just tell me what to do and what I need to understand.
```

> **Why not just let it fix things?** If Claude does it, you won't understand what happened — and at this stage, **understanding is the whole point.**

---

## Lesson 5 Cheat Sheet

| Command | What it does | When |
|---------|-------------|------|
| `git init` | Start keeping history for this folder | Once, per project |
| `git status` | What does Git see right now? | Constantly |
| `git add FILE` | Load a file into the pre-loading area | Before every commit |
| `git add .` | Load all changed files | Shortcut |
| `git commit -m "msg"` | Save to memory with a label | After add |
| `git log` | See all saved versions | Anytime |
| `git log --oneline` | Compact history view | Anytime |
| `git diff` | See what changed since last commit | Before committing |
| `ssh-keygen` | Make an SSH key pair | Once per machine |
| `git remote add origin URL` | Connect folder to GitHub | Once per project |
| `git branch -M main` | Name the main line "main" | Once per project |
| `git push -u origin main` | Send history online (first time) | First push |
| `git push` | Send history online (after first) | Every push |

**The everyday rhythm:** edit → `git status` → `git add` → `git commit -m "..."` → `git push`

---

## Take-Home Practice

After installing Git with your instructor, open your `notebook` folder and run the loop:

```bash
# add one more show to scifi-shows.txt, then:
$ git add scifi-shows.txt
$ git commit -m "Add another show"
$ git push
```

Refresh GitHub and watch your change show up. No due date — just practice.


---

# Lesson 6: Servers, AWS, EC2 & Linux

## Recap: Your Laptop vs a Server

**PC — Personal:** One person. Travels with you. Stops when you close it.

**Server — The Workhorse:** Built to run software, for many. Lots of raw power · no screen · cheaper.
- Lives in a data center
- Runs 24/7, never travels
- No fancy UI to pay for
- Cheaper for the work it does

## Recap: Don't Buy a Server — Rent It. That's the Cloud.

Own it = your problem: buy hardware ($$$), find space, stable power & internet 24/7, fix it when it breaks, manage it forever.

**Rent it = their problem.** A cloud provider's data center handles all of that — space, power, internet, repairs, management.

> You just rent a server…and pay only for the time you use it.

You pay **only for what you use**, and the giant in this space is **AWS**.

## AWS: Where Your Server Lives

AWS's data centers are grouped into **regions**. When you rent a server, you pick which region it lives in.

- AWS worldwide → many regions, all over the globe
- **US East (N. Virginia)** — the default & biggest — ours

> Plain version: your server will physically sit in **Virginia.**

## AWS Credits — Trying It for Free

You already created your AWS account during onboarding — on the **Free Plan**, so trying this out costs you nothing.

| What | Detail |
|------|--------|
| **$100–$200 in credits** | $100 when you sign up, plus up to $100 more for a few starter tasks |
| **About 6 months** | Spend it over roughly six months. If it runs out, AWS **stops** — it won't bill you |
| **A small server is cheap** | A `t3.micro` is about **$7.50/month** — your credit easily covers the course |

> One habit: **stop your server when you're done**, so the credit lasts.

## Let's Actually Rent One

The three steps: **Log in** to the AWS Console → **Launch a server** with default settings → **Connect** a terminal, in your browser.

### Step 1: Log into the AWS Console

You sign into your **AWS account** and land in the **AWS Console** — a **website** where everything in AWS is managed. That's all it is — a website you open in your browser.

### Step 2: Find EC2

AWS offers a lot of services. The one that **rents you a server** is called **EC2**.

EC2 is short for **Elastic Compute Cloud**. You find it by typing `EC2` in the console search bar.

### Step 3: Launch One Server

In the AWS Console:
1. Search **EC2** → open it
2. Click **Launch instance**
3. Keep the **default settings**
4. Click **Launch**

We keep everything default for now. We'll come back to the settings later; today we just create the server.

### Step 4: Connect from Your Browser

In the AWS Console:
1. Select your running instance
2. Click **Connect**
3. Choose **EC2 Instance Connect**
4. Click **Connect** — a terminal opens in your browser

No keys, no setup — that's the whole point of connecting this way today. That black window is a terminal running **on the server**, not on your Mac.

## You're on a Computer in Virginia

```
[ec2-user@ip-172-31 ~]$ whoami
ec2-user
[ec2-user@ip-172-31 ~]$
```

Your Mac (here, browser open to AWS) → EC2 Instance Connect → **EC2 Instance · Data Center, Virginia** (a real computer you rented).

> This terminal runs HERE — on the server, not on your Mac.

Clicking "launch" was easy — anybody can. As engineers, we go a level deeper: **what is this machine?**

## What Is This Machine?

Anybody can click "launch" and get a server. Engineers don't stop there — the real question is: **what is this machine, and what is it running?**

### The Word for It: An Instance

The server you launched on EC2 has a name: an **instance** — an EC2 instance.

Plain version: it's just **your one rented server.** Other clouds use different words — the idea is what matters.

### How Is It Different from My Mac?

| Your Mac | Your Server |
|----------|-------------|
| Runs Apple's operating system — **macOS** | Runs something different — **Amazon Linux** |

Why something different? To answer that, we need to know what an operating system even is.

## What Is an Operating System?

### Every Computer Has Three Layers

```
┌─────────────────────────┐
│      Applications       │  ← what you use
├─────────────────────────┤
│    Operating System     │  ← the platform in the middle (macOS · Windows · Linux)
├─────────────────────────┤
│        Hardware         │  ← the physical machine
└─────────────────────────┘
```

> Without it, you can't even install an app — let alone run one.

### The OS Is the Platform in the Middle

It sits between the hardware and your apps and lets them talk to each other. It's what lets you use the computer at all.

Without an operating system you can't even **install** an application, let alone run one. Your Mac's macOS does this for you right now — **Amazon Linux does it on the server.**

### Three Operating Systems You'll Meet

| OS | Where |
|----|-------|
| **macOS** | on Apple's Macs |
| **Windows** | on most other laptops, from Microsoft |
| **Linux** | a whole family — your server runs it |

Your server's **Amazon Linux** belongs to the **Linux** family.

## Linux

### Linux Is Open Source

| Property | Meaning |
|----------|---------|
| **Public code** | Anyone can see the code that makes it work |
| **Built by a community** | People worldwide improve it and fix it — often for free |
| **Free, owned by no one** | No single company owns it. It's free to use |

A familiar example: **Wikipedia**. Everyone can see it, and the community keeps making it better. Open-source software works the same way.

Safety: Trusted maintainers review every change before it's merged — a newcomer isn't trusted by default. Strong, but not perfect: an attacker once spent a year earning trust before slipping in bad code (caught just days before release).

### Why Servers Love Linux

It's free — and one of the best operating systems in the world for running a machine that never stops:

- **Free** — no license cost
- **Efficient** — lean, no wasted overhead
- **Robust & secure** — battle-tested for 24/7 uptime

**Key point: Linux runs on *any* computer.**

### So Why Not macOS on the Server?

**macOS:**
- Apple hardware only — runs only on machines Apple makes
- Not open source — you can't put it on a rented server

**Linux:**
- Runs anywhere — open source, any hardware
- Runs on a laptop, a server, a cloud instance — all of it

### Amazon Linux — AWS's Own Linux

The system on the instance you launched is **Amazon Linux** — AWS's own member of the Linux family, and the default for EC2.

> You've been using **Linux** this whole time — now you know what it is.

## Take-Home: Recreate One at Home — Then Terminate It

On your own, no rush:

1. Launch a fresh `t3.micro` with the default settings, then **Connect** with Instance Connect
2. Run one command on it — try `whoami` or `ls` — just to prove you're on the server
3. Then **Terminate** it — it's empty, so there's nothing to keep

> **Stop vs. Terminate:** `Stop` keeps your files for next time (you still pay a little for the saved storage). `Terminate` deletes the server for good. Today there's nothing on it — so terminate.

## Lesson 6 Quick Reference

| Term | Plain meaning |
|------|--------------|
| **Cloud** | Renting someone else's server instead of buying your own |
| **AWS** | Amazon's cloud — the biggest one |
| **Region** | A geographic cluster of AWS data centers (ours: US East / Virginia) |
| **EC2** | Elastic Compute Cloud — the AWS service that rents you a server |
| **Instance** | One rented server on EC2 |
| **OS** | Operating system — the platform between hardware and apps |
| **Linux** | Open-source OS family that runs most servers in the world |
| **Amazon Linux** | AWS's own flavor of Linux, the EC2 default |
| **EC2 Instance Connect** | Browser-based terminal that connects you to your server — no keys needed |
| **Stop** | Pause the instance; files saved; small storage charge continues |
| **Terminate** | Delete the instance permanently |

---

# Lesson 7: SSH, Networking & Firewalls — Find It, Log In, Guard It

## Today in Three Moves

Mac → Cloud → EC2

1. **Find it — the address**: Every server has an **IP address** on the internet, and a **port** — which door to knock on.
2. **Log into it — SSH**: A private **key** on your Mac opens the server — stronger than a password, and from your own terminal.
3. **Guard it — the firewall**: A **security group** controls who can reach the server at all, and through which door.

> Each one is a layer — the address gets you there, the key lets you in, the firewall says who's allowed near it.

## Recap: Training Wheels Are Off

Last time you rented a real server (an EC2 instance running Amazon Linux) and got onto it with the browser's **Connect** button. That was the training wheels.

Engineers connect from **their own terminal** — but to do that, you first have to point at the machine by its address.

> First, find your server. Open the EC2 console: if it's **running**, great; if you **stopped** it, start it again (its public address may have changed); if you **terminated** it, launch a fresh one — this time with a key.

## The Network

A **network** is computers connected so they can talk to each other. The **internet** is one giant network that nearly every machine plugs into.

Your **Mac** plugs in through your home router and your internet provider. Your **server** plugs in from inside a data center. Same giant network — so they can reach each other.

## IP Addresses

To reach a machine, you need its address — its **IP address**. Just like a house needs a street address so mail can find it.

```
54 . 226 . 10 . 18
```

Four numbers, each 0–255. This is what your server's address actually looks like.

> Your server has one. Your Mac has one. **Every machine on the network has one.**

### IPv4 vs IPv6

| Version | What it is |
|---------|-----------|
| **IPv4** | Four numbers like `54.226.10.18`. The original standard, still most common. The catch: **the world is running out of them.** |
| **IPv6** | A newer, much larger standard so we never run out. Most of the world is still moving over to it. |

Because IPv4 addresses are now scarce, **AWS charges a small hourly fee** for a public IPv4 address — on top of what you pay for the server itself.

### Public IP vs Private IP

**A public address is reachable from anywhere. A private one isn't.**

```
YOUR HOME NETWORK
┌─────────────────────────────────┐
│  Your Mac          Home router  │
│  private IP:       public IP ───┼──→ THE INTERNET ──→ Your EC2 server
│  192.168.1.5                    │                       public IP
└─────────────────────────────────┘
Outsiders reach the router — not your Mac directly.
```

> The internet **can't reach your Mac directly** — that's the defense.

So you can reach your EC2 from anywhere — but you couldn't reach a classmate's laptop across the internet.

## Ports — Which Door to Knock On

The IP address gets you to the machine. The **port** says which door — a machine has tens of thousands of doors (about 65,000), and we open only the few we need.

```
Port 22 = SSH — logging in
...different doors for different jobs
...most stay closed
```

> The door we'll use to log into the server is **door 22** — that's the one SSH uses.

## TCP vs UDP — How Data Travels

**TCP** is reliable — every message is acknowledged. **UDP** is faster, but messages can be lost.

| TCP | UDP |
|-----|-----|
| Reliable. In order. Every message is received and acknowledged. | Fast but unreliable. Some messages arrive, some are lost, order not guaranteed. |

Like talking: with **TCP** you catch every word; with **UDP** you might miss half, but it's faster. (Layer 4 of the OSI model — we won't cover the rest.)

## The Whole Path, End to End

From your Mac to your server — every hop is real:

```
Your Mac       Home router    Internet       The internet    AWS data        Your EC2
(in the room)  (Wi-Fi box)    provider       (one giant      center          (your server)
private IP  →  public IP   →          →       network)  →   Virginia    →   public IP
```

Both ends plug into the same internet — that's how they reach each other.

> Each arrow is a real handoff. **This is the picture to hold** when you type a connect command.

## Logging In with SSH

We've been getting on through the browser's Connect button — training wheels. Engineers log in from their own terminal, and the tool for that is **SSH**.

### Why Not Just a Password?

Your server has a **public IP** — reachable from anywhere. So anyone on the internet can sit there and guess your password.

```
123456   ✗
password ✗
qwerty123 ✗
… 99,997 more …
hunter2  ✓  in
```

**100,000+ guesses a second** — until one works.

A password alone is too weak. So servers use something stronger: **a pair of keys**.

### SSH: The Tool

**SSH** is a command-line tool that opens a secure login to another computer over the network.

It's already installed on **your Mac** and on your **Amazon Linux** server — it has to be on both ends. Nothing to install today.

### The Key Pair

You get a **pair** of keys that only work together:

- **Private key** — stays secret on your Mac. Never share it, never send it.
- **Public key** — sits on the server. Safe for anyone to see.

The server lets you in only when your private key matches the public key it holds.

### Two Ways to Make a Key Pair

Both end in the **same thing**: a private key on your Mac, a public key for the server.

| Method | How |
|--------|-----|
| **1 · The AWS console** | AWS makes the pair for you, and you download the private key as a `.pem` file. This is the pair an instance is launched with — and how you start a fresh server if yours is gone. |
| **2 · ssh-keygen** | You make your own pair on your Mac with one command, then put the public key on a server you already have running. |

#### Method 1 — AWS Console

```bash
# In the EC2 console
Key Pairs → Create key pair → name: my-key → downloads my-key.pem

# On your Mac — lock the file down so SSH will accept it
chmod 400 my-key.pem
```

That `my-key.pem` file **is your private key**. AWS keeps the matching public key and puts it on any server you launch with this pair — so if your instance is gone, **launch a fresh one and pick this key pair**, and it's born ready for SSH.

#### Method 2 — ssh-keygen

```bash
ssh-keygen -t ed25519 -C "my-laptop"   # press Enter through the prompts

ls ~/.ssh
id_ed25519        # the private key — stays on your Mac
id_ed25519.pub    # the public key — safe to share
```

If your server is still running, paste the `.pub` file's contents onto it (in `~/.ssh/authorized_keys`, via browser Instance Connect) and you're in — no relaunch. AWS made the pair in Method 1; here **you** made it. Same shape, same result.

## The SSH Command

```bash
ssh -i my-key.pem -p 22 ec2-user@54.226.10.18
```

| Part | Meaning |
|------|---------|
| `ssh` | the command |
| `-i my-key.pem` | your private key |
| `-p 22` | the SSH door |
| `ec2-user` | the login name on Amazon Linux |
| `@54.226.10.18` | the EC2's public IP |

> About `-p 22`: 22 is SSH's default door, so you can leave `-p 22` off and it still works. We show it so you can see which door you're knocking on.

### Success vs Failure

```
# First try might fail:
Permission denied — wrong key, wrong user, or the key file isn't locked down (chmod 400).

# Then you're on the server:
[ec2-user@ip-… ~]$   — same server as the browser window, now from your own machine.
```

## SSH Is on Mac and Linux — Not Windows

| OS | SSH |
|----|-----|
| **macOS** ✓ | Built in. Mac is Unix-based. |
| **Linux** ✓ | Built in. Same Unix family as the Mac. |
| **Windows** ✗ | Doesn't have it the same way. |

> You could even SSH from your Mac into a classmate's Mac — but only on the **same network** (same home or office), since a home Mac has no public IP. Be careful giving anyone access to your machine.

## Copying Files with scp

Same keys, one more command. `scp` copies files between your Mac and the server — **both directions**.

Which side you write first decides the direction:

```bash
# Send a file UP to the server
scp -i my-key.pem notes.md ec2-user@54.226.10.18:~/

# Pull a file DOWN from the server
scp -i my-key.pem ec2-user@54.226.10.18:~/notes.md .
```

> The server side always looks like `user@address:path`. The `.` at the end means "right here, in this folder."

## The Firewall — Security Groups

You can now log in from your terminal and move files. Your SSH key makes the **login** safe.

But there's an earlier layer: who can even **reach** your server over the network to try the door at all? That layer is a **firewall** — and on AWS it has a name.

### A Security Group Is Your Server's Firewall

A **firewall** is a set of network rules: who's allowed to reach your machine, and on which door. On AWS, that firewall is called a **security group**, and every server has one.

> You already have one. When you launched your server, AWS made a security group for you automatically — it's the reason your SSH connection on **port 22** got through at all.

### A Rule = A Source + A Door

Each rule allows traffic by two things:
- **Source** — which IP addresses may connect
- **Port** — which door they may reach

Example: *allow port 22 (SSH) from your IP only* — only you, from your address, can knock on the SSH door.

### Look at Your Own Security Group

```bash
# In the EC2 console
Instances → your instance → Security tab → open its security group

# Inbound rules — the doors that are open
Port 22  ·  Source: your IP   # this is what let your SSH in
```

> Today we just **look** — find the port-22 rule and see that it's what let you in. You *could* tighten the source from "anywhere" to just your IP, but be careful: the wrong change can lock you out of your own machine.

## Two Layers of Security

| Layer | What it does |
|-------|-------------|
| **SSH keys — the login** | Secures the login itself — proving it's really you. A password alone is too weak. |
| **Security group — the network** | Secures the network access — who can reach the server at all, and on which door. |

> Both do real work, at different layers. The firewall decides who reaches the door; your key decides who comes in.

## Take-Home

On your own, no rush:

1. SSH back into your server from your own terminal: `ssh -i my-key.pem ec2-user@<your-public-ip>`
2. Use `scp` to send one file **up** to the server, then pull one back **down**
3. Open your **security group** in the console and find the **port-22** inbound rule that's letting you in

> If you stopped your server, its public IP changed — grab the current one from the console. And **stop it again** when you're done, so your credit lasts.

## Lesson 7 Quick Reference

| Term | Plain meaning |
|------|--------------|
| **IP address** | The unique address of a machine on the network (e.g. `54.226.10.18`) |
| **IPv4** | Original 4-number IP format — the world is running out |
| **IPv6** | Newer, much larger address space — world migrating to it |
| **Public IP** | Reachable from anywhere on the internet |
| **Private IP** | Only reachable within your local network (e.g. `192.168.1.5`) |
| **Port** | A numbered door on a machine; SSH uses port 22 |
| **TCP** | Reliable delivery — every packet acknowledged |
| **UDP** | Fast delivery — some packets may be lost |
| **SSH** | Secure Shell — command-line tool to log into a remote machine |
| **Key pair** | A matched private key (your Mac) + public key (the server) |
| `.pem` file | Your private key downloaded from the AWS console |
| `chmod 400` | Lock down the key file — SSH won't work without it |
| `ssh-keygen` | Command to generate your own key pair |
| `scp` | Secure copy — moves files between your Mac and server |
| **Security group** | AWS's name for a firewall — rules controlling who can reach which port |
| **Inbound rule** | Allows traffic IN to your server (source IP + port) |

---

# Lesson 8: DNS, nginx & Deploying Your Website — Name It, Build It, Serve It

## The Goal: Four Moves

| Step | What | Details |
|------|------|---------|
| 1 | Name it | DNS — a real domain people can type |
| 2 | Build it | A website on your Mac (Claude writes it) |
| 3 | Install nginx | A web server on EC2 to hand out files |
| 4 | Serve it | Open the web door — live, for everyone |

---

## How DNS Works

**DNS = Domain Name System** — the internet's address book. It adds a layer **on top of** IP. The number doesn't go away; the name points at it.

```
aigul.click  →  DNS looks it up  →  54.226.10.18
```

Analogy: tapping "Mom" in your contacts → the phone dials the number.

**DNS servers** (also called name servers) hold the address book. Many of them, run by different companies. Amazon's name servers answer for AWS-managed domains.

**The full lookup flow:**
Your Mac (you type `aigul.click`) → ASKS Name server → `aigul.click = 54.226.10.18` → ANSWERS → EC2

---

## Buying a Domain

Domains are bought. Once you buy one, you are the owner — written down where the whole internet can check.

| Role | What They Do |
|------|-------------|
| **You** | Pick a name nobody owns yet, pay a few dollars/year |
| **The registrar** | Company you buy through — maintains/verifies ownership (like a title company). Route 53 is one. |
| **The domain registry** | Official list of who owns which name. Your entry: `aigul.click — owner: you` |

### Route 53 — AWS's DNS Service

Route 53 does both halves of the job:
- **A registrar** — buy your domain here (search, pay, it's registered)
- **Name servers** — Amazon's servers hold your address book and answer anyone who asks for your name

Your server already lives in AWS — so name and server sit in one console.

### How to Buy (in AWS Console)
```
Route 53 → Registered domains → Register domains
Search .click (usually ~$3/year) → pick a name → Proceed to checkout → complete purchase
```

If AWS says no (free plans): click Upgrade plan — it kept the free credits in place in class.  
Alternative: GoDaddy sells `.click` for ~$2 first year (+$0.18 ICANN fee). **Cancel auto-renew** — year two is ~$22.

Registration takes a few minutes, occasionally up to an hour.

---

## DNS Records

### The Hosted Zone

When registration completes, Route 53 automatically creates a **hosted zone** for your domain — the folder that holds its DNS records. It starts with two records:

| Record Name | Type | Value |
|-------------|------|-------|
| `aigul.click` | **NS** | `ns-1492.awsdns-58.org`, `ns-705.awsdns-24.net`, … (the four Amazon name servers) |
| `aigul.click` | **SOA** | Housekeeping details — there by default, nothing to memorize |

Those two came free. The record that points at your server — you create that yourself.

### The A Record

**An A record** = one line in your hosted zone: **this name → this IPv4 address**

```
server.aigul.click   A   54.226.10.18
^                    ^   ^
NAME                TYPE  VALUE (your EC2's public IP)
```

You can use the bare domain (`aigul.click`) or a subdomain (`server.aigul.click`) — both are A records, your choice.

### Creating Your A Record (in AWS Console)
```
Hosted zones → aigul.click → Create record

Record name: server        # or leave blank for the bare domain
Record type: A
Value:       54.226.10.18  # your server's public IPv4
→ Create records
```

⚠️ **CAREFUL — Stop changes your IP.** Stop → Start gives your server a NEW public IP. Your record then points at the old number — fix it by updating the record's value.

New records take a minute or two to spread. Watch it at dnschecker.org.

`AAAA` is the same record for IPv6. Our servers use IPv4, so A record is what we create.

### SSH by Name

Once the A record propagates, you can SSH using the name instead of the IP:
```bash
ssh -i my-key.pem ec2-user@server.aigul.click
```
If it fails: `Could not resolve hostname` — the record is still spreading. Wait a couple of minutes.

If you see **"WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!"** — the name pointed at a different server before. Clear and reconnect:
```bash
ssh-keygen -R server.aigul.click
```

---

## Building a Website

### A Website Is Just Files

- **A page** = one HTML file. Text in, drawn page out.
- **A website** = a folder of those files.
- **A browser** = the app that reads the file and draws it.

### The Build Rules: Three Pages, Your Idea

Claude Code writes the site — your job is everything that happens to these files next.

- Exactly **3 pages**: `index.html` at the top level, plus **two more pages each inside their own folder**
- One `style.css` is fine — holds the look (colors, fonts)

### Prompting Claude Code
```bash
cd ~/code/notebook   # the lab folder from the Git classes
mkdir website
cd website
claude
```

The prompt (swap in your own topic):
```
Build a small website about Kyrgyz recipes. Exactly three HTML pages:
index.html at the top level, and two more pages each inside its own
folder. One style.css is fine; no other files.
```

After: `ls`, then `find . -name "*.html"` — three pages with their paths.  
If Claude asks permission for every file, `Shift+Tab` switches to auto-accept for this session.

### File Structure and Paths

```
website/
├── index.html         ← the top — the main page
├── style.css          ← the look — not a page
└── recipes/
    ├── plov.html
    └── lagman.html
```

The two inner pages live **at paths** — folder, slash, file: `recipes/plov.html`.  
These are the same paths you've been walking since your first `cd`.

### Open It Locally
```bash
open .    # opens the folder in Finder — then double-click index.html
```

Address bar shows: `file:///Users/you/code/notebook/website/index.html`  
Your page, drawn by the browser — straight from the file. No internet involved.  
Click a link: watch it change to `.../recipes/plov.html`.

### The Problem: Only You Can See It

The website works — but it's on your Mac, which has **no public IP**. Nobody on the internet can reach it. Your server has a public IP and now a name. What's missing: a program on the server whose job is handing out files.

---

## What's an Application?

An application = **a program that runs and does a job** (Finder, Terminal, Claude Code — those have windows).

| Apps on your Mac | Apps on a server |
|-----------------|-----------------|
| Have windows and buttons. You click them, they do their job in front of you. | No window, no screen. They just run — all day, doing their job for anyone who connects. |

That's most of what a server is: a machine that runs applications around the clock.

---

## nginx — The Web Server

**nginx** (say it "engine-X") = a web server. When a visitor asks for a page, nginx finds the right file and hands it back — that's the whole job.

```
Visitor (any browser, anywhere)
  "give me /recipes/plov.html"
         ↓
      nginx (on EC2, runs all day, no window, waits for visitors)
         ↓ looks in
    the website folder
      → finds recipes/plov.html
         ↓
    hands the file back to the visitor
```

---

## Installing and Running nginx

### Package Managers Install Software by Name

No App Store on a server. Software arrives through a **package manager**:

| Package Manager | Platform |
|----------------|---------|
| `brew` | Your Mac |
| `dnf` | Amazon Linux (your server) — used today |
| `apt-get` | Other Linux (Ubuntu, Debian) |

`yum` is the old name most people remember — `dnf` is its successor, and `yum` still works on your server.

### Install nginx
```bash
sudo dnf install nginx    # run as admin, install nginx
  …resolves, downloads…
  Is this ok [y/N]: y
  Complete!

nginx -v    # prove it exists — prints the version
```

Your server now has a web server. It just isn't running yet.

### Services — Apps the System Runs for You

On Linux, background apps like nginx run as **services**: the system starts them, keeps them running, and can bring them back at boot. The control switch is `systemctl`:

```bash
sudo systemctl start nginx
#     ^          ^     ^
# run as admin  verb  which service
```

The verb in the middle is the part that swaps: **start** it, **stop** it, ask for its **status**.

### Start and Verify
```bash
sudo systemctl start nginx     # prints nothing — on Linux, silence is success

sudo systemctl status nginx
● nginx.service - The nginx HTTP and reverse proxy server
     Active: active (running) since Tue 2026-06-09…    ← the line to find
# q to leave if it pages
```

Green **"active (running)"** = your web server is alive. Learn to spot that line — you'll read it for every service from now on.

### Enable — Survive the Reboot

| Command | Today | After reboot |
|---------|-------|-------------|
| `start` only | RUNNING | STOPPED — your website is down |
| `start` + `enable` | RUNNING | RUNNING — system started it at boot |

```bash
sudo systemctl enable nginx    # prints "Created symlink" — Linux saying "noted"
```

Servers reboot (updates, failures, restarts). `enable` means nginx comes back without you.

---

## nginx Configuration and the Web Root

### Applications Keep Their Settings in Files

On Linux, an app's settings live in **text files** (config files). Same pattern as dotfiles on your Mac, but system-wide.

- `/etc` = the folder where Linux keeps applications' settings
- nginx's config file: `/etc/nginx/nginx.conf`
- The question: Which folder does nginx serve files from?

### Find the Config and Pull Out the Web Root
```bash
sudo find /etc -name "nginx.conf"    # find WHERE PATTERN
  /etc/nginx/nginx.conf

grep root /etc/nginx/nginx.conf
  root    /usr/share/nginx/html;    ← the answer
```

**`/usr/share/nginx/html`** is the **web root** — the folder nginx serves files from. Write it down.

Open the file with `less` for a look around — settings are readable text, not magic.

---

## HTTP — How Browsers Talk to Web Servers

**HTTP** = HyperText Transfer Protocol = the standard protocol (the agreed way of talking) between browsers and web servers. The browser asks for a path; the server answers with the file.

- Every address starts `http://` or `https://`. The S is the secure version.
- HTTP messages travel by **TCP** — the reliable delivery method from the networking classes.

### The Web Doors: Port 80 and Port 443

Every protocol has its usual door — SSH = door 22. The web has two:

| Port | Protocol | Use |
|------|---------|-----|
| **80** | HTTP | Standard web door — used today |
| **443** | HTTPS | Secure web door — we earn the padlock next class |

You can write the port in the address: `http://54.226.10.18:80` — but when you leave `:80` off, the browser assumes it. Same as `-p 22` being optional in `ssh`.

---

## Opening Port 80 in the Security Group

### Why the Browser Spins

Your security group has **one rule**: door 22, for SSH. A browser knocks on door 80. No rule for 80 → the guard ignores the knock → the browser spins.

**No rule, no entry.**

### Open Door 80 (in EC2 Console)
```
instance → Security tab → security group → Edit inbound rules → Add rule
  Type:   HTTP           # fills in port 80 for you
  Source: Anywhere-IPv4  # 0.0.0.0/0 — "anywhere" = the whole internet

Add rule again:
  Type:   HTTPS          # door 443 — open now, earn the padlock next class
  Source: Anywhere-IPv4

→ Save rules → refresh the browser
```

Result: **"Welcome to nginx!"** — the default page, reachable by IP and by name.

Why "Anywhere" is right: a website is FOR everyone. Your SSH door stays yours; the web door opens to the world.

---

## One Page Load, End to End

```
1. The browser          → someone types http://server.aigul.click anywhere on earth
2. DNS answers          → 54.226.10.18 (your A record, doing its quiet job)
3. Door 80, guarded     → security group checks: port 80, anyone — allowed ✓ (your rule)
4. nginx hears it       → the app you installed, started, and enabled
5. Your file            → index.html, from the web root, written by your prompt
                        ← the page travels back — the visitor sees your website
```

**Domain (you bought) · record (you created) · door (you opened) · server app (you installed) · files (you shipped).**

---

## Deploying Your Files

### Ship Your Files to the Web Root

The nginx "Welcome" page is its placeholder, living in the web root. Put **your** three pages there and nginx serves your site.

```bash
# Step 1 · On your Mac — send the folder up (note -r for recursive/folders)
scp -i my-key.pem -r website ec2-user@server.aigul.click:~
#                   ^          ^                          ^
#              recursive   what to send            home folder on server

# Step 2 · On the server, over SSH — copy contents into the web root
sudo cp -r ~/website/* /usr/share/nginx/html/

ls /usr/share/nginx/html    # verify — your pages, at their paths
  index.html    style.css    recipes/    …
```

**Why land in `~` and not the web root directly?** The web root belongs to root — you can't `scp` straight into it. Land in home folder first, then `sudo cp` into place. Two steps, every time.

The `*` copies the **contents** of `website/` — so `index.html` sits at the top of the web root and your site lives at the domain itself.

### Visit Your Live Site
```
http://server.aigul.click
```

Your site — not the nginx placeholder — the pages you built, served from your server, under your name. Take out your phone and type a neighbor's domain — it's a real public website. Anyone on earth can visit it.

Troubleshooting:
- "Refused to connect"? Your browser quietly tried `https://` — type `http://` yourself. The secure door comes next class.
- Still seeing the Welcome page? Hard-refresh (hold Shift while reloading).

### URL Paths Mirror Your File Paths

| In the address bar | On the server (web root) |
|-------------------|-------------------------|
| `http://server.aigul.click/` | `index.html` ← nginx default |
| `http://server.aigul.click/recipes/plov.html` | `recipes/plov.html` ← the same path |

`/` means "the homepage" — nginx serves `index.html` by default. Everything else is the file at that path under the web root. **The browser is walking your folders.**

---

## Take-Home

1. Open your own domain on your phone and a friend's phone — it's public, anyone can reach it.
2. Add or edit a page locally, `scp` it up, then `sudo cp` it into `/usr/share/nginx/html/`, refresh, and watch the change go live.
3. If you stop your box to save money, remember the **public IP changes** — update your A record before you panic.

**Two analogies to keep:**
- DNS is an **address book** (you tap "Mom," the phone dials the number)
- A security group is a **building with doors and a guard** — you just opened door 80 to everyone

---

# Lesson 9: curl, HTTP, HTTPS & TLS Certificates — Talk to It, Lock It, Check It

## The Goal: Three Moves

| Step | What | Details |
|------|------|---------|
| 1 | Talk to it | `curl` — read the web's conversation from the terminal |
| 2 | Lock it | A free certificate — "Not Secure" gone for good |
| 3 | Check it | Logs + network checks when something breaks |

Honest expectations: the certificate stretch is the **longest demo run of the course so far**. Your site showing secure is the destination.

## Recap: Where We Left Off

You now host a real website — anyone on earth can type your address:
- **Your domain** (`aigul.click`, registered to you) + **Your A record** (name points at EC2's IP)
- **nginx** (running on server, handing out files) + **Your three pages** (served from the web root)

So far the browser is how you've seen your site. But engineers check sites with **no browser at all** — servers have no browser, and scripts have no hands. Today the terminal becomes a place you can visit the web from.

---

## curl — The Command-Line Browser

**curl** sends an HTTP request and prints the answer — "a command-line browser, kind of." Except it doesn't draw anything: it shows you the **raw HTML file** the browser would have drawn.

```bash
curl http://server.aigul.click/recipes/plov.html
```

Already installed on your Mac **and** on your server — like ssh, it's on both ends. Nothing to install.

### Demo: curl Your Own Site
```bash
# On your Mac
curl http://server.aigul.click
  <!DOCTYPE html><html>…    # recognize it? your index.html, raw

curl http://server.aigul.click/recipes/plov.html    # path swaps like in the browser

# Bonus: over SSH, on the server itself
curl http://server.aigul.click    # the server can visit itself — no browser anywhere
```

Same files, two viewers: the browser **draws** them, curl **shows** them.

---

## Anatomy of an HTTP Request and Response

Every HTTP exchange has three parts:

| Part | What It Is |
|------|-----------|
| **Method** | What you want done. `GET` = "give me." What browsers do all day. |
| **Path** | Which file. `/recipes/plov.html` — same paths as ever. |
| **Headers** | Extra info lines — like sender details on an envelope: who's asking, what they accept. |

**The full flow:**
```
Your Mac (curl in terminal)                  Your EC2 (nginx)
  curl http://server.aigul.click/recipes/plov.html
         ↓
  sends: GET /recipes/plov.html HTTP/1.1    finds the file the path names
         Host: server.aigul.click
         ...headers...
                                             ↓
                        HTTP/1.1 200 OK + the file
                        (status code first, then headers, then the page)
```

One flag makes the whole conversation visible: **`-v`** — verbose, "show me everything."

### Demo: Watch the Whole Conversation (`curl -v`)
```bash
curl -v http://server.aigul.click/
```

**What curl sends — the request:**
```
> GET / HTTP/1.1           ← METHOD + PATH
> Host: server.aigul.click ← HEADER
> User-Agent: curl/8.7.1   ← HEADER
> Accept: */*              ← HEADER
```

**What the server answers — the response:**
```
< HTTP/1.1 200 OK          ← STATUS CODE
< Content-Type: text/html  ← HEADER
< Content-Length: 1024     ← HEADER
<!DOCTYPE html> …          ← THE FILE ITSELF
```

`>` means sent, `<` means received.

**`-L` follows redirects** — if a site answers 301 Moved, plain curl just prints the redirect and stops; `curl -L` goes on to the real page.

---

## Status Codes — The Answer's First Line

Every response starts with a verdict number:

| Code | Meaning |
|------|---------|
| **200 — OK** | "Here you go." The file existed; it's in the answer. |
| **404 — Not Found** | "I looked — that file isn't there." Usually a path typo. |

**The family rule — by first digit:**

| Range | Meaning |
|-------|---------|
| **2xx** | Fine — 200 lives here |
| **4xx** | Problem on **your** side — wrong path (404), or not allowed (401/403, like the portal off-VPN) |
| **5xx** | Problem on the **server's** side |

You'll see these numbers again in nginx's logs.

### Demo: Earn a 404 on Purpose
```bash
curl -v http://server.aigul.click/no-such-page.html
  > GET /no-such-page.html HTTP/1.1
  < HTTP/1.1 404 Not Found
  <html>…nginx error page…</html>
```

The server answered **properly**: "I looked, that file isn't there." An error code is the system **talking**, not the system broken.

---

## HTTP Methods

**GET** asks for a file. **POST** sends data *to* a server — forms, uploads. Others exist (`PUT`, `DELETE`) — recognize the names, that's enough for now.

`-X` picks the method:
```bash
curl -X POST http://server.aigul.click/
  < HTTP/1.1 405 Not Allowed    # your nginx hands out files; it doesn't accept any
```

The method **asks**; the server **decides**. Yours politely refuses — exactly right for a site that serves files.

### curl or Browser — Which, When

| The browser | curl |
|------------|------|
| Much simpler — you just click. Draws pages, runs page code. Perfect for **being a visitor**. | Works where no browser exists — servers, scripts. Shows the raw conversation. Perfect for **checking and automating**. |

Fancy curl commands take real skill — asking Claude to write the curl command is the normal move. Later, when we automate deployments, a curl check is how a script proves the site is up.

---

## The Problem with Plain HTTP

### HTTP Travels Like a Postcard

Your pages cross many machines on the way to a visitor — router, provider, the internet, AWS. With plain HTTP, **any machine on that path can read everything** — like a postcard, no envelope.

```
http:// — the postcard:
visitor → their router → the provider → the internet → AWS → your server
            CAN READ IT    CAN READ IT   CAN READ IT  CAN READ IT

https:// — the sealed envelope (same HTTP, encrypted in flight):
visitor → their router → the provider → the internet → AWS → your server
CAN UNSCRAMBLE  CAN'T    CAN'T          CAN'T         CAN'T  CAN UNSCRAMBLE
```

**TLS** is the name of that wrapping. The S in https is "secure"; TLS is *how*.

### The Encryption Concepts (Khan Academy video: youtu.be/6-JjHa-qLPk, ~6 min)

- **Encryption** = scrambling a message so it's unreadable
- **Modern keys are unguessable** — 256-bit; trillions of years, even for supercomputers
- **Public/private keys** — the mailbox: anyone drops mail in (public key); only the owner's key opens it (private key)
- **SSL/TLS** — the names behind HTTPS

### A Certificate Proves It's Really Your Site

Scrambling is half of what makes a site secure. The other half is **proof**. A **certificate** = a file on the server that does two jobs:

| Job | What it does |
|-----|------------|
| **Proof** | "This domain belongs to this server" — issued by an authority browsers already trust |
| **Keys** | Carries the keys used for the scrambling |

Callbacks: same public/private pattern as SSH keys — public piece shown to everyone, private piece that never leaves.

**Practical rule:** if a site shows "Not Secure," never type a password, card number, or SSN into it — on plain http every machine on the path can read it.

---

## Getting a Free Certificate: Let's Encrypt + certbot

### How It Works

**Let's Encrypt** issues certificates free. **certbot** is the tool that requests one.

The condition: **prove you control the domain** — certbot proves it by writing a record into your Route 53 hosted zone. Only the owner can do that.

**Three steps to a free certificate:**

```
1. certbot writes the proof
   From your Mac, with AWS keys, certbot drops a temporary record
   into your hosted zone:
     _acme-challenge → proof text   (only the owner can write here)

2. Let's Encrypt checks
   The certificate authority looks up that record on the public internet.
   It's there → the domain is yours.  (ownership proved ✓)

3. The certificate arrives
   Two files land on your Mac:
     fullchain.pem — certificate, public
     privkey.pem   — private key, secret  (same public/private pattern as SSH)
```

Next: scp both files to the server and tell nginx to use them.

### Five Moves to a Secure Site

| Step | Action |
|------|--------|
| **1 · PROVE** | certbot writes a proof record into your Route 53 zone (needs AWS CLI + your keys) |
| **2 · RECEIVE** | Two files on your Mac: `fullchain.pem` + `privkey.pem` at `~/letsencrypt/live/…` |
| **3 · SHIP** | `scp` both files up, then `sudo cp` into `/etc/nginx/ssl/` (same two-step as your pages) |
| **4 · POINT** | Edit `nginx.conf`: `listen 443 ssl;` / `ssl_certificate …` / `ssl_certificate_key …` · check with `nginx -t`, restart |
| **5 · SERVED** | Every https visitor is shown the certificate; the browser trusts it — site reads **secure** |

---

## The AWS CLI — AWS from Your Terminal

For certbot to write that record *for you*, your Mac needs permission to touch your AWS account. The **AWS CLI** = AWS as a command-line tool — everything the console does, typeable.

- **Console** (you click) = **AWS CLI** (you type)
- Today's narrow use: let certbot write one DNS record into your hosted zone
- Where this goes later: scripts that drive AWS — same keys power the automation topic ahead

### IAM — AWS's User and Permissions System

The CLI doesn't log in with your email and password. It uses **access keys** — two long strings (an ID and a secret) that belong to a **user** in your account. **IAM** = AWS's system for users and permissions.

| Part | Details |
|------|---------|
| IAM user (`aigul-cli`) | An account inside your AWS account for the CLI |
| Access key ID | `AKIAIOSFODNN7EXAMPLE` — public part |
| Secret | `wJalrXUtnFEMI/K7MDENG…` — shown **ONCE**; treat it like a password. **Never in chat, never in a screenshot.** |

Today: the minimum — one user · admin access · two keys. Coming soon: separate users, limited permissions, retiring root for daily work.

### Demo: Install the CLI and Create the User

```bash
# Beat 1 · On the Mac
brew install awscli
aws --version

# Beat 2 · In the AWS console
IAM → Users → Create user → name: aigul-cli
  → Attach policies directly → AdministratorAccess
  → the user → Security credentials → Create access key (CLI)
  # keep this page open — the secret shows ONCE
```

### Demo: Connect Them — `aws configure`

```bash
aws configure
  AWS Access Key ID:     paste the key ID
  AWS Secret Access Key: paste the secret
  Default region name:   us-east-1    # N. Virginia — a fine default
  Default output format: press Enter

aws route53 list-hosted-zones    # the proof it works
  "Name": "aigul.click."          # YOUR domain, answered in the terminal
```

The console, now typeable. Your Mac officially has AWS powers — exactly what certbot needs.

---

## Getting Your Certificate (The Demo)

### Install certbot and Its Route 53 Plugin

```bash
brew install certbot

"$(brew --prefix certbot)/libexec/bin/python3" -m pip install certbot-dns-route53
# brew alone doesn't include the Route 53 plugin — this second line adds it
```

⚠️ If you later run `brew upgrade certbot`: the plugin gets wiped — re-run the second line.

### Ask for Your Certificate

```bash
# On the Mac — NO sudo, on purpose
certbot certonly --dns-route53 -d server.aigul.click \
  --config-dir ~/letsencrypt --work-dir ~/letsencrypt/work --logs-dir ~/letsencrypt/logs

  …certbot writes the proof record, Let's Encrypt checks it, then…
  Successfully received certificate.
```

Two files land on your Mac:
- `~/letsencrypt/live/server.aigul.click/fullchain.pem` — the certificate (public, shown to every visitor)
- `~/letsencrypt/live/server.aigul.click/privkey.pem` — the private key (secret, never shown to anyone)

**Why no sudo?** sudo would look for AWS keys in *root's* home and miss what `aws configure` wrote in yours. The `--…-dir` flags keep certbot's folders in your home instead. `certonly` = "just get me the files" — we install them ourselves. `-d` names the certificate: use the exact address visitors type.

### Ship It to the Server

```bash
# Step 1 · On your Mac — scp both files up
scp -i my-key.pem \
  ~/letsencrypt/live/server.aigul.click/fullchain.pem \
  ~/letsencrypt/live/server.aigul.click/privkey.pem \
  ec2-user@server.aigul.click:~

# Step 2 · On the server, over SSH — copy into place
sudo mkdir -p /etc/nginx/ssl
sudo cp ~/fullchain.pem ~/privkey.pem /etc/nginx/ssl/
```

### Tell nginx to Use It

Nobody knows nginx's TLS settings by heart — search or ask Claude for the snippet. Into `nginx.conf` with `vi`:

```nginx
# The three lines that matter — inside the server block
listen 443 ssl;
ssl_certificate     /etc/nginx/ssl/fullchain.pem;
ssl_certificate_key /etc/nginx/ssl/privkey.pem;
```

```bash
sudo nginx -t               # "do my settings parse?" — cheap insurance
sudo systemctl restart nginx
```

Stuck? Claude can SSH in, look around, and explain back what it found — then **you** apply the fix. The certificate goes into place by your hands.

### Open Door 443 and Go Secure

Your security group already has port 443 open (you added it last class "just in case"). If not:
```
EC2 console → Security Group → Edit inbound rules → Add rule → HTTPS + Anywhere-IPv4 → Save
```

Now visit `https://server.aigul.click` in the browser:
- The "Not Secure" warning is **GONE**
- Click the icon next to the address → "Connection is secure" → view the certificate: issued by Let's Encrypt, for YOUR domain
- The browser's https-first habit — the thing you've been typing `http://` around all day — just stopped being a problem; your address now works **however you type it**

# Lesson 10: When It Breaks, Logs, the Triage Ladder & Your First Bot — Look, Check, Build

## Recap: TLS is now automatic

Your two cert files (`fullchain.pem` + `privkey.pem`) sit in `/etc/nginx/ssl/` and do their job on every single visit — no clicking, no action required. The conversation (method · path · status) is the same as always, just sealed in flight. Important weekend note: if your EC2 was stopped, the public IP may have changed — grab the current one from the console and confirm your A record still points to it before doing anything else.

**What you pulled off last class (four checkboxes):**
- Proved ownership — certbot wrote into your hosted zone; only the domain owner can do that
- Got a real certificate — issued free by Let's Encrypt, for your domain
- Installed it by hand — `scp`'d up, wired into nginx, restarted
- Walked through the secure door — port 443; the "Not Secure" warning gone

Key lesson: things broke for real along the way — spinning tabs, stale IP, "refused to connect," the 404 you earned on purpose. Each time, the fix started with **looking somewhere specific**. Engineers don't guess. **"Broken things are normal; checkable things are calm."**

---

## Log files — nginx's diary

A **log file** is where an app writes down what happened — one line per event, newest at the bottom. nginx keeps two:

| File | What it records |
|---|---|
| `access.log` | **Every visit.** Who came, what they asked for, what they got. |
| `error.log` | **Every problem.** What went wrong, when. |

They live in `/var/log/nginx/`. The Linux convention: settings in `/etc`, diaries in `/var/log`.

### Reading the live log with `tail -f`

```bash
sudo tail -f /var/log/nginx/access.log   # -f = follow: keep printing new lines as they arrive. Ctrl-C stops.
```

A real log line looks like this:
```
203.0.113.7 - - [09/Jun/2026:19:02:11 +0000] "GET /recipes/plov.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0 (iPhone…)" "-"
```

Breaking it down: **visitor's IP** · **when** · **method + path** (the curl words) · **status code** (200 = OK) · **their browser** · the "-" spots are extra details, often empty.

Refresh your site on a phone → watch the line appear in real time. Have a neighbor visit — there they are.

```bash
sudo tail /var/log/nginx/error.log   # one look, usually quiet
```

---

## nslookup — ask DNS directly

**First question when "the site doesn't open":** does the name still point where you think?

`nslookup` asks DNS: name in, IP out — your A record, checked from the outside world.

```bash
nslookup server.aigul.click          # name in, IP out — match against EC2 console
nslookup google.com                  # several IPs — big sites use many machines; fine
dig server.aigul.click               # alternative: same answer, more detail
```

`dig` = same job as nslookup, more detailed output. Web version: **nslookup.io** — a privately run website (not an official internet service), gives you a second opinion from outside your own machine.

---

## ping — are you there?

`ping` sends tiny "are you there?" messages and counts replies and round-trip time. The classic connectivity test.

```bash
ping 8.8.8.8   # 8.8.8.8 = one of Google's public servers — effectively always up. Worth memorizing.
```

When "nothing works," `ping 8.8.8.8` splits the world in two: **my internet** vs **everything else**. It runs forever — Ctrl-C stops it.

**Pinging your own server:** your security group opened ports 80, 22, and 443 — but not ICMP, which is ping's own protocol. So your server stays silent by default. Add an ICMP rule in the security group → the server answers (`64 bytes from … icmp_seq=0 time=1.7 ms`).

To test your own internet at home: `ping 8.8.8.8`, then turn Wi-Fi off — replies stop. Same tool, your own machine.

---

## The triage ladder — check in this order

When your site has a problem, run these four checks, in order:

| Step | Question | Command |
|---|---|---|
| 1 | My internet? | `ping 8.8.8.8` |
| 2 | The name? | `nslookup server.aigul.click` |
| 3 | The web server? | `curl -v https://server.aigul.click` → check status code |
| 4 | What happened? | `sudo tail -f /var/log/nginx/access.log` · `error.log` |

Every rung is a tool you personally ran. This ladder is most of what "debugging a website" means day to day — and it's what you tell Claude you already checked when you ask for help.

---

## Part Two: Build something new on your server

The hosting block is closed. Same EC2 — a new job. Stop *visiting* your server; start making it **work for you**.

**Today's finish line:** your server texts you the news.
- Your EC2 server → Claude runs on it and writes a short news update
- → Telegram → your bot posts it into your channel
- → Your phone → buzz, the news arrives

In future classes this bot learns to run by itself, hide its keys properly, and keep its history. Today: version 1, every piece by hand.

---

## Claude on the server — and the stuck screen

```bash
# On the EC2, over SSH:
curl -fsSL https://claude.ai/install.sh | bash   # install Claude Code on the server
claude -p "say hello from this server"
✗ Not logged in — no API key found.              # exact wording may differ
```

On your Mac, Claude opened a browser and you logged in — a person proved who they are. There's no browser on the server, and nobody sitting there. **Programs prove it differently.**

---

## API key — a keycard for programs

An **API key** = a long secret string a service gives you. A program shows it with every request — like a hotel keycard: **the door doesn't know your face, it knows the card.**

| Who | How they prove identity |
|---|---|
| You, on your Mac | Log in through the browser — a person proves who they are |
| A program, on a server | Shows its key — Anthropic knows: "this program acts for you, let it in" |

You already own a key like this: the SSH key that gets you into your server is the same idea — a secret that proves it's you.

### Getting your Anthropic API key

```
platform.claude.com → API keys → Create key
# The key shows ONCE — copy it now, treat it like a password
sk-ant-api03-…   # yours will look like this
```

**One hard rule:** never paste a key into a file you push to GitHub. Your notebook repo is public — a key in there is a key everyone has.

**Cost:** API usage is billed separately — your monthly Claude subscription does **not** cover it. Preload a small balance (~$5 is plenty for class), and use **Sonnet** (the medium model), not Opus, so a run costs pennies.

---

## Environment variables — labeled notes your terminal keeps

A **variable** = a name with a value kept under it — like a sticky note. Your terminal **session** (session = from login to logout) can keep notes like this, and any program you run can read them. They're called **environment variables**.

```bash
export MY_NAME="Aigul"   # "keep this note" · the label · no spaces around = · what's written
```

### The one rule everyone trips on: $ means "the value inside"

```bash
echo MY_NAME    # → MY_NAME   (just the word — forgot the $)
echo $MY_NAME   # → Aigul     (the value inside — correct)
```

Write the name to **set** it. Put `$` in front to **use** it. That's the whole rule.

### Practice demo

```bash
export MY_NAME="Aigul"
echo MY_NAME          # MY_NAME   (oops, no $)
echo $MY_NAME         # Aigul     (correct)
export MY_NAME="Aigul S."   # change the note — same label, new value
echo $MY_NAME         # Aigul S.
```

Two bonus commands: `env` lists every note in this session · `unset MY_NAME` removes one — no need to log out.

### Setting the real key

The label is **not your choice** this time. Claude Code looks for a note named exactly `ANTHROPIC_API_KEY` — a typo means it finds nothing, silently. That's how programs find their settings: an agreed place, an agreed label.

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-…"   # paste YOUR key — quotes keep the dashes as one string
claude -p "say hello from this server"
Hello from your server! 👋                   # resolved — no login, no browser needed
```

---

## The problem with session memory

```bash
exit                          # close the session
ssh -i my-key.pem ec2-user@… # come back
claude -p "hello?"
✗ Not logged in — no API key found.   # the note is gone
echo $ANTHROPIC_API_KEY               # (empty — the note vanished)
```

**Why?** The notes live in the session's **memory** — nothing was ever written to disk. Close the session and the notes go with it. Your files survive; the notes don't. Re-typing the key every login gets old fast — that's the rough edge you fix in the next class (a script the server loads automatically).

---

## Telegram: bots and channels

Most of you use Telegram every day. Today it becomes **infrastructure** — a working part of your system.

- **A bot** = a Telegram account that a **program** controls instead of a person
- **A channel** = a one-way feed that accounts can post into — followers just receive

**The plan:** your bot posts → your channel receives → your phone buzzes.

### Create your bot with BotFather

BotFather = Telegram's official bot for making bots. Message it, answer two questions, get a token:

```
In Telegram:
@BotFather → /newbot → pick a name → pick a username ending in "bot" → done
token: 7421…:AAH…    # that string is an API key — your SECOND one today

On EC2:
export TELEGRAM_BOT_TOKEN="7421…:AAH…"   # the move you already know — new label
```

Two keys, two jobs: the first lets Claude **think** · this one lets your bot **speak**. Same rules — it's a secret.

### Create your channel and add the bot

```
In Telegram — three taps:
New Channel → name it (e.g. Aigul's News) → public, pick a @username (e.g. @aiguls_news)
Channel settings → Administrators → add your bot
# admin = the bot is allowed to POST, not just read
```

Your bot shows up in the members list as an admin — "has access to messages" is what lets it post rather than just read.

### Fire the first post

```bash
# On the EC2 — watch Claude work, step by step:
claude -p "Check today's top news about space. Write a short, friendly update (3-4 sentences). Post it to my Telegram channel @aiguls_news using the bot API — the token is in TELEGRAM_BOT_TOKEN." \
--allowedTools "WebSearch" "Bash" --verbose
# → searching the news… → writing the update… → calling the Telegram API…
# buzz — today's news, in your channel
```

**Two new flags:**
- `--allowedTools` — in `-p` mode Claude can't use any tool unless you explicitly allow it. This allows two: WebSearch (to find the news) and Bash — the shell it runs `curl` in to post to Telegram.
- `--verbose` — print every step as it happens.

Claude is **a program doing steps**, not magic. Watch it think, write, and post.

---

## The full picture — every box is yours

```
YOUR EC2 SERVER (always on, in the cloud)
  claude -p  →  checks news · writes post
        |                          |
   ANTHROPIC_API_KEY          TELEGRAM_BOT_TOKEN
        |                          |
   ANTHROPIC               TELEGRAM → your channel → YOUR PHONE (buzz)
   (answers Claude's questions)     (your bot speaks)
```

| Key | Variable name | Job |
|---|---|---|
| Key #1 | `ANTHROPIC_API_KEY` | Connects to your Claude account — Claude is the thinker |
| Key #2 | `TELEGRAM_BOT_TOKEN` | Connects as your bot — which speaks (via text) |

**The two moves to remember:** `export NAME=value` — leave a note · `echo $NAME` — read it back.

---

## Take-home

- Run the **four triage checks** on your own site, in order: `ping 8.8.8.8` · `nslookup server.<domain>` · `curl -v https://server.<domain>` · then `sudo tail -f /var/log/nginx/access.log` while you load the site from your phone — watch yourself arrive.
- `curl` a classmate's site too — compare the status line and headers that come back.
- Run your news bot again: `export` both keys, then the post command with a topic you actually care about. Your phone buzzes.
- Notice you had to re-type both keys after logging back in. That re-typing is the one rough edge left — and it's exactly what you automate next, with a script the server runs for you.

# Lesson 11: Scripts, cron & Secrets Manager — Run It, Schedule It, Lock It

## Recap: the bot works, one step was missing

What you completed last class: got two keys (Anthropic + Telegram bot token), made the bot with BotFather, created your channel. One thing was left — the bot wasn't added as a channel admin yet, so the first post never fired. That's the very first fix today.

Note: if your EC2 was stopped since last class, its public IP may have changed — grab the current one from the console and reconnect before starting.

---

## Step 1 — Finish it: the first post

**Add the bot as admin** (in Telegram — three taps):
```
New Channel → name it (e.g. Aigul's News) → public, pick a @username (e.g. @aiguls_news)
Channel settings → Administrators → add your bot
# admin = the bot is allowed to POST, not just read
```

The bot shows up as "admin" in the members list. "Has access to messages" is what lets it post, not just read.

**Fire the first post** (on the EC2, keys already exported):
```bash
claude -p "Check today's top news about space. Write a short, friendly update (3-4 sentences). Post it to my Telegram channel @aiguls_news using the bot API — the token is in TELEGRAM_BOT_TOKEN." \
--allowedTools "WebSearch" "Bash" --verbose
# → searching the news… → writing the update… → calling the Telegram API…
# buzz — today's news, in your channel
```

Use **Opus or Sonnet** for this — a smaller model like Haiku may still pause for confirmation even with tools allowed.

---

## The pain that comes next

Every login: `export ANTHROPIC_API_KEY=…` — again. `export TELEGRAM_BOT_TOKEN=…` — again. The long claude command — again. The notes vanished with your session, so you retype every time. The news only arrives when YOU show up. The server is awake anyway — what if it did all of it without you?

---

## Step 2 — Make it run itself: scripts and cron

### What a script is

A **script** = a text file holding commands. The shell reads it top to bottom and runs each line **exactly as if you typed it**. Like a recipe card — the same steps you already cook by hand, written down so they run the same every time, even when you're not cooking. Every line in the file is a command you already know from version 1.

### The shebang — line 1 of every script

The first line names **which program reads the rest**:

```
#!/bin/bash
```

`#!` = the marker — "hash-bang," said fast: **shebang**. `/bin/bash` = the program that runs your lines. Always line 1, write it once and move on.

### Write news.sh

```bash
#!/bin/bash
export ANTHROPIC_API_KEY=sk-ant-api03-…      # note #1 — lets Claude think
export TELEGRAM_BOT_TOKEN=7421…:AAH…         # note #2 — lets your bot speak
claude -p "Check today's top news about space. …
  Post it to my Telegram channel @aiguls_news …" \
  --allowedTools "WebSearch" "Bash" --verbose  # your exact command from version 1
```

**Why `--verbose` stays:** run the script by hand and you watch Claude's steps print; when cron runs it, nobody is watching — the chatter is thrown away. Every line gets a "you know this."

### Make it runnable and run it

```bash
chmod +x news.sh    # permissions: x on a file = "runnable as a program"
./news.sh           # ./ = relative path — THIS folder, THIS file
                    # → searching… → writing… → calling API… → buzz
```

**Closing version 1's pain:**
```bash
exit → ssh back in → ./news.sh → buzz    # nothing retyped!
```

The session notes vanished — but **the script carries its own**. That's the fix.

### The catch: keys are now written in a file

```bash
cat news.sh
#!/bin/bash
export ANTHROPIC_API_KEY=sk-ant-api03-THE-WHOLE-SECRET-RIGHT-THERE
export TELEGRAM_BOT_TOKEN=7421…:AAH-AND-THIS-ONE-TOO
…
```

Anyone who reads this file owns your keys — and files get copied, backed up, pushed to GitHub by accident. There's a proper place for keys. That's step 3.

### cron — the server works while you sleep

At 9:00 tomorrow: you're not logged in, laptop closed. But your EC2 is always awake — nginx is already serving your site without you. **cron is the same kind of always-on service**: a list of "at this time, run this command."

**The cron line — five time slots, then the command:**

```
0  9  *  *  *  /home/ec2-user/news.sh
│  │  │  │  └─ every day of the week
│  │  │  └──── every month
│  │  └─────── every day
│  └────────── hour 9
└───────────── minute 0
```

Read it out loud: "at 9:00, every day — run my script." The `*` means "every." Other rhythms exist (every 30 min, weekdays only) — same five slots, different numbers. Not today's problem.

### Schedule it

```bash
# First time on Amazon Linux 2023 — cron isn't preinstalled:
sudo dnf install -y cronie          # the cron package
sudo systemctl enable --now crond   # start its daemon + keep it on after reboots

crontab -e                          # opens the list — in vi, which you know
0 9 * * * /home/ec2-user/news.sh
# :wq — same vi save as always
crontab -l                          # show the list — your line is on it ✓
```

**Job never fired?** The cron daemon isn't running — check with `systemctl status crond`. On AL2023 that's the usual culprit.

From now on, 9:00 belongs to the server. It runs `news.sh` on its own, even with you logged out and your laptop closed — tomorrow your phone buzzes and you did nothing.

**Make it yours:** open `news.sh` in vi and change the prompt to a topic you actually want — "today's football transfer news", "news from Kyrgyzstan today", "today's space launches". Rather have it at 7:00 than 9:00? Edit your cron line — you can read it now.

---

## Step 3 — Lock the keys away: Secrets Manager

### The problem

The script runs daily — one rough edge left: `cat news.sh` shows your keys in plain text. Anyone who reads the file owns them: a teammate on a shared server, a backup, one accidental `git push` to the wrong repo. The fix in one sentence: keep the secret in a locked place, and have the script ask for it when it runs.

### AWS Secrets Manager — a safe for keys

Like the safe in a hotel room: valuables go in, you ask for them when you need them, **they're never lying on the desk**. Secrets Manager is AWS's safe — it stores secrets, and programs request them at run time.

| Version | Where keys live | Risk |
|---|---|---|
| Version 1 & 2 | Written in the file (`export KEY=sk-ant-…`) | Anyone who reads the file owns the keys. Files get copied, backed up, pushed by accident. |
| Version 3 | Fetched from the safe at run time | The file holds no secrets. Copy it, push it — nothing leaks. |

Same bot, same behavior — only **where the keys live** changes. (AWS also has Parameter Store — we use Secrets Manager, the main one.)

### Fill the safe (in the console — twice, once per key)

```
Secrets Manager → Store a new secret → Other type of secret → Plaintext
  paste the key → name it news-bot/anthropic → Store ✓
  …and again: the bot token → news-bot/telegram → Store ✓
```

Two **separate** secrets — `news-bot/anthropic` and `news-bot/telegram` — each fetched by its own name. A name and a value, like your session notes — only the value now lives in the safe, not in your file.

### The AWS CLI — because a script can't click

Everything you've clicked in the console can also be typed as a command — that's the AWS CLI. Today it matters because **a script can't click a console**. Your Mac is already signed in to AWS (since the certificate work). Your EC2 is signed in as no one — that's where today's story ends.

### Ask for the key back — and get a wall of text

```bash
# On the Mac — the machine that's signed in:
aws secretsmanager get-secret-value --secret-id news-bot/anthropic
{
  "ARN": "arn:aws:secretsmanager:us-east-1:1234…",
  "Name": "news-bot/anthropic",
  "VersionId": "a81d…",
  "SecretString": "sk-ant-api03-…",
  "VersionStages": [ "AWSCURRENT" ],
  "CreatedDate": "2026-06-…"
}
```

Don't panic — the safe answered. It just answered with paperwork.

### JSON — how computers write things down

People write sentences. Computers want **key:value** pairs.

"My name is Aigul, I'm 30, and I live in Bishkek." → a computer writes that as:
```json
{
  "name": "Aigul",  "age": 30,  "city": "Bishkek"
}
```

A key, a colon, then its value — with braces `{ }` around the set. You already do this every day: a paper form with `Name ___` and `Phone ___` is the same thing. The safe answered in exactly this shape. Two fields matter; the rest is paperwork:
- `"Name"` → which secret this is
- `"SecretString"` → **the value we want** (our actual key)

### `--query` — ask for just one field

The answer has six fields; the script needs one. Two additions trim it down:

```bash
aws secretsmanager get-secret-value --secret-id news-bot/anthropic \
  --query SecretString --output text
sk-ant-api03-…    # exactly one line: the key
```

`--query SecretString` = just this field · `--output text` = no quotes, just the value. This exact tail — `--query SecretString --output text` — every time. One shape, no variations.

### `$( )` — run a command, drop its answer in

Like working out an answer mid-sentence: *"I live in… let me think… Bishkek."* You find the answer first, then say it. `$( )` tells bash the same thing: **run the part inside the brackets first, then put its answer right there.**

```bash
echo "I am in $(pwd)"
I am in /Users/aigul    # $(pwd) ran first — its answer dropped into the sentence
```

Two beats: `$(pwd)` runs and prints `/Users/aigul` → bash swaps that in → the line becomes `echo "I am in /Users/aigul"`. The brackets always run first.

### Fill the note with the key — without typing it

```bash
# On Mac (signed in):
export ANTHROPIC_API_KEY=$(aws secretsmanager get-secret-value \
  --secret-id news-bot/anthropic --query SecretString --output text)
# $() fetches the key → export saves it as the same note — you never see or type it
```

### news.sh version 3 — no secrets inside

```bash
#!/bin/bash
export ANTHROPIC_API_KEY=$(aws secretsmanager get-secret-value \
  --secret-id news-bot/anthropic --query SecretString --output text)
export TELEGRAM_BOT_TOKEN=$(aws secretsmanager get-secret-value \
  --secret-id news-bot/telegram --query SecretString --output text)
claude -p "Check today's top news…" --allowedTools "WebSearch" "Bash" --verbose
```

Proof: `cat news.sh` — **no keys anywhere in the file**. Copy it, push it — nothing leaks.

### Access Denied — the server has no identity yet

```bash
# On the EC2:
./news.sh
An error occurred (AccessDeniedException) … is not authorized to perform:
secretsmanager:GetSecretValue
```

The exact command that worked on the Mac fails here. The Mac is signed in to AWS; the server is signed in as **no one**. The safe didn't say "wrong key" — it said **"I don't know WHO is asking."** Who can do what in your AWS account is its own system — **IAM. That's next.**

### The retrieval cycle (how it all fits together)

```
news.sh (no secrets inside)
  → aws … get-secret-value (the CLI asks)
  → the safe (Secrets Manager)
  → JSON answer (--query picks the value, --output text drops quotes)
  → $() writes it into export
  → ANTHROPIC_API_KEY note is set
  → claude -p runs — same bot as always, zero secrets in the file
```

**The one-liner to remember:**
```bash
aws secretsmanager get-secret-value --secret-id news-bot/anthropic --query SecretString --output text
# Same shape for news-bot/telegram
```

One door still closed: the server has no identity. Giving it one — properly — is the next topic (IAM).

---

## Take-home

- Your bot runs itself — check your schedule with `crontab -l`; tomorrow at your chosen hour, your phone buzzes with nobody logged in.
- Open `news.sh` and set the prompt to a topic you actually want. From tomorrow it's your news, daily.
- On your Mac, pull a key out of the safe: `aws secretsmanager get-secret-value --secret-id news-bot/anthropic --query SecretString --output text` — one clean line.
- Try the same on the server — you'll hit Access Denied. It has no identity yet. That's exactly what we fix next.

# Lesson 12: IAM — Give Your Server an Identity

## Recap

The bot runs itself (news.sh + cron). Both keys are in the safe (Secrets Manager). The script fetches them at run time using `$()` so `cat news.sh` shows no secrets. But running `./news.sh` on the EC2 gave: `AccessDeniedException … is not authorized to perform: secretsmanager:GetSecretValue`. The server has no identity — AWS doesn't know who is asking.

One cleanup first: if you stored one combined secret last class, split it into two — `news-bot/anthropic` and `news-bot/telegram` — so each is one clean request. AWS holds deleted secrets for a **7-day minimum recovery window** before they're gone for good.

---

## Part 1 — IAM: the badge system

### IAM — the badge system for your account

Think of your AWS account as a building. **IAM is its badge system**: every door checks your badge, on every use — console clicks and terminal commands alike.

Every request (a console click, a CLI command, your cron script at 9:00) passes through the same checkpoint: **WHO is asking? Is that badge allowed to open THIS door?** The wall you hit was this checkpoint saying "no badge — I don't know who's asking."

The API key was a keycard for one service (Anthropic). IAM is the badge system for the whole building.

### A policy — what an identity is allowed to do

Attach a **policy** to a user or role, and that's exactly what it can do — which services, which actions. Two you'll see today:

- **AdministratorAccess** — every action, on every service, the whole account. The training wheels — we start here.
- **The bot's own list** — read `news-bot/anthropic` + `news-bot/telegram`, nothing else. Where we finish: **least privilege**.

We start on admin so the build keeps moving — and we shrink the list before we're done.

### Three kinds of policy

Where a policy comes from sets its lifecycle:

- **AWS-managed** — pre-made by AWS (the cube icon marks them). Use as-is — you can't edit or delete them. Copy one to start your own.
- **Customer-managed** — yours to create, edit, reuse across many identities. Has its own life — stays behind even if you delete the user it was attached to.
- **Inline** — tied to one identity. Born and deleted with that user or role — use it when the policy should belong to nobody else. *The bot's final policy is one of these.*

**Don't hand-write the JSON.** Say it in plain English — "allow start EC2, deny terminate, allow create S3" — and let AI emit the policy: an `Effect` (allow/deny), the `Action`s, and the `Resource` (a wildcard `*`, or one exact ARN to lock it down).

---

## Part 2 — Giving a person an identity: IAM users

### An IAM user — an identity for a person

A **user** is a named identity with credentials. For the terminal, the credentials are two long strings:

- **Access key ID** — says *which* user is making the request.
- **Secret access key** — the proof it's really that user. Shown once, treat like a password. Same rule as every key so far.

You made one quickly during the certificate work on your Mac. Today it gets understood properly — and then replaced with something better for servers.

### Make the user, hand it to the server

**In the console:**
```
IAM → Users → Create user → name: news-bot
  → Attach policies directly → AdministratorAccess     # training wheels, for now
  → the user → Security credentials → Create access key (CLI)
  # the secret shows ONCE — copy both strings now
```

Troubleshooting habit worth copying: in class the bot was run *before* its permission was attached — on purpose — so everyone saw the exact `AccessDenied` message first, then watched it clear the moment the policy went on.

**On the EC2 — aws configure and the wall comes down:**
```bash
aws configure
AWS Access Key ID:     paste the key ID
AWS Secret Access Key: paste the secret
Default region name:   us-east-1    # your EC2's region
Default output format: press Enter

./news.sh
# buzz — keys from the safe, news posted   (the no-secrets script is fully alive)
```

The same run that was denied last class just worked — the server finally had an identity to show.

---

## Part 3 — The catch with user keys: IAM roles

### The keys are sitting in a plain file

```bash
cat ~/.aws/credentials
[default]
aws_access_key_id = AKIA-RIGHT-THERE
aws_secret_access_key = THE-SECRET-IN-A-PLAIN-FILE
```

`aws configure` wrote the keys to a plain text file. The same problem as keys-in-the-script — **one layer down**. Anyone who gets onto the server can copy this file and use the keys anywhere.

For machines inside AWS, there's a way to store **no keys on the server at all**.

### A role — an identity attached to the machine itself

| A person at a laptop | A machine inside AWS |
|---|---|
| IAM **user** — named identity, keys in `~/.aws/credentials` | IAM **role** — attached to the machine itself |
| If someone breaks in, they copy the file and use it anywhere | No keys file — AWS hands short-lived passes automatically |
| Keys can be stolen | No file to copy — nothing to steal |

**The whole rule, two lines:**
- Person at a laptop → **IAM user**, keys in a file.
- Machine inside AWS → **Role**, attached to the machine. No keys stored, ever.

When in doubt: *is it a machine inside AWS?* Then use a role — attach it, store nothing.

### Attach the role, delete the keys — still works

**Step 1 — Create and attach the role (in the console):**
```
IAM → Roles → Create role → AWS service → EC2 → AdministratorAccess → name: news-bot-role
EC2 → your instance → Actions → Security → Modify IAM role → attach ✓
```

**Step 2 — Remove the old keys from the server:**
```bash
rm ~/.aws/credentials              # the file is gone…
# console → news-bot user → delete the access key   # …and the key is dead

./news.sh
# buzz — STILL WORKS   (nothing stored anywhere, and it still works)
```

The role takes over. AWS hands the machine short-lived passes automatically — no file, nothing to steal.

### Shrink the badge to its two doors — least privilege

The role has `AdministratorAccess` — it can read *every* secret in the account, more than the bot needs. Replace that with an **inline policy** naming only the two secrets it should ever touch:

```
IAM → Roles → news-bot-role → Create inline policy → JSON
```

```json
{ "Effect": "Allow", "Action": "secretsmanager:GetSecretValue",
  "Resource": [ "arn:aws:…:secret:news-bot/anthropic-*",
                "arn:aws:…:secret:news-bot/telegram-*" ] }
```

**Test the limit:**
```bash
aws secretsmanager get-secret-value --secret-id news-bot/anthropic    # ✓ works
aws secretsmanager get-secret-value --secret-id some-other-secret     # ✗ AccessDenied
```

Least privilege, for real: the bot reads its two secrets and nothing else. Inline, so it lives and dies with this role.

---

## Part 4 — Root, your admin user, and MFA

### Root — the owner's master key

Two ways into your account — only one for every day:

| Root — the owner's master key | Your daily login — an admin IAM user |
|---|---|
| The email + password that OWNS the account | A named user, made by you, for you |
| Can do everything — including billing and the account itself | Can do what daily work needs |
| **Stays in the drawer** — rare account-level tasks only | **Sign in with this from today on** |

At most companies you'll **never even see the master key** — you have one only because this account is personally yours. Practice the real-world setup now.

### Make your own admin user — and retire root

**In the console (last time signing in as root for daily work):**
```
IAM → Users → Create user → name: aigul ✓ console access
  → Attach policies directly → AdministratorAccess
sign out of root → sign in as aigul
# root goes in the drawer — rare account-level tasks only
```

From today: root retired for daily use. Your account now looks like a workplace account.

### MFA — a stolen password isn't enough

**MFA** adds a second step: a 6-digit code from an app on your phone that changes every 30 seconds. Now someone needs your password *and* your phone.

- Password alone → one secret. If it leaks, they're in.
- Password + code → two things, one on your phone. A leaked password is useless on its own.

**Set it up:**
```
IAM → Users → aigul → Security credentials → Assign MFA device
  → Authenticator app → scan the QR with the app on your phone → enter two codes ✓
```

---

## Take-home

- Your bot runs on the server with **no keys stored anywhere** — the role does it. Check `crontab -l`; tomorrow it posts with nobody logged in.
- Run `cat ~/.aws/credentials` on the server — there's nothing there. The attached role replaced the file.
- Sign in with **your own user**, not root. Root in the drawer — only for rare account-level tasks.
- Your login now asks for a code from your phone — keep that authenticator app handy so you're never locked out.

---

## The full security stack (where you've arrived)

```
news.sh           → no secrets in the file
~/.aws/credentials → doesn't exist — role handles it
IAM role          → attached to EC2, reads only news-bot/* secrets
Console login     → your own user (aigul), not root, protected by MFA
```
