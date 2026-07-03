# 312 School — Lessons Recap
*Travel-friendly summary. Key concepts + essential commands.*

---

## Lesson 1: The Terminal
The terminal is a text interface to your computer. The shell (bash) reads your commands and runs them.

**Prompt:** `[ec2-user@ip ~]$` — `~` = home directory, `$` = ready

**Essential commands:**
```bash
pwd           # where am I?
ls -la        # list all files including hidden
cd folder     # change directory
cd ..         # go up one level
cd ~          # go home
mkdir name    # make a folder
touch file    # create empty file
cat file      # show file contents
rm file       # delete file (no undo!)
rm -r folder  # delete folder and contents
cp src dst    # copy
mv src dst    # move or rename
```

**Paths:** Absolute starts with `/` (e.g. `/home/ec2-user`). Relative starts from where you are (e.g. `code/project`).

**Tips:** Tab = autocomplete. Up arrow = previous command. `Ctrl+C` = cancel.

---

## Lesson 2: Commands Work Together
Commands are building blocks. Chain them so the output of one becomes the input of another.

**Redirection:**
```bash
echo "hello" > file.txt    # write (overwrites)
echo "world" >> file.txt   # append
```

**Pipes `|`:** Takes output of left command → feeds it to right command.
```bash
ls | grep ".txt"       # list files, filter for .txt
cat file | wc -l       # count lines
history | grep git     # find git commands
```

**Useful commands:** `grep` (search), `wc -l` (count lines), `sort`, `head -n 5`, `tail -n 5`

---

## Lesson 3: Pipes, Search & PATH
```bash
grep "word" file.txt         # search in file
grep -r "word" folder/       # recursive search
grep -i "word" file.txt      # case-insensitive
grep -n "word" file.txt      # show line numbers
grep -v "word" file.txt      # lines that DON'T match

find . -name "*.txt"         # find files by name
find . -name "*.py" -type f  # files only

echo $PATH                   # see where shell looks for commands
which python3                # where does python3 live?
```

**Wildcards:** `*` = anything. `*.txt` = all .txt files. `?` = one character.

**History tricks:** `Ctrl+R` = reverse search. `!!` = run last command again.

---

## Lesson 4: File Permissions
```
-rwxr-xr--  ec2-user  script.sh
```
- First char: `-` = file, `d` = directory
- `rwx` = owner | `r-x` = group | `r--` = everyone

**r=4, w=2, x=1. Add them up:**
- `755` = owner: all, group+others: read+execute
- `644` = owner: read+write, others: read only
- `400` = owner read only (SSH keys)

```bash
chmod +x script.sh     # add execute
chmod 755 script.sh    # set permissions numerically
sudo command           # run as root
whoami                 # current user
```

---

## Lesson 5: Git & GitHub
Git = version control. Takes snapshots. GitHub hosts them online.

**Three stages:** Working directory → Staging area → Repository (commits)

**Core workflow:**
```bash
git init                  # start tracking
git clone url             # download repo
git status                # what's changed?
git add .                 # stage everything
git commit -m "message"   # save snapshot
git push                  # send to GitHub
git pull                  # get latest from GitHub
git log --oneline         # compact history
```

**SSH for GitHub:**
```bash
ssh-keygen -t ed25519 -C "you@email.com"  # generate key
cat ~/.ssh/id_ed25519.pub                  # copy to GitHub Settings
ssh -T git@github.com                      # test connection
git remote set-url origin git@github.com:user/repo.git  # switch to SSH
```

**.gitignore:** File that tells Git what NOT to track (`.DS_Store`, `.env`, `*.log`)

---

## Lesson 6: Servers, AWS & EC2
A server = computer that runs 24/7 waiting for requests. No screen.

**AWS key terms:** Region (location), EC2 (virtual machine), AMI (OS image), t2.micro (free tier instance type)

**Connecting:**
```bash
chmod 400 ~/Downloads/my-key.pem
ssh -i ~/Downloads/my-key.pem ec2-user@YOUR-IP
```

