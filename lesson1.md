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

