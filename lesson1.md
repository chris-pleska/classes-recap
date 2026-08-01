# Lesson 1: The Terminal

## What is the terminal?
The terminal is a text interface to your computer. Instead of clicking icons, you type commands. The computer does exactly what you type — no more, no less.

The **shell** (bash) is the program that reads your commands and runs them.

## The prompt
```
[ec2-user@ip ~]$
```
- `~` = your home directory (`/home/ec2-user` on EC2, `/Users/yourname` on Mac)
- `$` = ready for a command

## Essential commands

| Command | What it does | Example |
|---------|-------------|---------|
| `pwd` | print working directory — where am I? | `pwd` |
| `ls` | list files in current folder | `ls` |
| `ls -la` | list all files including hidden, with details | `ls -la` |
| `cd folder` | change into folder | `cd code` |
| `cd ..` | go up one level | `cd ..` |
| `cd ~` | go home | `cd ~` |
| `mkdir name` | make a new folder | `mkdir code` |
| `touch file` | create an empty file | `touch notes.txt` |
| `cat file` | show contents of a file | `cat notes.txt` |
| `rm file` | delete a file (no undo!) | `rm old.txt` |
| `rm -r folder` | delete a folder and everything in it | `rm -r tmp/` |
| `cp src dst` | copy a file | `cp a.txt b.txt` |
| `mv src dst` | move or rename a file | `mv old.txt new.txt` |
| `echo "text"` | print text to screen | `echo "hello"` |
| `clear` | clear the screen | `clear` |

## Paths
- **Absolute path**: starts from root `/` — e.g. `/home/ec2-user/code`
- **Relative path**: starts from where you are — e.g. `code/project`
- `./` = this folder; `../` = parent folder

## Tips
- Tab key = autocomplete (use it constantly)
- Up arrow = previous command
- `Ctrl+C` = cancel a running command
- `Ctrl+L` = clear screen

---

# Lesson 2: Compose — Commands Work Together

## The core idea
Commands are building blocks. You can chain them so the output of one becomes the input of another.

## Redirection

| Symbol | What it does |
|--------|-------------|
| `>` | send output to a file (overwrites) |
| `>>` | append output to a file |
| `<` | read input from a file |

```bash
echo "hello" > greeting.txt      # write to file
echo "world" >> greeting.txt     # append to file
cat greeting.txt                 # shows: hello\nworld
```

## Pipes `|`
The pipe `|` takes the output of the left command and feeds it as input to the right command.

```bash
ls | grep ".txt"        # list files, then filter for .txt
cat file.txt | wc -l   # count lines in a file
```

Read `|` as "and then send that to…"

## Useful composing commands

| Command | What it does |
|---------|-------------|
| `grep pattern` | filter lines matching a pattern |
| `wc -l` | count lines |
| `sort` | sort lines alphabetically |
| `uniq` | remove duplicate lines |
| `head -n 5` | show first 5 lines |
| `tail -n 5` | show last 5 lines |
| `less` | scroll through output page by page |

## Examples
```bash
cat /etc/passwd | grep ec2-user     # find ec2-user in passwd file
ls -la | sort -k5 -n                # list files sorted by size
history | grep git                  # find git commands you've run
```

---

# Lesson 3 (Session 04): Pipes, Search, and the Path Drill

## grep — search inside files
```bash
grep "word" file.txt              # search in one file
grep -r "word" folder/            # search recursively in folder
grep -i "word" file.txt           # case-insensitive
grep -n "word" file.txt           # show line numbers
grep -v "word" file.txt           # lines that do NOT match
```

## find — search for files by name/type
```bash
find . -name "*.txt"              # find all .txt files from here
find . -name "*.py" -type f       # only files (not folders)
find /var/log -name "*.log"       # search in /var/log
```

## The PATH variable
When you type a command, the shell looks for it in the folders listed in `$PATH`:
```bash
echo $PATH
# /usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```
The shell tries each folder in order until it finds the command.

```bash
which python3      # shows where python3 lives
which git          # shows where git lives
```

## Wildcards
| Pattern | Matches |
|---------|---------|
| `*` | anything (zero or more characters) |
| `?` | exactly one character |
| `*.txt` | all .txt files |
| `file?.txt` | file1.txt, filea.txt, etc. |

```bash
ls *.log           # all log files
rm tmp*            # delete everything starting with tmp
```

## Command history tricks
```bash
history            # show all past commands
history | grep ssh # find ssh commands
!!                 # run the last command again
!git               # run the last git command
Ctrl+R             # reverse search through history
```

---

# Lesson 4: File Permissions, Users & Groups

## Every file has three permission sets
```
-rwxr-xr--  1  ec2-user  ec2-user  1234  Jun 1  script.sh
```
- `-` = file type (`-` file, `d` directory, `l` symlink)
- `rwx` = owner permissions (read/write/execute)
- `r-x` = group permissions
- `r--` = everyone else (world)

## Permission letters
| Letter | Meaning | On file | On folder |
|--------|---------|---------|-----------|
| `r` | read | view contents | list files |
| `w` | write | edit/delete | create/delete files |
| `x` | execute | run as program | enter with cd |

## chmod — change permissions
```bash
chmod +x script.sh          # add execute for everyone
chmod 755 script.sh         # rwxr-xr-x
chmod 644 file.txt          # rw-r--r--
chmod 400 key.pem           # r-------- (SSH key protection)
```

**Numeric shorthand:** r=4, w=2, x=1. Add them up per group (owner/group/world):
- `755` = rwxr-xr-x (owner can do all; others can read+execute)
- `644` = rw-r--r-- (owner can read+write; others read only)
- `400` = r-------- (owner read only)

## chown — change owner
```bash
chown ec2-user file.txt              # change owner
chown ec2-user:ec2-user file.txt     # change owner and group
sudo chown root:root /etc/nginx.conf
```

## sudo — run as root
```bash
sudo command          # run one command as root
sudo -i               # become root (be careful)
```
Root can do anything. Use it only when needed.

## Users and groups
```bash
whoami                # current user
id                    # show user ID and group memberships
cat /etc/passwd       # list all users
cat /etc/group        # list all groups
```

---

# Lesson 5: Git & GitHub — Never Losing Your Files

## What is Git?
Git is a version control system — it takes snapshots of your code so you can go back to any point in history. GitHub hosts those snapshots online.

## The three stages
1. **Working directory** — files on your disk
2. **Staging area** — files you've said "include this in the next snapshot"
3. **Repository** — the saved snapshots (commits)

## Core workflow
```bash
git init                        # start tracking this folder
git clone url                   # download a repo from GitHub
git status                      # what's changed?
git add file.txt                # stage one file
git add .                       # stage everything
git commit -m "message"         # save a snapshot
git push                        # send commits to GitHub
git pull                        # get latest commits from GitHub
git log                         # see history
git log --oneline               # compact history
```

## Branches
```bash
git branch                      # list branches
git branch feature-x            # create a branch
git checkout feature-x          # switch to it
git checkout -b feature-x       # create and switch in one step
git merge feature-x             # merge into current branch
```

## SSH keys for GitHub
GitHub uses SSH keys so you don't type a password every push.
```bash
ssh-keygen -t ed25519 -C "you@email.com"   # generate a key pair
cat ~/.ssh/id_ed25519.pub                  # copy this to GitHub Settings
ssh -T git@github.com                      # test the connection
```

## .gitignore
A file named `.gitignore` lists patterns Git should never track:
```
*.log
.env
node_modules/
__pycache__/
```

---

# Lesson 6: Servers, AWS, EC2 & Linux

## What is a server?
A server is a computer that runs 24/7, waiting for requests. It has no screen — you connect to it over the network.

## AWS (Amazon Web Services)
AWS rents compute, storage, and networking in data centers worldwide. You pay for what you use. Key concepts:
- **Region**: geographic location (e.g. us-east-1, eu-west-1)
- **Availability Zone**: data center within a region
- **Console**: the AWS web UI at console.aws.amazon.com

## EC2 (Elastic Compute Cloud)
EC2 = a virtual machine (server) in AWS.

**Launching an EC2 instance:**
1. EC2 → Launch Instance
2. Choose AMI (Amazon Machine Image) — pick Amazon Linux 2023
3. Choose instance type — `t2.micro` (free tier)
4. Create or select a key pair (.pem file — download and keep it safe!)
5. Configure security group (firewall rules)
6. Launch

## Amazon Linux 2023
The OS that runs on your EC2. Uses `dnf` as its package manager:
```bash
sudo dnf install -y nginx          # install nginx
sudo dnf update -y                 # update all packages
sudo dnf search package-name       # search for a package
```

## Connecting to your EC2
```bash
chmod 400 ~/Downloads/my-key.pem
ssh -i ~/Downloads/my-key.pem ec2-user@YOUR-PUBLIC-IP
```

---

# Lesson 7: SSH, Networking & Firewalls — Find It, Log In, Guard It

## SSH (Secure Shell)
SSH creates an encrypted tunnel to another computer. Everything you type is encrypted in transit.

```bash
ssh -i key.pem ec2-user@1.2.3.4          # connect with a key file
ssh ec2-user@1.2.3.4                      # connect (if key is in ~/.ssh/)
exit                                       # disconnect
```

**Key file rules:**
- Keep the `.pem` file private — never commit it to Git
- Must have permission `400` (`chmod 400 key.pem`) or SSH refuses to use it
- The public key lives on the server in `~/.ssh/authorized_keys`

## How SSH authentication works
1. You have the **private key** (`.pem` file on your laptop)
2. Server has the **public key** (in `~/.ssh/authorized_keys`)
3. They do a handshake — if the keys match, you're in; no password needed

## Ports
Every network service listens on a numbered port:
| Port | Service |
|------|---------|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |

## Security Groups (AWS firewall)
A security group is a list of rules: which ports are open to which IP addresses.

**Inbound rules examples:**
- Port 22, Source: My IP → lets you SSH in
- Port 80, Source: 0.0.0.0/0 → public web traffic
- Port 443, Source: 0.0.0.0/0 → public HTTPS

If a port isn't open in the security group, traffic is blocked — even if the service is running.

## IP addresses
- **Public IP**: reachable from the internet (changes on EC2 stop/start unless Elastic IP)
- **Private IP**: only reachable inside AWS (stays the same)
- `0.0.0.0/0` = anywhere on the internet
- `1.2.3.4/32` = exactly that one IP address

---

# Lesson 8: DNS, nginx & Deploying Your Website — Name It, Build It, Serve It

## DNS (Domain Name System)
DNS translates human-readable names to IP addresses. Like a phone book for the internet.

```
www.example.com  →  DNS lookup  →  1.2.3.4
```

**Record types:**
| Type | Purpose | Example |
|------|---------|---------|
| A | name → IPv4 address | example.com → 1.2.3.4 |
| AAAA | name → IPv6 address | |
| CNAME | name → another name | www → example.com |
| MX | email servers | |

Changes to DNS can take minutes to hours to propagate worldwide.

## nginx (web server)
nginx listens on port 80/443 and serves web files (HTML, CSS, images) to browsers.

```bash
sudo dnf install -y nginx                  # install
sudo systemctl start nginx                 # start
sudo systemctl enable nginx                # start on boot
sudo systemctl status nginx                # check status
sudo systemctl restart nginx               # restart after config change
```

**Where files live:**
- Config: `/etc/nginx/nginx.conf`
- Default web root: `/usr/share/nginx/html/`

**Basic nginx server block:**
```nginx
server {
    listen 80;
    server_name example.com;
    root /usr/share/nginx/html;
    index index.html;
}
```

## Deploying a static site
```bash
# On your laptop — copy files to server
scp -i key.pem index.html ec2-user@IP:/usr/share/nginx/html/

# Or on the server
sudo nano /usr/share/nginx/html/index.html
sudo systemctl restart nginx
```

---

# Lesson 9: curl, HTTP, HTTPS & TLS Certificates — Talk to It, Lock It, Check It

## curl — command line HTTP client
`curl` makes HTTP requests from the terminal. Good for testing APIs and checking servers.

```bash
curl https://example.com                    # GET request, show body
curl -I https://example.com                 # headers only
curl -s https://example.com                 # silent (no progress bar)
curl -o file.html https://example.com       # save to file
curl -X POST -d '{"key":"val"}' url         # POST with JSON body
curl -H "Authorization: Bearer TOKEN" url   # add a header
```

## HTTP status codes
| Code | Meaning |
|------|---------|
| 200 | OK — success |
| 201 | Created |
| 301/302 | Redirect |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

## HTTP vs HTTPS
- **HTTP**: plain text — anyone on the network can read it
- **HTTPS**: HTTP + TLS encryption — traffic is encrypted end-to-end
- Browsers show a padlock for HTTPS; warn or block HTTP sites

## TLS certificates
A TLS certificate proves the server is who it says it is, and enables encryption.

**Let's Encrypt** gives free certificates via `certbot`:
```bash
sudo dnf install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com
# follow prompts — it edits nginx.conf automatically
sudo certbot renew --dry-run     # test auto-renewal
```

Certificates expire every 90 days; certbot sets up auto-renewal.

---

# Lesson 10: When It Breaks, Logs, the Triage Ladder & Your First Bot — Look, Check, Build

## When something breaks: the triage ladder
1. **Is it running?** → `sudo systemctl status nginx`
2. **What do the logs say?** → `journalctl -u nginx -n 50`
3. **Is the config valid?** → `sudo nginx -t`
4. **Is the port open?** → check security group in AWS console
5. **Can you reach it?** → `curl http://localhost`

## systemctl — managing services
```bash
sudo systemctl status service      # is it running? last logs?
sudo systemctl start service       # start it
sudo systemctl stop service        # stop it
sudo systemctl restart service     # restart (picks up new config)
sudo systemctl enable service      # start on boot
sudo systemctl disable service     # don't start on boot
```

## Logs
```bash
journalctl -u nginx                 # all logs for nginx
journalctl -u nginx -n 50           # last 50 lines
journalctl -u nginx -f              # follow (live stream)
journalctl -u nginx --since "1 hour ago"
tail -f /var/log/nginx/access.log   # nginx access log live
tail -f /var/log/nginx/error.log    # nginx error log live
```

Log locations:
- `/var/log/nginx/` — nginx logs
- `/var/log/messages` — system messages
- `journalctl` — systemd journal (catches everything)

## Your first bot: news.sh
A bash script that fetches news from an API and sends it to Telegram.

```bash
#!/bin/bash
NEWS=$(curl -s "https://newsapi.org/v2/top-headlines?country=us&apiKey=KEY")
curl -s -X POST "https://api.telegram.org/botTOKEN/sendMessage" \
  -d chat_id="@channel" \
  -d text="$NEWS"
```

---

# Lesson 11: Scripts, cron & Secrets Manager — Run It, Schedule It, Lock It

## What is a script?
A script is a text file containing commands the computer runs in order — instead of you typing them one by one.

```bash
#!/bin/bash          # shebang: tells the OS to run this with bash
echo "hello"
ls -la
```

**Make it executable and run it:**
```bash
chmod +x script.sh      # add execute permission
./script.sh             # run it (./ = from this folder)
```
`./` = relative path, meaning "look in this folder." Without it, the shell looks in $PATH and won't find your script.

## cron — scheduled tasks
cron runs commands automatically on a schedule.

```bash
crontab -e          # edit your cron jobs
crontab -l          # list your cron jobs
```

**Cron schedule format:**
```
* * * * * command
│ │ │ │ │
│ │ │ │ └── day of week (0-7, 0/7=Sunday)
│ │ │ └──── month (1-12)
│ │ └────── day of month (1-31)
│ └──────── hour (0-23)
└────────── minute (0-59)
```

**Examples:**
```bash
0 9 * * * /home/ec2-user/news.sh          # every day at 9am
*/5 * * * * /home/ec2-user/check.sh       # every 5 minutes
0 9 * * 1 /home/ec2-user/weekly.sh        # every Monday at 9am
```

**Install and enable cron on Amazon Linux 2023:**
```bash
sudo dnf install -y cronie
sudo systemctl enable --now crond
```

## AWS Secrets Manager — storing secrets safely
Never put API keys directly in your script. Secrets Manager stores them securely.

**Store a secret:**
AWS Console → Secrets Manager → Store a new secret → Other type of secret → key/value pairs

**Fetch a secret in your script:**
```bash
SECRET=$(aws secretsmanager get-secret-value \
  --secret-id news-bot/anthropic-key \
  --query SecretString \
  --output text)
```

## JSON: key-value pairs
Secrets are stored as JSON:
```json
{
  "api_key": "abc123",
  "token": "xyz789"
}
```
JSON = key:value pairs inside `{ }` braces.

## `$()` — command substitution
`$()` runs the command inside and pastes the result in place:
```bash
TODAY=$(date)
echo "Today is $TODAY"

SECRET=$(aws secretsmanager get-secret-value --secret-id mykey --query SecretString --output text)
```

## news.sh version 2 (secrets from Secrets Manager)
```bash
#!/bin/bash
ANTHROPIC_KEY=$(aws secretsmanager get-secret-value \
  --secret-id news-bot/anthropic-key --query SecretString --output text)
TELEGRAM_TOKEN=$(aws secretsmanager get-secret-value \
  --secret-id news-bot/telegram-token --query SecretString --output text)
# no secrets in the file itself
```

`AccessDeniedException` when fetching secrets = EC2 has no identity yet → IAM is the fix.

---

# Lesson 12: IAM — Give Your Server an Identity

## What is IAM?
IAM (Identity and Access Management) is the badge system for your AWS account. Every request to AWS must pass the badge check — who are you, and what are you allowed to do?

## Policies — what an identity is allowed to do
A policy is a JSON document that lists permissions:
```json
{
  "Effect": "Allow",
  "Action": "secretsmanager:GetSecretValue",
  "Resource": [
    "arn:aws:secretsmanager:region:account:secret:news-bot/anthropic-*",
    "arn:aws:secretsmanager:region:account:secret:news-bot/telegram-*"
  ]
}
```

**Three policy types:**
| Type | Can edit/delete? | Scope |
|------|-----------------|-------|
| AWS-managed | No | Attached to any identity |
| Customer-managed | Yes | Reusable across identities |
| Inline | Yes | Tied to one identity; deleted with it |