**Package manager (Amazon Linux 2023):**
```bash
sudo dnf install -y nginx
sudo dnf update -y
```

---

## Lesson 7: SSH, Networking & Firewalls
SSH = encrypted tunnel to another computer.

**Key ports:** 22 = SSH, 80 = HTTP, 443 = HTTPS, 5432 = PostgreSQL

**Security Groups** = AWS firewall. Rules control which ports are open to which IPs.
- Port 22 open to My IP = SSH access
- Port 80/443 open to `0.0.0.0/0` = public web traffic

**If `curl` works but site is unreachable** → check Security Group rules first.

**known_hosts error (host key changed):**
```bash
ssh-keygen -R hostname    # remove old fingerprint
```

---

## Lesson 8: DNS, nginx & Deploying a Website
**DNS** = translates domain names to IP addresses. A record = name → IPv4.

**nginx:**
```bash
sudo dnf install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx       # start on boot
sudo systemctl status nginx
sudo systemctl restart nginx      # after config changes
sudo nginx -t                     # test config before restarting!
```

**Key paths:**
- Config: `/etc/nginx/nginx.conf`
- Web files: `/usr/share/nginx/html/`

**Copy files to server:**
```bash
scp -i key.pem file.html ec2-user@IP:/usr/share/nginx/html/
scp -i key.pem file1 file2 ec2-user@IP:~    # copy multiple files
```

---

## Lesson 9: curl, HTTP, HTTPS & SSL
```bash
curl https://example.com           # GET request
curl -I https://example.com        # headers only
curl -v https://example.com        # verbose (shows TLS handshake)
curl -X POST -d '{"k":"v"}' url    # POST request
```

**Status codes:**
- `2xx` = success (200 = OK)
- `3xx` = redirect
- `4xx` = client error (404 = Not Found, 405 = Method Not Allowed)
- `5xx` = server error

**HTTPS/TLS:** Certificate proves identity + enables encryption. Issued by a Certificate Authority (CA) like Let's Encrypt. Browser trusts it because the CA is pre-installed on your OS.

**The padlock protects data in transit — it does NOT guarantee the site is safe or trustworthy.**

---

## Lesson 10: When It Breaks — Logs & Triage
**Triage ladder:**
1. Is it running? → `sudo systemctl status nginx`
2. What do logs say? → `journalctl -u nginx -n 50`
3. Config valid? → `sudo nginx -t`
4. Port open? → Check AWS Security Group
5. Can you reach it? → `curl http://localhost`

**Log commands:**
```bash
journalctl -u nginx -f              # follow live
tail -f /var/log/nginx/access.log   # nginx access log
tail -f /var/log/nginx/error.log    # nginx error log
```

---

## Lesson 11: Scripts, cron & Secrets Manager
**Script basics:**
```bash
#!/bin/bash          # shebang — tells OS to use bash
chmod +x script.sh  # make executable
./script.sh         # run it
```

**cron — scheduled tasks:**
```
* * * * * command
│ │ │ │ └── day of week (0=Sunday)
│ │ │ └──── month
│ │ └────── day of month
│ └──────── hour
└────────── minute
```

```bash
0 9 * * *    # every day at 9am
*/5 * * * *  # every 5 minutes
0 9 * * 1   # every Monday at 9am

crontab -e   # edit cron jobs
crontab -l   # list cron jobs
```

**Secrets Manager — never hardcode API keys:**
```bash
SECRET=$(aws secretsmanager get-secret-value \
  --secret-id my-secret \
  --query SecretString \
  --output text)
```

`$()` = command substitution — runs the command and pastes the result.

---

## Lesson 12: IAM — AWS Identity & Access
**IAM** = badge system for AWS. Every request must say who you are.

- **IAM User** = for humans at a laptop (access key + secret key)
- **IAM Role** = for machines inside AWS (no keys stored — EC2 gets them automatically)
- **Policy** = JSON document listing what's allowed

**Least privilege** = only give the permissions actually needed, nothing more.

```bash
aws configure                    # store credentials
aws sts get-caller-identity      # verify who you're authenticated as
rm ~/.aws/credentials            # remove stored keys (use role instead)
```

**Rule:** Person at laptop → IAM user. Machine in AWS → IAM role.

---

## Lesson 13: Bash Scripts — Variables, if/else, Exit Codes
```bash
NAME=value          # set variable (no spaces around =)
echo $NAME          # read variable
export NAME=value   # make available to child processes

REPO_DIR=$HOME/code/quiz-bot    # use $HOME not ~ in variables
```

**if/else:**
```bash
if [ -d "$REPO_DIR" ]; then     # -d = is this a directory?
    git pull
else
    git clone $URL $REPO_DIR
fi
# Spaces inside [ ] are required!
```

**Exit codes:** `0` = success. Anything else = failure. `echo $?` reads the last one.

**Failing loudly:**
```bash
git clone $URL $REPO_DIR
if [ $? -ne 0 ]; then
    echo "ERROR: git clone failed"
    exit 1    # stop the script
fi
```

**set -e** at top of script = stop automatically on any error.

---

## Lesson 14: Python Basics
```python
print("hello")              # print to screen
topic = "git"               # variable — = sets, == compares
type(topic)                 # check data type

# Types:
# str = text in quotes: "hello"
# int = whole number: 42
# float = decimal: 3.14
# bool = True or False

# Lists
classes = ["git", "linux", "networking"]
classes[0]     # → "git" (starts at 0!)
len(classes)   # → 3

# For loop
for c in classes:
    print(c)

# enumerate — loop with numbers
for i, c in enumerate(classes, 1):
    print(f"{i}. {c}")

# f-strings
name = "Chris"
print(f"Hello {name}")    # → Hello Chris

# if/else
if c == "git":
    print("reviewing git")
else:
    print(c)

# Functions
def greet(name):
    return f"Hello {name}"

result = greet("Chris")   # call it
print(result)

# Dictionaries — key:value pairs
movie = {"title": "Inception", "year": 2010, "rating": 8.8}
movie["title"]    # → "Inception"

for key, value in movie.items():
    print(f"{key}: {value}")
```

---

## Lesson 15: Python — glob, os, subprocess
**The four verbs of file automation: List · Loop · Skip · Run**

```python
import glob, os, subprocess

# LIST — find files/folders by pattern
glob.glob("decks/session-*")   # like ls *.txt
glob.glob("/Downloads/*.dmg")

# LOOP
for folder in sorted(glob.glob("decks/session-*")):
    print(folder)

# SKIP — check if file/folder exists
os.path.exists("decks")         # True or False
os.listdir("/home/user/folder") # list all files
os.makedirs("Photos", exist_ok=True)  # create folder (safe to run twice)

# RUN — execute a shell command from Python
subprocess.run(["ls", "/Downloads"])
subprocess.run(["git", "pull"])

# Capture output + log errors
result = subprocess.run(["claude", "-p", "prompt"],
                        capture_output=True, text=True)
if result.returncode != 0:
    with open("error.log", "a") as f:
        f.write(result.stderr)
else:
    print("Success!")

# shutil — copy/move files
import shutil
shutil.copy("source/file.txt", "destination/")
```

**Environment variables in Python:**
```python
import os
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("Error: token not set")
    exit(1)
```

---

## Lesson 16: AI Agent — Direct & Verify
An **AI agent** plans, writes code, runs it, reads errors, and fixes — by itself.

**Your two jobs:**
1. **Direct** — give clear context and rules
2. **Verify** — check it did what you asked

**Golden rule:** `it runs ≠ it's right ≠ I understand it`

**Good brief = specific brief.** "Build me a stock app" = vague. "One company, pretend money, on my EC2, Flask + PostgreSQL, price from Finnhub, only the server changes data" = real brief.

**Architecture (stock app):**
- Browser = asks questions, shows results
- Flask = program logic on the server
- PostgreSQL = database (cash, shares, trades)
- Finnhub = external API for real stock prices
- Secret key = lives ONLY on the server, never in the browser

**Verify a trade:** Predict what should change (cash, shares) → make the trade → check the numbers match.