`AdministratorAccess` = full access to everything = training wheels. Goal: **least privilege** (only what's needed, nothing more).

## IAM users — for humans at a laptop
An IAM user is a named identity with an access key ID + secret access key (like a username and password for the API).

```bash
aws configure          # stores credentials in ~/.aws/credentials
```
This saves keys to `~/.aws/credentials` on the server — same problem as keys-in-the-script, just one layer down.

## IAM roles — for machines inside AWS
A role is attached to the machine itself. No keys stored anywhere. AWS automatically hands the EC2 short-lived credentials that rotate constantly.

**Attach a role to EC2:**
1. IAM → Roles → Create role → AWS service → EC2
2. Attach policy: `AdministratorAccess` (then narrow to least privilege)
3. Name: `news-bot-role` → Create
4. EC2 Console → select instance → Actions → Security → Modify IAM role → select `news-bot-role`

**Then remove the stored keys:**
```bash
rm ~/.aws/credentials        # on the server
# Also: delete the access key in IAM console
```
Bot still works — it now uses the role automatically.

## Least privilege inline policy (final form)
```json
{
  "Effect": "Allow",
  "Action": "secretsmanager:GetSecretValue",
  "Resource": [
    "arn:aws:secretsmanager:...:secret:news-bot/anthropic-*",
    "arn:aws:secretsmanager:...:secret:news-bot/telegram-*"
  ]
}
```

## Which identity where?
| Who | Use |
|-----|-----|
| Person at a laptop | IAM user (with MFA) |
| Machine inside AWS | IAM role |

## Root account
Root = owner's master key. Has access to everything including billing. Keep it in a drawer — use your own admin IAM user for daily work.

## MFA (Multi-Factor Authentication)
6-digit code from a phone app that changes every 30 seconds.
IAM → Users → your-user → Security credentials → Assign MFA device

---

# Lesson 13: The Quiz Bot — Variables, if/else, Exit Codes & Failing Loudly

## quiz-bot.sh — a new file
This is a new product, not an edit to `news.sh`. Built on Mac first.

## Bash variables
```bash
NAME=value          # set: no spaces around =, no $ sign
echo $NAME          # read: dollar sign to read
```
Variables live in this terminal session only — they disappear when you close it.

**Use `$HOME` not `~` inside variables:**
```bash
REPO_DIR=$HOME/code/quiz-bot/decks    # correct
REPO_DIR=~/code/quiz-bot/decks        # ~ doesn't always expand inside variables
```

## The decks repo
`git@github.com:312school/26a.312school.com.git`
Structure: `session-N/deck.html` — session-14 is newest.

## Clone vs pull
```bash
git clone URL folder    # first time: download the repo
git pull                # already have it: get updates
```
Running `git clone` a second time to the same folder → `fatal: destination path already exists`

## if/else — the four words
```bash
if [ -d "$REPO_DIR" ]; then
    git pull
else
    git clone $URL $REPO_DIR
fi
```
Four keywords: `if` · `then` · `else` · `fi`
**Spaces inside `[ ]` are required.** `[-d "$REPO_DIR"]` fails; `[ -d "$REPO_DIR" ]` works.

`-d` = "is this a folder?"

## Exit codes
Every command finishes with an exit code:
- `0` = success
- Anything else = failure

```bash
ls /real/path       # exit code 0
ls /fake/path       # exit code 2
echo $?             # read the last command's exit code
```

A failed `git clone` returns exit code `128`.

## Silent failure — the problem
Without a check, a broken `git clone` → script marches on with no warning.

## Failing loudly — the fix
```bash
git clone $URL $REPO_DIR
if [ $? -ne 0 ]; then       # -ne = "not equal"
    echo "ERROR: git clone failed"
    exit 1                  # stop the script, leave exit code 1
fi
```
`exit 1` = stop here and report failure. Now the script is: loud-and-stopped when it fails; quiet-and-onward when it works.

## Telegram + Claude call flags
```bash
TELEGRAM_BOT_TOKEN="..."
TELEGRAM_CHAT_ID="@channel_name"    # bot must be channel admin

claude --model sonnet \
  -p "your prompt here" \
  --allowedTools "WebSearch" "Bash" \
  --verbose
```
Use `"Bash"` NOT `"Bash(curl:*)"` — the narrow form silently skips the Telegram send step.

## Why not cron yet?
Laptop sleeps and goes offline → cron jobs miss. Needs an always-on server (the EC2 from Lesson 6).

---

# Lesson 14: Python — Programs, Variables, Types, Lists & Loops

## What is software?
Software is just instructions. Every app — Telegram, a website, Maps — is a list of instructions a computer follows, in order. The computer does **exactly** what it's told, step by step. No magic underneath.

## What is a program?
So far you've typed commands by hand, one at a time. A program is those same instructions **written down once** in a file — the computer runs all of them, in order, by itself.

## The language: Python
Programs are written in a language the computer understands. The language here is **Python**:
```python
print("hello")    # read it: "print hello" — says hello on screen
```
You'll be able to read a lot of Python before you can write it.

## The editor: VSCode
Writing code in the bare terminal is painful. VSCode shows your whole file, colors it, and keeps the terminal you already know right inside it.

Setup:
```
1. open VSCode
2. File → Open Folder → ~/code/quiz-bot
3. Terminal → New Terminal
python3 --version  →  Python 3.x     # ✓ Python is here
```
Don't have the folder? `mkdir -p ~/code/quiz-bot` first.

## Your first program
New file → save as `hello.py`:
```python
print("Hello from my first program")
```
Run it:
```
python3 hello.py
Hello from my first program
```
`python3` is the thing that runs your file. The `.py` extension tells the computer it's Python.

**No output?** File not saved — a white dot by the filename means unsaved. Press ⌘S or turn on Auto Save. `cat hello.py` only *shows* text; `python3 hello.py` *runs* it.

## Variables
A variable is a name that holds a value. The program remembers it:
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

## Three kinds of values (types)
| Type | What it is | Examples |
|------|-----------|---------|
| string | text — always in quotes | `"git"`, `"hello"` |
| integer | whole number, no decimal | `42`, `0`, `-3` |
| float | number with decimal point | `3.14`, `0.5` |

The quotes make it a string; a decimal makes it a float; a plain whole number is an integer.

## Lists
A list holds things in order, using square brackets `[ ]`:
```python
classes = ["git", "linux", "networking"]
```
Reach in by position — Python counts from **0**:
```python
classes[0]   →   "git"        # first item is [0] — trips everyone once
classes[1]   →   "linux"
```

## The for loop
Say it once — the computer repeats for every item:
```python
for c in classes:
    print(c)
# prints: git, linux, networking
```
`c` becomes each item in turn. Three items → three passes.

**Bash vs Python for loops:**
```bash
# Bash
for c in git linux networking; do
  echo "$c"
done
```
```python
# Python — reads like the English sentence
for c in classes:
    print(c)
```

## The one trap: indentation
Python cares about spaces at the start of lines — they're **invisible**:
```python
for c in classes:
    print(c)       # ✓ indented — works

for c in classes:
print(c)           # IndentationError — not indented
```
Fix: line them up.

## if — a program that chooses
```python
if c == "git":
    print("← let's review git")
# if false: skip it
```
Until now every line ran no matter what. `if` lets the program **choose**.

## Putting it all together
```python
classes = ["git", "linux", "networking"]
for c in classes:
    if c == "networking":
        print(c, "— the tricky one!")
    else:
        print(c)
# Output: git / linux / networking — the tricky one!
```

## Summary: what you can now do
```python
print("hi")                      # say something
topic = "git"                    # a name holds a value
classes = ["git", "linux"]       # a list, in order
for c in classes:                # do it for every item
    if c == "git": print(c)      # ...only when true
```

---

# Lesson 15: Write the Real Quizzes — List, Loop, Skip, Run

**Goal:** Python lists your classes, skips the ones already done, and runs the command that buzzes your phone.

## The finished bot
```
python3 quiz_bot.py
decks/session-1: writing and sending…   # 📱 buzz
decks/session-2: writing and sending…   # 📱 buzz

python3 quiz_bot.py                      # run again
decks/session-1: already done, skipping
decks/session-2: already done, skipping
```
First run: every class buzzes. Second run: nothing sends.

## Pre-flight: three checks
```bash
cd ~/code/quiz-bot
ls decks              # → session-1 session-2 … (your real classes)
claude -p "say hi"    # → a reply
```
Telegram token goes in the environment: `export TELEGRAM_BOT_TOKEN=…` in your shell — not hard-coded in the script.

## One class, one command (the starting point)
```bash
claude --model sonnet -p "Read decks/session-1/deck.html, write one
  multiple-choice quiz question, save it to decks/session-1/quiz.md,
  and post it to my Telegram channel." \
  --allowedTools "Bash" --dangerously-skip-permissions
```
- `--allowedTools "Bash"` = Claude may run commands (open deck, save, post)
- `--dangerously-skip-permissions` = don't pause before each step
- `--model sonnet` = model for these demos

**Problem:** run it twice → same quiz sends twice. Need: every class, once. That's Python's job.

## Four verbs: List · Loop · Skip · Run

### Verb 1: List — real folders off disk
```python
import glob
glob.glob("decks/session-*")
# → ['decks/session-1', 'decks/session-2', 'decks/session-3']
```
`import glob` = "load this toolkit." `glob.glob(...)` finds folders by a `*` pattern — same idea as `ls *.pdf`.

### Verb 4: Run — Python can't run `claude` directly, asks the terminal
```python
import subprocess
subprocess.run(["echo", "hi"])    # → hi
subprocess.run(["sleep", "2"])    # waits 2 seconds (subprocess WAITS)
```
Each piece of the command is its own list item. Quiet on screen = it's working, not broken.

**The real Claude call:**
```python
prompt = "Read decks/session-1/deck.html, write one quiz question, \
    save it to decks/session-1/quiz.md, and post it to my channel."
subprocess.run(["claude", "--model", "sonnet", "-p", prompt,
                "--allowedTools", "Bash", "--dangerously-skip-permissions"])
```
Your phone buzzes. Bot works on one class.

**Building a path with `+`:**
```python
print("decks/session-1" + "/quiz.md")   # → decks/session-1/quiz.md
```

### Verb 2: Loop — cover all classes
```python
for folder in sorted(glob.glob("decks/session-*")):    # once per class
    # …same claude command, with folder instead of "session-1"
```
`sorted(...)` = same order every time. **Backfill** = going back and quizzing every class not done yet. Rate-limit message at home = expected, not a bug — stop, wait, re-run; the skip means it picks up where it left off.

### Verb 3: Skip — don't re-send if done
```python
import os
os.path.exists("decks")    →   True
os.path.exists("nope")     →   False

not os.path.exists("decks")   →   False   # not flips the answer
not os.path.exists("nope")    →   True    # nope is missing → not = True
```
`if not os.path.exists(folder + "/quiz.md"):` = do the thing only when the file is **NOT** there yet.

When the command works (exit code `0`), Python saves a tiny `quiz.md` next to the deck. `ls` before and after — "done" is a file you can see. Run again → "skipping," no buzz.

## The whole bot — about ten lines
```python
import glob, os, subprocess

for folder in sorted(glob.glob("decks/session-*")):     # LIST + LOOP
    if not os.path.exists(folder + "/quiz.md"):         # SKIP if done
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

Claude could've done this whole loop from one prompt — you wrote the loop yourself, and that's the skill that carries into the app and the database.

---

# Lesson 16: Inside the Machine, Inside the App

**The investment app:** Pretend money, real companies. It rides one story — the AI boom and the chain feeding it (compute → power → materials). You'll trade the companies whose chips you're about to study. Each buy or sell is a **trade**.

## What even is software?
A computer on its own does nothing — it just sits there, metal and chips, waiting to be told what to do.

- **A program** = a list of instructions that tells the computer exactly what to do, step by step
- **Software** = just the everyday word for programs

Your browser, Slack, a game, the camera on your phone — every one is a program. Your news bot and the web page you put up are programs too.

## The instructions are written as code
You write a program's instructions as **code** — in a **programming language**. Your news bot is written in Python. Code is just those instructions in a form the computer can follow exactly. Normally a person writes every single line by hand. But you won't — at least not at first.

**Vibe coding** = you describe it; the AI writes the code. You say what you want in plain words → the AI writes the code → the app is made of parts you can now name. It makes building easy, but you still have to know *what to ask for*. You need to understand the machine and the app first, then vibe-code it.

## The four parts of every computer
Every computer (laptop, phone, server) is built from the same few parts:

| Part | Role | Details |
|------|------|---------|
| **CPU** | The worker | Does the actual work — runs the steps of a program |
| **RAM** | Fast, temporary space | Where a running program holds what it's working on. Wiped when power's off |
| **Disk** | Storage | Where files are saved. Kept when the power's off |
| **Network** | The connection | How it sends and receives data over the internet |

### Reading a real spec sheet (MacBook Air M5)
| Part | Spec | What it means |
|------|------|---------------|
| CPU | 10 cores | 10 workers doing the work |
| Memory (RAM) | 16 GB | Fast temporary space a running program uses |
| Storage | 512 GB SSD | Where files are saved — about 32× bigger than RAM |
| GPU | 8 cores | The chip for graphics and AI math |

### CPU: one core = one task at a time
A CPU is split into **cores** — each one is one worker. One worker does one thing at a time; more workers means more at once. A MacBook Air has 10 cores; your EC2 server has **2**. In Activity Monitor, a process's CPU% is of *one* core, not the whole chip.

### RAM vs Disk: why unsaved work disappears
- **RAM** — fast, but temporary. A running program holds its work in RAM. Cut the power → it's wiped. Your unsaved page lived only here.
- **Disk** — slower, but kept. Hit save and it's written to the disk. Keeps what's on it after the power's off.

⌘S / Ctrl+S writes your work from RAM to the disk — like a tiny `git commit`. Data safely on disk is **persistent**. So our app needs somewhere real to put a trade — in RAM alone, it vanishes the moment the app restarts.

### Network: data goes out, data comes in
The **network** is how a computer sends and receives data. Your server already works in both directions: your nginx page goes OUT to a visitor's browser; news comes IN from a news site. Later, the app will ask another computer for stock prices — that ask travels over this same network.

### The GPU — a different kind of chip
The CPU and GPU are built for **opposite** jobs:

| CPU | GPU |
|-----|-----|
| A few big workers | A crowd of tiny ones |
| A handful of strong cores — great at complicated things, one after another | Thousands of small cores doing simple math all at once |
| What your laptop and server run on | What **runs AI** — fills datacenters |

Your EC2 server has **no GPU** — you don't need one to host a site. But it's the chip everyone is racing to buy.

**Why chips are in the news:** The AI boom needs GPUs and memory faster than the world can make them. Shortages push prices up.
- **NVDA** (NVIDIA — makes the GPUs): ~$4.7 trillion, the world's most valuable company
- **MU** (Micron — makes the memory): up ~325% in 2026, on a record memory shortage

You'll soon be trading these exact companies in the app you build.

### Ask a real server what it's made of
```bash
nproc        # CPU — how many cores?  → 2
free -h      # RAM — how much fast temporary space?  → ~1 GB
df -h        # Disk — how much storage, how much free?  → 8 GB
top          # everything at once, live — like Activity Monitor
```
This server is a **t3.micro**: 2 cores, ~1GB RAM, 8GB disk, no GPU. The exact numbers don't matter; what matters is that any machine answers the same way — the parts are the ones we just named.

## What makes a thing an "app"?

| | Scheduled script (news bot) | Static site (nginx page) | App (investment app) |
|--|--|--|--|
| Does something? | Yes — one task | No | Yes |
| Keeps data? | No | No | **Yes ← the new thing** |
| Always on? | No — runs, then stops | Yes, but fixed | Yes — answers anyone |

The new thing an app does is **keep what it's given** — across visits, across restarts.

## Three questions our app must answer

1. **Where does all its data live?** — Prices, people, every trade — a lot to keep, and it must find any one piece fast. → *answered next*
2. **Where do live stock prices come from?** — They move every second — we can't type them in ourselves. → *right after that*
3. **How do all the parts connect?** — The page, the app, the data — wired together. → *at the end*

### Question 1: We need to organize a lot of data
Take one stock — NVIDIA. Already a fair bit to keep: symbol, name, price, market cap. Add every other company, every person, and every trade. That's a lot of data — and it all has to survive a restart.

**Why not just a file?** A file of every trade: `Ali bought 3 NVDA / Sam sold 1 MU / Ali bought 2 MU...` "What does Ali own right now?" → you'd read every line and add it up by hand, every time anyone loads the page. Slow, and easy to get wrong. We need storage we can look one thing up in instantly.

**That's a database.** A **database** keeps data in organized tables, so a program can find or update *any one thing* instantly. It lives on the disk — so it survives a restart. The one we'll use is called **Postgres**.

```sql
SELECT * FROM companies WHERE symbol = 'NVDA';
-- → finds the NVIDIA row instantly
```

Tables in the app: `companies`, `trades`, `holdings`.

### Question 2: Prices never stop moving
Our app shows live stock prices — and they change every second. Typing them in by hand is hopeless: the moment you type one, it's already wrong. The prices have to come from **outside** our app.

**You get them from a service (SaaS).** Some companies track the market and publish prices in real time — that's their whole business. You use their service over the internet instead of building your own. That's **SaaS** — software as a service: software you use over the internet, run by someone else. Most have a free plan, fine for us. We'll pick one when we build.

*(Slides 21–40 not yet captured — resend remaining screenshots)*

---

# Lesson 17: Direct an AI to Build Your Live App

**Goal:** You give one instruction; a working app on your own server comes out — then you take that instruction apart until you could have written it yourself.

## The finished thing
A live web page, on a real server, on the internet right now. It shows one company, pretend money, real prices.

**Vocabulary to know first:**
| Term | Meaning |
|------|---------|
| **Share** | A company is split into many tiny equal pieces; one piece is a share. Own one, you own that slice. |
| **Trade** | Buying or selling a share |
| **Position** | How many shares you hold right now |
| **Paper-trading** | Pretend money, not real money — so you can't lose anything |

On a Buy, the pretend cash goes **down** and the share you now own **appears**. By the end, this is *your* app, on *your* server, with a company *you* picked.

## The AI agent — not just an answerer
The Claude Code you already met was a **tutor**: you asked a question, it answered. Today the same tool does something different — you tell it what to **build**, and it builds it.

The real name for a tool that acts on its own like this: an **agentic AI**, an **AI agent**.

**Before (as tutor):** you ask a question → it answers (two steps, calm, it just talks)

**Today (as agent):** plan → write the code → run it (try it out) → read its own errors → **fix** → loops until it works

The surprising part: it reads its own errors and fixes them.

## Your two real jobs: direct and verify
You are not the typist anymore. You have two jobs, both hard:
- **Directing** — say clearly what you want, with enough context
- **Verifying** — use the app yourself and check it did what you asked

**The golden rule:** `it runs ≠ it's right ≠ I understand it`

The AI types, fast and all of it — but it can't tell if it built the right thing. You think and check; the AI types.

## How AI coding tools got here
Three generations:
1. **Autocomplete** — finishes the word you're typing (code editors, since the 1990s)
2. **Suggests a line** — AI writes the next line of code for you (~2021)
3. **Does whole tasks** — plans, writes, runs, and fixes — an agent (2024–25, today)

Same idea, bigger steps. That last one is where we are today.

## The agent does a small throwaway job first
Before anything valuable rides on it, give the agent a harmless task and see the question-answerer become a **doer**:
```
# type this to the agent, in plain words:
Make a file called hello.txt, put the line "it works" in it, then read it back to me.

# or, pointed at the server:
Log into my server and tell me what's running on it.
```
It doesn't just tell you how — it goes and **does it**. That's the whole shift.

## The architecture: everything on one server
```
YOUR BROWSER                YOUR ONE SERVER (EC2)
the page you see     asks→  FLASK · the program
shows: price/cash/position      receives the ask
buttons: Buy / Sell             makes the change, records it
                                sends back the new numbers
writes nothing itself    ←shows POSTGRESQL · your data
holds no secret key             cash · position · every money move

                           FINNHUB KEY · secret
                                lives ONLY on the server
                                never sent to the browser
                           ↕
                           FINNHUB · outside service
                                the real price comes from here
```
One box you own. Pretend money, nothing precious. The page only **asks** — the server makes every change and holds every secret.

## Give the agent the keys — SSH access
**SSH access** = permission to log into your server and run commands there — so the agent can reach your EC2, where everything runs.

## Brief it first — a vague brief gets a vague app
You don't shout an order. You **brief** the agent: what you're building, where, and the rules.

| Vague | Real brief |
|-------|-----------|
| `"build me a stock app"` — agent guesses, wrong company, wrong money rules, wrong place | `"I'm a complete beginner… here's what I want… everything on this one server…"` — context, rules, and the exact shape |

Directing is real work. A vague brief gets a vague app.

## Approve the plan before it runs
With a big open-ended build, look at the plan (or a rough version) **before** it builds the real thing — so it doesn't build the wrong app and waste your effort. Cheap to redirect early; expensive to redirect after.

Today's build is one clean paste — the instruction was pre-tested ahead of time so you go straight to a working build instead of failing for an hour.

## Paste the prepared instruction — fill three blanks
The whole prepared instruction is one message. Fill in three things that are **yours**, then paste into Claude Code:

```
ssh -i <path to your SSH key> ubuntu@<your server address>
Finnhub key:  <your free key>
Company:      <the ticker you picked, e.g. NVDA>
```

A lot is about to scroll past. You are **not** meant to read or understand it now — watch for one thing: does a working page appear at the end?

## The instruction you ran — seven plain parts
```
context   — I'm a complete beginner; just build it, I'll watch. A small practice stock app,
              pretend money, on my own server, anyone can open it in a browser.
one server — the page, the program, and the data all on this one server; nothing else except
              Finnhub for prices.
the tools  — the standard way: Python + Flask, data in a PostgreSQL database. I'll learn each one later.
the ask    — one company: name + price, $10,000 pretend cash, shares I own, Buy/Sell one share,
              green if up / red if down.
the rule   — only the server may change my cash or holdings; the page just asks; my key stays on the server.
the record — write every money move as a new row you never edit or erase; add them up for my cash and shares.
the data   — use my Finnhub key on the server to look up the real price, save it, show the saved price.
stay up    — keep running after I log out; start again on its own if the server restarts.
```

## Verify — never trust, always check

**Is the price even right?**
- Open the page in your browser
- Open the source — a news quote, or Finnhub's own number
- Compare the two. Close enough (prices lag a few minutes) = it's real

The **method** is worth more than the number.

**Verify a trade: predict the change, then check it.**
Before Buy → predict: cash $10,000 → $9,799.91 (down by one share's price), shares 0 → 1.
After Buy → check: cash $9,799.91 ✓, shares 1 ✓, up/down shown in green ✓.

"The computer's probably right" is the trap — that's how you switch off and stop checking. Keep a plain record of ask → change; that's the habit that lasts.

## Take it apart — seven lines, seven things

**Line 1 → context (the brief)**
"small practice app… pretend money… runs on my own server… anyone can open it" — no jargon, no code. Three phrases, three things it produced: practice·pretend money, my own server, anyone can open it.

**Line 2 → the tools (Flask + PostgreSQL)**
- **Flask** = the program's **framework** — the standard, well-trodden way to write the program behind a web page in Python
- **PostgreSQL** = the **database** — where the app keeps your cash, your shares, and every money move

You'll learn what each one is in the next unit.

**Line 3 → the ask (what's on the page)**
Every phrase points at one visible thing: one company → name + price; $10,000 pretend cash → the cash line; shares I own → your position; Buy/Sell → the two buttons; green up/red down → profit/loss. Up or down = what your shares are worth now vs. the average price you paid.

**Line 4 → the rule (only the server changes your money)**
"only the server may change my cash or what I own; the page just asks; my key lives only on the server." The browser can **knock** — not reach in. Asks cross left, writes and keys stay right.

**Line 5 → the honest record (the ledger)**
"write every money move as a new row you never edit or erase; add them up."

Every trade = a new row appended. Cash and shares = sum of the list (derived, never stored as a running total):
```
10000 - 200.09 - 200.09 + 201.50 = 9801.32
```
Rows are only ever **added** — nothing above is ever edited or erased.

**Line 6 → the data (your key, real prices)**
The Finnhub key lives on the **server**, never in the browser. Server looks up the price, saves it, page shows the saved copy. This is the line you leaned on when you checked the price was real.

**Line 7 → stay up (always on)**
"keep running after I log out; start again if the server restarts."
- After you log out: the app keeps running on the server — it doesn't stop when you close your laptop.
- After a restart: the app starts itself again — the page is always there when someone opens the address.

How it does that (services that restart themselves) is the next unit.

## You could direct this yourself
You can point at **any line** and say why it's there. There's no magic phrase — just a clear description of things you now understand. Seven plain lines, seven real parts of an app.

## Grow it by directing — expect some mess
Bigger asks: "add the rest of these companies," "make it shareable," "change how it looks." The normal loop:

**Big ask** → **Partial** (does half, or gets one part wrong) → **Re-prompt** (say what's off, ask again) → **Fix · verify** (it corrects — then you check)

This part is messy on purpose. A clean one-shot would be the surprise. **Verify after each change.**

## Close: vibe got it working — next, we make it legible
Today: you made it work — directed and verified a real, live app.

Next: **True engineering** — learn in detail how each part works (the database, the backend, the API) and harden the server. From vibe coding to true engineering: you feel the system first, then open up each part and learn how it works.

## After class: grow your own app
Direct your app with your **own** instructions — and verify each change:
- **Add companies** — ask it to add more of the companies you care about
- **Change the look** — tweak the colors, the layout — make it yours
- **Share it** — send the link; it's pretend money, safe to share

Stuck? Go up the ladder in order: read the error → ask Claude in the browser → ask Claude in the terminal → post in Slack. Not graded — the point is the reps.

---

# Lesson 18 — Ports and the Firewall: Who Can Reach Your Server

## The Deal, Renegotiated

Every time you asked what something really is — a database, a network, a firewall — you got the short version **on purpose**, so we could keep building. That deal ends today. One box at a time, in this order: The Machine (EC2), The Firewall, The Network, Storage, The Database.

Same contract, other half: AI is back to being your tutor — it explains, **you** do. When you ask Claude anything about your server, end your prompt with *"do not change anything"* — Claude Code can act on your box, and those four words keep its hands off.

---

## What You Rented — The Virtual Machine

Your EC2 instance is a **virtual machine** — a computer made by software. It behaves like a whole computer of your own, but no single physical box in the building IS your box.

That "AWS building" is a real place: a **datacenter** — a warehouse packed with racks, thousands of screenless bare-metal servers, and enough cooling and power to keep them from melting. A region (e.g. `us-east-1`) is a city-sized *area*, not an address. AWS never publishes exactly where — a security matter. When one hiccups, a big region having a bad day can stall a large slice of the internet.

**Virtualization** = making machines out of software instead of metal. One big physical server gets carved into many virtual ones.

**Hypervisor** = the one program that runs on the physical server whose "programs" are entire machines. It hands out the slices and keeps the VMs from seeing each other.

| Server type | Who's in charge |
|---|---|
| One server, one OS (bare metal) | OS owns the hardware directly |
| One server, many VMs (cloud) | Hypervisor owns the hardware; each VM gets its own OS |

Your server? It's one of the machines a hypervisor is running on some physical box in that building. That's what "launch instance" made.

**Real resources, virtual slices:** The hypervisor assigns each VM a **vCPU** (virtual CPU = scheduled time on the real cores, not a chip soldered off for you). Your t3.micro slice: **2 vCPU · 1 GB RAM**. Your disk lives outside the box (a coming topic).

**Virtualization names you'll hear:**
- **VMware (ESXi)** — the big commercial one; runs many company datacenters
- **KVM** — built right into Linux; free, open source, everywhere
- **Microsoft Hyper-V** — the Windows world's hypervisor
- **Xen** — what AWS ran on for years; a few old instance types still do
- **AWS Nitro System** — AWS's own stripped-down hypervisor, built on KVM; what your t3.micro actually runs on

**On-premises vs cloud vs hybrid:**
- **On-premises** — company owns the physical servers in its own datacenter and runs the hypervisors itself. Still common today.
- **Cloud** — someone else's datacenter, someone else's hypervisors — you rent VMs by the hour. The default for most companies and nearly every startup.
- **Hybrid cloud** — both at once, connected. Common in banks and big enterprises.

The cloud is not a different technology. It's **someone else's datacenter, someone else's hypervisors** — the exact machinery you just met, rented out.

---

## Live — Inside the Machine

Five commands on the app's server (plus one bonus):

```bash
sudo dnf install htop   # htop is NOT preinstalled on Amazon Linux
htop                    # the vCPUs and the RAM, moving in real time
btop                    # optional: a nicer htop
nproc                   # count the vCPUs
free -h                 # the RAM slice, in human units
df -h                   # the disk, seen from inside
uname -a                # what OS and kernel this box reports
```

Reading htop: the two bars at the top are your **2 vCPUs** (mostly idle on a fresh box); `Mem` shows the RAM slice — ~913 MB, i.e. your 1 GB.

---

## Your Slice — Decoding t3.micro

`t3.micro` = **t** (family) · **3** (generation) · **micro** (size)

- Family = what the machine is shaped for
- Generation = which hardware era it runs on
- Size = how big your slice is

**Machine families:**
- `t`, `m` — **general purpose**: balanced CPU and RAM; your t3.micro lives here
- `c` — **compute-heavy**: more CPU per GB of RAM; for number-crunching
- `r` — **RAM-heavy**: much more RAM per core; for data that must sit in RAM ("memory optimized")
- `g`, `p` — **GPU**: the graphics + AI chips; model-training machines

**One line to keep: you pay for the shape you pick.**

**Why t3.micro costs cents — burstable:**
- `t` family: your slice shares its cores **aggressively** with neighbors and is allowed short bursts of full speed. Costs cents. Perfect for our app — it sits idle between visits.
- `c` family: gets its cores **full-time**, no bursting, no sharing tricks. The price reflects that.

**On-demand vs reserved — the money lever:**
- **On-demand** — walk-up price; pay by the hour, start and stop anytime. Flexible, but the most expensive way to run something always on.
- **Reserved** — commit to 1–3 years up front and AWS drops the rate hard — often ~40% off the very same instance.
- Real numbers: a big compute box at ~$4.8/hr runs about $42,000/year on-demand. A 3-year reservation at ~40% off saves roughly $17,000 a year — on a single instance. Companies run hundreds of them.
- **FinOps** = the real job of picking the right size and right commitment. Saving the company money on its cloud bill is one of the clearest reasons they hire you.

---

## The OS Inside

**OS** = everything a machine ships with so programs can run and people can use it: the program-starter (launches and schedules every program), the file system (the folders and files you've been `cd`-ing through since week one), and users & permissions (`chmod`, `sudo`, who-may-do-what).

Three OSes: **Linux** (servers — what your EC2 runs) · **macOS** (your laptop) · **Windows** (big-company desktops, PC gaming).

From the VM picture: **every VM runs its own full OS** — that's what makes each one a whole machine.

**The kernel** = the core of the OS (not the whole OS) — the engine of the car; the rest of the OS is the wheel, the body, the seats. The kernel is the **one program allowed to touch the hardware**.

Your app, `psql`, `htop` — none of them touches the hardware. They ask the kernel. And in your VM, the kernel's "hardware" has a secret: the kernel asks what it *thinks* is hardware — **the hypervisor is answering**. That one sentence is the whole trick.

**AMI (Amazon Machine Image)** = a frozen starting disk: OS pre-installed, ready to copy. "Launch instance" copies that image — your VM is born ready, OS and all. Remember picking an operating system on the launch page? That was you choosing the AMI.

Two common picks:
- **Amazon Linux 2023** — AWS's own Linux; package installer is `dnf`; your news-bot box was born from this one
- **Ubuntu** — the other popular server Linux; installer is `apt`; log in as `ubuntu` instead of `ec2-user`; the vibe build used this one

**Where AMIs come from:**
- **Golden AMI** — one *you* make; snapshot a box you've set up just right, then launch identical copies from it. How teams keep servers consistent.
- **Marketplace** — sold by a vendor, pre-loaded with their software. You pay the creator on top of the instance price.
- **Community** — free, shared by anyone — and **unvetted**. AWS takes no responsibility for what's inside; verify before you trust one.

Same mechanism every time: **a box is a copy of an image**. The only question is *whose* image.

---

## Live — The Instance Page

Five facts on your instance page (EC2 → Instances → your instance):

| Field | Example | What it means |
|---|---|---|
| Instance ID | i-0… | its name in AWS's books |
| Instance type | t3.micro | decoded today — family · generation · size |
| Instance state | Running | the VM the hypervisor is running for you |
| AMI | ami-0… | the image it was born from — AL2023 or Ubuntu |
| Storage · volume | 1 volume, 8 GB | the disk exists — a whole topic of its own, coming |

---

## Ports and the Firewall

### The Callback — What You Actually Clicked, Weeks Ago

When your server was launched, a thing called a **security group** got created, and two rules appeared in it. You clicked past them. They've been guarding your box ever since:

| TYPE | PROTOCOL | PORT | SOURCE |
|---|---|---|---|
| HTTP | TCP | 80 | 0.0.0.0/0 |
| SSH | TCP | 22 | 0.0.0.0/0 |

`0.0.0.0/0` just means "from anywhere." By the end of this lesson you can read every column yourself.

### A Port — The Numbered Ways Into a Machine

Every machine has **65,535 ports**. A program picks one and **listens** on it (listens = waits there for connections). Port 80 = websites. Port 22 = SSH.

Most ports sit silent — until a program picks one and listens.

**`sudo ss -tlnp`** — see who's listening:
- `-t` = TCP connections (the kind the web and SSH use)
- `-l` = only ports being listened on
- `-n` = show numbers, not names
- `-p` = show the program

```
State   Local Address:Port   Process
LISTEN  0.0.0.0:80           gunicorn   ← answering the web port
LISTEN  0.0.0.0:22           sshd       ← how your terminal gets in
LISTEN  127.0.0.1:5432       postgres   ← a port that matters in a later topic
```

**A port belongs to a program, not to magic.**

### A Firewall — A Guard With a Written List

A **firewall** checks every incoming connection against a written list of rules **before** it reaches any port. Every company has one. Your home router has one.

Your app's security group = AWS's firewall, checked **before traffic ever reaches the machine**. It's an allow-list: not on it → turned away silently.

**Reading the inbound rule:**

| Column | Means |
|---|---|
| TYPE | which kind of traffic this rule is about |
| PORT | which port it may reach |
| SOURCE | who may connect (`0.0.0.0/0` = anyone) |

### Live Demo — The Port-80 Rule Comes Out

On the demo box: the port-80 rule is removed → site stops loading (checkable from any phone). But `ss` proves **gunicorn is still listening on 80**. The app never stopped.

The rule goes back → site returns within seconds. Reversibility is part of the lesson.

**The server never stopped — the firewall stopped letting traffic through.**

### So Who Answers on Port 80?

You already saw the name in the real output — `gunicorn`. Three programs between a visitor and your app:

- **Flask** — what the app is *written with* (the framework from the build)
- **gunicorn** — the program **answering port 80** — the name in the `ss` output
- **systemd** — the **starter** — why the app came back after every reboot

The mystery is closed: **you now know every program between a visitor and your app.** (We come back to all three when we open the app layer — today, only the names.)

### Inbound, Outbound — And Why Replies Just Work

- **Inbound** — who may connect *in*, to which ports (checked against the security group list)
- **Outbound** — where your box may call *out* to (default: anywhere — e.g. the app calls the price service every day; no gate in this direction)
- **Replies don't need their own rule** — a reply isn't a new connection. It rides back on the one the visitor already opened, and the security group remembers who opened it. That memory is called being **stateful**.

### Port 22 Is Yours — SSH

Every terminal session you've ever had with your server came in through **port 22** — past this exact rule.

| Source option | Means | Trade-off |
|---|---|---|
| `0.0.0.0/0` | "anyone on the internet may try" | Trying ≠ entering — your SSH key still guards the login. What your rule says today. |
| Your own IP | Only your address may even knock — safer | Your home IP changes; when it does, you're locked out until you update the rule. |

No right answer to memorize — just know **what each choice means**.

---

## Take Home — Open Your Own Box + Firewall

After class: run `htop`, `nproc`, `free -h`, `df -h`, `uname -a` on your own server; find the 5 facts on your instance page; do the kill-and-restore on your own box (revert step written first).

**Done this lesson:** The machine opened (virtualization, slice, OS, kernel, AMI) · Ports decoded · Firewall and security group understood  
**Next topic:** The Network — the street the machine lives on


---

# Lesson 19 — The Neighborhood: Where Your Server Lives

The machine, opened. Its firewall, opened. Now zoom out: the box sits somewhere. Today — its addresses, how they really work, and the fenced network around them.

---

## What a Network Actually Is

A **network** = computers that can pass messages to each other, each with an **address**. That's the whole definition.

The **internet** = networks, connected to networks — nothing more mysterious than that. A home network, an office network, and AWS's network are all the same idea; the internet just connects them.

---

## You Already Own a Network — Your WiFi

At home, the router runs a small network: every device gets an inside address like `192.168.0.5` — and the **whole house shows up to the internet as ONE address**.

Your router is the little network's gatekeeper — it hands out inside addresses and carries everything in and out. The inside numbers repeat in every apartment in the building, and nothing breaks. Hold that thought.

---

## Your Box Has TWO Addresses

The console shows both on the instance page, and `ip addr` on the box confirms the second:

| Address | Example | What it means |
|---|---|---|
| **Public IP** | 3.91.24.7 | Reachable from the internet — the address behind the URL you've been visiting since the app went live |
| **Private IP** | 172.31.5.14 | Only means something **inside its own fence** — like the `192.168` numbers at home |

Hold the question: **why does every machine need two?** The answer starts with what this number actually *is*.

---

## An IP Address, Taken Apart

An **IPv4** address is **four slots**, separated by dots. Each slot holds a number from **0 to 255** — that's one byte: 8 on/off switches, 256 combinations.

`172 . 31 . 5 . 14` → Slot 1 · Slot 2 · Slot 3 · Slot 4

Four slots × 256 choices each: **256 × 256 × 256 × 256 ≈ 4.3 billion possible addresses.**

32 switches in total (4 slots × 8) — engineers call this a **32-bit address**.

---

## The Internet Ran Out of Addresses

IPv4's ~4.3 billion addresses — **all handed out**. The world has far more phones, laptops, TVs, and servers than that.

**The workaround the world picked: private addresses** — reuse the same inside-numbers behind every fence. That's why your box carries a private address next to its public one. Your WiFi has been doing this all along.

You'll also see **IPv6** (e.g. `2600:1f18:4b2:...`) — the newer, enormously bigger scheme; nothing to do today.

And that's why a box needs two addresses: four slots only make ~4.3 billion numbers — fewer than the world has devices. The workaround: **private addresses** — your WiFi has been doing it all along.

---

## Private Ranges — The Same Numbers in Every Fence

Three blocks of addresses are reserved as **private**: they only mean something **inside a fence**, so every home, office, and cloud can reuse them without asking anyone:

| Range | Who uses it |
|---|---|
| `192.168.x.x` | Home-router favorite — your WiFi uses this one |
| `172.16–31.x.x` | The middle range — **AWS hands your box its `172.31…` address from here** |
| `10.x.x.x` | The big one — offices and large companies |

That's why your neighbor's laptop and yours can both be `192.168.0.5` and nothing breaks — and why a box needs a **public** address too, the moment the world must reach it. And that public address? **AWS only lends you one.**

---

## Elastic IP — A Public Address You Keep

Your box's public IP is **borrowed** from AWS's pool. Stop the box and start it again — you get a **different number**, while your DNS record still points at the old one: **the site goes dark** until you fix the record.

| Option | What happens |
|---|---|
| **Borrowed (default)** | Handed out at start, taken back at stop. Stop → start = a new number and a stale A record. |
| **Elastic IP — reserved** | A public IPv4 reserved for your account: survives stop→start, moves to a replacement box in one click — **DNS never notices** |
| **Price** | $0.005/hour ≈ $3.65/month for **any** public IPv4 (borrowed or reserved); the catch: a reserved one **keeps billing while idle** — box stopped, or not attached at all |

Why does a number cost money? Only ~4.3 billion exist — AWS even caps you at **five per region**. Reserve one while it has a job, **release it when it doesn't**.

New AWS accounts run on sign-up credits — this charge quietly eats them before you ever see a bill.

---

## CIDR — The /Number, Decoded

`172.31.0.0/16` = where the block starts / switches locked (of the 32 total — here: the first two slots are fixed).

Locked slots are fixed; the free slots make the block's **size**. Every 8 locked switches = one full slot:

| Notation | Slots locked | Addresses | Example |
|---|---|---|---|
| `/8` | 1 slot locked | 16,777,216 | `10.0.0.0/8` — the big private range |
| `/16` | 2 slots locked | 65,536 | `172.31.0.0/16` — remember this one |
| `/24` | 3 slots locked | 256 | `192.168.0.0/24` — one home's worth |
| `/32` | All 32 locked | 1 | Exactly one address |

And the one you've met twice already: **`0.0.0.0/0`** = zero locked = **every address on the internet**. That's why the firewall rule's source column used it to mean "anyone."

---

## The VPC — Your Fenced Patch of AWS's Network

**VPC** (Virtual Private Cloud) = your own fenced-off patch of AWS's network. What it owns is a block you can now read yourself: **`172.31.0.0/16`** — two slots locked, 65,536 private addresses. Yours since day one.

The VPC is to your servers what your home WiFi is to your devices — **with you as the landlord**.

---

## Subnets — The VPC's Block, Split Up

A **subnet** = a smaller block cut from the VPC's block — same CIDR idea, more switches locked. Slices never overlap.

The rule that surprises everyone: **a machine never launches "into the VPC" — it always launches into one subnet.**

Example: VPC block `172.31.0.0/16` →
- Subnet `172.31.0.0/20` (4,096 addresses: `.0.0` – `.15.255`) — YOUR SERVER `172.31.5.14` lives here (`.5` sits between `.0` and `.15`)
- Subnet `172.31.16.0/20` (4,096 addresses: `.16.0` – `.31.255`) — room for future machines
- More slices as needed...

Picture: streets inside a fenced neighborhood — the word to keep is **subnet**.

---

## Route Tables — The Subnet's Written Directions

Your box sends a message. Its subnet decides the path with its **route table**: a short list of rows, each reading **"traffic going THERE → send it THIS way."**

The first row you can already read yourself:

| DESTINATION | TARGET | Meaning |
|---|---|---|
| `172.31.0.0/16` | **local** | Any address in the VPC's block → deliver directly, stay inside the fence |

One row handles the whole neighborhood: box-to-box traffic **never leaves the fence**. But your box also calls the stock-price service on the internet every day — so there must be a second row.

---

## Everywhere Else → The Internet Gateway

Complete route table:

| DESTINATION | TARGET | Meaning |
|---|---|---|
| `172.31.0.0/16` | **local** | Inside the block → stay inside |
| `0.0.0.0/0` | **igw-0a1b2c…** | Every address (zero locked!) → the internet gateway |

The **internet gateway** = your VPC's **one way in or out**. Nothing in your fence reaches the internet — or is reached — except through this gateway. Built once per VPC, attached at the edge.

When an inside address matches both rows, the rule is: **the more locked row wins** (`/16` beats `/0`) — so neighborhood traffic never accidentally leaves.

---

## Public or Private — One Line Decides

| Subnet type | Route table has |
|---|---|
| **Public** | `172.31.0.0/16 → local` AND `0.0.0.0/0 → igw-…` |
| **Private** | `172.31.0.0/16 → local` only — the gateway row is simply **missing** |

A subnet is **public** if its route table includes "everywhere else → the internet gateway" — and **private** if that row is simply missing. **One missing row. That's the entire difference.** A database would love the private one.

---

## Live — Your Box's Subnet, Found in the Console

Four clicks, every name taught in the last five slides — nothing new appears:

Instance page (both IPs + VPC id) → **Its VPC** (the fence, `172.31.0.0/16`) → **Its subnet** (the `/20` slice the box launched into) → **Its route table** (both rows — local and `0.0.0.0/0 → igw-…`)

---

## The Whole Path — Follow One Request, Start to Finish

Before any message travels, the browser asks **DNS** to turn the name into an address. Then the journey starts:

1. A phone opens your app
2. **DNS**: `yourapp.example` → `3.91.24.7`
3. **The internet** (networks of networks)
4. **Internet gateway** (the one way in)
5. **Public subnet** `172.31.0.0/20` (its route table includes the gateway — that's what makes it public)
6. **Security group** (the allow-list check: port 80 — on the list)
7. **Your server** `172.31.5.14` — gunicorn answers → your app

**name → address → internet → gateway → subnet → the allow-list → port 80 → the app. Every word is yours now.**

---

## Take Home — Find All of It on Your Own Account

After class: find your two addresses on the instance page and with `ip addr`; do the four clicks (instance → VPC → subnet → route table); draw the request start to finish on your own copy — this drawing grows with every box you open.

**Done this lesson:** The neighborhood, opened — IP addresses slot by slot, Elastic IPs, CIDR blocks, the VPC, subnets, route tables, the internet gateway  
**Next topic:** Where your bytes live — the disk that isn't in the box, and storage that isn't a disk at all

Optional: reading CIDR is the main line. Want to *calculate* any block by hand — odd masks like `/21` or `/27`, or splitting a VPC into equal subnets? Use a visual subnet calculator (linked in #class-26a) or just ask Claude.


---

# Lesson 20 — Data Storage: Where Your Bytes Live

## All Data is Bytes

A photo, a song, your app's code — to the computer, it's all just bytes.

| Unit | How Big | Feels Like |
|------|---------|------------|
| bit | a single 0 or 1 | the smallest piece of data there is |
| byte | 8 bits | one letter — "A" |
| kilobyte (KB) | ~1,000 bytes | a paragraph of text |
| megabyte (MB) | ~1,000 KB | a phone photo is a few MB |
| gigabyte (GB) | ~1,000 MB | a movie is 1–2 GB |
| terabyte (TB) | ~1,000 GB | hundreds of movies |

Today's whole question: **where is your data kept?**

## Today in Two Parts

**Part 1 — EBS (your server's disk):** what a disk actually is, moving one between servers, backups (snapshots) and restores, what happens when it fills.

**Part 2 — S3:** files kept by AWS, each with a web address; what real apps keep there; how pricing differs.

You already know: RAM vs disk · `df -h` · `sudo`. New today: EBS volumes · snapshots · S3.

The thread held the whole way: **you press Buy on a share in the investment app — where does that fact live when the power goes out?**

## RAM vs The Disk

- **RAM** — the working space. Fast, wiped clean on every reboot. Anything that lives only in RAM is gone when the power goes.
- **The disk** — the keeping space. Slower, and it stays. Files survive the reboot.

## What a Disk Actually Is

A disk is a real, physical object — a device that keeps bytes even with the power off.

- **HDD (hard disk drive)** — spinning metal platter; a little arm writes and reads bytes. Slower, big, cheap.
- **SSD** — chips only, nothing moves. Much faster. What's inside your laptop and inside AWS's data centers.

Every file you've ever saved landed on a device like these. Your AWS server writes to a disk too — the question is where that disk actually sits.

## EBS — Your Disk Is Outside the Server

**EBS volume** — the disk your server uses. It sits on separate storage hardware, attached to your server over the network.

```
YOUR VM — YOUR SERVER          SEPARATE STORAGE HARDWARE
  /dev/nvme0n1 — 8 GB   ←— attached over the network —→   your EBS volume — 8 GB
  "a disk," as far as                                        (other customers' volumes)
   anything inside can tell
```

It behaves exactly like a disk inside the server — it has never been inside it. The `df -h` from the machine topic was reading this exact disk the whole time.

Inside AWS's data center: two kinds of racks — the **server rack** (computers, including yours) and the **storage rack** (shelves of disks — your volume is here). AWS reserved 8 GB on a storage rack, a network cable away from your server.

## Attaching a Second Disk Live

Three steps: **create** a second 8 GB disk in the AWS console → **attach** it to the server → **write a file** on it. The server never stops running.

Key commands:

| Command | What it does |
|---------|-------------|
| `lsblk` | list the disks the server can see (not the space inside them — that's `df -h`) |
| `mkfs` | put an empty filesystem on a blank disk — format it, like a new USB stick |
| `mount` | plug a disk's contents into a folder, so the server can read them |
| `sudo` | as the machine's admin |

**The demo sequence:**

```bash
lsblk                                    # one disk: nvme0n1 — the 8 GB root volume
# console: Volumes → Create volume (8 GB) → Attach → this server
lsblk                                    # second disk appeared: nvme1n1 — blank
sudo mkfs -t ext4 /dev/nvme1n1           # format it (put empty filesystem on it)
sudo mount /dev/nvme1n1 /mnt/spare       # plug its contents into a folder
sudo vi /mnt/spare/survivor.txt          # write a file (i · type · Esc · :wq)
cat /mnt/spare/survivor.txt              # read it straight back off the disk
# 312 — this byte survives.
```

Nobody plugged anything in. AWS reserved another slice on a storage rack and connected it over the network — that's all "creating a disk" means in the cloud. And the server never stopped running.

## A Server and Its Storage Are Two Separate Things

- **The server** — CPU + RAM. It does the work. Kill it, and the computer is gone.
- **The storage** — a separate disk on a storage rack. It keeps the bytes — whether your server is alive or not.

Kill the server — the disk is fine. It survives because it's on separate hardware; your bytes were never inside the server.

## The Root Disk Exception

Your server boots from its **root disk** — the OS and your app live on it. At launch, a checkbox decides its fate: **"delete this disk when the server is deleted" — checked by default.**

- The **root disk** — deleted with the server by default
- A **spare disk** (like the one from the demo) — no checkbox touches it, survives on its own

So the spare disk survives the server — but the disk your app lives on, by default, does not. Which is why you need a **backup**.

## Backup

**backup** — a copy of your data stored in a **different place** than the original, so that one accident can't destroy both.

Three ordinary accidents:
- **A wrong click** — the volume is deleted in the console; every byte on it, gone
- **A bad command** — one mistyped command wipes the disk; it happens to real engineers
- **The server dies** — and takes its root disk with it (the default you just saw)

The one rule: **a copy on the same disk is not a backup.** If the disk dies, both copies die together. The copy has to live somewhere else.

## Snapshot — AWS's Built-In Backup

**snapshot** — a backup of the whole disk at one moment, one click; AWS keeps the copy **away from your server**.

```
EC2 → Volumes → the volume you just wrote to → Actions → Create snapshot
Snapshots → snap-... · the volume's size
# finishes in the background over a couple minutes — the server never pauses
```

A kept snapshot is the first thing that costs money: cents per month, and only for bytes actually written.

## The Snapshot Survives Everything

- The server — gone (terminated, nothing left to connect to)
- The volume — wiped (one wrong click, one bad command — bytes are gone)
- The snapshot — **safe** (the copy AWS keeps, away from any server; it survived both)

A backup only counts if you can get the data back. That's the restore.

## Restore: From Snapshot Back to Your Files

```
THE SNAPSHOT → "Create volume from snapshot" → A NEW VOLUME → attach → mount → cat → your files
```

**Live steps:**
```bash
# Snapshots → the one you watched get taken → Create volume from snapshot → attach
sudo mount /dev/nvme1n1 /mnt/spare
cat /mnt/spare/survivor.txt
# 312 — this byte survives.   ← the line you watched being written, back off a disk that didn't exist a minute ago
```

**A broken disk is not lost data — if a backup exists.**

## The Disk Fills Up

The volume is 8 GB only. Three things keep writing to it: the operating system, your app, and the database's files (Postgres).

```bash
df -h /
# Filesystem      Size  Used  Avail  Use%  Mounted on
# /dev/nvme0n1p1  8.0G  4.2G  3.9G   52%  /
```

At **100% full**, programs that need to write — including the database — start failing. Check it occasionally; it's one command.

```bash
sudo du -sh /* | sort -h    # shows what's eating the disk, biggest last
```

## S3 — Storage That Isn't a Disk at All

The disk is 8 GB and serves one server. Some things outgrow that: backups, logs, images — files that grow forever and belong to no one server.

**S3** — you hand AWS a file and a name. AWS keeps the file and hands it back to anyone allowed to ask for it by that name. No disk of yours, no server of yours, no `df -h`, no size to pick. You reach S3 over the network — like a website.

S3 doesn't replace the disk — it sits **beside** it.

## Bucket and Object — S3's Two Words

- **bucket** — a named container in AWS's storage service; you make one, it holds your files
- **object** — one file in a bucket; fetched by name, and **replaced whole, never edited in place** (S3 keeps files; it doesn't open them)

Every object gets a **web address:**

```
https://312school-storage-demo.s3.us-east-1.amazonaws.com/312-logo.png
         ↑ bucket                ↑ S3 service + region             ↑ object
```

The disk serves **YOUR server**. S3 serves **anyone you allow**.

## S3 Demo — Make a Bucket, Put a File In, Fetch It by Name

**Three acts:**
1. **Create + upload** — a new bucket, one logo image into it
2. **Locked, by default** — its URL answers `AccessDenied`: new buckets are private; nothing is public unless you decide it
3. **The unlock** — a decision, never a default; the URL then fetches clean

**The whole class proves it:** the same URL loads on every phone at once, wherever each student is sitting. The disk needs your server running to serve anything — S3 served the whole class with **no server of yours involved at all**.

## What S3 Is Actually Used For

- **Backups** — a database backup file must live somewhere safer than the disk it backs up
- **Logs** — they pile up forever and belong to no one server
- **Images & video** — files every visitor fetches by name (delivery photos, logos)
- **Entire static websites** — page files fetched by name, no server of yours involved

Four different jobs, one shape every time: **files that grow forever, served by name.**

## Pricing: Renting a Disk vs Paying for Bytes

| | EBS Volume (rented disk) | S3 Bucket (bottomless) |
|--|--------------------------|------------------------|
| Size | You pick up front (8 GB) | No size to pick, ever |
| Cost | Pay for all of it — full or empty | Pay for exactly what you store — cents per GB/month |

Big, ever-growing things — backups, logs, media — **end up in buckets, not on disks.**

## The Disk and S3 Side by Side

| | EBS — The Disk | S3 — Buckets of Files |
|--|----------------|----------------------|
| Serves | one server: yours | anyone you allow, by web address |
| Size | fixed (8 GB, full or empty) | no size — just grows; pay per GB stored |
| Holds | OS, your app, the database's files | backups, logs, images, whole websites |
| Needs your server? | yes — needs server running to serve anything | no — AWS runs it all |
| Backup | the snapshot | AWS keeps the copies itself |

**Files for your server → the disk. Files that grow forever, served to the world → S3.**

## The Full Map: Where Your Bytes Live

**Memory (working space — emptied when the power goes):**
- RAM — what programs are using right now; fast, and gone on every reboot

**Storage (keeping space — it stays):**
- The disk (EBS) — the server's own disk; the OS, your app, Postgres's files. Its backup: **the snapshot**
- S3 — files with web addresses; backups, logs, images; served to **anyone allowed**

Postgres isn't a fourth place — it's a **program** whose files live on the disk.

## The Answer: You Pressed Buy — Where Does That Share Live?

The question from the start: in the investment app, you press Buy on a share. The app must remember that fact forever — through reboots, power cuts, even a dead server.

```
The share you bought  →  a row in Postgres  →  bytes in files  →  on the EBS volume  →  outside the server
(the fact, as the DB     (Postgres keeps its    (your server's      (on a storage rack —
 keeps it)               data as regular        disk — all 8 GB     where it survives
                         files, in a folder)    of it)              the server)
```

Postgres is a **program using the disk** — not a third kind of storage. So reboot, even kill the server: **the share you bought is still out there, on the volume.** That was the whole question.

## After Class

- **The full round trip:** billing alarm first → snapshot your disk → create a volume FROM the snapshot → attach it → see it in `lsblk` → clean up
- **A bucket with one file:** fetch its URL, hit the default AccessDenied, follow the unlock click-path, fetch again — then send your URL to someone
- **Your drawing grows:** add the storage layer (volume drawn outside the server; S3 off to the side)

**Next topic: The database, for real** — the program sitting on that disk; what it is, and how your app talks to it.

---

# Lesson 21 — The Database, for Real

## The Problem: Never Lose a Fact

Your app remembers every trade you ever made. Close it. Restart the server. Open it again — still there. You never wrote the code that saves them. So where do they live?

Yesterday you bought 2 NVIDIA shares. That one fact has to be there tomorrow, next month, next year — through every restart, every crash, every reboot. The app has to keep: every buy and every sell since the beginning, your cash, the companies and their prices. Money facts, kept for years, correct to the cent.

## Why a File Won't Work

You could write every trade into `trades.txt`, one line per trade. Three days later that file will meet:

- **The power dies mid-write** — app is halfway through writing a buy when the server reboots. What's in the file now? Half a line — half a money fact.
- **Find one line in a million** — one trade, somewhere in a million-line file. Reading the whole file every single time — how long, at line 999,999?
- **Two saves, same instant** — two people buy at the same moment; both write the file. Whose write wins — and whose is gone? The day an app has more than one user, this day comes.

A file answers none of these. Keeping records safe is a **full-time job** — and there is a kind of program built for exactly that job.

## What a Database Is

**database** — a separate program whose only job is records: keep them safe, answer questions about them fast, and serve many programs and people at once — without ever losing a fact.

Two programs talking: your app asks → the database answers — the records. Stop the app, crash it, rebuild it — **the records sit safe in the other program.**

Every real app has one behind it:
- **Bank's app** — holds accounts, transfers, card payments; your balance is read from it, never guessed
- **Instagram** — holds photo links, comments, likes, follows; pictures sit in storage, the database keeps the facts about them
- **Your investment app** — database on your own server, holding companies and trades; yesterday's buy is in there right now

## Records Sit in Tables

A database is not one big pile of everything. Records are sorted into **tables** — a grid that holds **one kind of fact**.

Your app's companies table:

| SYMBOL | NAME | PRICE |
|--------|------|-------|
| NVDA | NVIDIA | 131.26 |
| AMD | Advanced Micro Devices | 117.53 |
| TSM | Taiwan Semiconductor | 184.10 |

One row = one fact. One column = one detail. **A table is that simple** — and a database keeps many of them.

## Two Kinds of Facts — Two Tables

Companies are one kind of fact. Trades are another — they get their own table. But the trade has to say **which company** was bought.

How should a trade name its company — copy all its details in, or point at it?

## Relational — Point, Don't Copy

The trade stores one small thing: the company's number. Row #1 is NVIDIA, so the trade says "company 1" — it points, and nothing is written twice:

```
transactions:                    companies:
ID    | COMPANY_ID | SHARES | AMOUNT    ID | SYMBOL | NAME
4183  |     1      |   2    | -262.52    1 | NVDA   | NVIDIA
                   points at ──────────→  2 | AMD    | Advanced Micro Devices
```

**relational database** — records kept in tables, and the tables point at each other.

Tables that point at each other are **related** tables. That one word describes how nearly every serious app on earth keeps its facts.

## Postgres — The Database on Your Server

**PostgreSQL** (Postgres for short) is a particular database program — real software. The vibe build installed it on your server.

1. **Installed** — put on the server with `dnf` (the same installer as any other program)
2. **Running** — started once, then on day and night, waiting (not run-and-exit like your scripts)
3. **On duty** — holding every trade since the vibe build

```bash
systemctl status postgresql
# ● postgresql.service — active (running)   ← on since the vibe build — you just never looked
```

You never installed it and never started it — **the Claude Code agents did both during the vibe build.**

## How Your App Talks to Postgres

Postgres runs as a **server program**: always on, waiting for questions on **port 5432** (the port from the firewall topic). Any program that connects and asks is a **client**. Two clients today:

- **psql** — the client you type into, from the terminal
- **your app** — the other client, connected since the vibe build

Both connect to port 5432. Postgres holds tables: companies, transactions.

## The Database Landscape

Databases are a field of products. Five big names:

| Database | What it is |
|----------|-----------|
| **PostgreSQL** | serious open-source default — the one on your server right now |
| **MySQL** | the classic of the web |
| **SQLite** | the tiny one hiding inside phones and apps |
| **SQL Server** | Microsoft's big corporate one |
| **Oracle** | the other big corporate one |

All five keep records the same way: tables that point at each other — **relational** databases, all of them. And **all five speak the same language — SQL.** Learn it once, it works on all five.

## NoSQL — The Other Family

Not every database keeps tables. The other family is **NoSQL** (non-relational):

- **MongoDB** — keeps documents, not tables
- **Redis** — works out of RAM, very fast; can still save to disk
- **DynamoDB** — AWS's own

Different shapes for different jobs — **not better or worse.** Our app lives in the relational world.

## Why Postgres

- **Free and open source** — no license to buy; you can run it tonight, on any server
- **Production-common** — what serious production teams commonly run
- **Skills transfer** — all five speak SQL; everything learned here works across the family

One line of honesty: **MySQL would also have been a fine choice** — the skills are the same.

## Install From Scratch — on a Clean Server

```bash
sudo dnf install postgresql16-server              # dnf — the machine's software installer
sudo postgresql-setup --initdb                    # creates the data folder — on the EBS disk, where else
sudo systemctl enable --now postgresql            # the starter — from now on it survives reboots
sudo ss -tlnp | grep 5432                         # listening — the exact port from the firewall topic
echo 'host all all 127.0.0.1/32 md5' | sudo tee -a /var/lib/pgsql/data/pg_hba.conf
                                                  # let a password log in — the step that bites everyone
sudo systemctl restart postgresql                 # re-read that file
```

Born with nothing in it: no tables, no records, empty. **Remember this empty server.**

## Step Inside — as the Admin

A fresh Postgres lets exactly **one** user in: an admin account named `postgres`, made by the install.

```bash
sudo -u postgres psql
postgres=#           # the prompt changed — you're inside now, as the admin
```

`sudo` = as the machine's admin · `-u postgres` = acting as "postgres" account · `psql` = open the database terminal

Inside once, as the admin — to make **two decisions**: who may talk to this database, and where the app's tables will live.

## The Two Decisions: a User, and Its Database

**database user** — a name + password **the database itself** checks — separate from the machine's users.

```sql
-- at the postgres=# prompt:
CREATE USER app_user WITH PASSWORD '...';       -- who may talk (password typed live, never on slides)
CREATE DATABASE investapp OWNER app_user;       -- named database INSIDE Postgres, owned by that user
```

One word, two meanings — hold this one: `Postgres` = the database **program** (one, running on the server). `investapp` = a named database **inside** it, where the tables live. Your app names both when it connects.

## Set Up Your Access — on the App's Server

The app's server was built by the vibe build — it has the data, but no user for you yet.

```bash
# turn on password logins, then restart
echo 'host all all 127.0.0.1/32 md5' | sudo tee -a <pg_hba.conf>
sudo systemctl restart postgresql
sudo -u postgres psql -d investapp
CREATE USER app_user WITH PASSWORD '...';
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_user;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;   -- sequences too, or pg_dump fails
```

Here your user **owns nothing** — so you **grant** it what it needs: read the data, nothing more.

## psql — Talk to the Database From the Terminal

**psql** — the terminal client for Postgres: what the terminal is to the machine, psql is to the database.

```bash
psql -U app_user -d investapp      # connect: which user, which database
investapp=>                        # prompt changed — talking to the database now, not the shell
\dt                                # list the tables
# ledger | quote_cache             ← YOUR build's names may differ
```

The clean server answered `\dt` with **nothing**. This one has **a history** — the tables the vibe build made.

## Columns and Types — the Table's Own Plan

Every table declares its columns. Ask with `\d`:

```
\d companies
Column | Type
-------+--------
id     | integer
symbol | text
name   | text
price  | numeric
```

**column** — one detail every row has, declared up front with a name (`price`) and what it holds (`numeric`).

Column types, mapped to Python:

| \d says | Python said | What it holds |
|---------|------------|---------------|
| `text` | `str` | words — a symbol, a name |
| `integer` | `int` | whole numbers — an id, a count |
| `numeric` | (no float!) | money — exact decimals, no missing fractions |
| `timestamp` | — | a date-and-time — when the trade happened |

**Why money never goes in a float:** A float stores decimals only *approximately*. `0.1 + 0.2` in Python prints `0.30000000000000004` — not 0.3, but 0.3 plus a tiny error. Tiny errors on money are missing cents. `numeric` stores decimals exactly — that's why money lives there.

## The Schema — the Database's Whole Plan

Run `\d` on every table. The full picture of what this database keeps is its **schema**:

- **companies**: `id · symbol · name · price`
- **transactions**: `id · company_id · shares · amount`

**schema** — the written plan of the whole database: which tables exist, which columns each one has, what type each column holds.

It is a **contract the database enforces**: a row that doesn't fit the plan is refused — not quietly saved wrong.

## Primary Key — Every Row Has a Number

**primary key** — the row's permanent number: how the database (and the app) point at exactly one fact and no other.

```
transactions:
ID    | COMPANY_ID      | SHARES | AMOUNT
4183  | 1 → (NVDA's id) |   2    | -262.52
```

The trade's `company_id` holds `1` — and 1 is NVIDIA's id. **That is how a trade names its company: by number, never by copying.**

## SQL — Ask the Database a Question

**SQL** — the program's fourth language: English → bash → Python → **SQL** — the language of questions about records.

`SELECT` — ask the database a question. "Show me every company — first five." In SQL:

```sql
SELECT * FROM companies LIMIT 5;
```

- `SELECT *` = show what (every column)
- `FROM companies` = which table
- `LIMIT 5;` = how many (first five); `;` is SQL's full stop — the sentence isn't sent without it

## WHERE — Filter the Results

`WHERE` — the `if` you already wrote in Python:

```sql
SELECT * FROM companies WHERE price < 100;
```

- The test: `price < 100` — comparison works exactly as in Python
- What WHERE does: keeps **only the rows where the test is true** — the rest never leave the database

The database does it where the data lives, without shipping every row to you first.

## Text Wears Quotes

Numbers compare bare. Text goes in **single quotes**:

```sql
SELECT * FROM companies WHERE symbol = 'NVDA';
```

`'quotes'` — single quotes tell the database "this is text, not a column name or a number."

This exact line runs on PostgreSQL, MySQL, SQLite, SQL Server, Oracle — **unchanged.** Rule: **numbers bare, text in quotes.**

## Your Buy — On the Screen and in the Database

```
App's page:                    psql — same server:
NVDA · NVIDIA                  SELECT * FROM transactions WHERE symbol = 'NVDA';
2 shares · $262.52             id   | symbol | shares | amount
bought yesterday               4183 | NVDA   | 2      | -262.52
```

The screen and the row are **the same fact** — everything the app shows you is an answer it got from the database.

Opening question answered: "Your app remembers every trade — where do they live?" **That row — right there — is where.**

## The Backup Question: What If You Lost It?

Imagine your bank lost its database tonight: every balance, every transfer — **gone, with no way back.** Banks survive because they prepare for exactly that day. So will we.

Which single table, if lost, kills the app?

- **companies — recoverable**: app can ask the price service for the full list again
- **prices — recoverable**: go stale within minutes anyway; the app refetches them all day long
- **transactions — gone is gone**: the app's book of every buy and sell — its **ledger**. Your trades exist **nowhere else on earth**; there is nowhere to ask for them again

**backup** — a copy of the facts that exist nowhere else — kept **somewhere else**.

## pg_dump — The Whole Database as One Readable File

**pg_dump** — the program that writes the whole database out as one `.sql` text file.

```bash
pg_dump -U app_user investapp > backup.sql    # the whole database, into one file (> redirect you know)
less backup.sql                               # your tables, your rows — readable text you could email
```

Where should that file live? **The storage topic already answered it: a bucket** — never the same disk it's saving.

## Restore — Into the Server Born Empty

**restore** — feeding the dump file back in — the records, rebuilt from text.

A plain `pg_dump` carries tables + rows, but **NOT users/roles** — so first re-make them:

```bash
echo 'host investapp app_user 127.0.0.1/32 md5' | sudo tee -a /var/lib/pgsql/data/pg_hba.conf
sudo systemctl reload postgresql
psql -U app_user -d investapp < backup.sql    # feed the dump back in
\dt    # before: nothing → after: companies | transactions
```

To carry users/roles too: `pg_dumpall --globals-only > roles.sql`

**Two proofs at once: the install was real, and the backup is real.**

## Self-Managed vs Managed

We run our own Postgres on our own EC2 **deliberately** — hands dirty, learning what a database actually is.

- **Self-managed (us, today)**: install, back up, patch — we saw every piece. Nothing is magic now.
- **Managed (AWS RDS)**: someone else installs, backs up, patches. That's the Scale course — and by then you'll know exactly what it's managing for you.

**You now know what "managed" manages.**

## After Class

- **The full build**: install Postgres on a server → create the user → connect → `\dt`, `\d` → run the SELECTs → find your own transactions
- **One new question**: write ONE new SELECT about your own trading — "how much have I spent on NVDA in total?" — with Claude as tutor, not author. Bring the query and the number.

**What you own now:** what a database is, the field it comes from, a from-scratch install, its user, SQL questions about your own money — and a backup you proved by restoring it.

---

# Lesson 22 — The Page: HTML, CSS & JavaScript

## The Problem: What Arrives Is Not What You See

You have opened thousands of web pages in your life. Today, for the first time, you read one.

Every page you've ever visited works the same way: what **arrives** over the network is text — a wall of it. What you **see** is that text, rendered. The gap between the two is the whole topic.

## A Label Marks What Each Part IS

Take a heading and a paragraph — plain text:

```
Plov House
Plov — rice, carrots, lamb.
```

Wrap each in a label that says what it **is**:

```html
<h1>Plov House</h1>
<p>Plov — rice, carrots, lamb.</p>
```

The labels mark what each part IS — this is a heading, this is a paragraph — **so that a program can render it.** That is the whole idea. Two labels are enough to start; the rest arrive when a need arrives.

## The One Page Shape

The labeled text doesn't float loose — it sits inside a shape every page on earth shares:

```html
<html>                            <!-- the page, whole — everything lives inside -->
  <head>                          <!-- about the page — the browser reads this part -->
    <title>Plov House</title>     <!-- what the browser tab shows -->
  </head>
  <body>                          <!-- the page itself — what the visitor sees -->
    ...your labeled text...
  </body>
</html>
```

Four labels, nested one inside another: `html` holds everything, `head` is about the page, `body` is the page. Learn this shape once — it returns in every topic ahead.

## HTML — a Markup Language

**HTML (HyperText Markup Language)** — a markup language: a language whose statements **label** content. It describes — it cannot compute.

| | What it does |
|---|---|
| **Python — a programming language** | Variables, `if`, loops — it **computes**. You give it steps; it carries them out. |
| **HTML — a markup language** | Labels only. No variables, no `if`, no loops — on purpose. It says what things ARE, and nothing else. |

Deliberately **not** a programming language. A label only describes — it cannot crash.

The "HyperText" part: text that can point at other text — the founding idea of the web. That idea gets cashed in below, once files start pointing at each other.

## The Element

Opening tag + content + closing tag = an **element**:

```
<h1>  Plov House  </h1>
 ↑         ↑          ↑
opening   content   closing
 tag      (what a    tag —
(the      visitor    same word,
label,    reads)     a slash
opened)              closes it
```

Say it like an engineer: HTML is a markup language — its statements label content. It describes and cannot compute — no variables, no ifs, no loops. Every piece of it is an **element**: opening tag, content, closing tag.

## One Standard, Three Decades

| When | What happened |
|------|----------------|
| **1991** | CERN. Tim Berners-Lee invents the web — and HTML with it |
| **1990s** | standardized — every browser maker agrees to read the same labels |
| **2014** | HTML5 — the version the modern web runs on |
| **today** | a living standard, maintained by WHATWG — the browser makers, jointly |

The world's first website, from 1991, is written with labels you already know — a title, headings, links. Thirty-five years old, and you can read it. That is what a standard buys.

That agreement means any three strangers can work together without ever meeting:

- **Any author** — anyone can write a page: a physicist in 1991, an AI in 2026, you, in twenty minutes.
- **Any server** — any machine can hand the page over; it's just text, and the server doesn't need to understand it.
- **Any browser** — Chrome, Safari, Firefox all render the same labels the same way. A page written in 1996 still opens today.

Every website you have ever used — your bank, Instagram, your own app — is this **one format**. That is what "HTML is the standard for websites" means.

## Type One By Hand

Your first page is a fundamental, so it gets typed, not pasted — the same way your first `.py` did.

```bash
mkdir ~/code/menu                 # a product folder, like ~/code/quiz-bot — not a class folder
code ~/code/menu                  # opens VS Code on it
# New File → index.html           # index — the traditional name for a site's first page
```

Filled with the one page shape:

```html
<html>
  <head>
    <title>Plov House</title>
  </head>
  <body>
    <h1>Plov House</h1>
    <p>Plov — rice, carrots, lamb. $12</p>
    <p>Lagman — hand-pulled noodles. $10</p>
  </body>
</html>
```

```bash
open ~/code/menu/index.html       # Chrome opens — and it's YOUR page
```

No internet involved. A file on your disk, and a program that renders it. **That is a web page.**

## Render

**render** — to turn labeled text into the on-screen page. The browser reads the labels and renders the content — that is the word engineers use.

Your ten lines arrived as text. Chrome read `h1` and drew a big heading, read `p` and drew paragraphs, read `title` and wrote the tab. Labels in — pixels out.

Every browser carries a **rendering engine** for this job — Chrome's is named **Blink**. You never talk to it; you just know it's there.

## References: Pointing at What Text Can't Hold

A menu needs a photo, and a photo is not text — you cannot paste it into a text file. So HTML does the only honest thing: **it points at it.**

```
<img src="images/plov.png">
```

**reference** — one file pointing at another, by path. The photo stays its own file — the browser follows the pointer and renders both.

Notice: `img` has no closing tag. It wraps no text — there is nothing to put content around. A few labels are like that; their information rides inside the tag itself.

The pointer can aim at a URL too — `src="https://…/plov.png"` — but you don't own that file: if it moves or is deleted, your image breaks. Keep your own copy.

## The Attribute and the Path

| Part | Role | What it does |
|------|------|---------------|
| `<img …>` | the tag | "a picture goes here" |
| `src=` | an attribute | a named setting written inside the tag — the element just grew one more part |
| `"images/plov.png"` | the path | the same relative paths you've typed since week one — `images/…`, `../` |

```bash
mkdir ~/code/menu/images              # a folder for pictures
# <img src="images/plov.png">         # the new line, in index.html — right after the h1
# reload                              # the photo appears on your page
```

Paths that start with `/` are absolute — to what? That question gets its real answer once a site moves onto a server. Today, everything stays relative.

## One Broken Reference — the Rest Survives

```bash
mv images/plov.png images/plov2.png   # rename the photo — the pointer now points at nothing
# reload the page                     # the page is fine; the photo is the broken-image icon
mv images/plov2.png images/plov.png   # name it back → reload → whole again
```

- **Nothing crashed** — the browser rendered everything else anyway: headings, paragraphs, all of it.
- **One pointer failed** — one reference pointed at nothing, so one part is missing, and only that part.
- **You can see WHICH** — the broken-image icon marks the exact spot. Diagnosis by eye, no tooling needed.

The instinct to keep: **a page is assembled from parts; each part can fail separately.**

## A Link Is a Reference to Another Page

```
<a href="drinks.html">Drinks</a>
```

| Part | Role |
|------|------|
| `<a> … </a>` | the tag — a link. Its content ("Drinks") is what the visitor clicks |
| `href=` | another attribute — where the link points |
| `"drinks.html"` | the path — a file, found the same way the photo was |

A click opens THAT file instead — rendered, same as always. With a link back on the drinks page, you can walk between them forever.

## A Website Is Files Pointing at Files

```
index.html                          drinks.html
<h1>Plov House</h1>                 <h1>Drinks</h1>
<img src="images/plov.png">         <p>Green tea — by the pot. $3</p>
<a href="drinks.html">Drinks</a>    <a href="index.html">Back to the menu</a>
```

The held word, cashed in: **HyperText** — text that points at other text. Two pages, two pointers, one site. Every website you have ever used is this, scaled up.

## Markdown — a Different Markup, NOT for Web Pages

Said up front: Markdown is not for web pages — the browser never gets it. It is the markup for notes, and you've written it since week one: the lab README, the quiz decks your bot fed to `claude -p`.

```
Code (raw text)                    Preview (rendered)
# My lab                           My lab
Setting up my server, step by      Setting up my server, step by
step.                              step.
- launch EC2                       • launch EC2
- connect over SSH                 • connect over SSH
```

The same two-sided idea as the wall you opened at the start of today — raw text on one side, rendered on the other. Markdown is *also* a markup language; GitHub renders it. `#` is a heading the way `<h1>` is — no closing tags, no page shape. Lighter, on purpose.

## Markdown's Job: Notes for Humans — and Now for AI

Markdown was invented in 2004 so the *raw* text reads like a normal document — no wall, no labels in the way.

- **For humans writing to humans** — documentation, READMEs in a repository, instructions: readable before any rendering happens.
- **And today: the format AI reads and writes best** — your own quiz bot already proved it: markdown decks in, quizzes out.

One line to keep them apart, forever: **HTML is rendered by browsers for visitors; Markdown is read by people and AI where it lives.**

## The AI Grows the Site — and Explains It Back

You typed the fundamental. Growing it into a real site is a lot of typing — exactly what the AI is for. Claude Code, in `~/code/menu`, with one prompt:

```
Grow this into a small restaurant site for the restaurant already in
index.html. Three pages, photos, prices, and a reserve-a-table form.
Plain HTML and one CSS file (style.css) — no frameworks, no JavaScript
beyond what the form strictly needs (prefer none). Keep my hand-typed
index.html content recognizable. AND write MENU.md explaining every file
and what each part of the HTML does, one to one — so I can verify the
whole site by reading MENU.md first.
```

Back comes the site — pages, photos, one `style.css` — and `MENU.md`, the explanation you asked for up front. **Always ask for both: the work, and the explanation you will check it against.**

## Read the Map First, Then Verify

1. **The map** — `MENU.md`: the AI's explanation, written in the markup you write yourselves
2. **The files** — each `.html` file, read against the map: `h1`, `p`, `img`, `a` — you know every one of these
3. **The verdict** — does it match? Every claim in the map, checked against the file it describes

The standing practice, from here on: **the AI builds. The AI explains back. You verify.**

## CSS — the Looks Live in a Second Language

Where did the colors and fonts come from? Not from the HTML. The AI's pages carry one more reference — pointing at a second language:

```
<link rel="stylesheet" href="style.css">
```

**CSS (Cascading Style Sheets)** — the language of looks. **HTML says what things ARE; CSS says how they LOOK.**

```bash
# open style.css → change one color word → reload
# the whole site changes; the HTML never moved
```

Recognizing that line is the whole job today. CSS is a world of its own — writing it is not this program's path.

## Your Whole Site Is Files Pointing at Files

| Tag / attribute | Points at | What it is |
|------------------|-----------|------------|
| `link href=` | `style.css` | the looks |
| `img src=` | `images/plov.png` | a picture |
| `a href=` | `drinks.html` | another page |

One idea, three payments: **a tag holding a path.** `MENU.md` sits alongside, pointed at by nobody — it's for people and AI, not the browser.

## Frozen — Until Something Executes

Render the menu and it sits there — every pixel fixed until you reload. But the pages you use every day change **without reloading**:

- **A menu folds open** — tap the three-line menu button; it unfolds. No reload happened.
- **A form complains** — "You forgot your name" — before anything was sent anywhere.
- **A feed keeps growing** — scroll Instagram; more arrives, the page never reloads.

So something must be **executing instructions** — right there, in the browser, after the render. You know what a program is; you wrote them: instructions in a file, carried out step by step.

## JavaScript — the Third Language

**JavaScript** — the third language a page carries: instructions, brought along with the labels and the looks — and the browser **executes** them, step by step, after the render.

| Language | Job |
|----------|-----|
| **HTML** | what things ARE — rendered |
| **CSS** | how they LOOK — rendered |
| **JavaScript** | what to DO — executed |

The folding menu, the complaining form, the growing feed — all JavaScript, executed by the browser you're using right now.

## One Browser, Two Engines, Two Verbs

```
index.html (HTML)    style.css (CSS)         menu.js (JavaScript)
      \                    /                        |
       \                  /                         |
    rendering engine (Blink)              JavaScript engine (V8)
    reads labels + looks,                 carries out instructions
    draws the page                        step by step, after the render
         |                                          |
      RENDERS                                  EXECUTES
         |                                          |
    the page you see                    the page changing — a menu
                                         folds open, a feed keeps
                                         growing, no reload
```

HTML and CSS are **rendered**; JavaScript is **executed** — an engine for each. Chrome's pair: Blink and V8.

## Where Pages Carry Their Instructions

Not pasted into the page — **pointed at**, like everything else. When a page carries instructions, its head holds one more reference:

```
<script src="menu.js"></script>
```

| Reference | Points at | What it is |
|-----------|-----------|------------|
| `link href=` | `style.css` | the looks |
| `img src=` | `images/plov.png` | a picture |
| `a href=` | `drinks.html` | another page |
| `script src=` | `menu.js` | instructions |

One idea, four payments: **a tag holding a path.** You can now read every kind of pointer a page carries.

The honest boundary: JavaScript is a real language, deep enough for a whole course. Today you recognize it and say what it does — writing it is not this program's path. And *where* code runs — this machine, or the server — has its own topic ahead.

## Read Your Own App's Page

```
<!doctype html>                          ← one bookkeeping line: "this is HTML" — read it, move on
<html> <head>                            ← ✓ the shape you typed today
  <title>Invest — portfolio</title>      ← ✓ yours to read
  <link rel="stylesheet" href=…>         ← ✓ a reference — the looks
  <script src=…></script>                ← ✓ a reference — instructions
</head> <body>
  <h1>Portfolio</h1>                     ← ✓ an element — you know its anatomy
  <p>Cash: $10,000.00</p> …<img…> …<a…>  ← ✓ ✓ ✓
  <form> … <button>Buy</button> …</form> ← wait. what are THESE?
</body> </html>
```

When class started, this was a wall. Now you read most of it — as promised. Except the Buy button lives in a tag too: `form` and `button` — the tags a page uses to *send data back*. Today, just their names.

## The Click Needs a Program to Receive It

| | What happens |
|---|---|
| **The menu site** — Reserve-a-table, pressed | Nothing happens. A local file is just text — there is no program behind it to receive the click. |
| **Your app** — Buy, pressed | The buy lands; prices update. A running program received that click and acted on it. |

How a click travels from the page to that program — and how the answer comes back — **is the rest of true engineering.**

## After Class

- **Push `~/code/menu` to GitHub** — the git moves you know. Then open `MENU.md` on the repo page: it renders, the Code ↔ Preview toggle, on your own repo.
- **Grow it by hand** — one more page, `desserts.html`, typed yourself, linked from index and back. No AI: ten lines, your hands.
- **Read the web** — view-source three sites you use every day. Count what you can read now: `h1, p, img, a, link, script` — and notice the form tags waiting for us.

**What you know now:** a page is labeled text, and you typed one. References assemble a site — pictures, pages, looks, instructions, all files pointing at files. The browser renders HTML and CSS and executes JavaScript. And one question stays open on purpose: how does a click reach the program behind your app?

---

# Lesson 23 — HTTP: the Conversation Your Browser Is Having

## The Problem: A Click Needs a Program to Receive It

Last lesson ended on a question. Reserve-a-table on the menu site, pressed — nothing. A file on a disk has no program behind it. A stock buy on your app, pressed — the buy lands, prices update: **a running program received that click and acted.**

How the click travels there, and how the answer comes back, is the rest of true engineering. Today: the request and the response — and by the end, you read both raw.

## The Network Tab, Opened

Chrome ships a set of tools for engineers — **dev tools** — a troubleshooting surface, opened when something is broken. One tab of it matters here: **Network**. Opened with `right-click the page → Inspect → Network`, or `⌥⌘I` then Network.

Reload your app with it open, and rows fill in: `portfolio`, `style.css`, `app.js`, `logo.png` — each with a status, a type, a size, a time.

**Each row is one request sent, one response received.** Learning to read these rows is this whole lesson.

## Protocol — the Term Behind "They Just Understand Each Other"

Your browser was written at Google. The program answering on your EC2 was written by different people entirely. They have never met — yet the page arrives and renders, every time. The only way that works: both sides follow **the same agreed format** for every message — what the first line says, where the address goes, how the answer starts.

**protocol** — an agreed set of rules two programs follow to talk to each other, so programs that have never met can still understand each other.

Not a new idea — you've used protocols for weeks:

| Protocol | What it's the rules for |
|----------|--------------------------|
| **SSH** | a remote terminal — your Mac and your EC2 speak it every time you connect, on port 22 |
| **DNS** | turning a name into an address — spoken every time your domain finds your server |
| **HTTP** | asking for pages and answering — this lesson's protocol |

## Client and Server

| Role | Who plays it |
|------|---------------|
| **client — the one asking** | Your browser, asking for the page. `curl`, asking without a browser. Whoever **sends the request** is the client. |
| **server — the one answering** | Your EC2, answering with the page. Whoever **sends the response** is the server — the word literally means "the one that serves." |

The same machine can play either part: when you SSH in, your Mac is the client and your EC2 is the server — the same two roles, a different protocol.

## HTTP — HyperText Transfer Protocol

Unpack the name on the address bar:

| Part | What it names |
|------|----------------|
| **HyperText** | what travels — pages that point at other pages, the HTML you already read |
| **Transfer** | what happens to it — moving it from one machine to another |
| **Protocol** | how — agreed rules both sides follow |

**HTTP (HyperText Transfer Protocol)** — the agreed shape of the request a client sends and the response a server answers with. Every browser and every web server on earth speaks it. Designed together with HTML, by the same person, in the same year.

| When | What happened |
|------|-----------------|
| **1991** | CERN. Tim Berners-Lee invents the web: HTML the page, HTTP the way it travels |
| **1997** | HTTP/1.1 — standardized by the IETF, the internet's standards body. Plain text, readable |
| **2015+** | HTTP/2, HTTP/3 — faster carriers for the same conversation. Names to recognize |
| **today** | every browser, every server — request-then-response, never changed |

We read HTTP/1.1 today because it is plain text — your eyes can read every character of it. The newer versions carry the same conversation, packed tighter for speed.

## The URL, Read Left to Right

```
http://server.aigul.click/portfolio
```

| Part | Says |
|------|------|
| `http://` | which protocol — which rules this request follows |
| `server.aigul.click` | which machine — the domain, the name that finds the server |
| `/portfolio` | which thing — the path, what you want from that machine |

The menu site's bar, read the same way: `file:///Users/you/code/menu/index.html` — no machine, no request. **`file://` reads your own disk; `http://` asks another machine.**

## Name → Machine → Port, Refreshed

```
your domain (server.aigul.click)
        │  DNS looks it up
        ▼
   the machine's IP address
        │  arrives at a port
        ▼
http → port 80 · https → port 443 · (SSH stays on 22)
```

Requests get in at all because of the port-80 rule you added to your security group — the checkpoint in front of the machine — which is exactly what admits these requests.

If your domain has gone stale after a stop/start, the IP still works directly: `http://<your-public-ip>/portfolio` — no DNS involved.

## The Request, Raw

```
GET /portfolio HTTP/1.1          # the request line — verb, path, version
Host: <their-domain>             # a header — a labeled fact: which site this request is for
User-Agent: ...                  # another header — who is asking (the browser names itself)
```

| Part | Role |
|------|------|
| `GET` | the verb — "give me." Other verbs exist; they wait for a later lesson |
| `/portfolio` | the path — the same path from the address bar |
| `HTTP/1.1` | the version — which edition of the rules both sides speak |

Headers are labeled facts about the request — real requests carry a dozen more, and nobody reads them all.

## The Response, Raw

The answer comes back in four parts: **the status line** (how it went), **headers**, **one empty line**, then **the body** — the same HTML you already learned to read.

```
HTTP/1.1 200 OK                  # the status line — 200 is the number every answer carries
Content-Type: text/html          # a header

<!DOCTYPE html>                  # the empty line above ends the headers — this is the body
<html>...
```

One ask, one answer — you can read every character of both.

## curl — the Raw Answer, in the Terminal

**curl** — fetches a page from the command line. It shows you the answer raw, nothing rendered.

```bash
curl http://<their-domain>/portfolio      # the body fills the terminal — HTML, and you can read it
curl -i http://<their-domain>/portfolio   # -i: the status line and headers appear above the body
```

Domain stale? The IP works directly: `curl http://<your-public-ip>/portfolio`.

Status line, headers, empty line, body — the exact shape you just read raw, arriving for real.

## curl vs Chrome: What You Get vs What You See

| | What it does |
|---|---|
| **curl** | prints what arrives, and stops |
| **Chrome** | renders it, then keeps going — it requests every reference it finds, by itself |

curl made **one** request and stopped. Chrome made **four** — and the Network tab from the start of the lesson shows exactly that: **one row per request.**

## The Number Every Answer Carries

Last lesson we said a browser's report of a missing part has a name and a number. Here it is: the **status code** — the number on every status line. Four families:

| Family | Meaning |
|--------|---------|
| **2xx** | it worked — `200 OK`, the one you've been seeing all day |
| **3xx** | go elsewhere — the answer lives at another address |
| **4xx** | the request is wrong — `404 Not Found`: no such thing here |
| **5xx** | the answering side broke — the server failed to build an answer |

The engineer's reading: **4xx — check the request; 5xx — check the server.** The number tells you which side to check first.

The honest note: the menu site's broken image had no number — a file opened from disk has no response to carry one. The name-and-number exists only on the web.

## A Thing That Isn't There — the Answer Is 404

```bash
curl -i http://<their-domain>/no-such-thing
HTTP/1.1 404 NOT FOUND           # the status line: the request was wrong — no such thing here
```

The same path in Chrome: the Network row turns red, status 404.

- **The server did its job** — it read the request, found nothing at that path, and answered properly: status line, headers, a small body.
- **The number named the problem** — 404, the request is wrong, not the server. The same number a broken image reference produces on the web.

Nothing crashed — **the answer is "no such thing."**

## One Stock Buy — the Answer Is a Redirect

Network tab open, Preserve log **ON** — without it the first row vanishes. Press Buy — two rows appear:

| Row | Answered | What it means |
|-----|----------|-----------------|
| 1 — the stock buy's request | **302** — a redirect | "done — now ask over there." A 3xx: go elsewhere. The answer names the new address. |
| 2 — the browser obeyed | **200** | the browser read the number and made the second request by itself — the fresh portfolio page. |

Builds vary — some don't redirect at all. Read yours. What the stock buy carried — the ticker, the amount — is its own lesson ahead.

**Some status codes are instructions the browser follows.**

## One Click, Many Rows

Back to the first look at the Network tab, now readable:

1. **You asked for one page** — the first row is the HTML itself
2. **Chrome read that HTML and found every reference** — `style.css`, `app.js`, `logo.png`
3. **It requested each one, by itself**

**The first row is the page. Every other row is a reference Chrome requested by itself.**

## A Reference Can Point at Another Machine

Every `src` you've read so far held a path on the same site. But `src` can hold a full URL — and then Chrome's follow-up request goes to *that* machine:

```html
<img src="https://…s3.amazonaws.com/logo.png">
```

On a real site, one row often comes from elsewhere — an image or video answered by **S3**, object storage, fetched by name. Its row shows a different domain.

**A page assembles from many servers.** One EC2 sent the HTML; S3 sent the logo — one page, two machines. Your own build most likely serves its logo from its own disk — read your logo row's domain to see whose machine answered.

A site you use every day, reloaded with the tab open, shows the difference in scale:

| Site | Rows |
|------|------|
| **your app** | 4 rows — one page, three references, two machines |
| **a bank homepage** | dozens to hundreds of rows — pictures, styles, scripts, fonts — from many machines |

Any row reads the same way: **name · status · type · size · time** — the same five columns, the same request and response underneath.

## Under HTTP: TCP and IP

Before any text moves, the two machines **open a connection** — TCP, the Transmission Control Protocol. A quick **three-way handshake** — hi, hi back, got it — then every byte arrives, in order, both directions. Your request rides it through machines you will never see.

```
Your Mac (client, its IP)  ──── TCP connection ────  Your EC2 (server, its IP, port 80)
                             (one open channel;
                          every byte, in order,
                            both directions)
                                   │
                       inside it rides the readable
                          HTTP request text
```

Plain http is a postcard: **every machine that passes it along could read it.**

**IP finds the machine · TCP carries the bytes · HTTP gives them meaning.**

TCP's sibling — **UDP**: no handshake, no confirmation, just broadcast. Right for video and live games, where a dropped frame beats waiting. The application picks: web, SSH, and databases run on TCP; streaming leans on UDP.

## HTTPS — the Same Conversation, Sealed

The same text, **encrypted before it leaves** — only the two ends can read it. The address on the outside stays readable: delivery still needs it.

```
Your Mac  ──── TCP connection (port 443) ────  Your EC2
             inside: the HTTP text, sealed —
             gibberish to anyone in between
```

The machines in between still deliver it; they just can't read it anymore — only the two ends can.

**HTTPS is just a secure HTTP** — same request, same response, sealed on the way.

The padlock proves the address, not the owner: it means no one in between can read your data and the page really is at that address — not that whoever holds the address is honest. A look-alike domain can carry a padlock too.

Week 5, recalled: `certbot` fetched your certificate from Let's Encrypt — what a server needs before browsers will seal a conversation with it. The padlock in the address bar means it worked.

## What's Next

Your menu site is still a file on one Mac. Nobody can send it a request.

| Today | Next lesson |
|-------|--------------|
| `file://` — your disk, no machine, no request — only you can open it | `http://` — a server listens, waits for these requests, and answers each one with the right file — **that is hosting** |

## After Class

- **curl your app** — `curl`, then `curl -i` — find the status line, the headers, the empty line, the body.
- **Find your stock buy's answer** — Network tab, Preserve log ON, one stock buy. Does your build answer with a redirect like the instructor's, or another shape? Read the rows either way.
- **Count your page's rows** — reload with the tab open. First row: the page; match the rest to lines in the source. One extra row like `favicon.ico` (the tab icon — Chrome asks by itself) is normal.
- **Whose machine answered your logo?** — read your logo row's domain. Most builds: your own EC2, from its disk. On a big site: often S3 or a CDN — a different machine.

**What you know now:** every page is an answer to a request, and you can read both raw — the verb, the path, the status line, the number. The Network tab shows every request a page makes. TCP carries the bytes; HTTP gives them meaning; HTTPS is the same conversation, sealed.

---

# Lesson 24 — Static Hosting: Your Menu Site Goes on the Internet

## The Problem: An HTML File Opens Two Ways

The menu site is still files on your Mac, opened only by you. An HTML file needs a program to open it — so far that program has been Chrome, reading a file off your own disk. The address bar shows it: `file:///Users/you/code/menu/index.html` — nothing left the machine, and it only works on this Mac.

To open it **from the internet**, the address starts with `http://`, and the file must be **on a machine that answers HTTP requests**. Today the menu site goes live, two ways: your own server running nginx, then S3.

## What a Machine Needs, to Answer for a Site

Three things, in words you already own from the HTTP lesson:

| Requirement | Why it matters |
|---|---|
| **Always on** | Awake and reachable at any hour — a request can arrive at 3 a.m. and must still be answered |
| **A public IP address** | An address the whole internet can reach — the way a request finds the machine at all |
| **A program listening on port 80** | A program that reads each request's path, finds the file, and sends it back in the response |

**hosting** — keeping your files on a machine that does exactly this: always on, publicly addressed, a program answering requests for them.

Not your Mac: home wifi gives it a private address the internet can't reach, and a laptop sleeps the moment you close it — a host can never sleep.

## We Have Done This Before — Week 5, Refreshed

Back in week 5 you put a page on the web with three moves, copied without the ideas behind them:

1. **Install a web server** — one command on your first server, and a program appeared and started answering
2. **Put a page in a folder** — a file dropped into one specific place on the machine
3. **The site was live** — an address, and the page came back

Every one of those steps has a name and a reason. This lesson does it again — and this time you can read each line.

## nginx — a Web Server, Named

**a web server** — a program that listens on a port, reads the request's path, finds the file, and answers with it. **nginx** (say "engine-x") is the one we run.

| | |
|---|---|
| **2004** | written by Igor Sysoev — to answer huge numbers of requests at once |
| **open source** | free to read and run — anyone can see exactly how it works |
| **today** | the most-used web server on the internet |
| **yours** | it served your week-5 site — and much of what you browse daily |

The other big name is **Apache** — it ran most of the early web, and you'll hear it named beside nginx for the rest of your career. We run nginx; that's all you need of Apache today.

## A Server of Its Own

Port 80 on your app's server is already taken — by whatever answers your app. Two programs can't listen on the same port on the same machine. So the menu site gets its own fresh, small server, launched the same way as the app's:

| Setting | Value |
|---|---|
| **AMI** | Amazon Linux 2023 — the operating system for the machine |
| **type** | `t3.micro` — small and cheap; a static site needs little |
| **key pair** | the key that lets you SSH in — same as the app's server |
| **security group** | open port 22 (SSH) and port 80 (HTTP) |

The security group is the checkpoint in front of the machine — opening port 80 there is what lets HTTP requests reach it at all, the rule you first added in week 5.

## Launched, Reachable — and Silent

The new server is up: a public IP, port 80 open in the security group, SSH'd in. But no web server is installed on it yet. Ask it for a page from your Mac:

```bash
curl http://<public-ip>
# → curl: (7) Failed to connect to <public-ip> port 80: Connection refused
```

Port 80 is **open**, but empty. **Connection refused** means the connection reached the machine — and nothing was listening to answer.

You may see `connection timed out` instead of `refused`. **Refused** = the packet reached the machine and nobody answered (port open, no listener). **Timed out** = it never got there — a security-group or routing gap. Either way, nginx isn't up yet.

## Install nginx — the Same Request Now Answers 200

```bash
# on the server
sudo dnf install nginx                  # dnf: the AL2023 package installer
sudo systemctl enable --now nginx       # start it now, and keep it started on every reboot
```

Run the same request again — same address, new answer:

```bash
# from your Mac — same request, new answer
curl -i http://<public-ip>
# → HTTP/1.1 200 OK
#   Server: nginx
#   Content-Type: text/html
#   ...<!DOCTYPE html> ... Welcome to nginx! ...
```

The same `curl -i`, now **200 OK** — status line, headers, an HTML body: the exact shape you read raw last lesson. In Chrome: the nginx welcome page.

## The One Rule This Whole Lesson Rests On

That welcome page is a file on the server's disk. nginx's rule is simple: **the request's path names a file under one folder — the root.**

| Request | File served |
|---|---|
| `GET /` | `index.html` — by convention, `/` means `index.html` |
| `GET /drinks.html` | `drinks.html` |
| `GET /nothing.html` | no matching file → `404 Not Found` |

Own this sentence: **this address → this file**. Every file nginx hands back lives under the root folder — nginx serves nothing outside it. `404` means it looked and found none.

## Where the Rule Is Written

nginx reads its settings from `/etc/nginx/nginx.conf`. Most of it we skip today — but three settings carry the whole static story:

```
http {
  server {
    listen 80;                    # answer on port 80 — IPv4
    listen [::]:80;               # the same port 80 — IPv6
    root /usr/share/nginx/html;   # the folder every path is found under
    index index.html;             # for /, hand back index.html
    ...                           # the rest — skipped on purpose
  }
}
```

**listen** the port, **root** the folder, **index** the page for `/`. (`listen` twice = port 80 for IPv4 + IPv6.)

## Put the Menu Where nginx Looks

The menu site — three pages, `style.css`, the images — has lived at `~/code/menu` on your Mac since the page lesson, and its take-home pushed it to GitHub. The server can't see your Mac's disk — so it takes the files from GitHub:

```bash
# on the server — clone the menu, copy it into the root folder
git clone https://github.com/<instructor>/menu.git
sudo cp -r menu/* /usr/share/nginx/html/
```

Open `http://<the-ip>/` — the menu site, live on the internet, reachable from any laptop or phone, anywhere.

Copy into the default root, `/usr/share/nginx/html`. Pointing nginx at a home folder answers **403 Forbidden** instead — a classic permissions trap.

## The Live Site, Read in the Network Tab

Reload the live menu with the Network tab open — one row per file: `<public-ip>` (document), `style.css` (stylesheet), `plov.png` (png) — each `200`. Click **Drinks** → a new row, `GET /drinks.html` → `200`.

Ask for something that isn't there:

```bash
curl -i http://<public-ip>/no-such-thing
# → HTTP/1.1 404 Not Found
```

A 404 means nginx looked under its root, found no file at that path, and said so. Nothing crashed — the server did its job.

## Absolute Paths, Answered

The menu already uses a path that starts with `/` — `<img src="/images/plov.png">`. Absolute, we said — but absolute to *what?*

| | |
|---|---|
| **Absolute to the root folder** | the path is counted from the root folder — on this server, `/images/plov.png` is the file `/usr/share/nginx/html/images/plov.png` |
| **The root folder is also the boundary** | nginx serves only what's under it. The server's keys and configs sit elsewhere on the disk — a request through this rule can't reach them |

## Static — the Real Term

Every answer this server gives **existed as a file before the request came** — same address, same bytes, for everyone, every time.

**a static site · static hosting** — a site whose files are written ahead of time and handed back unchanged; serving one this way is static hosting.

## S3, Recalled — Before We Host on It

From the storage lesson — the second way to host lives here, so recall what S3 is:

| | |
|---|---|
| **A bucket holds files** | you create a bucket in the S3 console and put files in it. S3 calls each stored file an object |
| **Every file has a name** | you get a file back by asking for it by name. No disk, no machine of yours — AWS's machines keep it stored |
| **The asking is HTTP** | fetching a file from S3 is a plain GET request — the same kind of request you've been reading for two lessons |

You've already watched S3 answer one: in the HTTP lesson, an app logo can arrive from an S3 domain — its own row in the Network tab, status 200.

## Why S3 Can Host the Menu

Hosting took three things — always on, a public address, a program that finds the file and answers. Check S3 against that list:

| | |
|---|---|
| **Always on** | the machines behind the bucket are AWS's — they never sleep, and they're AWS's to patch and keep awake, not yours |
| **A public address** | a bucket can be given a website address — an endpoint any browser can reach |
| **This address → this file** | ask for a file by name, get it back. The menu site *is* files — pages, `style.css`, images — so S3 can serve every one of them |

The same rule nginx follows — **this address → this file** — with no server of yours behind it.

## Host the Menu on S3

All in the S3 console — no SSH, nothing to keep running. Pick your **own** bucket name; names are global, so everyone would collide on one.

1. Create a bucket, and **upload the menu files** into it.
2. Turn **OFF** "Block public access" — a master override that keeps private buckets (medical records, backups) off the internet no matter what the policy says. This bucket is public on purpose, so we turn it off; AWS shows scary red warnings — expected here.
3. Add a **bucket policy** allowing public `s3:GetObject` — switching off the block does not by itself make objects public. (`GetObject` = read/download only, not write or delete.)
4. Properties → **Static website hosting** → on; index document `index.html`.
5. Open the **website endpoint URL** — the same menu site, served by AWS.

```
http://<bucket>.s3-website-<region>.amazonaws.com
```

The endpoint starts with `http://` — expected here, not a mistake. Nothing to SSH into, nothing to keep alive. Open the **website endpoint**, not a plain object URL (`.s3.amazonaws.com/...`) — only the website endpoint serves `index.html` for `/`.

On the school AWS account, steps 2–3 can fail "not authorized" even as admin — an org-level rule (SCP) can block making buckets public. If your take-home hits this, that's why — ask in Slack.

## Your Own Server, or S3 — the Honest Trade-Off

| | Your own server | S3 static hosting |
|---|---|---|
| **What runs it** | nginx on an EC2 machine you keep alive | a bucket where AWS runs the listeners |
| **Control** | full control, HTTPS is possible (the week-5 certbot steps) | you live by AWS's rules |
| **Cost** | ≈ $108/yr — a machine to keep alive, patch, and pay for | ≈ $10/yr — no machine, scales with no server of yours to overload |
| **HTTPS** | yes, with certbot | no — the piece that adds it (CloudFront) is a name for later |

Both are real choices — an app can use both at once: its pages from its own server, its logo from S3.

## What's Next

The menu site is on the web, two ways — but every answer it gives was written before the request came.

| Today | Next lesson |
|---|---|
| A static site — every file exists before you ask for it | A price that changes since this morning — no file written in advance can be that answer. Something has to build the answer at the moment you ask |

## After Class

- **Redo the server** — launch a fresh small server, install nginx, put the menu in the root — your site on your own IP.
- **Redo it on S3** — the five bucket steps. Bucket names are global — pick your own name, don't reuse the demo's.
- **Optional: a real name** — point `menu.<your-domain>` at the server, using the week-5 DNS steps.

**What you know now:** hosting means files on an always-on, public machine. nginx is the web server, listening on port 80. This address → this file — the root folder and the index.html convention. Static means every answer written in advance. S3 hosts the same site with no server of yours.

---

# Lesson 25 — Dynamic and the API: When Static Hosting Can't Be the Answer

## The Dead End: Could nginx Serve the App?

The menu site sits still: same files, same bytes, for everyone, every time. The investment app can't work that way — three reasons nginx alone can't be the answer:

| Reason | Why a saved file fails |
|---|---|
| **The price moves** | A saved page is stale within minutes — the market doesn't wait for you to re-save a file |
| **Every stock buy changes the page** | Rewrite the file after every click, forever? No process does that |
| **A stock buy isn't a page at all** | It's work to **do** — check the price, move the cash, record the trade — not a file to hand back |

Static — **every answer already existed as a file.** The app needs answers that don't exist yet, at the moment you ask for them.

## Dynamic: The Answer Composed When You Ask

**dynamic** — the response is made at the moment of asking, from what is true at that moment. Static's mirror: that answer existed before the question.

Think of a print stand versus a street artist. The print stand sells copies finished before you came — **static: the answer existed before the question.** The artist starts sketching when you sit down — **dynamic: the answer is made because the question arrived.**

## The Same GET, Answered Two Ways

Same request, two different machines behind it:

| | The menu server (static) | The app's server (dynamic) |
|---|---|---|
| **Request arrives** | `GET /` reaches nginx | `GET /` wakes the app's program |
| **What it does** | Reads the path, finds `index.html` on disk | Reads the database — cash, holdings, prices, as they are right now — and does the math |
| **What it sends** | The same bytes, unchanged | HTML written fresh, composed for this moment |
| **Label** | **found** | **composed** |

No file existed for the dynamic answer — it was written just now.

## Live: Same Address, Asked Twice

Three steps, on the instructor's real app:

```bash
# Step 1 — read cash and holdings
curl http://<the-ip>/
# → Cash: $10,000.00   NVDA: 0 shares

# Step 2 — one stock buy, in the browser (between the two curls)

# Step 3 — same address, a few minutes later
curl http://<the-ip>/
# → Cash: $9,814.80   NVDA: 1 share
```

Same address, different answer — nobody edited any file. The database changed between the two curls, so the program wrote different bytes the second time.

## What Came Back Is Still HTML

Read what the second curl actually printed — ordinary HTML, the same tags you already own:

```html
<html>
  <head> <title>Invest — portfolio</title> <link rel="stylesheet" …> </head>
  <body>
    <h1>Portfolio</h1>
    <p>Cash: $9,814.80</p>
  </body>
</html>
```

Written fresh — from what? The code keeps a **template**: the tags, with blanks where numbers go. Each request, it fills the blanks. The template is a file — the finished page never is.

## "Dynamic" Names the Answering — Nothing Else

Three things sit in this picture. Only one of them moves:

| Part | Still or dynamic |
|---|---|
| **The code** | Still — a file on disk, sitting there |
| **The page** | Still — plain HTML, finished by the time it reaches you |
| **The answering** | **Dynamic** — same address, different answer, depending on what's true right now |

"Dynamic" doesn't mean the code changes, or the HTML is some new kind of tag. It means the *answering* happens live.

## Who Runs the App's Code — Found on Port 80

You ran this in assignment 11. In English: list every program listening, and on which port:

```bash
sudo ss -tlnp
```

| Flag | Meaning |
|---|---|
| `-t` | TCP connections — the kind the web and SSH use |
| `-l` | only ports being listened on |
| `-n` | show numbers, not names |
| `-p` | show the program |

```
LISTEN  0.0.0.0:80      users:(("gunicorn",…))   # the app's own program — not nginx
LISTEN  0.0.0.0:22      users:(("sshd",…))       # how your terminal comes in
LISTEN  127.0.0.1:5432  users:(("postgres",…))   # the database chapter's program
```

Port 80: **gunicorn** — running since the vibe build. Yours might differ: some builds show nginx on `:80` instead, forwarding to gunicorn on an internal port — a **reverse proxy**. Same job as nginx at the door, gunicorn cooking inside — one extra hop.

## Code Doesn't Run Itself

Your quiz bot sat on disk doing nothing — until you ran it with `python3`. The app's code is Python too. But on the app's server, nobody is at a keyboard. So what runs your app's code, day and night, with nobody there to type the command?

## Flask Is in the Code — gunicorn Runs the Code

Two names, two jobs:

| | Job |
|---|---|
| **gunicorn** | **The runner.** Like you typing `python3` — but always on. It holds port 80 and runs your code for every request, day and night. |
| **Flask** | **Inside the code.** Ready-made Python parts the code is built from — the web plumbing came ready; your code adds the stocks and the cash. |

Nobody writes "receive a request over the network" from zero — you take ready parts (Flask) and something to run them (gunicorn). Every language has its own pair.

## gunicorn Runs Copies — Nobody Waits

Requests — `GET /`, a stock buy, `GET /` again — all arrive at port 80. gunicorn is the container holding the port; inside it, it runs several copies of your code at once: one answering a request, another at the same time, a third — nobody waits in line. Same code, several times over, written with Flask. Each copy sends back a fresh page.

## gunicorn Is a Choice, Not a Standard

| | What it means |
|---|---|
| **Standards — every website shares** | HTTP · ports · HTML. That's why one browser can talk to all of them. |
| **Choices — what this build picked** | Python · Flask · gunicorn · Postgres. Other apps pick other languages — and other runners. |

Meet any new app: expect the standards to be there — and the choices to be different.

## "Server" Now Names a Program Too

First the machine was "the server." Then nginx — a program — was too. Now the app's program is one more:

| | The menu server | The app's server |
|---|---|---|
| **What listens on :80** | nginx — a program you installed | gunicorn — the app's own program |
| **How it answers** | Hands back files, unchanged | Composes every answer fresh |

**"The server answered"** usually means the program — which one, you read from context.

## The Backend — The Half Nobody Sees

**backend** — the half of your app that runs on the server: your Flask code, run by gunicorn. No screen, no buttons, never seen. It composes every answer from the database beside it — call it **the brain of the application**.

## The Database — The Backend's Memory

You sat inside one this week with `psql`. Everything a backend says, it reads from here first:

| Database | What it holds |
|---|---|
| **Yours** | cash · holdings · prices — every number the dashboard shows |
| **Your bank's** | every balance, every transfer ever made |
| **Instagram's** | every post, every like, every follower |

Everything that matters is in there. So why can't your browser ask it directly?

## You Can't Query the Database Directly — On Purpose

Requests from anyone on the internet — your browser, anyone else's, any program — all land on the backend, which alone decides what can be asked and holds the only path to Postgres. There is no path straight from the internet to the database — none exists, on purpose. Your own `psql` moment was a separate, controlled path: you, over SSH with your key, then `psql` from inside the server. The app's users have no such path.

## Frontend — What the Browser Shows

**frontend** — HTML, CSS and JavaScript, rendered in your browser, on your machine. Engineers say **client-side**. The frontend asks, the backend answers — HTTP, the same conversation from the last two lessons. Some code runs in your browser, some runs on the server.

## Frontend, Backend, Database — a Three-Tier Setup

| Tier | What it is |
|---|---|
| **Tier one — the frontend** | The dashboard rendered in your browser |
| **Tier two — the backend** | Your Flask code, run by gunicorn, holding port 80 |
| **Tier three — the data tier** | Postgres, reachable only through the backend |

Today, tiers two and three share one machine. Say it like a system designer: **ours is a three-tier setup** — three parts. (Your `psql` moment, talking straight to the database, was **two-tier** — no backend standing between you and the data.)

## The API — How Programs Ask Programs

Your news bot, weeks ago, asked two programs for help — no browser, no screen, no clicks, and it worked every morning: request #1 asked Claude ("find today's news, write the post" — the key said which account was asking), request #2 asked Telegram's bot service ("post this into my channel" — the token said which bot), and your phone buzzed. Programs asked programs. No human clicked anything.

**API — Application Programming Interface** — the agreed list of requests a program offers other programs. Making one request from the list is **an API call**.

Humans get screens and buttons. Programs get an agreed list of requests. `ANTHROPIC_API_KEY` names *which account* is calling the Anthropic API — Claude's list of requests. `TELEGRAM_BOT_TOKEN` names *which bot* is calling the Telegram Bot API — Telegram's list. Two keys, finally explained.

A taxi ride is the same shape: your phone and the driver's phone are both frontends; the taxi company's backend matches you, computes the fare, and composes what each phone shows — and it in turn calls a maps company's API and a payments company's API. DoorDash, checkouts, maps — same shape everywhere. The web runs on programs asking programs.

## Your App's API — the Requests It Answers

Same shape, your size. Your backend holds its own agreed list — what you can ask me: check the portfolio (`GET /`), buy a stock, sell a stock. The frontend asks all three. One request runs the other way: when a saved price is stale, the backend asks the price service for a fresh one — on that request, **your backend is the client**. Every request has the same shape: a verb (do what) and a path (to what). Paths differ per build — the shape is shared.

## The API, Watched in the Network Tab

One dashboard load, one stock buy — **Preserve log ON first**, or the buy row vanishes on the redirect. Sort the rows into two kinds:

| Row | Status | Kind |
|---|---|---|
| the buy | `302` | API call — answered by the backend, composed |
| the portfolio reload | `200` | API call — answered by the backend, composed |
| `style.css` | `200` | plain file fetch — a finished file |
| `logo.png` | `200` | plain file fetch — a finished file, from S3 |

The 302's meaning, at last: the stock buy changed things, then sent the browser for the fresh page.

## Login — Skipped on Purpose

**login · authentication** — the backend's check of *who* sends each request, before it answers. "Login" is the everyday word; **authentication** is the engineer's.

A bank's backend checks every request: whose balance is this? Yours skips this on purpose — one server, one owner. Anyone who reaches it sees the same one portfolio. A real app adds this check first.

## What's Next

| Today | Next lesson |
|---|---|
| Frontend asks, backend answers — a request with just a verb and a path | The stock buy told the backend **which** stock and **how many**. How does a click carry data into the request, and into your app's own code? |

## After Class

- **curl twice around a stock buy** — on your own app. If the two curls match, nothing is broken — your build may hold data a different way; a later lesson names it.
- **Find what holds port 80 on yours** — `sudo ss -tlnp` on your own server. Builds vary — read what **yours** says.
- **Sort your app's rows** — Network tab, Preserve log ON, one stock buy. API calls — or plain file fetches?

---

# Lesson 26 — What the Buy Button Sends: Payload, the Dict & the Route That Reads It

## Fetch vs Send — Two Kinds of Clicks

Every click so far in this course *fetched* a page — a link, a refresh, "give me that page," nothing travels but the address. Some clicks carry something **from you**:

| | What travels |
|---|---|
| **Fetch** | A link, a refresh. Nothing travels but the address. |
| **Send** | A Google search, a login, a chat message, **your stock buy** — what you typed travels with the request. |

The app can't know which stock you want — **unless the click brings it along.** Plain browsing is a fetch, a GET, just asking for a page. The moment you buy, sell, or change data through the UI, that's a send.

## Live: What the Buy Button Actually Sent

Network tab, **Preserve log ON** first — without it, the buy row vanishes on the redirect. One stock buy in the browser, then click the buy row and open **Payload**:

```
symbol: NVDA      ← which stock
shares: 1         ← how many
```

**payload** — what a request carries in. Like an envelope, the payload is what's inside: small, readable, each value with a label on it. Some builds send this in the URL instead of a Payload panel — same key:value pairs, a different place (why, later in this lesson).

## Key and Value — Naming Instead of Position

The list from the Python lesson stores by position — `classes[0]` — and position doesn't say what a value means. The payload stores by **name**: the label is the **key**, what sits under it is the **value**. It's the same shape as a database row — `symbol, name, price` over `NVDA, NVIDIA, 131.26` — every value under a named column. A name, then its value, twice over.

## The Dict — Python's Type for Key:Value

The Python lesson's list read by position. The dict reads by name — braces instead of brackets:

```python
order = {"symbol": "AAPL", "shares": 2}   # braces make a dict; each pair is key: value; commas between
order["symbol"]                           # read by NAME → 'AAPL' — the list's brackets, a name where the position went
```

| | Reads by |
|---|---|
| **The list** | position — `classes[0]` |
| **The dict** | name — `order["symbol"]` |

A row was described in the database lesson, in passing, as "a dict — one bundle of named values." Reading by name is like a bilingual dictionary: you give it the word, it gives you the translation.

## Live: Dict Practice — Make, Read, Break

```python
order = {"symbol": "AAPL", "shares": 2}
print(order["symbol"])          # read by name → AAPL
order["shares"] = 3             # change a value by name
order["price"] = 202.50         # a new name adds a pair
print(order["ticker"])          # a name that isn't there…
```

The program stops on the last line:

```
KeyError: 'ticker'   # a precise answer: no such name. The 404 of the dict.
```

This same file is the take-home — try it, then try your own (`car.py`: model, year, mileage — same moves).

## JSON — the Same Shape, Traveling

Facts written as key:value pairs in braces. Secrets Manager answered you in it, back in the scripts lesson:

```
{ "Name": "news-bot/anthropic", "SecretString": "sk-ant-…" }   # --query pulled one value out BY NAME
```

The price service's answer, from the AI-agent lesson, was the same shape — never named then:

```
{ "symbol": "NVDA", "price": 184.32 }
```

## The Dict and JSON — One Shape, Two Places

A dict lives only while a Python program runs — **at rest**, inside memory. JSON is the same pairs written as plain text, crossing the wire — **traveling**. Read back into another program, any language can parse it, because JSON belongs to none of them. Where you'll meet each: the price service and the Anthropic API answer in JSON; a stock buy from a form travels as form fields instead — where things ride is next.

## GET vs POST — Looking or Changing

| | What it means |
|---|---|
| **"Show me my portfolio"** | Looking. Repeat it all day — **nothing changes.** |
| **"Buy one share"** | This one **changes your account.** |

The web marks the kind — it's the first word of the raw request, from the HTTP lesson:

| Verb | Meaning |
|---|---|
| `GET` | looking — safe to repeat |
| `POST` | sending something in, to change things |

Your rows, sorted: dashboard, `style.css`, the S3 logo — all GET. The stock buy is the one POST.

## Where What You Send Rides — Query String vs Body

```
GET /search?q=nvidia+stock HTTP/1.1   # every Google search you've ever made — a little rides in the address
Host: www.google.com
```

```
POST /buy HTTP/1.1
Host: <the-app-ip>
                                       # the blank line from the HTTP lesson
symbol=NVDA&shares=1                  # the payload — the same pairs from the panel
```

Same first line you've always read — now with what you sent under it. Seeing your own password in plain text in the Payload panel is normal, not a leak: DevTools shows the body before HTTPS encrypts it on the wire.

## The Form — Where the Labels Come From

View-source on the dashboard — the buy button sits inside a form:

```html
<form action="/buy" method="POST">
  <input name="symbol">              <!-- the input's name… -->
  <input name="shares">
  <button>Buy</button>               <!-- submit packs every name=value pair into the body -->
</form>
```

The panel's labels, the body's pairs — they're the form's input names. The page source, from the HTML lesson, now doing a job.

## POST-Redirect-GET — Why Refresh Doesn't Buy Again

You hit refresh after a stock buy. Does it buy again?

| | |
|---|---|
| **Refresh repeats the last request** | If the last request was the POST — **that's buying again.** The browser's "Confirm Form Resubmission" warning is asking exactly this. |
| **So the app answers "done — ask over there"** | The 302 from the API/network-tab lesson. After it, the last request is the harmless GET — **refresh all you like.** |

**POST-redirect-GET** — answer every POST with "go look at the fresh page." Engineers' name for the pattern your app already follows.

## Into the Code: the Function and the Route

SSH to the app's server, open the code with `less` — read-only, nothing edited, nothing restarted. The whole app is a page or two of Python, and a pattern repeats: a line starting `@app.route`, a `def` line, an indented block under it. One of those blocks answers the stock buy.

```python
def buy():          # def gives the block below a name: buy
    …               # the indented lines are the block
```

**function** — a named block of code. It runs when it's called — not when it's read.

```python
@app.route("/buy", methods=["POST"])   # "when a POST arrives at /buy, run the function below"
def buy():
    …
```

**route** — the code's rule matching a verb + path to a function. The **path** is the address part; the **route** is the rule for it. The API lesson's list — "what you can ask me" — is exactly the app's list of routes.

## Reading the Payload — the Dict Move, in Your Own App

The same label follows the whole trip: the Payload panel's `symbol`, the POST body's `symbol=NVDA`, and inside the function, read by name — the dict move:

```python
@app.route("/buy", methods=["POST"])      # the route
def buy():                                # the function
    symbol = request.form["symbol"]       # the payload, read by name
    …                                     # the work — talks to the database
    return redirect("/")                  # "done — ask over there": POST-redirect-GET
```

Panel → body → code: the same labels at every stop. The names the form gave the values are the names the code asks for. You directed an AI to build this — now you can read it.

## Flask — the Framework Underneath

Nothing in the file reads raw HTTP, matches paths, or assembles responses. Flask does those jobs — ready-made parts, with a real name now:

**framework** — the standard jobs, pre-written. Your code is only routes and decisions; gunicorn holds the port and hands each request in.

| Framework | What it is |
|---|---|
| **Flask** | Python's small one — standard since 2010. Small enough to read whole. |
| **Django** | Python's big, batteries-included one. |
| **Express** | the JavaScript counterpart. |

This is the split behind the job titles: a **back-end** engineer writes the code that receives the data and puts it in the database; a **front-end** engineer builds the UI you click.

## Your Build May Differ — Two Correct Shapes

Each of you built the app with your own Claude — two shapes came out, and both are correct:

| | |
|---|---|
| **The page reloads** | Form POST → redirect → the backend composes **the whole fresh page**. |
| **The page asks for its numbers** | The page stays; its own code sends the request and **JSON comes back** — no redirect. In the Network tab: `fetch/xhr` rows. |

Same backend, same routes, same dict either way. If your take-home screens don't match today's, this is why — not a mistake.

## What's Next

| Today | Next lesson |
|---|---|
| What travels (payload, dict, JSON) and how it rides (GET/POST, query string/body, the form) into a function and a route | Who keeps the answering program running day and night — and the SQL lines inside your routes that talk to the database. |

## After Class

- **Write `order.py`** — the class's dict file, typed by you: make it, read by name, change it, add a pair, and read the `KeyError`. Want your own? Try `car.py` (make, model, year, mileage) — same moves.
- **Open your stock buy's payload** — Network tab, Preserve log ON, one stock buy, the Payload panel. What are YOUR labels? A `fetch/xhr` row instead — your build is the second shape; its payload panel reads the same way.
- **Find your buy route** — in your own code: the `@app.route` line, the `def` line, and the line that reads the payload by name.

**What you know now:** a payload is what a request carries in — key:value pairs, the same shape as a database row. Python's dict reads by name instead of position; JSON is the same shape written as text, so it can travel between programs. GET looks, POST changes something — and what you send rides in the query string or the body, packed by a form's input names. POST-redirect-GET is why refresh doesn't buy twice. Inside your code, a route matches a verb + path to a function, and the function reads the payload by name — the same dict move, on your own app. Flask is the framework underneath; your code is only routes and decisions.

**What you know now:** dynamic means the answer is composed at the moment you ask, from what's true right now. gunicorn runs your Flask code on port 80; Flask is the ready-made parts, gunicorn is the always-on runner. The backend is the half nobody sees, holding the only path to the database. The frontend is what the browser renders — frontend, backend, database make a three-tier setup. An API is the agreed list of requests a program offers other programs — and your app's API is a small list of its own.

---

# Lesson 27 — Who Keeps It Running: systemd, nginx & the Renewed Padlock

## The Bucket Test, One More Time

The menu site could live in an S3 bucket because everything it needs to run, runs in the visitor's browser — HTML, CSS, JavaScript, handed over as-is. The backend is Python, with Postgres beside it. Try the same test on it:

```bash
python3 order.py   # the dict file from the payload lesson, downloaded to a Mac — it runs
```

Uploaded to a bucket instead, that exact same file arrives as plain text — nothing there runs Python. **A running program needs a computer with a runner.** The frontend borrows the visitor's; the backend gets no such loan — it needs its own machine, the EC2 you've been SSHing into all along. Writing the backend in JavaScript wouldn't change this: the browser is still the visitor's machine, and Postgres only answers the one trusted program running beside it.

## Nobody Starts the App

Since the vibe build, nobody has SSH'd in to start your app — not after a reboot, not at 3am — and it answers anyway. Something on the machine starts it and keeps it up. One screen names it:

```bash
sudo systemctl status <the-app-service>   # over SSH, read-only
```

```
● investapp.service — Investment app
     Active: active (running) since Wed 2026-07-01 19:42:03 UTC   ← running since the vibe build
   Main PID: 2481 (gunicorn)                                       ← the process, named right there
     CGroup: /system.slice/investapp.service
             └─2481 /usr/bin/gunicorn --bind 127.0.0.1:8000 app:app  ← the exact command being run
```

Three facts, one screen — and the program showing all this is the one that started it.

## systemd — the Machine's Supervisor

**systemd** — the program that starts the machine's services at boot, tracks them, and restarts them when their settings say so. `systemctl` is how you talk to it. You've already used it without naming it: `sudo systemctl enable --now nginx` in the static-hosting lesson, `sudo systemctl restart nginx` in the HTTPS lesson — same program behind both. Amazon Linux runs it; so do the other big Linux distributions.

## The Unit File — a Service's Settings, Readable

```
/etc/systemd/system/<the-app-service>.service   # read only

[Unit]
Description=Investment app

[Service]
ExecStart=/usr/bin/gunicorn --bind 127.0.0.1:8000 app:app   # the command — the whole mystery in one line
Restart=always                                              # when to bring it back

[Install]
WantedBy=multi-user.target                                  # the rest — settings we don't need today
```

Claude wrote this file during the vibe build; now you can read it. `systemctl is-enabled <the-app-service>` answers whether it starts at boot — the same `enable --now` you typed in the static-hosting lesson is what sets that.

## Live: The Kill Test

```bash
sudo systemctl status <the-app-service>   # read the Main PID
sudo kill -9 <that-pid>                   # end that process now, no cleanup — it dies mid-run
sudo systemctl status <the-app-service>   # status again
```

```
Active: active (running) since … 3s ago
Main PID: 2907 (gunicorn)              ← a different number — systemd started a new one
```

The comeback is the **Restart line's doing** — a unit without that line stays dead until someone runs `systemctl start`. (A refresh mid-restart can fail once; that's the deal.)

## The ExecStart Line, Word by Word

```
gunicorn --bind 127.0.0.1:8000 app:app
```

| Word | What it does |
|---|---|
| `gunicorn` | the runner — the program that holds a port and runs your code |
| `--bind 127.0.0.1:8000` | which address and port to answer on — **this is where the two shapes differ** |
| `app:app` | where the Flask app is — the file, then the app inside it |

On a build where gunicorn still faces the world itself, this same line reads `--bind 0.0.0.0:80`. One word, in one line — the whole difference between the shapes.

## localhost — Two Addresses in the Listener Column

```bash
sudo ss -tlnp
```

```
LISTEN  0.0.0.0:80      users:(("nginx",…))      ← answers anyone
LISTEN  127.0.0.1:8000  users:(("gunicorn",…))   ← only this machine
LISTEN  127.0.0.1:5432  users:(("postgres",…))   ← only this machine
```

| Address | Who can reach it |
|---|---|
| **the public IP** | the world |
| **the private IP** | machines in your VPC — the networking lesson |
| **127.0.0.1 — localhost** | only this machine, talking to itself |

**localhost — 127.0.0.1** — every computer's name for itself. Your Mac has one too; it means "this machine," whichever machine you're standing on.

## Answering Only Your Own Machine Is a Choice

| | Why |
|---|---|
| **Postgres chose 127.0.0.1** | It holds every account's money records — only the app standing on the same machine gets to talk to it. |
| **gunicorn — the same move** | On the shape most builds already have, it sits at `127.0.0.1:8000`; on the other shape it still faces the world itself. |

The target is the same for everyone: gunicorn on the postgres side of that line, with something else taking the front.

## nginx in Front — the Reverse Proxy, Named

The API lesson's aside — some builds show nginx on `:80` forwarding to gunicorn — gets its full name now:

**reverse proxy** — the program in front. It takes every request and passes it to the program behind. A very common shape for real Python sites; gunicorn's own docs say to put a server like nginx in front of it.

| | Job |
|---|---|
| **nginx** | Faces the internet. Many visitors at once, files served fast, the certificate handled in one place. |
| **gunicorn** | Runs Python. Your code, for every request — behind nginx, on 127.0.0.1. |

## The Target, Drawn

Whichever shape a build started as, it ends here:

```
LISTEN  0.0.0.0:80      users:(("nginx",…))      ← the program facing the world
LISTEN  127.0.0.1:8000  users:(("gunicorn",…))   ← the app — inside, beside postgres
LISTEN  127.0.0.1:5432  users:(("postgres",…))   ← made this move on day one
```

If yours already reads this way, nothing to change — Claude built it during the vibe build. If gunicorn still answers `0.0.0.0:80` directly, one ask fixes it: tell Claude, on the server, to put nginx in front of gunicorn on an inside-only port. The handing rule inside nginx's settings is typing nobody does by hand anymore — knowing the shape, and reading the proof, is the engineering.

## HTTPS, Refreshed — What the Padlock Promises

HTTPS is HTTP with **encryption switched on** — nobody between the browser and the server can read or change what passes. The HTTPS lesson turned it on once, by hand. Two questions settle what actually happened: what switches the encryption on, and why should a browser believe this server is the right one?

## Two Keys, Made as a Pair

SSH already works this way — the `.pem` file on your Mac, and its other half on the server:

| | |
|---|---|
| **the private key** | Stays with its owner — never shared, never travels. |
| **the public key** | Handed to anyone. Made together with the private one: what one locks, only the other opens. |

```
privkey.pem     ← the server's private key — never leaves the server
fullchain.pem   ← the certificate — carries the public key, handed to every visitor
```

The two files the HTTPS lesson had you carry into place, finally read for what they are.

## The Certificate and the Authority

**the certificate** — the server's public key plus its name, signed. Who signed it is the whole point.

**certificate authority — CA** — a company every browser already trusts; browsers ship with a short list of them. The deal: prove the name is yours, and the CA signs. From then on, every browser believes the signature. **Let's Encrypt** is the free CA behind the HTTPS lesson's certificate; **certbot** is the program that proves the name and asks the CA to sign.

The whole visit, in four stops: the browser asks the server to prove itself; the server hands over the certificate; the browser checks the name matches and the signer is on its trusted-CA list; the padlock goes on — only the private key's holder can finish the handshake. The private key never travels. That's the whole trick.

## Live: HTTPS Back

With nginx already answering on port 80 at the domain's address, certbot can prove the name and write the config right there:

```bash
curl http://<your-domain>/                              # confirm your domain still answers this server
sudo apt install certbot python3-certbot-nginx           # Ubuntu — on Amazon Linux: sudo dnf install certbot python3-certbot-nginx
sudo certbot --nginx -d <your-domain>                    # proves the name on port 80, writes the config itself
```

```
listen 443 ssl;
ssl_certificate     /etc/letsencrypt/live/<your-domain>/fullchain.pem;   ← the key pair, placed by certbot this time
ssl_certificate_key /etc/letsencrypt/live/<your-domain>/privkey.pem;
+ a block sending http → 301 → https
```

Confirm port 443 is open in the security group first — the HTTPS lesson opened it; check it's still there, add it if not. The browser shows the padlock again, and `curl http://` now answers **301** — the redirect you can read.

## Renewal — the Machine's Job Now

Certificates are short-lived on purpose — about three months. Left alone, that means a person has to remember to renew one. certbot ships the fix as a **timer**, systemd's version of the cron job your news bot runs — but it arrives switched off:

```bash
sudo systemctl enable --now certbot.timer   # the command you know — switches it on
# certbot-renew.timer on Amazon Linux instead — systemctl list-timers shows which one you have
```

```
NEXT                        LEFT      UNIT               ACTIVATES
Thu 2026-07-23 03:14:00     11h       certbot.timer      certbot.service   ← checks and renews before it runs out
```

Renewal belongs to the machine now — the same supervisor, running a scheduled job.

## What's Next

| Today | Next lesson |
|---|---|
| Who keeps the answering program running (systemd, the unit file), the reverse-proxy shape, and HTTPS turned on and renewed on the server itself | The SQL your app runs, caught live in the database's own log — and the connection string that ties app to database. |

## After Class

- **Find how YOURS is kept running** — the service, the unit file, the ExecStart line. Builds vary — read what yours says before changing anything.
- **Which shape is yours?** `sudo ss -tlnp`. Already nginx in front of gunicorn: nothing to change. Still gunicorn facing the world: ask Claude to put nginx in front on an inside-only port, then re-run the same `ss` to see the target.
- **Domain → certbot → timer** — point your A record at your server if it's drifted, run certbot with the nginx plugin, enable the renewal timer, and finish with the padlock and `sudo ss -tlnp`.

**What you know now:** a running program needs a computer with a runner — the backend can't live in a bucket the way the frontend can. systemd is the machine's supervisor: it starts services at boot from a unit file, tracks them, and restarts them when the file's `Restart` line says so — `systemctl status` reads all three facts back. localhost, 127.0.0.1, is every computer's name for itself; Postgres and, on most builds, gunicorn answer only there, on purpose. nginx in front of gunicorn is a reverse proxy — one program facing the internet, the other running your Python behind it — and whichever shape a build started as, both end at the same `ss` output. HTTPS runs on a key pair made together, a certificate that carries the public key and a name, and a certificate authority the browser already trusts to have checked that name; running certbot on the server itself, instead of by hand, lets it prove the name and write the nginx config on its own — and a systemd timer, not a person, keeps the certificate renewed.

---

# Lesson 28 — Going Deeper on the Database, and the Move Begins

## Five Separate Topics, Not One Story

In the last database session you queried the database by hand. Tonight is the next five things — **not one story, five different topics**, taken one at a time: logging, SQL injection, how the app connects, migrations, and the rules for money data.

| # | Topic | What it is |
|---|---|---|
| 1 | **Logging** | the record of every query the database runs |
| 2 | **SQL injection** | a security hole, and how to close it |
| 3 | **Connecting** | how the app reaches the database |
| 4 | **Migrations** | how the tables got their shape |
| 5 | **Money data** | the rules that keep a ledger correct |

## Live: The Database Can Record Every Query

**log** — a running record written to a file as things happen. Recording every query is **off by default** — one setting turns it on:

```bash
sudo -u postgres psql -c "ALTER SYSTEM SET log_statement = 'all'"   # write down every statement
sudo -u postgres psql -c "SELECT pg_reload_conf()"                  # make Postgres re-read its settings
sudo tail -f /var/log/postgresql/postgresql-*.log                  # follow the log as it's written
# (then click a page in the app)
```

```
LOG:  statement: SELECT * FROM quote_cache …   ← the click, as the database saw it
```

The app is just **another client** — it sends the same kind of `SELECT` you typed by hand, over the same port 5432. Open the app's code at that line and you'll see the exact query.

You won't read logs this way at work — nobody SSHes in to `tail` a file. The logs ship somewhere you can search by time and filter instead: **Datadog**, CloudWatch Logs, Grafana, Dynatrace. Your company picks one and you learn that one. Same lines underneath, same job: something broke an hour ago — go back an hour and look.

## SQL Injection — Your Text, Glued Into a Sentence

When you search for a stock, the app glues what you typed into a ready-made SQL sentence, and sends the whole line to the database:

```
you type:       AAPL
the app sends:  SELECT * FROM companies WHERE symbol = 'AAPL'
```

The database receives **one line of text**. It cannot tell which part the app wrote and which part you typed — it just reads the sentence. Your text is supposed to sit **between the quotes**, as plain data. So what happens if your text **contains a quote**?

## Live: One Line Returns Every Row

```
you type:       ' OR '1'='1
the app sends:  SELECT * FROM companies WHERE symbol = '' OR '1'='1'
```

Your first quote pairs up with the app's opening quote — the data ends early, and the rest of your text is read as **SQL commands**:

| Piece | Reads as | Why |
|---|---|---|
| `symbol = ''` | matches nothing | "symbol equals empty text" — true for no row |
| `OR` | …or… | either side being true is enough |
| `'1'='1'` | always true | 1 equals 1, on every single row — so **every row matches** |

That's **SQL injection**: what you typed stopped being data and became part of the command. The search box just handed back the whole table.

## The Fix — Give the Input to the Database Separately

Don't paste the input into the sentence. Leave a **blank** — a placeholder, written `%s` — and pass the value as a **separate argument**:

```python
cur.execute("… WHERE symbol = %s", (user_input,))
```

The sentence and your text arrive **separately**, so the database always knows which is which — a quote you type stays a plain character and can never end the sentence. That comma is the whole habit.

**parameterized query** — the value goes in through a placeholder, so it can never become part of the SQL.

Fixing this day to day is **developer work, not ours**. A platform engineer needs to know how it works and what it can cost — and when you build something yourself, ask Claude to check it for SQL injection.

## Is Our App Safe?

Open the search query in our app's code and compare it to the two shapes:

| Shape | Looks like |
|---|---|
| **Unsafe** | the input pasted straight into the sentence — `"… = '" + user_input + "'"` |
| **Safe** | a placeholder, value passed separately — `"… = %s", (user_input,)` |

If it's the safe shape — good, and now you know why. If it's the unsafe one, **you just found a real bug**, and you know exactly what to ask Claude to change.

## The Connection String

When you connect by hand, you hand `psql` the facts one flag at a time:

```bash
psql -U app_user -d investapp -h localhost   # -U who · -d which database · -h which machine
```

The app needs the same facts, but as **one line**:

```
postgresql://app_user:…@localhost:5432/investapp
```

| Piece | Role | What it means |
|---|---|---|
| `app_user:…` | who | a database user + password; the `…` hides the real password |
| `localhost` | which machine | where the database is — today, this same server. On RDS this is a long AWS **endpoint** instead |
| `5432` | which port | Postgres's port |
| `investapp` | which database | the named database on that server |

It lives in a config file or an environment variable — wherever the build put it. Keep this: when the database moves to its own server, **exactly one of these four changes.**

## Migrations — the Tables' Build History

Someone created these tables — the columns, the types. Not by hand on the live database. It was written down as **numbered files, run in order**, each one a single change to the database's shape:

```
migrations/
  001_create_companies.sql        step 1: the companies table
  002_create_transactions.sql     step 2: the ledger
  003_…                           run in order, once each, on every copy of the database
```

**migration** — a change to the database's structure, written down as an ordered, repeatable step.

Ours doesn't have this folder. Claude built our tables the quick way — straight into Postgres as it went. That's fine for a one-off; it's not how a team ships a change to a live database. Not your job to write them — just don't be surprised by the folder, and know the question: **ask Claude how your tables got their shape.**

## The Rules for Money Data

The list of every deposit, buy, and sell is called a **ledger**. Ledgers follow rules banks have used for centuries — how mistakes are handled, whether anything is deleted, and where your balance is kept.

## A Ledger Never Deletes

You bought the wrong stock. Why not just delete that row, or edit it? A ledger doesn't:

| id | symbol | shares | amount | |
|---|---|---|---|---|
| 4183 | NVDA | 2 | -262.52 | the wrong buy — left in place |
| 4184 | NVDA | -2 | +262.52 | a new row that cancels it out |

| Term | Meaning |
|---|---|
| **append-only** | rows are only ever added — a fix is a new row, not an edit |
| **soft delete** | to remove something, mark it removed — the row stays |

Why: **an edited past can't be checked.** Every bank works this way. Does ours? A build that edits or deletes old rows is a real finding.

## The Balance Is a Sum, Not a Stored Number

```
Deposit +1,000 → Buy 2 shares @ $100, −200 → add them up: 1,000 − 200 = $800
```

A bank keeps **no saved balance**. The number is **added up from the ledger every time it's asked** — arithmetic you could do on paper. A stored copy is a second version of the truth that can drift from the rows.

## Live: The SUM

One new word, and it's the adding-up you just did on paper:

```sql
SELECT SUM(amount) FROM ledger;
```

| Piece | Role |
|---|---|
| `SELECT SUM(amount)` | `SUM` = the paper arithmetic, in one word |
| `FROM ledger;` | every line, deposits and buys — your build's name may differ |

Run it — three numbers on one screen: the paper number, the query's number, the number on the app's page. **All three agree.** The balance is computed, not stored.

## Where One Query Actually Goes

The first half you already own: phone → DNS → internet gateway → subnet → security-group check → nginx on 443 → gunicorn → the app. Today it gains its last leg — the app sends its SQL query, with its own name and password (the connection string), through port 5432, to Postgres, whose data folder sits on the EBS disk, where the buy's row lands.

Today it all lives on **one server**, so the query never leaves the machine. Change the endpoint in that connection string, and it would — which is exactly what's next.

## Part 2: Give the Database Its Own Server

Right now the database shares a machine with the app. This is a **two-class move**, always safe to stop at: tonight got through Steps 1–5; the class after this one finishes it, starting from the wall hit at the end.

## Why Move It At All

`sudo ss -tlnp`, the command from the hosting chapter, shows three programs sharing one machine:

| Program | Job |
|---|---|
| **nginx** | serves the website to the internet |
| **gunicorn** | runs the app's code |
| **postgres** | holds the money records (the database) |

- **They slow each other down** — one machine's CPU and memory, split three ways. If nginx gets busy, it takes the food off the database's plate.
- **The website is open to the internet** — so this machine is too. The database holds everyone's money records — it shouldn't sit on a machine the internet can reach.

And they all fall together: one machine breaks, everything is down. Give the database **its own machine** — its own CPU and memory, and one that can be **closed off from the internet.**

## The Plan — One Tier to Two

A second machine, just for the database — the app server (nginx, gunicorn, the app) stays in its public area; a second server, in a private area of the network, holds only postgres. The app reaches postgres over the network on port 5432.

**One-tier** — everything on one machine, the setup we started with. **Three-tier** — front end, back end, and database each on their own machine, the shape you'll hear named at work. Tonight goes from one tier to two; the database is the piece that moves.

A word to watch: moving a database like this is also called **migrating** it — not the same as the migration files (the tables' change history) from earlier. Same word, two meanings.

From your phone to the app, **nothing changes**. The only difference is that the app's database now lives on a different machine.

## Live, Step 1: Back Up the Database

```bash
sudo -u postgres psql -l                             # list the databases on this machine — yours may not be called investapp
sudo -u postgres pg_dump investapp > investapp.sql
```

That makes one file with every table and every row. It does **not** include the database logins — the usernames and passwords allowed to connect. Those get created by hand on the new server. Never change a database without a backup first.

## Live, Step 2: Make the Subnet

A **subnet** is a section of your private network. Make a new one in the **same VPC as your app server** — they have to be able to reach each other. Three things to get right:

| Setting | What to do |
|---|---|
| **Address range** | cannot overlap an existing subnet — try `172.31.0.0/20`, and if it says it overlaps, walk the number up (16, 32, 48…) until it takes |
| **Auto-assign public IP** | **leave it off** — a machine here should have a private address and nothing else |
| **Availability zone** | pick the same one your app server is in — same building, shorter trip, no cross-zone charge |

The subnet exists now — but it is **not private yet**. It was born attached to the VPC's main route table, and that table has a way out to the internet. Next step fixes that.

## Live, Step 3: Give It a Route Table of Its Own

The main route table sends anything not local out through the internet gateway — that row is what makes the default subnets public. So make a **new route table**, leave that row out, and **associate it with the new subnet**. The new table has one row only: `local` — traffic inside the VPC's own address block stays inside. No internet row. That one absence is what private means.

Check the wiring in the VPC console's **Resource map** — every subnet, and the route table each one follows, drawn in one picture. Your new subnet should be on its **own line, to its own route table.** If it's still drawn to the main one, the association didn't save — and the subnet is still public.

Nothing routes out of this subnet now. That is **exactly what we want** — and, in a few minutes, exactly what stops us.

## Live, Step 4: Launch the Server, With the Right Firewall

Launch it like any other EC2 instance — the one thing that matters is choosing the **new subnet** under Network settings, and the **same key pair** you already use. Give it a security group of its own:

| Type | Port | Allowed from |
|---|---|---|
| PostgreSQL | 5432 | the app server's security group |
| SSH | 22 | the app server's security group |

The source is **a security group, not an address.** Any machine in that group may connect; nobody else — not the internet, not your laptop. Addresses change when a server restarts; the group doesn't. Watch the region you're in when you go looking for that group — the wrong region shows a stranger's-looking list and the launch fails.

## Live, Step 5: Reach It in Two Hops

It has no public address, and its firewall lets SSH in from the app server only — so your laptop cannot reach it. You go **through** the app server:

```bash
# your laptop — once: put the key on the app server, hop 2 needs it
scp -i key.pem key.pem ubuntu@<app-public>:~
# hop 1 — into the app server, as always
ssh -i key.pem ubuntu@<app-public>

# app server — hop 2, over the private network (ubuntu@ or ec2-user@, whichever image you chose)
chmod 400 key.pem
ssh -i key.pem ubuntu@<db-private-ip>
```

The app server is the one machine on **both sides**. Leaving your private key on it is a real smell — a later class shows the version with no key to copy.

## Where We Stopped, and What Stopped Us

| Step | Status | What happened |
|---|---|---|
| The backup | Done | One `.sql` file on the app server, with every row |
| The private subnet | Done | Its own route table, no way out to the internet |
| The server, reachable | Done | Launched inside it, firewalled to the app server, two hops in |
| Install Postgres | **Stuck** | `apt update` hangs at 0%. Nothing to download from |

A brand-new server is an empty machine. To put Postgres on it, it has to fetch Postgres — and we just took away every road out.

## What's Next

| Today | Next lesson |
|---|---|
| Logging, SQL injection, the connection string, migrations, and the money rules for a ledger — then the database move begun: backup, private subnet, its own route table, a firewalled server, and two-hop SSH in — stopped at an empty machine with no way out to install anything | Why the obvious fix doesn't work, what a NAT gateway is, and building one; then installing Postgres, opening it to the network, copying the backup across, restoring it, and pointing the app at the new server |

## After Class

- **Find how YOURS does it** — the query log, your connection string's four parts, your search query's safety, and how your tables got their shape. Table and file names differ across builds — every step starts with "find how mine does it."
- **Turn on the query log** — the same one setting as in class — and watch a click arrive. Find your connection string and read its four parts.
- **The security check** — find your search query in the code. Safe placeholder, or pasted-in input? Either answer is a win — if it's unsafe, tell Claude to fix it and check again.
- **The money rules** — ask Claude how your tables got their shape. Then run the `SUM` on your ledger and check: does your build store a balance, or compute it?

**What you know now:** a database log records every query, off by default until one setting turns it on — the app is just another client sending the same kind of `SELECT` you'd type by hand. SQL injection happens when user input is glued straight into a SQL sentence instead of passed as a separate, parameterized argument — one habit, one comma, closes the hole. The connection string carries the same four facts `psql` takes as flags — who, which machine, which port, which database — and moving the database changes exactly one of them. Migrations are the tables' ordered, repeatable build history, kept separate from the live database's day-to-day changes. A ledger is append-only — mistakes are corrected with a new row, never an edit or delete — and a real balance is summed fresh from the ledger every time, never stored. Moving the database off the app server means a new private subnet with its own route table and no internet route, a firewalled second server reachable only through the app server in two SSH hops — and an empty machine that, once sealed off from the internet, has no way yet to fetch the software it needs.

---

# Lesson 29 — Finishing the Database Move: NAT Gateway, Restore & Cutover

## Where We Left Off

Last class got the new database server built, private, and reachable — then hit a wall. `sudo apt update` sat at 0% forever:

| Step | Status | What happened |
|---|---|---|
| The backup | Done | One `.sql` file on the app server, with every row |
| The private subnet | Done | Its own route table, no way out to the internet |
| The server, reachable | Done | Launched inside it, firewalled to the app server, two hops in |
| Install Postgres | **Stuck** | `apt update` hangs at 0%. Nothing to download from |

A brand-new server is an empty machine. To put Postgres on it, it has to fetch Postgres — and the private subnet took away every road out. Tonight starts by explaining that wall, then finishes the move: install, open it to the network, copy the backup across, restore it, point the app at it, and seal the server back up.

## Two Walls, and the Obvious Fix Only Clears One

```
$ sudo apt update
0% [Connecting to archive.ubuntu.com]     … and it sits there. No error. Just nothing.
```

Everyone tries the same fix first: put the internet row back in the route table. It doesn't work, and the reason is worth keeping. There are **two** walls, not one:

| Wall | What it is | Why the fix doesn't clear it |
|---|---|---|
| 1. The route table | No internet row, so nothing addressed outside the VPC has anywhere to go | Adding the row back is the "obvious fix" — but it still isn't enough |
| 2. The internet gateway | Only carries traffic for a machine that **has a public address** | Our database server has none, on purpose — the gateway has nothing to hand the answer back to |

**An internet gateway only carries traffic for a machine with a public address.** Ours has none. That's what a NAT gateway is for.

## Two Ways Out

| Option | How it works | Trade-off |
|---|---|---|
| **NAT gateway** (the real answer) | A box in a *public* subnet that makes outbound calls on the private server's behalf. The server keeps its private address and stays unreachable from outside | About 4.5¢/hour for the gateway + a public address + 4.5¢/GB — roughly $36/month if left running (~$33 of that is the gateway alone). Every part-hour bills as a full one, so a class costs pennies: create it, install, delete it. At a real job you leave it running — an hour of engineer time costs more than a month of gateway |
| **A public address for a few minutes** | Give the database server an Elastic IP, put the internet row back, install, then take both away | Cheaper, and it works — but adding that row is *the definition of a public subnet*. For those minutes the database server is a machine on the internet with only its firewall in the way. Undo **two** things, not one: release the address **and** delete the `0.0.0.0/0` row — dropping the address alone still leaves the subnet public for the next thing launched in it |

We build the NAT gateway — it's what you'll meet at work, and it's the honest answer to "how does a private server get updates?" Then we delete it, because ours never needs the internet again.

**NAT gateway** — a one-way door out of a private subnet. The private server *starts* a connection out (an update, a download) and the answer comes back on it; nothing outside can start a connection in. That asymmetry is the whole point.

## Live, Step 6: Build the NAT Gateway

Three fields, in a **public** subnet — any default subnet, not the database's:

| Field | What to put |
|---|---|
| Subnet | a **public** one — not the database's private subnet |
| Connectivity | Public |
| Elastic IP | Allocate a new one — the door's own public address |

Then one row in the **database subnet's** route table — everything not local goes to the NAT gateway, not the internet gateway:

| Destination | Target |
|---|---|
| `172.31.0.0/16` | local |
| `0.0.0.0/0` | `nat-…` — the NAT gateway |

Wait for **Available**, then run `sudo apt update` again — it moves. Note to self: delete this later. It bills whether you use it or not.

## Live, Step 7: Install Postgres, Create the Login and Database

Same install as the database chapter — match the **major version** to the app server, or the backup won't load. Then create the login and database by hand; the backup file doesn't carry them:

```bash
psql --version                                              # check the app server's version first — match it here

# Ubuntu:
sudo apt update && sudo apt install -y postgresql
# Amazon Linux (15/16/17/18 also offered — match the app server):
sudo dnf install -y postgresql18-server
sudo postgresql-setup --initdb                              # Amazon Linux only — Ubuntu does this for you

# both, once Postgres is installed:
sudo -u postgres createuser --pwprompt app_user             # --pwprompt = ask you to type its password
sudo -u postgres createdb -O app_user investapp             # -O = owned by app_user · yours isn't called investapp
```

Use the **same username, password, and database name** as the old server — then the app barely notices the move. You can read all three out of the app's connection string.

## Live, Step 8: Tell Postgres to Answer the Network

A fresh Postgres only answers its own machine. Two settings change that:

```bash
sudo -u postgres psql -tAc 'SHOW config_file; SHOW hba_file;'   # find both files — works on any distro, any version
```

```
# in postgresql.conf — answer on the network, not just this machine
listen_addresses = '*'

# in pg_hba.conf — network logins: this database, this user, any address, password required
host  investapp  app_user  0.0.0.0/0  scram-sha-256
```

```bash
sudo systemctl restart postgresql       # the files are read at start — restart to load them
```

From **any** address?! Yes — **where from** is the firewall's job (Step 4: only the app server's security group). Postgres checks **who**: the right user and password. Two separate guards, both have to say yes — and it's how RDS, AWS's managed database, is set up too.

### The Gotcha: First Match Wins

`pg_hba.conf` is read top to bottom, and the **first** matching rule wins — the rest are never looked at. Two lines ship with Postgres, above wherever you add yours:

```
local  all  all                peer
host   all  all  127.0.0.1/32  ident
# ↓ yours, added at the end of the file — never reached
host  investapp  app_user  0.0.0.0/0  scram-sha-256
```

```
FATAL: Ident authentication failed for user "app_user"
```

That message says *authentication* — so the instinct is to go check the password again, and the password was never the problem. Move your line **above** the two shipped ones and the same password works at once. (Ubuntu calls the second-line method `peer`, Amazon Linux calls it `ident` — same wall.) **When a rule looks ignored, read what sits above it.**

## Live, Step 9: Copy the Backup Across

The backup from Step 1 (`investapp.sql`) is still sitting on the app server — the new server has never seen it. Copy it over the private network with `scp`, the same command that put the SSH key there, pointed the other way:

```bash
# app server — check the file first (named after YOUR database, not investapp)
ls -lh investapp.sql
scp -i key.pem investapp.sql ubuntu@<db-private-ip>:~   # ec2-user@ instead of ubuntu@ on Amazon Linux
```

Read it as a sentence: `scp` — copy over ssh · `-i key.pem` — with this key · `investapp.sql` — this file · `ubuntu@<db-private-ip>:~` — to that user, on that machine, in their home folder. The `:` is what makes it a remote copy instead of a rename.

Private address, private network — this file never touches the internet. Check it landed: `ls -lh ~` on the database server, same size as before.

## Live, Step 10: Restore, Then Count the Rows on Both

`count(*)` means "how many rows." Ask the old database, then ask the new one **over the network** — the numbers have to match:

```bash
# database server — load the file just copied over
psql -U app_user -d investapp -f investapp.sql
# and let the app's user use what it just created
GRANT ALL ON ALL TABLES IN SCHEMA public TO app_user;
```

```bash
# app server — the old database, the ledger
psql -d investapp -c "SELECT count(*) FROM ledger;"
# → 1247

# now the new server, over the network, as app_user
psql -h <db-private-ip> -U app_user -d investapp -c "SELECT count(*) FROM ledger;"
# → 1247
```

That second command is the first time the app server has ever talked to the database over a network. If it answers, the firewall rule and both Postgres settings are right. **Same number of rows — nothing was lost.**

## Live, Step 11: Point the App at It

The connection string has four parts. Only **one** changes — the address (the **endpoint**), from `localhost` to the new server's private address:

```
postgresql://app_user:…@<db-private-ip>:5432/investapp
```

```bash
sudo grep -rl DATABASE_URL /etc /opt /srv /home 2>/dev/null   # find the file that holds it
# common answers: /etc/<app>.env · /opt/<app>/.env · beside the app's .py file
sudo systemctl restart gunicorn                                # or whatever your app's service is called
```

You almost certainly do not edit Python code here. A well-built app reads the connection string from a file outside the code — that's why the password was never committed to Git. Look for the `.env`-style file, not the address inside `app.py`.

Restart the app, then make a **real buy on the live site** — it works. The old database is still running on the app server, untouched — that's the way back if anything's wrong.

## Live, Step 12: Close the Way Out

Postgres is installed; the database never calls out again. Delete the `0.0.0.0/0` row from the database subnet's route table, and **delete the NAT gateway** — it charges by the hour whether anything uses it or not. Release its Elastic IP too.

```bash
curl -m 5 https://example.com    # worked a minute ago — now it times out
```

Cost check before closing the laptop: NAT gateway deleted, Elastic IP released, **in that order** — the address is separate from the gateway that held it, the button is called *Release* rather than Delete, and it stays greyed out until the gateway finishes deleting. Wait a minute, then release.

And the website still works — **a buy never needed that route.** The only traffic the database server does is answer the app.

## You Try It: Can Your Laptop Reach the Database?

No — the server has no public address to even aim at. `nc` asks one question: "can I open a connection to this machine, on this port?"

```bash
# Mac — -vz = just check, send nothing · -G 5 -w 5 = timeouts, give up after 5 seconds
nc -vz -G 5 -w 5 <db-private-ip> 5432        # → times out

# Windows (PowerShell) — same question, one command
Test-NetConnection <db-private-ip> -Port 5432   # → failed

# the same ssh that worked from the app server:
ssh -i key.pem ubuntu@<db-private-ip>           # → times out
```

Note: not `ping` — it speaks ICMP, which no rule here allows, so it fails even where things do work; it's not a reliable test.

Straight to the database: no way in. Yet the site still loads — **the app talks to the database for you.** Nobody else can.

## Logging In Later: the Jump Host

Through the app server — the same two hops as Step 5. The pattern is common enough to have a name and a shortcut:

**jump host** (or **bastion**) — a machine you're allowed to reach, that you connect *through* to reach one you can't reach directly. Here: the app server.

```bash
ssh -i key.pem -J ubuntu@<app-public> ubuntu@<db-private-ip>
```

`-J` = "jump via" — both hops in one command, **and no key left on the app server.** Delete the copy you put there in Step 5.

At a real job, a bastion is a machine of its own, not your app server, and a small team holds the keys. Increasingly it's no machine at all — AWS **Session Manager** opens a shell from the console with no key and no open port 22.

## Why That Order

Every step was safe to stop at:

- Backed up **before** touching anything.
- Created the login on the new server **before** the restore needed it.
- Counted the rows on both databases **before** pointing the app anywhere.
- Left the old database running until a **real buy** proved the new one works.
- Made **one change at a time**, checking after each.
- Closed the way out **last** — only after everything worked.

We stopped in the middle of this move for two days and nothing broke, because every stopping point was a safe one. **That's how you change something people depend on.**

## And at a Real Job

| Path | What it looks like |
|---|---|
| **Keep splitting: three tiers, three teams** | Split once more — nginx on one machine, the app on another, the database on a third — and you have the **three-tier** shape most older systems still run. The reason is people, not computers: front-end, back-end, and database each get owned by a different team, and each can deploy without waiting on the other two |
| **Or hand the machine back: RDS** | AWS runs the database server for you — you pick the engine and size, they patch, back up, and restore. Every step done by hand tonight becomes a button (*restore to point in time* instead of `pg_dump` + `scp` + reload). You never SSH in, because there's nothing to SSH into. It costs more; companies pay it because an engineer's hours cost more still |

So why do it the hard way once? Because **the buttons only mean something if you know what they replace.** You moved a live database without losing a row — when RDS does it for you, you'll know exactly what it did.

## One Buy, End to End

The full path a buy takes now: phone → DNS → internet gateway → public subnet → firewall check → nginx on 443 → gunicorn → the app — all on the app server. Then the app sends its query **over the network** into the private subnet: through the database's firewall, port 5432, to Postgres on its own server, where the buy's row is saved to disk.

You can now follow one buy the whole way, and name every machine it passes through.

## After Class

Optional practice and Q&A — less structured, working through the move on your own build with the instructor:

- **Do the move on your own server** — billing alarm first, and delete the NAT gateway when you're done.
- **Find how yours does it** — your own database name, table names, and connection-string file differ from the demo; every step starts with "find how mine does it."
- **Confirm the two-guard model** — check that your database server's security group source is a security group, not an address, and that `pg_hba.conf` matches your app's actual user and database name.
- **Practice the jump host** — reach the database server with `ssh -J` in one line, and confirm no copy of your key was left behind on the app server.

**What you know now:** a private subnet with no internet route blocks outbound traffic in two places, not one — the missing route row, and the internet gateway's refusal to carry traffic for a machine with no public address — and a NAT gateway is the one-way door that fixes both without giving the server a public address of its own. Installing Postgres on the new server means matching the app server's major version and recreating the login and database by hand, since a backup file carries rows but not logins. `pg_hba.conf` is read top to bottom and stops at the first match, so a new rule has to sit above the shipped defaults or it's silently never reached. The whole move — backup, subnet, route table, server, firewall, NAT gateway, install, restore, cutover, teardown — was staged so every stopping point left a working system, with the old database left running until a real transaction proved the new one worked. A jump host (or bastion) is how you reach a machine with no public address at all, `-J` collapses the two hops into one command, and at a real job that role is either its own guarded machine or replaced entirely by AWS Session Manager, which needs no key and no open port.

---

# Lesson 30 — Many Engineers, Same Code: Branches, Pull Requests & Conflicts

## The Situation

You change line 5 of a file. At the same time, somebody else changes line 40 of that same file. You both save. You both send it. What happens to their work? What happens to yours?

Everything you've done in Git so far, you did alone in your own repo — this question never came up. Tonight it does, because one file — `index.html`, the class menu page — belongs to the whole class. Everybody is allowed to send changes to it, and one part of it is marked with your name. You change **your** part; somebody else changes theirs. So the file gets changed by many people on the same day, in different places inside it. Hold on to that — it's the whole reason today exists.

## Six Commands You Already Have

A refresh, not a re-teach:

| Command | What it does |
|---|---|
| `git status` | What changed |
| `git add` | Pick what to save |
| `git commit` | Put one save into Git's memory |
| `git push` | Send your saves to GitHub |
| `git clone` | Copy a repo that already exists |
| `git pull` | Bring down saves you don't have |

**A repo** is a folder Git is watching, plus every save it remembers for it. Access comes before the clone — check you're let in before you copy anything:

```bash
git ls-remote git@github.com:312school/class-menu-page.git
# a list of long codes           → you're in
# Permission denied (publickey)  → no working SSH key yet

git clone git@github.com:312school/class-menu-page.git
```

**Permission denied means no working SSH key.** Being in the organization isn't enough on its own — that's a trip to the unstuck ladder, not a sign the clone command is wrong.

## Why a Shared Push Fails

Your saves sit in a line, and that line has a name: `main`. Every `git commit` adds one save to the end of it. In the Git lesson, that line belonged to you alone. Here, it belongs to everybody in the class.

Engineer one changes a line and sends it — nothing new, exactly what you already do:

```bash
git commit -m "Raise the coffee price"
git push
# To github.com:312school/class-menu-page.git
#    2bcda9a..4e77d90  main -> main
```

`main` on GitHub now has one more save than before. Engineer two changes a **different** line and tries the same thing:

```bash
git commit -m "Raise the tea price"
git push
#  ! [rejected]        main -> main (fetch first)
# error: failed to push some refs to 'github.com:312school/class-menu-page.git'
# hint: Updates were rejected because the remote contains work that you do not
# hint: have locally. This is usually caused by another repository pushing to
# hint: the same ref.
```

| What Git says | What it means |
|---|---|
| `(fetch first)` | Nothing was sent. Get GitHub's saves first |
| `the remote contains work that you do not have` | GitHub's `main` has a save your copy has never seen |

They changed a **different line** — so this isn't the content clashing. The line of saves simply moved while they were working. That's a different problem from a conflict, and it needs a different fix: branches.

## Branches — the One New Idea

A branch is a second line of saves, with its own name. It **starts from the save you're on** — everything before that point it shares with `main`. Your next `git commit` goes onto your line, not onto `main`. And `main` doesn't move while you work — `main` **is a branch too**, just the one that was already there.

A branch is not any of these three things people assume:

- **Not a new folder.** You still have one folder, with one `index.html` in it.
- **Not a backup.** A branch protects nothing; `commit` and `push` do that.
- **Not a separate repo.** Same repo, same GitHub, same saves underneath.

So what is it? A name for where your next saves go. Git puts the files for whichever branch you're standing on into your one folder, and swaps them when you switch. Git's own word for the branch you're standing on is `HEAD`.

```bash
git switch -c color-fix
# Switched to a new branch 'color-fix'

git branch
# * color-fix
#   main
```

`-c` means **create** — make the branch, then stand on it. The `*` marks the branch you're standing on. You'll also see `git checkout -b color-fix` — the older name for the same thing, and still what a lot of people type. `git switch` came later to make this one job clearer.

Your one folder shows one branch at a time:

```bash
git commit -m "Make the heading green"   # a save on color-fix

git switch main        # refresh the page → the green is gone
git switch color-fix   # refresh again      → the green is back
```

Nothing was lost either time — both versions are saved, you're just looking at one, then the other. Git prints the same history in the terminal:

```bash
git log --oneline
# 9c2f1ab (HEAD -> color-fix) Make the heading green
# 4e77d90 (origin/main, main) Raise the coffee price
# 2bcda9a Sections: only active students
```

| Term | Meaning |
|---|---|
| `HEAD` | Git's word for the branch you're standing on |
| `origin/main` | GitHub's `main`, as your machine last saw it |

Adding `--graph --all` draws the two lines as branching text — it's noisy on a real repo, and nothing later needs it. `--oneline` is the one worth keeping.

## Pushing a Branch

Until you push it, nobody else can see it. Before the push, `color-fix` exists only in the folder on your machine, next to `main` — GitHub has `main` only. `git push -u origin color-fix` sends it up:

```bash
git push -u origin color-fix
# remote: Create a pull request for 'color-fix' on GitHub by visiting:
# remote:      https://github.com/312school/class-menu-page/pull/new/color-fix
# To github.com:312school/class-menu-page.git
#  * [new branch]      color-fix -> color-fix
# branch 'color-fix' set up to track 'origin/color-fix'.
```

`origin` is the name your folder uses for "the copy on GitHub" — set when you cloned. `-u` links your branch to the one on GitHub, so after this, `git push` on its own is enough. The branch now exists in both places, and GitHub noticed — it's already offering the next step.

## Pull Requests and Reviews

A **pull request** asks for your branch to go into `main`. In plain words: here is my line of saves, please add it to `main`. It's a page on GitHub where the change can be looked at and talked about *before* it goes in — and nothing enters `main` until somebody presses **Merge**.

```
Pull requests → New pull request
base: main   ←   compare: color-fix
Title + description: what changed, and why
→ Create pull request
```

Each pull request covers one person's own part of the page, so nobody waits on anybody to open theirs. Opening it notifies nobody in practice — copy the link into the team channel and ask, and ask politely: text carries no tone, and "can you please review this" reads very differently from "review this."

A pull request can target any branch, not only `main` — teams often aim at a shared release branch. Branch names at work follow a pattern too: `fix/coffee-row`, `feat/add-cake-row` — a short prefix, then what the change does.

Git and GitHub are two different things with similar names:

| | What it is |
|---|---|
| **Git** | The program on your machine. It saves versions and makes branches. Works with no internet and no account |
| **GitHub** | A company that keeps repos for you. It adds the web page, who's allowed in, reviews, and the pull request |

Git itself has no pull requests at all — the service adds them, and each one uses its own word for it: GitHub and Bitbucket say **pull request**; GitLab says **merge request**.

A **diff** is the list of lines that changed — the same thing `git diff` shows you, drawn as a web page:

```diff
  <li>Tea <b>2.00</b></li>
- <h1>Class Menu</h1>
+ <h1 style="color: green">Class Menu</h1>
  <li>Cake <b>3.00</b></li>
```

`-` and red is the line that was taken out; `+` and green is the line that was put in; grey with no sign is unchanged, shown so you can see where in the file you are.

Reviewing means reading the diff, then approving it or asking a question — **Files changed** is the tab with the diff on it, **Review changes** is Comment, Approve, or Request changes, and GitHub won't let you approve your own — somebody else has to read it. Claude can explain a diff you don't follow — paste it and ask what changed, but **approving is still your decision.** An approval is cover, not ceremony: a merged pull request breaks production sooner or later, and when it does, the question is whose change it was and who read it. Reviewed by somebody else, that's a team's miss. Merged alone, it's yours.

## Merging

Merging puts one line of saves into another. Merge `color-fix` into `main`, and `main` then has your saves as well as its own — the two lines become one line going forward. Your branch is not harmed by merging; it simply stops being ahead. On GitHub this is the **Merge pull request** button; in the terminal it's `git merge <branch>` — same thing.

```
Merge pull request → Confirm merge → Delete branch

# then, standing on main:
git switch main → git pull → git log --oneline
```

Deleting the merged branch is safe — the saves are in `main` now, the branch was only the name they were written under. Your machine keeps its own copy either way; `git branch -d color-fix` removes that one.

If a second branch — say `add-button` — started **before** that merge, it's now behind: it began at an older commit than the one `main` ends on. Nothing is broken and nothing is lost, the branch is simply older, and it doesn't have what `main` gained until it catches up.

## Conflicts

The whole rule comes down to one question: the same line, or different lines?

| | What happens |
|---|---|
| **Different lines** — you changed line 12, they changed line 40 | Git puts both in and never asks |
| **The same line** — you both changed line 12 | Git cannot know which one you meant, so it stops and asks |

That's all a conflict is: **Git will not guess.** It's not an error, and it's not something you broke. Lines that touch count as the same spot — Git reads the file in blocks, and one untouched line between them is enough to keep them apart.

A conflict, end to end — bringing `main` into a branch that touched the same line:

```bash
git switch main → git pull → git switch add-button → git merge main
# CONFLICT (content): Merge conflict in index.html

vi index.html → git add → git commit → git push
# the pull request goes green → Merge pull request
```

Both engineers' work ends up on the same line of the same file — nothing was overwritten. Git writes three marker lines into the file so you can choose:

```
<<<<<<< HEAD
  <li>Coffee <b>2.50</b> <button>Order</button></li>
=======
  <li>Coffee <b>2.80</b></li>
>>>>>>> main
```

| Marker | Meaning |
|---|---|
| `<<<<<<< HEAD` | Your side — the branch you're standing on |
| `=======` | The divider |
| `>>>>>>> main` | What came in from `main` |

Keep what you want, delete all three marker lines. Here the answer is both — the new price and the button. **The common mistake:** committing with `=======` still in the file — the page then shows it to everybody who opens it.

A conflict needs two branches, not two people — you can make one on purpose to practice:

1. On `main`, pick one line in your own part of the page.
2. `git switch -c change-one` → change that line → `git commit`.
3. `git switch main` → `git switch -c change-two` → **the same line**, differently → `git commit`.
4. `git switch main` → `git merge change-one` → clean.
5. `git merge change-two` → **CONFLICT**, guaranteed.

In step 3, the second branch starts from `main` — not from `change-one`. Start it there instead and Git merges cleanly, with nothing to practice on.

Claude resolves conflicts, and that's the normal way now — it's good at this, including large and messy ones, and hardly anybody works through conflict markers by hand any more. Show it the conflicted file and say what you want kept:

> "There is a conflict in `index.html`. Keep the new price and the Order button, and remove the markers."

**Read the file afterwards.** You're the one pressing Merge, so you're the one saying the result is right.

## Keeping Up with Main

The same four commands as resolving a conflict — this time with nothing to decide, because the changes are on different lines:

```bash
git switch main → git pull → git switch add-button → git merge main
# Merge made by the 'ort' strategy.   ← different lines, nothing to decide
```

The direction is the other way round from the pull request: here `main` gives and **your branch receives** — `main` isn't touched. Do this **before** you push, as ordinary daily practice, not recovery from a problem — then anything to decide, you decide on your own branch, not on a pull request somebody is already reading.

## .gitignore

One file lists what Git should never save:

```
.gitignore
─────────────
.env            your API keys
*.pem           key files
__pycache__/    Python leftovers
.DS_Store       macOS junk
```

One line per thing Git should never track. Commit the file itself, and everybody in the repo gets the same list — this is the **never push a key** rule from the news-bot lesson, written down where Git can act on it.

**The honest limit:** it stops a file being saved *in the first place*, and does nothing about a file already in the history. A key that was ever pushed has to be replaced with a new one — `.gitignore` can't undo a push that already happened.

## Named, Not Drilled: rebase and revert

Two more words, so they aren't new later:

| | What it is |
|---|---|
| **rebase** | A second way to catch up. Merging joins the two lines and adds a save that ties them together. Rebase instead moves your saves so they start from `main`'s newest save — one straight line, no join. A topic of its own, later — it rewrites your saves, which is why it isn't today |
| **revert** | Undoing a pull request that was already merged. One button on GitHub: Revert — it opens a new pull request, and that one needs an approval too. It doesn't erase anything; it adds a new save that puts the file back |

`git fetch` is the half of `git pull` that only downloads — `pull` is `fetch` then `merge`. Claude can run either of these for you when it comes up.

## Where You Are

Three things you can do now:

- **A branch you made** — created, worked on, pushed.
- **A merged pull request** — into code the whole class shares, read by somebody else first.
- **A conflict you fixed** — made on purpose, read, decided, finished.

## After Class

Optional practice and Q&A held after the main lecture — less structured, working through the flow again with the instructor:

- **One more change through the whole flow** — a fresh branch, a commit, a push, a pull request, a review, a merge.
- **One more conflict on purpose** — two branches off `main`, the same line, differently, and resolve it either by hand or by asking Claude.
- **A `.gitignore` in your own app repo** — commit it, and confirm nothing in it is already tracked from before.

**What you know now:** `main` is a branch too — a line of saves everybody in the class shares, and a shared push gets rejected with `(fetch first)` the moment somebody else's save landed on it before yours. A branch is a second line of saves starting from the commit you're on — not a copy, not a backup, not a separate repo — and `HEAD` is Git's name for whichever one you're standing on. Pushing a branch makes it visible on GitHub; a pull request asks for it to be merged into `main`, and nothing lands until somebody presses Merge, one diff and one approval at a time. Merging joins two lines into one without harming the branch that was merged in; a branch that forked before that merge is simply behind, not broken. A conflict only happens when two branches change the **same line** — different lines merge silently — and the three markers, `<<<<<<< HEAD`, `=======`, `>>>>>>> main`, mark your side, the divider, and their side, all three deleted once you've chosen. Catching up with `main` uses the same four commands as resolving a conflict, just with nothing to decide, and it's daily practice, not damage control. `.gitignore` keeps a file from ever being tracked in the first place — it can't undo a key that already got pushed.
