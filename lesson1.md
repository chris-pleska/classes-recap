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

---

# Lesson 31 — Infrastructure as Code: Terraform, Start to Finish

## Why Write Infrastructure Down

Everything you own in AWS so far, you built by clicking through the console. A click works — but it can't do three things:

| A click can't... | Why |
|---|---|
| **Repeat it** | Not exactly, and not a month later |
| **Review it** | Nobody can check it before it happens |
| **Rebuild it** | When it's gone, it's gone |

This course also turns on things that bill by the hour — load balancers, gateways, databases. Some of it is past the free tier, and it bills whether or not anyone is learning. Two things fix that: a **budget alarm** on your account (a spending limit that emails you — a few screens in AWS Billing), and one command that turns it all off. You'll meet that command by the end of today.

## The Idea: Infrastructure as Code

**Infrastructure as code**: you write down the infrastructure you want in files, and you keep those files the way you keep code. A program reads them and makes reality match.

That's the opposite of a script. **A script performs steps**, in the order you wrote them. **This describes a destination**, and the program works out the steps itself.

A file can do the three things a click can't:

| | A file |
|---|---|
| **Repeat it** | Run the same file again and get the same thing — a year later, too |
| **Review it** | Someone reads the file, and the change it would make, before anything happens |
| **Rebuild it** | Everything gone? Run the file. It comes back |

## The Field: Several Tools, One Idea

| Tool | What makes it different |
|---|---|
| **CloudFormation** | AWS's own. Describes what should exist — but only ever on AWS |
| **Pulumi / CDK** | You write a real programming language (Python, TypeScript) and it produces the infrastructure |
| **Ansible** | Not infrastructure as code at all — it's **configuration management**. It configures machines that already exist (one command puts a new version of nginx on all of them), a different job from creating them |
| **Terraform** | Describes what should exist, against any cloud — the one we teach |

None of these is the winner. They're different answers to the same question, and you'll meet all four names on job postings.

**Why Terraform specifically:**
- **Not tied to one cloud.** The same tool describes AWS, Google Cloud, a DNS provider, a database service — you learn the idea once.
- **It's the name job postings use.**
- **Its certification is one of two this program targets** — the other is Kubernetes, much later.

You'll read that Terraform belongs to IBM now, and that it's no longer open source. Both are true: the license changed in August 2023, and there's a community fork called **OpenTofu** that works almost identically. What it means for you: free to use, for learning and for work — you just may not sell a product that *is* Terraform. We teach Terraform.

## Setting Up Terraform

Installing it is the step most likely to go wrong today. Errors here are expected and say nothing about anybody — one tool, this many different machines.

| OS | Install |
|---|---|
| macOS (Homebrew) | `brew tap hashicorp/tap && brew install hashicorp/tap/terraform` |
| Amazon Linux (yum) | `sudo yum install -y yum-utils shadow-utils` then add the HashiCorp repo, then `sudo yum install terraform` |
| Ubuntu/Debian (apt) | add the HashiCorp gpg key and repo, then `sudo apt update && sudo apt install terraform` |

**When it doesn't go clean, the three that actually happen:**

```bash
terraform version
# → any version above 0.12 is fine for today. Stop here.
# → brew says "already installed, just not linked"? Run the brew link
#   command it prints, then close and reopen the terminal.
```

```bash
xcode-select --install
# macOS error mentioning "command line tools" — a long download, start it and wait,
# then run the brew command again.
```

```
code . → command not found
# VS Code: Cmd⇧P → "Shell Command: Install 'code' command in PATH"
```

None of these is about you, and the newest version isn't required for anything today.

**The editor:** in VS Code, install the extension called **HashiCorp Terraform** — published by HashiCorp, with the verified tick (there are convincing lookalikes). Restart VS Code — nothing changes until you do. It completes resource types and argument names for you, which is most of what you'll type today.

**Two commands confirm the install:**
```bash
terraform version
# → a version number. That's the new tool.

aws sts get-caller-identity
# → your own account number. Terraform borrows these same credentials —
#   the ones you already set up with `aws configure`.
```

**Then a repository to keep the files in**, named exactly `infra-as-code-YOUR_GITHUB_USERNAME`. Your username on the end so no two are the same. It becomes the history of every change you ever make to your infrastructure.

## The Five New Words

**`provider`** — a plug-in that knows how to make one kind of thing, usually one company's cloud. Think of it as an interpreter: Terraform speaks to it, and it speaks AWS.

```hcl
provider "aws" {
  region = "us-east-1"
}
```

Who you are is never in this file — that came from `aws configure`, off your machine. This block is only *how to speak AWS*.

**`resource`** — one thing that should exist. A network is a resource. A server is a resource. A firewall rule is a resource. Your file is a list of them.

```hcl
resource "aws_vpc" "scratch" {
  cidr_block = "10.99.0.0/16"
}
```

Every resource is written with two names:

| | Meaning |
|---|---|
| **the resource type** (`"aws_vpc"`) | What kind of thing it is. The provider decides the list of possible types — you can't invent one |
| **the name** (`"scratch"`) | What *you* call this one, so you can refer to it later in the file. AWS never sees it |

AWS gives the real thing an id of its own — something like `vpc-0a1b2c3d4e5f6a7b8` — and that's what shows up in the console. Your name for it stays in the file.

Two of the same type can't share a name — copy a block, forget to rename it, and this is what you get:

```
Error: Duplicate resource "aws_subnet" configuration
  on main.tf line 14:
  14: resource "aws_subnet" "private" {
An aws_subnet resource named "private" was already declared at main.tf line 8.
Resource names must be unique per type in each module.
```

Terraform tells you the file, the line, the name it objected to, and the rule — copy-then-rename is the single most common way to hit it.

**The whole shape, and there's only one:**

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "scratch" {
  cidr_block = "10.99.0.0/16"
}
```

## init, plan & apply

**`terraform init`** — download the providers this folder needs, into this folder. It's a download: nothing is created in your account, nothing costs money. Run it again whenever the set of plug-ins the folder needs changes, **not** every time you change a resource. `terraform init -upgrade` gets a newer version of a plug-in you already have.

**`terraform plan`** — asks AWS what exists, compares that to your file, and prints what it would do to make them match. **Nothing changes.** Run it as many times as you like — it's a question, not an instruction.

**`terraform apply`** — do what the plan said. It shows you the plan again and asks once before it starts. This is the only command that changes anything in your account — everything else looks, downloads, or reports.

The whole thing, on something real:

```bash
terraform init
# → .terraform/ appears, with the AWS plug-in inside
# → .terraform.lock.hcl records which version you got

terraform plan
# → 1 to add. Nothing has happened yet.

terraform apply
# → it asks. You say yes. Then the AWS console, and there it is.
```

`10.99.0.0/16` is deliberately odd-looking, so it's obviously not your real network — a network costs nothing.

## Reading a Plan

Read it backwards — the last line first:

```
Plan: 1 to add, 0 to change, 0 to destroy.
```

Not every attribute — no engineer reads that. You read the count, you read the symbols, and **you stop if the destroy number isn't what you expected.**

Seven symbols, two of them with an order built in:

| Symbol | Meaning |
|---|---|
| `+` | create something new |
| `-` | destroy it |
| `~` | change it where it stands — nothing is destroyed |
| `-/+` | **destroy it, then create the replacement** — read left to right, that's the order the work happens in |
| `+/-` | create the replacement first, then destroy the old one |
| `<=` | read something that already exists, without touching it |
| *(none)* | not changing — most lines of a long plan |

## Turning It Off: terraform destroy

**`terraform destroy`** — delete everything *this folder* made. Nothing else. It shows you a plan first, where every line is a minus, and asks once. This is the command that makes the rest of the course affordable.

```bash
terraform destroy
# → read it: every line is a minus. Then yes.
# → refresh the console. Gone, in about ten seconds.
```

You now know how to make something and how to remove it, and you've done both on something that didn't matter. Everything after this is the same two commands on things that do.

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **Finish the install** if it didn't go clean live — brew link, Xcode command line tools, or the VS Code `code` command, one at a time.
- **Run the loop again** on a second scratch resource — `init` → `plan` → `apply` → check the console → `destroy`.
- **Read a plan out loud** before running `apply` — say what each `+`, `-`, or `~` means before you approve it.

**What you know now:** infrastructure as code means describing the destination in a file and letting a program work out the steps, instead of performing the steps yourself — the opposite of a script. A `provider` is the plug-in that speaks to one cloud; a `resource` is one thing that should exist, named with a type the provider fixes and a name you choose. `terraform init` downloads the providers a folder needs; `terraform plan` asks what would change and changes nothing; `terraform apply` is the only command that touches your account, and it asks once before it does. A plan reads backwards — the counts, then the symbols, stopping if the destroy count is a surprise. `terraform destroy` removes everything a folder made, which is what keeps a course full of hourly-billed services affordable.

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

---

# Lesson 32 — Real Infrastructure: State, Drift, Sharing & Writing It Once

## The Real Network: Seven Resources

Last session's `aws_vpc` was scratch — a network that cost nothing and did nothing. This time it's real, and it takes seven resources to make a network anything can actually run on:

| Resource | What it is |
|---|---|
| `aws_vpc` | a private network of your own |
| `aws_subnet` ×2 | a section of it, in two availability zones |
| `aws_internet_gateway` | one way in and out |
| `aws_route_table` | where traffic goes |
| `aws_route_table_association` ×2 | this subnet uses that table |

The addresses: `10.0.0.0/16` for the network, then `10.0.1.0/24` and `10.0.2.0/24` for the two subnets, one per availability zone. Both of these subnets are public — both reach the gateway — so they're named `public_a` and `public_b`, never `private`. Five kinds of resource, seven blocks in the file, because the subnets and the associations come in twos.

The build happens one resource at a time: say what you want in one plain sentence, write that resource in the file, `plan` to check what it would do, `apply` and it exists. Then the next one. Nothing gets added blind, and the plan gets read every single time.

Open the VPC in the console after `apply` and there's a second route table you never wrote — no name, no subnet attached to it:

**the main route table** *(every VPC has one)* — AWS creates it together with the network. Terraform didn't make it, so Terraform will never touch it and it will never show up in a plan. You can't delete it; it goes when the VPC goes. Nothing is associated with it, so no traffic uses it — seeing it in the console isn't a sign anything went wrong.

## Order Without an Order: the Dependency Graph

Nothing in the file says "do me second." But look inside the subnet block:

```hcl
resource "aws_subnet" "a" {
  vpc_id            = aws_vpc.main.id
  availability_zone = "us-east-1a"
  cidr_block        = "10.0.1.0/24"
}
```

The subnet *mentions* the network, so the network has to exist first — and Terraform can see that. **The dependency graph** is Terraform's map of which resource mentions which. It's also read backwards, to work out a safe order for deleting.

Getting traffic out takes three more resources, and one value you can't copy blind:

```hcl
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"   # → anywhere that is not inside this network
    gateway_id = aws_internet_gateway.gw.id
  }
}
# → then one association per subnet: subnet_id + route_table_id, four lines each.
```

`0.0.0.0/0` is the whole point of a route: **anywhere else**. The Terraform Registry's own example puts a narrower range there instead — paste that unchanged and `apply` fails part-way, with some resources made and some not. Fix the value and run `apply` again.

## Change or Outage: One Word Decides

Same file, same command, a very different consequence depending on what you touched:

| Change | Symbol | What happens |
|---|---|---|
| Change a tag | `~` | changed where it stands — nothing is destroyed, nothing goes down |
| Change a subnet's address range | `-/+` | destroyed and built again — safe here only because these subnets are empty |

In the console, that same address-range change just happens the moment you click. Terraform is the only one of the two that told you first.

## Drift: When Somebody Changes It by Hand

**drift** — reality has moved away from what your file says, usually because somebody changed something in the console instead of in the file. It happens on every real team, usually in a hurry, usually with a good reason at the time.

Terraform finds it without being asked:

```bash
terraform plan
# → Note: Objects have changed outside of Terraform
# → and it offers to put it back the way the file says.
```

The file is what you meant; the cloud is only what happens to be true right now. Nothing gets fixed until a person runs `apply` — there's no schedule, and nothing running in the background.

There's a flag that skips the yes/no prompt entirely:

```bash
terraform apply -auto-approve
# → no plan to read, no yes to type. It just happens.
```

This exists for the machine that runs Terraform when nobody's watching — a pipeline that applies your code after somebody merges it, a later course. **Don't use it yet.** Reading the plan is the thing you're here to learn — type `yes`.

## The State File: Terraform's Memory

You've made and deleted several networks in that account today. Your file says `"main"`. AWS has never heard that word. So when you run `plan`, how does Terraform know which network it's looking after?

**state** *(the file is called `terraform.tfstate`)* — Terraform's memory file, how it remembers what it has already made and what it hasn't. For each thing, it stores the name from your file beside the real AWS id.

Watch what happens without it:

```bash
mv terraform.tfstate /tmp/keep-this-safe
terraform plan
# → 7 to add. Your network is still sitting in AWS, untouched.

mv /tmp/keep-this-safe terraform.tfstate
terraform plan
# → No changes. It remembers again.
```

One file moved, and nothing else. Same code, same cloud, two different answers — so the answer was never coming from just those two things.

Deleting the memory file does not delete your network. Your network is still sitting in AWS, running and billing — Terraform has simply forgotten it exists. And that's the dangerous part: next time you run `apply`, it builds a *second* network beside the first, because as far as its memory goes, it never made one. The state file isn't a copy of your infrastructure, and it isn't disposable.

## What's Inside It — and Why It's Gitignored

The state file stores every detail of everything it made — not just names and ids, but every setting, every value, exactly as AWS reported it back. Including the ones you wouldn't want stored: when you create a database later in this course, its password lands in this file in plain text. Nobody has to do anything unusual for that to happen — it's just another value the resource returned.

```
.terraform/        the downloaded plug-ins. Big, and easy to get again.
*.tfstate          the memory file. Can hold passwords.
*.tfstate.*        its backups. Same reason.
*.tfvars           value files, which often hold secrets too.

— and the one people wrongly add to that list —
.terraform.lock.hcl  ← NOT ignored. You COMMIT this one: it pins which
                     provider version you got, so next month you get that same one.
```

Your Terraform files belong in git, and so does the lock file. The memory file never does:

```bash
git add . && git commit -m "the network, in code"
git push
# → every change from here on is a commit.
```

## One Laptop Isn't Enough: Remote State

The memory of your entire infrastructure is a file in a folder on your machine, and it's not in git. What happens when that laptop dies? Or when a second person has to run this?

**remote state** — the memory file kept in shared storage instead of on one machine, so it survives the laptop, and any machine that's allowed to can read and write it. Three places do this job: an **S3 bucket** (ours), an **Azure storage account**, or **Terraform Cloud**.

```hcl
terraform {
  backend "s3" {
    bucket = "your-unique-bucket-name"
    key    = "unit1/terraform.tfstate"
    region = "us-east-1"
  }
}
```

The backend does nothing until you run this:

```bash
terraform init
# → "Do you want to copy existing state to the new backend?"   yes

terraform init -reconfigure   # ← every later time you change this block
```

The bucket has to exist **before** this works — Terraform will not make it for you. So you make that one bucket by hand, once (versioning on, public access blocked), and it lives outside everything you'll ever destroy. `backend.tf` itself is committed to git: it holds the address of the memory, not the memory.

There's one exception to how Terraform normally works: the backend block will not take a variable.

```hcl
backend "s3" {
  bucket = var.bucket_name     # ← rejected
  region = var.region          # ← rejected
}
```

Terraform reads this block **before** it reads anything else in your files — it has to find the memory before it can work out what a variable means. So the bucket name and the region get typed out in full. This is the one place in the file where writing the value out again is correct.

## Two People at Once: State Locking

If the memory is shared, two people can run `apply` at the same moment. Both write the memory file. One of them silently wins, and the other's record of what it built is gone.

**state locking** — while one person is applying, the memory file is **locked** and nobody else can start. They get told to wait. You have to ask for it: add `use_lockfile = true` to that backend block. **It's off unless you turn it on**, and nothing warns you.

```bash
# terminal one:  terraform apply   — then stop at the yes/no prompt
# terminal two:  terraform apply
# → with locking off: it runs. Nobody is warned, and nothing says a word.

# terminal two, with locking on and re-init'd:  terraform apply
# → Error: Error acquiring the state lock
#   S3 PutObject, status code 412: at least one of the preconditions
#   you specified did not hold — and who is holding it, since when.
```

The lock is held for as long as that prompt sits there unanswered. On a real team, that name is your colleague's — this is how you find out they're mid-change instead of overwriting them.

## Say It Once: Variables

Look back at your file: `us-east-1` is in the provider, and again in each subnet. The address range appears more than once too. Change one and forget another, and you have a bug that `plan` cannot warn you about — because the file is exactly what you wrote.

**variable** — a named value you declare once and refer to everywhere else. Change it in one place and every use of it changes.

```hcl
variable "region" {
  type    = string
  default = "us-east-1"
}

region = var.region    # ← how you refer to it, anywhere in the file
```

On its own, a variable needs no quotes, nothing around it. Inside a piece of text it has to be wrapped, or it's not read as a variable:

```hcl
availability_zone = "${var.region}a"        # → us-east-1a
name              = "${var.region}-main-db"   # → us-east-1-main-db
```

Leave the `${ }` off inside quotes and Terraform doesn't complain — it hands AWS the literal letters `var.region`, and AWS is the one that objects: `Invalid AWS Region: var.region`.

## Getting a Value Back Out: Outputs

**output** — a value you ask Terraform to **print for you** when it finishes, usually something only AWS could tell you, like the real id of a thing it just made.

```hcl
output "subnet_a_id" {
  value = aws_subnet.a.id      # ← and a second one just like it, for b
}
```

```bash
terraform output       # ← prints the real ids, ready to paste
```

A variable is a value going **in**. An output is a value coming **out**.

## One Description, Many Resources: for_each

Look at what's actually in your file right now:

```hcl
resource "aws_subnet" "a" {
  vpc_id            = aws_vpc.main.id
  availability_zone = "us-east-1a"
  cidr_block        = "10.0.1.0/24"
}

resource "aws_subnet" "b" {
  vpc_id            = aws_vpc.main.id
  availability_zone = "us-east-1b"
  cidr_block        = "10.0.2.0/24"
}
```

Eight lines, and only two values are actually different. A third subnet would be eight more.

**for_each** — you hand Terraform a **set of names** and **one description**. It makes one of the thing for each name. It is not a loop: nothing runs in order, no counter, no first or second — both subnets are made at once.

```hcl
variable "subnets" {          # ← the set of names, and what goes with each
  type = map(string)
  default = {
    "us-east-1a" = "10.0.1.0/24"
    "us-east-1b" = "10.0.2.0/24"
  }
}

resource "aws_subnet" "main" {
  for_each          = var.subnets
  vpc_id            = aws_vpc.main.id
  availability_zone = each.key     # ← the name it is on: us-east-1a
  cidr_block        = each.value   # ← what sits beside it: 10.0.1.0/24
}
```

Two blocks became one. The next `plan` is **not** "no changes" — the subnets have different names now, so Terraform destroys both and builds them again. Safe here only because they're empty.

## When for_each Breaks What Pointed at the Old Names

There's no `aws_subnet.a` any more. Both route table associations named it, so both stop working — and the fix is that they become one block with `for_each` too:

```hcl
resource "aws_route_table_association" "main" {
  for_each       = aws_subnet.main
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}
```

Two errors show up, in this order. First `Reference to undeclared resource` — the old name is gone. Then `Missing resource instance key` — you reached `aws_subnet.main` as if it were one thing, and it's a set now. Your outputs move the same way.

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **Build the seven-resource network again on your own** — one resource, one sentence, one plan, one apply, checked in the console before moving to the next.
- **Cause drift on purpose, then let plan find it** — change a tag by hand in the console, run a plain `plan`, and read what it offers to do.
- **Move the state file aside and back** — watch a plan go from "7 to add" to "No changes," on infrastructure that never actually changed.
- **Rewrite your two subnets as one `for_each` block**, then fix everything that pointed at the old names — the associations, and any outputs.

**What you know now:** a real network is seven resources whose order comes from what they reference, not from the order you wrote them in — and AWS quietly keeps its own default route table alongside the one you made. Drift is reality moving away from your file, usually by a console click, and `plan` finds it without being asked. Terraform's memory of what it has built is the state file — lose it and your infrastructure doesn't disappear, but Terraform forgets it exists and will happily build a second copy. That file holds secrets in plain text, so it's gitignored (the lock file isn't). Remote state moves that memory into shared storage like S3, using a `backend` block that — uniquely — can't take a variable; state locking stops two people from applying at once, but only if you turn it on. Variables let you say a value once and use it everywhere; outputs print a value back out when Terraform finishes. And `for_each` replaces near-identical copies of a resource with one description over a set of names — not a loop, all made at once — at the cost of rewriting everything that referenced the old, individually-named resources.

**What you know now:** `main` is a branch too — a line of saves everybody in the class shares, and a shared push gets rejected with `(fetch first)` the moment somebody else's save landed on it before yours. A branch is a second line of saves starting from the commit you're on — not a copy, not a backup, not a separate repo — and `HEAD` is Git's name for whichever one you're standing on. Pushing a branch makes it visible on GitHub; a pull request asks for it to be merged into `main`, and nothing lands until somebody presses Merge, one diff and one approval at a time. Merging joins two lines into one without harming the branch that was merged in; a branch that forked before that merge is simply behind, not broken. A conflict only happens when two branches change the **same line** — different lines merge silently — and the three markers, `<<<<<<< HEAD`, `=======`, `>>>>>>> main`, mark your side, the divider, and their side, all three deleted once you've chosen. Catching up with `main` uses the same four commands as resolving a conflict, just with nothing to decide, and it's daily practice, not damage control. `.gitignore` keeps a file from ever being tracked in the first place — it can't undo a key that already got pushed.
---

# Lesson 33 — One Server, Built From Code: AMI, Data Sources & the Security Group

## Nobody Configures a Real Environment by Hand

Your network is already in Terraform — the VPC, the subnets, the internet gateway, the route table. This session adds the one thing that runs the app: the machine itself, described in the same file, created by the same `apply`.

Three reasons nobody does this by clicking, and the third one settles it:

| Reason | Why it matters |
|---|---|
| **People make mistakes** | Anything done by hand is done slightly differently at 2am |
| **It can't be reproduced** | You know this one already — it's why your network is a file |
| **Real environments run thousands of servers** | Nobody configures a thousand machines one at a time |

Maersk's machines were wiped in 2017. Recovery meant rebuilding *4,000 servers and 45,000 computers*, in ten days, round the clock, while ships kept sailing with nobody able to tell them where to go. That's the scale the third reason is actually about.

## Describing a Machine Means Deciding Five Things

Before any AWS word, a server is just a thing you describe, and describing one means deciding five things:

| # | Decision | Answered by |
|---|---|---|
| 1 | Which operating system it starts with | The AMI |
| 2 | How big it is | The instance type |
| 3 | Where in your network it sits | The subnet |
| 4 | Who is allowed to reach it | The security group |
| 5 | What it's allowed to do inside AWS | The instance role and profile — *next session* |

Every AWS word in this lesson is the answer to one of the first four. A key pair is a sixth thing you almost always want, but it isn't required — an instance with no key exists and runs, you just can't get onto it.

**The instance needs a subnet, not a VPC.** The console asks you to pick a VPC first, but that's only a filter — it's how the console decides which subnets to offer. The instance itself only ever records the subnet. Give Terraform `subnet_id` and it works out the VPC from that; there's no `vpc_id` argument on an instance.

## Decision One: AMI — the Disk It Starts From

**AMI** (Amazon Machine Image) — the starting disk: an operating system, and optionally everything else you want already installed on it. Picking "Amazon Linux" in the console is picking an AMI.

You can make your own — take an EC2, SSH in, install and configure everything, then create an AMI from it. That's called a **golden image**, and it turns a one-time configuration into something you can stamp out many times. This is Part 3 of the unit.

Four places AMIs come from:

| Source | What it is |
|---|---|
| **Quick start** | Amazon's own, kept up to date |
| **My AMIs** | Ones you built — empty until you build one, and shareable with other AWS accounts |
| **Community AMIs** | Published by other organizations — Debian's official images, Kubernetes-tuned images |
| **AWS Marketplace** | Companies selling prepackaged, configured, maintained software as an AMI |

The Marketplace is a real alternative to building it yourself. Palo Alto and Fortinet sell their firewalls this way — buy the firewall as an AMI, launch it, and it's configured and patched, versus building an EC2, buying a license, and maintaining it forever by hand. Some listings **sell support hours alongside the image**: "this subscription includes five hours of support so we can help you install it." In real jobs the choice usually comes down to the cost of engineer time, not the cost of the license.

**An AMI id is not worth writing down.** Every AMI has an id like `ami-0abc123…`. It's **different in every region**, and it's **replaced whenever Amazon publishes a newer image**. Hard-code one and your file is wrong in another region and stale within weeks. Putting it in a variable doesn't fix this — a variable just moves the hard-coded value to a different line; it's still a value you typed. The fix is to describe the image you want and let Terraform look up today's id.

## data — Reading a Fact Instead of Creating One

Typing `us-east-1a` into a file assumes that zone exists and always will. AWS already knows the real list — so ask it.

**data source** — a resource you **read** instead of create. Terraform fetches the fact; it makes nothing and changes nothing and owns nothing. The difference from a variable, put most simply: in a variable, *you* put the value in. A data block takes the value *directly from Amazon.*

```hcl
data "aws_ami" "linux" {
  most_recent = true                            # newest match wins
  owners      = ["amazon"]                      # Amazon's own images, not a stranger's

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

# read it as data.aws_ami.linux.id
```

The `owners` line matters: anyone can publish an AMI, and without an owner filter you're booting a stranger's disk image.

In `terraform plan`, a data read shows as `<=` rather than `+` or `~` — the first time you see that symbol. It means *read*.

**Matching nothing is an error, and that's the point:** `Your query returned no results`. That error means **your filter is wrong**, not that the image is missing — Terraform stops rather than guessing.

**Filtering by a tag has the same trap as everything else about drift.** Filter a subnet on its `Name` tag, and if it doesn't match, the fix is *not* to open the console and add the tag by hand — that works once, and the next `apply` sees a tag that isn't in your file and removes it, breaking the filter again. The right fix is to set the tag **in the Terraform that creates the subnet**, so the file and AWS agree:

```hcl
resource "aws_subnet" "public" {
  # …
  tags = { Name = "subnet-1" }
}
```

And if the subnet is in your own Terraform anyway, you don't need a data block at all — reference it directly as `aws_subnet.public.id`. **A data block is for things Terraform did not create.**

## Decisions Two and Three: How Big, and Where

Both of these you've already chosen before, by clicking.

**Instance type** — how much CPU and RAM. In `t3.micro`, **`t3` is the family and `micro` is the size.** The family is what the machine is built for; the size is how much of it you get.

| Family | Built for |
|---|---|
| **T** | General purpose. Ordinary servers — the one you use |
| **M** | General purpose, larger and steadier than T |
| **C** | Compute optimized — a high ratio of CPU to memory |
| **R** | Memory optimized — applications that need a lot of RAM |
| **I, D, H** | Storage optimized |
| **P, G** | Accelerated computing — machines with GPUs, for AI and graphics |
| **HPC** | High performance computing — simulation and modeling |

Storage optimized means AWS physically places the storage close to the machine in the data center, so the distance the data travels is short. On your laptop that difference is invisible; at the scale of a billion-dollar company, nanoseconds add up into money.

**Both bill by the hour from the moment the machine exists**, whichever family and size you pick, and whether or not anything is running on it.

**Subnet** — which part of your own network the machine sits in. You built subnets in Terraform already; the machine goes in one of them.

## Decision Four: The Security Group, One Resource Per Rule

**Security group** — the checkpoint in front of the machine: which ports are open, and to whom. A new machine answers nobody until you allow it. You clicked one of these into existence when your site first went live.

```hcl
resource "aws_security_group" "app" {
  name   = "app-sg"
  vpc_id = aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "ssh" {
  security_group_id = aws_security_group.app.id   # which group this rule is in
  from_port = 22 , to_port = 22 , ip_protocol = "tcp"
  cidr_ipv4 = "0.0.0.0/0"                          # from where
}

resource "aws_vpc_security_group_egress_rule" "out" {   # going out — write it
  security_group_id = aws_security_group.app.id
  ip_protocol = "-1" , cidr_ipv4 = "0.0.0.0/0"
}
```

**The group on its own is empty.** Creating it opens nothing. Each rule is a separate resource, and each one names the group it belongs to with `security_group_id`. **One port per rule** — `from_port` and `to_port` are a range, and setting them to the same number opens exactly one port, which is what you almost always want. Open 22 and 80 with two ingress rules, not one range from 22 to 80. Rule names must be unique, so copying a block to make a second rule means changing the label too, or the plan fails on a duplicate name. The source can be a reference — `cidr_ipv4 = aws_vpc.main.cidr_block` means "anyone inside my own VPC"; `"0.0.0.0/0"` means the whole internet.

**Outbound access is free in the console, and it is not free in Terraform.** Create a security group by clicking, and AWS quietly adds an allow-all outbound rule you never asked for. Terraform doesn't do this — nothing exists that you didn't write. A group with no egress rule gives you a machine that boots, lets you SSH in, and then can't download anything: no `yum install`, no `git clone`, nothing.

**`vpc_security_group_ids`, not `security_groups`.** Two arguments on `aws_instance` look like they do the same thing. They don't — `security_groups` is for EC2-Classic and the default VPC only. You're in your own VPC, so it's the wrong one, and using it makes Terraform **destroy and recreate the whole instance** every time the group changes.

## Two Arguments Any Block Can Take

**`depends_on`** — Terraform normally works out build order from your references: a subnet block that names `aws_vpc.main.id` can't be built before the VPC, so it isn't. When two resources are related but **neither one names the other**, Terraform is free to try them in either order, and an apply can fail because the machine went first and the subnet didn't exist yet — a failure that often disappears on a second apply, which is what makes it confusing.

```hcl
resource "aws_instance" "app" {
  # …
  depends_on = [aws_subnet.public]
}
```

Square brackets — it takes a list. You won't need it often; reach for it when an apply fails on ordering.

**`lifecycle { ignore_changes = [...] }`** — worth a second look now that it applies to a machine you'll SSH into and poke at by hand. Terraform's normal behavior is to be the boss: anything changed outside the file gets undone at the next apply. Sometimes you don't want that for one specific value — something outside Terraform is allowed to own it, and you want Terraform to keep managing everything else.

```hcl
resource "aws_instance" "app" {
  # …
  lifecycle {
    ignore_changes = [tags]
  }
}
```

## The Decisions, Written Down: One Machine, in One Block

```hcl
resource "aws_instance" "app" {
  ami                    = data.aws_ami.linux.id      # 1 which operating system
  instance_type          = "t3.micro"                 # 2 how big
  subnet_id              = aws_subnet.public.id       # 3 where in your network
  vpc_security_group_ids = [aws_security_group.app.id] # 4 who may reach it
  # iam_instance_profile = ...                        # 5 what it may do — next session

  key_name               = "my-key"                   # so SSH works

  associate_public_ip_address = true                  # or it has no address to SSH to
}
```

Four decisions here, and the fifth next session. **`associate_public_ip_address = true` is what gives the machine an address you can SSH to** — without it the instance is created, runs, and is unreachable. **Read the plan before you say yes:** change this or the security-group argument on a machine that already exists, and Terraform destroys it and builds another one.

**The EC2 resource is called `aws_instance`.** Searching the registry for "EC2" gives a long list, and none of the obvious names is the right one — the registry is also split into resources (things you create) and data sources (things you read), so check you're in the right half before copying anything.

**`terraform plan` is documentation.** If you don't know what an argument is called, run `plan` and read the output — it prints every attribute the resource is going to have, with its real name, ready to copy straight back into your file.

**Key pairs are regional.** A key created in `us-east-1` doesn't exist in `us-east-2` — hit `InvalidKeyPair.NotFound` on an apply and the key almost certainly does exist, just in a different region from the one your provider block resolves to.

## output, Again: Marking a Value Sensitive

```hcl
output "instance_id" {
  value     = aws_instance.app.id
  sensitive = false
}
```

`terraform output` prints it. A variable is a value going **in**; an output is a value coming **out** — use it for anything only AWS can tell you, like the real id of something Terraform just made. `sensitive = true` is the reason outputs matter beyond convenience: a generated database password is a value you need once and must not have scrolling through a shared screen or a CI log. Mark it sensitive and Terraform prints `(sensitive value)` instead — you read it deliberately, once.

## SSH In — and There Is Nothing On It

```bash
chmod 400 ~/Downloads/my-key.pem
ssh -i ~/Downloads/my-key.pem ec2-user@<public-ip>
```

`ec2-user` is the username on Amazon Linux images; Ubuntu images use `ubuntu`. The `chmod 400` is required — SSH refuses a key file that other users on your machine could read.

No app. No packages. No database. A machine described in five lines, created by `apply`, and completely empty. So the next question is the one this unit is really about: **what puts the app on it?**

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **Add the missing public IP** — the most common issue in the room was an instance with no address at all, fixed with `associate_public_ip_address = true`, which forces a destroy-and-rebuild on a machine that already exists.
- **Open port 22, not just 80** — the security group as written in the main session only opened port 80; SSH needs a second ingress rule, a copy of the first block with a different label and `from_port = 22`, `to_port = 22`.
- **Reference a resource made with `for_each` from another file** — same folder, one configuration, no import needed, but a subnet made with `for_each` is a map, not a single resource, so it's picked by its key: `aws_subnet.main["us-east-1a"].id`.
- **Pull the SSH key name from a variable** instead of typing it twice — `key_name` takes the name of the key as it appears in the AWS console, not a file path and not the `.pem` filename.
- **Run `terraform destroy` at the end**, every time — everything built in class was created by Terraform, so destroying it costs nothing; the file is still there and one `apply` brings it all back.

**What you know now:** describing a machine means deciding five things — which operating system (the AMI), how big (the instance type), where in your network (the subnet), who may reach it (the security group), and what it's allowed to do in AWS (next session) — and every new AWS word this session was the answer to one of the first four. A `data` block reads a fact from AWS instead of creating anything, shows as `<=` in a plan, and exists so an AMI id or an availability zone never has to be typed and go stale. A security group is empty until you add rules, and each rule is its own resource naming the group it belongs to — outbound access that the console gives you for free, Terraform makes you write down, and `vpc_security_group_ids` is the correct argument in your own VPC where `security_groups` forces a destroy-and-rebuild. `depends_on` states an order Terraform can't infer from references alone; `lifecycle { ignore_changes = [...] }` tells it to stop fighting over one value that something outside the file is allowed to own. An instance with no public IP is unreachable, not broken, and changing that setting on a live machine replaces it. SSHing in at the end lands on a machine with nothing installed — the app still has to get there, which is where the next session picks up.

---

# Lesson 34: One Server, Built From Code — Identity, Installation & the Disposable Machine

## Decision Five: The Machine Needs an Identity of Its Own

The app on this machine has to read a database password out of Secrets Manager. To be allowed to, the machine has to be *somebody* in AWS — the fifth of the five decisions from last session: what the machine is allowed to do.

| Term | What it is |
|---|---|
| **Role** | An identity in AWS with a set of permissions attached. You've used roles as a person; this is the same object, for a machine. |
| **Instance profile** | The object AWS actually attaches to a machine. It holds the role — a machine can't be given a role directly, the profile is the thing in between. |

In the console this is one dropdown, and AWS writes the profile for you without saying so. In code, nothing is written for you — it's three resources and one argument on the instance.

## Why Your Own Keys Don't Go Onto the Machine

The obvious shortcut is to copy your own AWS access keys onto the machine — and it works: `aws sts get-caller-identity` on that machine answers with your own name. It's the wrong answer for three reasons:

| Reason | Why it breaks |
|---|---|
| **The keys are one person's** | Everyone who reaches that machine is now that person in AWS |
| **Copying them on is manual** | The machine stops being something you can delete and rebuild from the file |
| **They expire** | Somebody has to log into a running server and paste new ones in |

None of the three is a problem once the machine has an identity *of its own* — which is what a role and a profile give it.

## Writing Decision Five Down: Three Resources, One Argument

```hcl
resource "aws_iam_role" "ec2_role" {                # 1 the identity
  assume_role_policy = ...                          # who may assume this role
}

resource "aws_iam_role_policy" "ec2_policy" {        # 2 what it may do
  role   = aws_iam_role.ec2_role.id
  policy = jsonencode({ ... })
}

resource "aws_iam_instance_profile" "ec2_profile" {  # 3 the object AWS attaches
  role = aws_iam_role.ec2_role.name
}
```

```hcl
# ec2.tf — nothing happens until this line exists
iam_instance_profile = aws_iam_instance_profile.ec2_profile.name
```

A role has two separate lists, answering two different questions:

- **`assume_role_policy`** — who may **assume** the role, taking on its permissions for a while. Here that list has one entry, the EC2 service. Without it, the machine is refused before it asks for anything.
- **`policy`** — what the role may then do. `Action: "*"` on `Resource: "*"` means every action on every service in the account — write down what the machine actually needs instead (for this app, Secrets Manager). The **AWS Policy Generator** builds the JSON for you.

Run `aws sts get-caller-identity` again from a machine that has a profile, and the answer changes:

```bash
aws sts get-caller-identity
# → arn:aws:sts::...:assumed-role/ec2_role/i-0a1b2c3d   the machine, not you
```

No keys anywhere on the disk, and nothing anybody has to rotate.

## The Full Machine, Five Decisions, One Block

```hcl
resource "aws_instance" "app" {
  ami                    = data.aws_ami.linux.id             # 1 which operating system
  instance_type          = "t3.micro"                        # 2 how big
  subnet_id              = aws_subnet.public.id              # 3 where in your network
  vpc_security_group_ids = [aws_security_group.app.id]       # 4 who may reach it
  iam_instance_profile   = aws_iam_instance_profile.app.name # 5 what it may do

  key_name               = "my-key"

  associate_public_ip_address = true
}
```

Five decisions, five arguments. `plan`, then `apply`, and the machine exists — **read the plan before you say yes**: changing `associate_public_ip_address` or the security-group argument on a machine that already exists destroys it and builds another one.

SSH onto it and there's still nothing there. No app, no packages, no database — a machine described in five lines, created by `apply`, and empty. So the next question is the one this stretch of the unit is really about: **what puts the app on it?**

## Two Ways to Get the App Onto a Fresh Machine

Both are used in the real world, and the only difference between them is where the app comes from.

| | Amazon's image + your script | Your own image |
|---|---|---|
| **How fast a new machine is ready** | Slow — it installs first | Fast — already installed |
| **Is the code current** | Always — fetched on every boot | Only as current as the image |
| **When the work happens** | Every time a machine starts | Once, when you build the image |
| **What you maintain** | A script | A script, an image, and the habit of rebuilding it |

In the file, only one argument changes:

```hcl
# Amazon's image + your script
resource "aws_instance" "app" {
  ami       = data.aws_ami.linux.id
  user_data = file("install.sh")
  # ...
}

# Your own image
resource "aws_instance" "app" {
  ami       = "ami-<the one you built>"
  # no script — it already ran
  # ...
}
```

Nothing else in the configuration moves — this is a choice, not an architecture, and you can change it later by editing one line.

Which one a real company picks depends on **how often the company changes its code**, not on the tool: a team shipping several times a day can't wait for an install on every boot; a team shipping once a month shouldn't be maintaining an image either. A healthcare company in the matrix rebuilds its images *every month* on a schedule, because a regulator requires its machines to run patched software — that rebuild happens whether or not the code changed.

## What the Script Actually Does

Nothing on this list is new — you've done every one of these by hand, on a real machine. What changes is who types them, and that they happen the same way every time:

1. Install the packages
2. Install and start the database
3. Get the code
4. Write the service file
5. Start the web server

```hcl
user_data                   = file("install.sh")   # runs once, on first boot, as root
user_data_replace_on_change = true                 # edit the script → build a new machine
```

The script runs once, as the machine first boots — editing it does nothing to a machine already running. `user_data_replace_on_change = true` means Terraform destroys the machine and builds another one with the new script whenever it changes; `false` (what you get if you never write the line) means Terraform stores the new script but the machine keeps running the old one until somebody stops and starts it by hand.

```bash
# on the machine, when the app is not up
sudo cat /var/log/cloud-init-output.log   # everything the script printed
```

The database in this script installs right next to the app, on the same machine — deliberately not the setup from Foundations, and covered further below.

## The Script Can't Hold a Secret

Step 2 needs a database password. The script is a file in your repository, and anything written into it is in the repository too.

- **Not in the script** — that's the repository.
- **Not in the image** — anyone who can launch it can read it.
- **Not typed in by you** — then only you can ever build a machine.

The answer is decision five, doing its job — the machine fetches the secret itself, as it boots:

```bash
# the secret itself, made once, from your own laptop:
#   aws secretsmanager create-secret --name app/db --secret-string "..."
DB_PASSWORD=$(aws secretsmanager get-secret-value \
  --secret-id app/db \
  --query SecretString --output text)
```

The machine is only allowed to ask because the role's policy allows `secretsmanager:GetSecretValue`. `create-secret` is what makes a secret; `put-secret-value` only changes one that already exists.

**Environment variable** — a name and a value the operating system hands to a program when it starts. The app doesn't change at all: the script's only job is to put the value where the app already looks, writing `DB_PASSWORD` into the environment file the service reads when it starts the app.

## Building Your Own Image, for Real

```bash
aws ec2 create-image \
  --instance-id <the machine you built> \
  --name "app-with-everything-on-it"
```

A machine launched from that image comes up with nothing installing — no packages, no clone, no wait. Nobody needs to build one at home; seeing both methods run is the lesson. An image you forget about keeps costing money.

## Disposable: Destroy It, and It Comes Back

```bash
terraform destroy    # the machine is gone
terraform apply      # a new one, and the app answers on it
```

Nobody logged in. Nobody installed anything. Nobody remembered a step. The second machine isn't a copy of the first — both were built from the same file. That's what makes a machine a thing you can throw away and replace, and it changes what the app itself has to do.

## Five Things the App Has to Do, Now That It Can Be Replaced

| | Requirement | Where it stands |
|---|---|---|
| ✓ | Start by itself, on boot | Your service file already does this |
| ✓ | Listen on a known port | Your web server already does this |
| ✓ | Take its configuration from the environment | Your environment file and your secret already do this |
| — | Be able to answer "are you working?" | Nothing has ever asked your app this |
| — | Send its logs somewhere that outlives the machine | Yours are on the machine. The machine goes. |

Three of the five you already do, without ever having called them anything.

## The Fourth: A Health Endpoint

**Health endpoint** (usually at the path `/health`) — a URL that answers only when the app can do its job. From outside, it's the only way to tell a working machine from a switched-on one.

`/health` is a convention, not a rule — nothing in AWS or the operating system requires that word. Teams use it so everyone knows where to look; plenty of apps have no such path at all until something is going to ask.

**It must not check the database.** If it does, one database wobble reports *every machine* as dead at the same moment, over a problem none of them actually had. The rule: check what this machine is responsible for, nothing further away than itself.

One word, two meanings worth keeping straight — here, *endpoint* is a path on your app. When a managed database arrives, its *endpoint* is a hostname you connect to.

## The Fifth: Logs That Outlive the Machine

Reading a log by connecting to the machine has worked all year. It stops working once machines are *replaced* instead of repaired — a log on a destroyed machine is gone with it.

What it needs: something has to install a log agent while the machine boots, one more step in the same script. Where it gets built: the **monitoring** topic, later in this stage, which is also where the logs get somewhere to go.

## Where You Are: Two Machines, Both Billing

| | |
|---|---|
| **The hand-built one** | Still serving your domain, still holding your certificate — it has to stay |
| **The coded one** | Answers on its own address only. You can delete it and bring it back whenever you like — that's now two commands |

Do this at the end of every working session:

1. List the machines running in your account
2. Keep the one serving your domain
3. Run `terraform destroy` on the other one

Moving your domain onto the new machine, and deleting the hand-built one for good, is covered in the **load balancer** topic.

## One Thing About This Setup Is Wrong, on Purpose

The database is on the same machine as the app. In Foundations you moved the database *off* the app server, onto a machine of its own with no public address — the machine built this session has one installed right next to the app.

That's because the database machine from Foundations is in the old network, and this one is in the new network and can't reach it — building a private database tier here would be a whole topic of its own. What replaces it: a **managed database**, one AWS runs for you instead of a machine you install Postgres on and look after yourself — its own topic, coming up next.

## What's Next

| Today | Next lesson |
|---|---|
| Decision five (role and instance profile), the two ways to install the app, secrets fetched at boot, and the disposable machine — three of five app requirements already true, health checks and logs still open | The database moves off this machine for good, onto a managed database — Amazon RDS |

## After Class

Optional practice and Q&A held after the main lecture, ending in `destroy`:

- **Repeat it end to end** — the five decisions, the security group, the boot script — and reach the app over SSH.
- **Prove it's disposable** — `destroy`, then `apply`. If the machine comes back and the app answers on it, you have it.
- **Then stretch** — point the script at **your own app** instead of the demo app. Working from the demo app is fine while yours is still coming together, but the moment your script installs your app is the moment this stops being something you watched.

**What you know now:** a machine gets its own identity in AWS through a role — who may assume it — and an instance profile, the object actually attached to the machine, and only with that identity is it allowed to fetch a secret from Secrets Manager instead of carrying anyone's personal keys. The app gets onto a fresh machine one of two ways: a script that installs it at boot, current every time but slow to start, or a custom image with everything already on it, fast to start but only as current as the last rebuild — which one a real team picks is a fact about how often they ship, not about which tool is better. A secret never lives in the script, the image, or a value you typed in — the machine fetches it itself at boot, using the identity decision five gave it, and hands it to the app as an ordinary environment variable. `terraform destroy` and `terraform apply` prove the machine is disposable, and that's what turns "start on boot, listen on a port, read config from the environment" from accidents into requirements — along with two the app doesn't do yet: answer a health check that reports on itself and nothing further away, and send its logs somewhere that outlives the machine. The database sitting on this machine, next to the app, is wrong on purpose — it's a placeholder for a managed database, which is where this unit goes next.

---

# Lesson 35: The Data Tier — Amazon RDS, Managed Databases & Moving Your Data

## Two App Servers Means Two Separate Databases

Postgres has been on the app server because the boot script installs it there, every time the server is built. That was fine with one server. It stops being fine with two: the second server runs the same boot script, so it installs its **own** Postgres — an order saved on one server does not exist on the other. Two app servers pointed at two different databases is not high availability, it's two different apps that happen to look the same.

**Your code can rebuild the server. It cannot bring back your data.** Prove it to yourself:

```sql
-- put one row in, with your own name in it
INSERT INTO trades (symbol, note) VALUES ('AAPL', 'Kurmanbek');
```

```bash
terraform destroy   # then   terraform apply
```

```sql
SELECT * FROM trades;
-- 0 rows, or an error that the table does not exist. Your row is gone.
```

The server came back because a file describes it. The row didn't, because **no file describes your data**. Keep running `destroy` — it's what keeps the bill small. The fix isn't to stop destroying servers; it's to move the data somewhere a `destroy` can't reach.

## Five Jobs Have to Be Done, Wherever a Database Lives

| Job | What it means |
|---|---|
| 1. Install and patch the engine | Postgres itself, and every security update to it |
| 2. Back up, and prove the restore | A backup nobody has restored is not a backup |
| 3. Keep it serving when the machine dies | Hardware fails. Something has to answer for that |
| 4. Hold the password out of the code | The application needs it. The repository must not have it |
| 5. Report whether it is healthy | Somebody has to be able to see that it is in trouble |

**Managed** means another company does jobs from this list, and you cannot log in to the machine. It's not a quality level and not an easier version of the same database — it's a different division of labor.

## You Did Four of These Yourself. The Fifth Had No Answer

| Job | What you actually ran |
|---|---|
| 1 · install and patch | `dnf install postgresql-server`, `initdb`, `systemctl enable` |
| 2 · back up and restore | `pg_dump`, then `\dt` on the other side to prove it came back |
| 3 · survive the machine dying | Nothing. If that server was lost, the database was lost with it |
| 4 · hold the password | Secrets Manager, read by the machine's own identity at boot |
| 5 · report health | `systemctl status`, `ss \| grep 5432` — you, looking |

The one the room found the hard way: `pg_dump` carries **no users and no roles**. `pg_dumpall --globals-only` is what carries those.

Moving Postgres to its own server, on its own, only solves job 3 — if the app server dies, the database keeps running, because it's no longer on that machine. The other four don't change: you still install it, still patch it, still back it up, still watch it, and now on **two machines instead of one**. That's why we don't stop there.

## What a Managed Database Takes Away From You

| Loss | What it means |
|---|---|
| **No superuser** | Your account is powerful, but it isn't the Postgres superuser. Some extensions and commands are closed to you |
| **No access to the operating system** | There's a machine and an OS underneath, but no SSH, no shell, no log file to read on disk |
| **No `postgresql.conf`** | The same settings exist, but you change them through a **parameter group** instead of editing a file |
| **More per hour** | The same size of machine costs more as a managed database than as a raw server |

If you need something at the operating-system level on the database machine, a managed database is the wrong answer, and you run it yourself.

## Four Ways to Run a Database, and the One We Use

| Option | Who does the five jobs |
|---|---|
| On a server you own | You. This is what you've been doing |
| A managed relational service | The cloud provider. **Amazon RDS** is this one |
| Hosted Postgres from a vendor | A company that only does databases — not AWS |
| A re-engineered engine | Rebuilt underneath, still speaks Postgres. **Aurora** is this one — not our topic |

**Ours is Amazon RDS for PostgreSQL.** The same PostgreSQL, the same SQL, the same `psql`, the same `pg_dump`, your schema, your roles and grants, your app's driver. Nothing you learned stops being true.

## An RDS Instance Is Not an EC2 Instance

It's called an instance, but it isn't one of your machines — there is nothing in your account to log in to.

| | What's true of it |
|---|---|
| **no SSH** | There's no key pair, and you didn't miss a step. Nothing is listening for you |
| **no shell** | You cannot run a command on it. You talk to it in SQL, and nothing else |
| **a hostname** | A name that points at wherever AWS is running it. AWS calls this the **endpoint** — a hostname here, not a URL path |
| **port, user, password** | Exactly what `psql` has always wanted from you |

## Availability Zones and the Subnet Group

**Availability zone** (often written AZ) — its own power and its own cooling, inside the same region, joined to the other zones by fast private cable. A region is made of several of them. Your subnets already sit in one zone or another — you've just never had to care which.

You hand RDS subnets in **two** zones, and AWS will not accept a subnet group whose subnets are all in the same zone. The database itself is a single machine running in a single zone — the second zone is just somewhere for it to move to later, if a standby is turned on.

## A Database Needs Nothing From the Internet

It never browses. It never downloads. Nobody outside your network should be able to reach it. So give it subnets with:

- **no route to the internet** — nothing outside can start a conversation with it, and it can't start one either
- **no NAT gateway** — a NAT gateway exists so private machines can reach *out*. This one has no reason to, and a NAT gateway isn't cheap
- **no public address** — AWS calls this *not publicly accessible*. The only things that can reach it are inside your network

And of the things that are inside your network, only your app servers may reach it, on the Postgres port. You'd normally allow an address range for that rule — name the app servers' **security group** instead. Servers get replaced and their addresses change; the group doesn't.

## Everything You Choose When You Create It

| What you choose | What it means |
|---|---|
| Engine and version | PostgreSQL, and which release |
| Size and storage | The smallest one is fine for this |
| Which subnets | The subnet group — two zones, no route out |
| Who may reach it | The app servers' group, port 5432 |
| When it may be patched | A weekly window you pick. **That's job 1, handed over** |
| How long backups are kept | A number of days. **That's job 2, handed over** |

Two of the five jobs stop being work and become **settings you choose once**. It takes about ten minutes to build.

## The Master Password Ends Up in the State File

One of those choices is the master password. Terraform writes everything it creates into the state file, and the password goes in as **plain text** — however you produced it. Typing it, reading it from a variable, generating a random one: all three end the same way.

- **Protect the state file** — yours is already in S3. Encrypt the bucket and let only the people who run Terraform read it. Anyone who can read state can read every password in it.
- **Or never put it there** — `manage_master_user_password` hands the job to RDS. It creates the password, keeps it in Secrets Manager, rotates it, and your state file never sees it.

This is true of every secret Terraform touches, not only this one. The state file is as sensitive as the things inside it.

## Prove You Can Reach It Before You Move Any Data

```bash
# from the app server, in this order
nc -vz <the endpoint> 5432

psql 'host=<the endpoint> port=5432 dbname=investment_app user=investment_app sslmode=require' \
  -c "SELECT version();"
```

| Result | What it tells you |
|---|---|
| `nc` fails | Nothing is listening for you — the security group rule, or the database and the server aren't in the same network |
| `nc` works, `psql` fails | The network is fine. Now it's the user, the password, or the database name |

Run these from the app server, not from your laptop — the app server is the thing that has to reach it.

## The Connection: Five Pieces of Information

`host`, `port`, `user`, `password`, `database name` — together called **the connection**. Every application has them written into it somewhere: a configuration file, environment variables it reads, or a line of code.

When the database moves, the host is wrong and something has to change it. Changing what an application does is **the developer's job**, not the platform engineer's — in this room, Claude is the developer.

## Find Which Case Your App Is

| Case | What happens |
|---|---|
| **Nothing changes** | It already reads the host from a variable. The boot script writes a different value into the same variable |
| **One line changes** | It has `localhost` written into it. Claude changes it to read the host the way it already reads the password |
| **A real change** | It keeps its data in a file rather than in Postgres — a different path, covered below |

The way the app gets its settings never changes: the boot script fetches them and writes them where the app already looks. **Job 4 stayed yours** — keeping the password out of the code is still your work.

## The Whole Connection Lives in One Secret

Your boot script already fetches a secret from Secrets Manager. That secret now holds all five pieces — host, port, user, password, database name — and Terraform puts the host in, because Terraform created the database and knows its address.

A hostname isn't secret. It lives there because *that's where the rest of the connection already is* — one place to look, one thing to change when it moves.

## Moving the Data, Once, By Hand

```bash
# from the app server. the same connection line as setup.
pg_dump -h 127.0.0.1 -U investment_app -d investment_app -f app.sql

psql 'host=<the endpoint> port=5432 dbname=investment_app user=investment_app sslmode=require' \
  -f app.sql

psql 'host=<the endpoint> port=5432 dbname=investment_app user=investment_app sslmode=require' \
  -c "SELECT * FROM trades;"
```

Without `-h 127.0.0.1`, `pg_dump` connects over the local socket, where PostgreSQL requires your Linux user name to match the database user name — and you're logged in as `ec2-user`. The row with your name in it, from the start of setup, is inside the dump file and is in the new database after the restore.

No tool, no script, nothing automated. **Once, by hand.** This is the only time your data moves.

## If Your App Keeps Its Data in a File, There's Nothing to Dump

Some apps store their data in a file on the server instead of in Postgres — that file *is* the database, and it has no host to point somewhere else.

1. **Claude changes the application** to speak to PostgreSQL instead
2. **It creates your tables** in the new database, empty
3. **Same place as everyone else**, from here on

Your old rows don't come with you, and that's fine — it's practice data you made yourself.

## Take Postgres Off the App Server for Good

```bash
# in the boot script — the database server goes, the client stays
- dnf install -y postgresql16-server   # remove
- postgresql-setup --initdb            # remove
- systemctl enable --now postgresql    # remove
+ dnf install -y postgresql16          # keep the psql client

terraform destroy   # then   terraform apply
```

This is the win: your app is running on a server that **has never had a database on it**, and the row with your name in it is still there.

## The Health Check Still Must Not Ask the Database

A health check answers one question: is this server able to serve? If it queries the database to decide, a slow database makes **every server report itself as dead at the same moment**, and one problem becomes a total outage. Check what this machine is responsible for, and nothing further away.

AWS publishes whether the database is up, and its basic numbers — that's half of job 5, handed over. Deciding what counts as unhealthy, and being told about it, is its own topic and isn't answered here.

## RPO and RTO: The Two Questions That Decide Everything

Before choosing any of what follows, answer both for the app you built — not in general, for yours:

| Question | What it decides |
|---|---|
| **How much data can you afford to lose?** | An hour of orders? A day? This decides how often backups happen. The real term is **recovery point objective**, RPO |
| **How long can you afford to be down?** | Ten minutes? A morning? This decides what you build, not what you back up. The real term is **recovery time objective**, RTO |

A hospital can't restore from yesterday. An airline is busy at every hour, so there's no safe time to be down. The numbers come from the business, and the engineering follows them.

## Backups, Snapshots & Point-in-Time Recovery Are Three Different Things

| | What it is |
|---|---|
| **Automated backup** | Runs on a window you set and **expires** after the number of days you chose. You don't take it; it happens |
| **Snapshot** | One copy, taken by you, that **stays until you delete it** — the same word you used for disks |
| **Point-in-time recovery** | Go back to **a moment** inside the retention window, not to a copy someone took |

This is **job 2**, the one you proved by hand. It's running from the moment the database exists, and you didn't have to remember.

## Restoring Gives You a New Database, Not the Old One Back

All three behave the same way when you restore: you get a **new database with a new hostname**, running beside the one you already have. Nothing is ever put back in place.

So recovery is three steps, not one: restore it, check it's right, then *point the app at the new hostname*. That's why the hostname lives in the secret and not in a file that rebuilds the server.

## A Standby Survives the Machine Dying — Job 3

Turn it on and AWS keeps a full copy of your database in the other zone, always up to date. If the machine running your database fails, the standby becomes the database — **and the hostname doesn't change**, so your app never knows.

This is **job 3** — the one that had no answer when the database was on your own server. Watch this one; don't build it. A standby is a second database and it roughly doubles the price.

## Read Replicas Are for Reading — Standbys Are Not

You cannot read from the standby; it has no address you can connect to. A **read replica** is a different thing: a copy with its own hostname that you *can* read from — and it **lags**, so a value you just wrote may still show the old one.

Neither of these is something you create tonight. Both are extra databases, and both bill by the hour from the moment they exist.

## You Never Destroy a Production Database

That's the rule, and it's the reason the data had to move off a server you throw away. A **development** database is a different matter — and even then, if you're not certain, take a backup first.

This one exists so you can learn on it, and it bills against your credits for as long as it runs. Two ways to stop paying for it:

- **Stop it** — a database can be stopped for **up to seven days**, then it starts itself again. You stop paying for the machine; storage and snapshots still cost a little
- **Snapshot it, then delete it** — the snapshot keeps your data. When you need the database again, restore it, and you'll get a **new hostname**, exactly as above

Deleting a database asks you one more question: **take a final snapshot first?** On this one you skip it. On a production database you always take it.

## Five Jobs. Where Each One Went

| The job | Who does it now |
|---|---|
| Install and patch the engine | AWS, inside a window you choose |
| Keep it serving when the machine dies | AWS, if you turn the standby on |
| Back up, and prove the restore | AWS takes them. **Proving the restore is still yours** |
| Report whether it is healthy | AWS publishes the numbers. **Deciding what's wrong is still yours** |
| Hold the password out of the code | You. This one didn't move |

Two moved, two moved halfway, and one stayed with you. That's what "managed" bought you, and now you can say exactly what it costs.

---

# Lesson 36 — The Cutover: Moving Your Data, Reading a Route Table & When It Goes Wrong

## Where We Left Off

The database exists: RDS, in your private subnet group, closed off from the internet, reachable only from the app servers' security group on port 5432. Tonight is the rest of the story — reading the network well enough to say *why* it's private instead of taking the name's word for it, moving the real rows across, and the moment the whole exercise pays off: the server that used to hold your database no longer does, and nothing was lost.

## Only the Route Table Tells You Whether a Subnet Is Public or Private

The name proves nothing — you can call a subnet `public-a` and give it no route to the internet. The address range proves nothing either, because every subnet sits inside the VPC's range and a VPC is never given internet addresses itself. The only real answer is in the subnet's route table, on the row for `0.0.0.0/0`.

| That row... | Reads as |
|---|---|
| points at an **internet gateway** | **Public.** Something on the internet can open a connection to a server in this subnet |
| points at a **NAT gateway** | **Still private.** A server here can reach out and get an answer back. Nothing on the internet can open a connection to it |
| doesn't exist | **Private.** Nothing goes out and nothing comes in. This is what your database subnets are |

Every route table also carries a `local` line that AWS puts there and you can't remove. It means the address is inside this VPC, so the traffic stays inside — **it is not a route to the internet**, and it's the line people mistake for one.

## Reach It Before You Move Anything: nc, Then psql, In That Order

The same two commands from setup, run again with intent this time — proving the path before trusting it with real rows:

```bash
# from the app server, in this order
nc -vz <the endpoint> 5432

psql 'host=<the endpoint> port=5432 dbname=investment_app user=investment_app sslmode=require' \
  -c "SELECT version();"
```

| Result | What it tells you |
|---|---|
| `nc` fails | Nothing is listening for you — the security group rule, or the database and the server aren't in the same network |
| `nc` works, `psql` fails | The network is fine. Now it's the user, the password, or the database name |

Run both from the **app server**, not your laptop — the app server is the machine that actually has to make this connection, every time it starts.

## The Environment File Is the Only Thing That Changes

Everyone in the room runs the same repository now, so the answer is the same for all of you: the app reads all five pieces of the connection — host, port, user, password, database name — from one file, and the boot script writes that file. The app reads it exactly once, when it starts.

```bash
# /etc/investment-app.env, written by the boot script
DB_HOST=127.0.0.1          # the only line that changes
DB_PORT=5432
DB_NAME=investment_app
DB_USER=investment_app
DB_PASSWORD=…              # fetched from Secrets Manager at boot
```

The way the app gets its settings never changes: the boot script fetches them and writes them where the app already looks. **Job 4 stayed yours** — keeping the password out of the code is still your work, no matter which machine the database is on.

## Move the Data, Once, By Hand

```bash
# from the app server. the same connection line as the reach check.
pg_dump -h 127.0.0.1 -U investment_app -d investment_app -f app.sql

psql 'host=<the endpoint> port=5432 dbname=investment_app user=investment_app sslmode=require' \
  -f app.sql

psql 'host=<the endpoint> port=5432 dbname=investment_app user=investment_app sslmode=require' \
  -c "SELECT * FROM trades;"
```

Without `-h 127.0.0.1`, `pg_dump` connects over the local socket, where PostgreSQL requires your Linux user name to match the database user name — and you're logged in as `ec2-user`. No tool, no script, nothing automated. **Once, by hand.** This is the only time the data moves.

## The Cutover: Edit, Restart, Buy One More Share

The dump is restored on the new database. The app is still talking to the old one, because it only read the environment file once, back when it booted.

```bash
# on the app server, after the data is in the new database
sudo vi /etc/investment-app.env     # DB_HOST=127.0.0.1  becomes  DB_HOST=<the endpoint>

sudo systemctl restart investment-app
```

Editing the file changes nothing on its own — **restarting is what makes the app read it again.** How you know it actually worked: refresh the page and buy one more share. The new database now has your old rows *and* the new one. The database still running on the app server keeps the number it had before, and it will never change again — that gap between the two counts is the proof the cutover happened.

## The Host Belongs in the Secret — But Not Yet

The boot script already fetches a secret from Secrets Manager to get the database password. The host belongs in that same secret, put there by Terraform, because Terraform created the database and knows its address. A hostname isn't secret — it goes there because *that's where the rest of the connection already is*: one place to look, one thing to change when the database moves again.

You just changed the host by hand, in the file on the server. That works once. The boot script writes that file from scratch on every new server, so **a rebuilt server goes back to looking for a database on itself.** The repository doesn't do this yet — making the boot script read the host from the secret is your work now, not something already built for you. A literal hostname written into the boot script itself isn't the fix either: editing the boot script replaces the machine, which is exactly what a restore already forces — the secret is the one place that survives a rebuild.

## Take Postgres Off the Server — With the Right Command

```diff
# in the boot script — the database server goes, the client stays
- dnf install -y postgresql16-server   # remove
- postgresql-setup --initdb            # remove
- systemctl enable --now postgresql    # remove
+ dnf install -y postgresql16          # keep the psql client

terraform apply   # user_data_replace_on_change = true, so you get a new server
```

**Do not run `terraform destroy` here.** The database now lives in the same folder as the app server, in its own file — and it's set to skip its final snapshot. `destroy` would take the database down with the server, undoing the exact move you just finished by hand. `apply` alone is enough: the repository already sets `user_data_replace_on_change = true`, so changing the boot script is enough to force a fresh machine, with an explicit line telling Terraform never to touch the database.

This is the win: your app is running on a server that **has never had a database on it**, and the row with your name in it is still there.

## Then: Backups, a Standby, and the Rule About Production

The rest of the night answered the question a working database still raises: what happens when it, or the machine under it, gets damaged? Two numbers decide the answer for your own app — **RPO**, how much data you can afford to lose, and **RTO**, how long you can afford to be down. An **automated backup** runs on a schedule and expires; a **snapshot** is one you take yourself and it stays until you delete it; **point-in-time recovery** goes back to a moment, not a copy. All three hand you back a *new database with a new hostname* when you restore — never the old one, in place — which is exactly why that hostname lives in a secret and not in a file that rebuilds the server. A **standby** answers the job a lone server never could: the machine dies, the standby takes over, and the hostname doesn't move. A **read replica** is the different tool for reading — its own hostname, its own lag. And the rule underneath all of it: you never destroy a production database. You stop it, or you snapshot it and delete it — never the other way around.

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor. Most of tonight's after-class time went to one ladder, run over and over until it was automatic:

- **`nc`, then `psql`, in that order** — on your own endpoint, until a failure at either step tells you immediately which half is broken.
- **Read your own route tables** — find the row for `0.0.0.0/0` on your public and private subnets, and say out loud which kind each one is before checking.
- **Run the cutover for real** — edit your own environment file, restart your own service, and prove it with a change only the new database could show.
- **Say why `terraform apply` alone is now correct** — and what `terraform destroy` would take with it, now that `database.tf` shares the folder.

**What you know now:** a subnet's name and address range tell you nothing about whether it's public — only the route table's `0.0.0.0/0` row does, and a `local` row is never a way out. `nc` before `psql` isolates a network failure from a credentials failure in one step each. The connection lives in one environment file the boot script writes and the app reads once at boot, so a cutover is exactly two actions — edit the file, restart the service — proven by a change the old database can't show. The data itself crosses exactly once, by hand, with `pg_dump` and `psql -f`. The host belongs in the same secret as the password, but the repository doesn't fetch it from there yet — that's your work, not a gap in what you were given. And once a database shares a Terraform folder with the server, `destroy` is no longer a safe reset — `apply` alone, backed by `user_data_replace_on_change`, is what rebuilds the server without touching the data you just spent the night moving.

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **The whole move, on your own account** — your own subnets, your own database, your own connection changed. Find how your app does it; no two of these apps are the same.
- **Stop paying for it when you finish** — stop the database, or take a snapshot and delete it. Don't leave it running and forget it — it's on your standing check of what's costing you money.
- **Then prove the restore, for real** — next time you need it, restore from your own snapshot. Connect, run `\dt` and `\du`, and put the **new hostname** into your secret.

**What you know now:** a database needs five jobs done no matter where it lives — install and patch the engine, back it up and prove the restore, keep serving when the machine dies, hold the password out of the code, and report whether it's healthy — and "managed" means another company does some of them from a list, not a quality level. Amazon RDS is not an EC2 instance: no SSH, no shell, only a hostname (the **endpoint**), a port, a user and a password, running across a subnet group that spans two availability zones even though the database itself lives in one. The database needs nothing from the internet, so its subnets get no route out, no NAT gateway, and no public address, and only the app servers' security group is allowed to reach it. The master password Terraform sets lands in the state file as plain text unless `manage_master_user_password` keeps it out entirely — the state file is as sensitive as the secrets inside it. The connection — host, port, user, password, database name — lives together in one secret, and moving it is the developer's job: change what the app reads, not what the platform runs. The data itself moves exactly once, by hand, with `pg_dump` and `psql -f`, after which Postgres comes off the app server's boot script for good. Backups, snapshots, and point-in-time recovery are three different things, but all three hand you back a **new database with a new hostname** — recovery is restore, verify, then repoint, never an in-place fix. A standby answers job 3 by keeping the hostname stable when the machine dies; a read replica is a separate, laggy copy you can actually query. You never destroy a production database — you stop it or snapshot it — and by the end, two of the five jobs have moved to AWS, two moved halfway, and one, the password, never left you.

---

# Lesson 37 — When It Breaks, and When It Can't Answer: Backups, Standbys & the Health Check

## Where We Left Off

The cutover from last session proved itself: edit the environment file, restart the service, and a row count that only the new database could show. The database now lives in RDS, off the app server for good. Two questions were still open. First, the one a working database always raises next — what happens when it, or the machine under it, gets damaged? Second, one that has nothing to do with the database at all: a machine can be reported as running and still be unable to answer a single request.

## The Health Check Still Must Not Ask the Database

A health check answers exactly one question: is this server able to serve? If it queries the database to decide, a slow database makes every server report itself as dead at the same moment, and one problem becomes a total outage. Check what this machine is responsible for, and nothing further away.

AWS already publishes whether the database itself is up, along with its basic numbers — that's half of **job 5**, handed over the moment you moved to RDS. Deciding what counts as unhealthy for your own application, and being told about it, is a different topic — the one the rest of this lesson builds toward.

## Two Questions Decide Everything: RPO and RTO

Before choosing anything that follows, answer both for the app you built — not in general, for yours.

| Question | What it decides |
|---|---|
| **How much data can you afford to lose?** | An hour of orders? A day? This decides how often backups happen. The real term is **recovery point objective**, RPO |
| **How long can you afford to be down?** | Ten minutes? A morning? This decides what you build, not what you back up. The real term is **recovery time objective**, RTO |

A hospital can't restore from yesterday. An airline is busy at every hour, so there's no safe time to be down. The numbers come from the business, and the engineering follows them.

## Backups, Snapshots & Point-in-Time Recovery Are Three Different Things

| | What it is |
|---|---|
| **Automated backup** | Runs on a window you set and **expires** after the number of days you chose. You don't take it; it happens |
| **Snapshot** | One copy, taken by you, that **stays until you delete it** — the same word you used for disks |
| **Point-in-time recovery** | RDS does this. Go back to **any moment** inside the retention window, not to a copy someone took — it ships the transaction log to S3 every five minutes |

This is **job 2**, the one you proved by hand with `pg_dump`. It's running from the moment the database exists, and you didn't have to remember.

## Restoring Gives You a New Database, Not the Old One Back

All three behave the same way when you restore: you get a **new database with a new hostname**, running beside the one you already have. Nothing is ever put back in place.

So recovery is three steps, not one: restore it, check it's right, then *point the app at the new hostname*. That's exactly why the hostname lives in the secret and not in a file that rebuilds the server.

## A Standby Survives the Machine Dying — Job 3

Turn it on with `multi_az = true` and AWS keeps a full copy of your database in the other availability zone, always up to date. If the machine running your database fails, the standby becomes the database.

| What the failover does | What your application sees |
|---|---|
| The hostname stays the same | Nothing to edit, nothing to redeploy |
| Open connections are dropped | Every live connection breaks and has to be made again |
| It takes 60 to 120 seconds | Requests fail for that long — this is not invisible |
| Nothing moves back afterward | The promoted standby stays the database. The machine that failed returns as the new standby |

This is **job 3** — the one that had no answer when the database lived on your own server. Watch this one; don't build it. A standby is a second database, and it roughly **doubles the price**.

## Read Replicas Are for Reading — Standbys Are Not

The standby has no address you can connect to. A **read replica** is a different thing: a copy with its own hostname that you *can* read from — and it **lags**, so a value you just wrote may still show the old one.

A third shape has its own name, a **Multi-AZ DB cluster**: one writer and two readers across three zones, behind one set of endpoints. Named here, not built. You build none of these tonight — each one is an extra database, billing by the hour from the moment it exists.

## You Never Destroy a Production Database

That's the rule, and it's the reason the data had to move off a server you throw away. A **development** database is a different matter — and even then, if you're not certain, take a backup first.

Two ways to stop paying for a database you're done with:

- **Stop it** — a database can be stopped for **up to seven days**, then it starts itself again. You stop paying for the machine; storage and snapshots still cost a little.
- **Snapshot it, then delete it** — the snapshot keeps your data. When you need the database again, restore it, and you'll get a **new hostname**, exactly as above.

Deleting a database asks you one more question: **take a final snapshot first?** On a practice database you can skip it. On a production database you always take it.

## Five Jobs. Where Each One Went

| The job | Who does it now |
|---|---|
| Install and patch the engine | AWS, inside a window you choose |
| Keep it serving when the machine dies | AWS, if you turn the standby on |
| Back up, and prove the restore | AWS takes them. **Proving the restore is still yours** |
| Report whether it is healthy | AWS publishes the numbers. **Deciding what's wrong is still yours** |
| Hold the password out of the code | You. This one didn't move |

Two moved, two moved halfway, and one stayed with you. That's what "managed" bought you, and now you can say exactly what it costs — the data tier is done.

## More Than One App Server

One address in front of two machines, a check that decides which machine receives requests, and a group that keeps the number of machines running — that's the whole shape of what's ahead. An **Application Load Balancer** in front of a second app server, and an **Auto Scaling group** to keep the right number of them running, are named here and built later. What gets proven tonight is the thing they both depend on: deciding, correctly, whether a single machine can actually serve.

## Running Is Not Answering

Some of you have already had a site stop answering while the machine was fine. You opened the page and nothing came back. You connected to the machine over SSH and it was perfectly healthy — you could type on it, the console said `running`, nothing looked wrong.

What had happened: the application on it had died. **The machine kept reporting that it was running.** A machine can be running and still be unable to answer a request.

## Two Different Facts About One Machine

| | Who answers it |
|---|---|
| **Is it running?** | EC2. It's a fact about the machine |
| **Can it answer a request?** | Only the application. It's a fact about the software on the machine |

Two commands, one for each question, run from the app server itself:

```bash
# is the service running? — this asks EC2's view of the machine
sudo systemctl is-active investment-app

# can it answer a request? — this asks the application itself
curl -i localhost:PORT/HEALTH_PATH
```

## A Health Endpoint Is a Path. A Health Check Is Someone Asking For It.

**Health endpoint** — a small path your application serves for one purpose: to answer that it's working. It does no other job.

**Health check** — something outside the machine asking for that path, on a timer, and keeping score of the answers.

## An Application Can Die While Its Machine Keeps Running

```bash
sudo systemctl stop investment-app
# the instance state stays running. The console still says running.

sudo systemctl start investment-app
```

Stopping the service doesn't touch EC2's view of the machine at all — the console keeps saying `running` the whole time. Only a request to the health path shows the difference.

## The Five Settings a Health Check Has

| Setting | What it means | If you set nothing |
|---|---|---|
| **Path** | The path asked for | `/` |
| **Interval** | How long between one check and the next | 30 s |
| **Timeout** | How long to wait for an answer before that single check counts as a failure | 5 s |
| **Unhealthy threshold** | How many failures in a row before the machine is taken off the list | 2 |
| **Healthy threshold** | How many successes in a row before it's put back on | 5 |

These five are the whole configuration. Nothing else decides whether a machine is on the list or off it.

## Counting Failures Until the Machine Comes Off the List

Picture a check firing every interval. Two checks answer 200, so the count of consecutive failures stays at nought. The next check answers nothing before the timeout runs out, so the count becomes 1. The check after that fails too — the count reaches **2**, and 2 is the unhealthy threshold, so the machine comes off the list. **A check that times out is a failed check**, counted exactly like an error code — silence and an error move the count the same way.

## What Counts as an Answer, and What Doesn't

| Response | Result |
|---|---|
| **200** | The check **passes**. Unless you configured other codes, 200 is the only one that does |
| **A redirect** | The check **fails** — the console calls it `Target.ResponseCodeMismatch` |
| **No answer at all** | The check **fails** — the timeout ran out; the console calls it `Target.Timeout` |

A failed check is a failed check either way. A redirect and a silence both count toward the unhealthy threshold, exactly like an error code does.

## An Application Has to Listen on Every Address the Machine Has

```bash
# on your own app server — what's listening, and on which address
ss -tulnp
# the number before the colon is the address it accepts connections on
0.0.0.0:80      → every address this machine has. A check from outside reaches it.
127.0.0.1:5432  → this machine only. Nothing outside can ask it anything.
```

The check comes from **outside** the machine, so an application listening only on `127.0.0.1` fails every check while looking perfectly healthy from a shell on the box itself.

## Why More Than One, Asked About Nine Real Industries

The matrix exercise ran four questions across nine real industries, one cell at a time: who uses it, when it peaks, could one server do it, and what stops if it dies. Then back to your own account: **you have exactly one machine, and it is the whole site** — exactly the gap the health check, the load balancer, and the Auto Scaling group close, in that order, starting next session.

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **Turn the backups on** — automated backups are off on the database you built. Choose a retention period, and a maintenance window in the hours your own application is least busy.
- **Try the standby once** — add `multi_az = true` to the database resource and apply it. It's a second database at roughly double the cost, so turn it off again once you've seen it.
- **Ask your app the two questions** — on your own server: `systemctl is-active`, then `curl -i localhost:80`. Break it on purpose, watch the two answers disagree, then put it back.

**What you know now:** two numbers — RPO, how much data you can afford to lose, and RTO, how long you can afford to be down — decide everything about how a database is protected, before any tool gets chosen. Backups, snapshots, and point-in-time recovery are three different things, but all three hand you back a **new database with a new hostname**, never the old one in place. A standby answers job 3 by keeping the hostname stable through a 60-to-120-second failover when the machine dies; a read replica is a separate, laggy copy you can actually query, and a Multi-AZ DB cluster is a third shape, named but not built. You never destroy a production database — you stop it or snapshot it first. And a machine being **running** and a machine being **able to answer** are two separate facts, answered by two separate things — EC2 for one, a health endpoint for the other — checked on a timer with five settings (path, interval, timeout, unhealthy threshold, healthy threshold) that decide, on their own, whether a machine stays on the list. A timeout counts as a failure exactly like a wrong status code does, and none of it works if the application only listens on `127.0.0.1` instead of every address the machine has.

---

# Lesson 38: More Than One App Server — the Application Load Balancer

## Where We Left Off

Last session proved the difference between a machine that's running and a machine that can answer, and named the gap it opens: one machine is the whole site. Two things were named but not built — the Application Load Balancer and the Auto Scaling group. Tonight builds the first one, plus the piece of Terraform that makes a second machine possible at all: `for_each`.

## `for_each` Has Been in Your Files Since the Network

`for_each` repeats one resource block once per entry in a set you give it — no chapter had taught it, even though it was already sitting in your Terraform since the networking unit.

```hcl
for_each = {
  frontend = "red"
  backend  = "green"
  worker   = "blue"
}

name = each.key                 # frontend, backend, worker
tags = { color = each.value }   # red, green, blue
```

Add a line, get a resource. Delete a line, Terraform destroys that one and leaves the others alone. Yours has two entries, one per public subnet, so the two app servers land in two different availability zones.

## Turning One Machine Into a Set Proposes Destroying It

Terraform identifies a resource **by its name**. Change how a resource is named — a single `aws_instance.app` becoming an `aws_instance.app` with `for_each` — and Terraform sees a different resource. `terraform plan` proposes destroying the old one and creating the new ones in its place.

That's fine here. These app servers hold no data. Replacing one costs boot time and nothing else — and that's only true because the database moved off them onto RDS last session.

## Two Machines Have Two Addresses. A Customer Has One Name to Type.

Two app servers means two addresses, and nothing yet decides which one a request reaches. A customer types one domain name. Something has to sit between that name and the two machines and choose.

## An Application Load Balancer Is One Address That Hands Off to a Machine That Can Answer

**Application Load Balancer (ALB)** — one address that accepts requests, keeps a list of the machines behind it, and gives each request to one machine that is currently answering.

## Four Kinds of Load Balancer, and Yours Reads HTTP

| Kind | What it works on | What it is for |
|---|---|---|
| **Application** | HTTP and HTTPS | Reads the request, so it can route on the host name or the path. **Ours.** |
| **Network** | TCP | Faster and simpler. Does not read the request. |
| **Gateway** | Traffic passing through | Sends traffic to inspection appliances. |
| **Classic** | The old one | Still in real accounts you'll inherit. Not used for new work. |

Ours is **internet-facing** rather than internal, because the customers are outside.

## Which of the Four You'll Actually Meet

Roughly eight in ten load balancers you meet in the real world are Application or Network, and about half of those are Application. **Application** is the one you'll work with most — nearly every website you use is behind one. **Network** is the other one you'll actually meet, used more often between services inside a network than facing customers. **Gateway** and **Classic** are rare enough that working engineers go years without configuring one, or you inherit one someone else built. Learn Application and Network properly; recognize the other two by name and move on.

## The Balancer Is Not a Machine, and It Has No Address You Keep

- **Not a machine** — nothing to SSH into.
- **Two zones, minimum** — one is not allowed.
- **A name, not an address** — you never write an address down; you get a DNS name that AWS owns.

It bills by the hour for existing, plus a usage unit called an **LCU**, a Load Balancer Capacity Unit — not per request.

## A Balancer Has Three Parts, and Each One Has a Name

- **Listener** — the port and protocol the balancer accepts on.
- **Rule** — what the listener consults to decide which target group a request goes to.
- **Target group** — the list of machines, and the health check that decides who is on that list.

You'll type all three of these words into the console, and an interviewer will use all three.

## The Request Goes Straight From the Balancer to One Machine

The part that gets drawn wrong most often: the listener and the rule are **inside** the balancer, and the target group is a list the balancer reads. **None of the three is a machine the request passes through.** One request arrives at the balancer, the balancer consults its listener and rule, reads its target group list, and sends the request straight to the one machine it chose.

## How the Balancer Picks Which Machine

| Algorithm | How it decides |
|---|---|
| **Round robin** (default) | First request to the first machine, second to the second, then back to the first. Doesn't look at how busy either machine is. With two machines running the same application, this is the right answer, and you leave it alone. |
| **Least outstanding requests** | The request goes to whichever machine has the fewest requests still in flight. Worth changing to when some requests take far longer than others. |

This is a setting on the **target group**, not the balancer — the interview word for it is the **routing algorithm**. Neither algorithm ever picks a machine that's off the list. **The health check decides who is on the list; the algorithm only chooses between the machines already on it.**

## What a Rule Routes On, and What a Target Group Can Hold

A **rule** routes on the **host name** or the **path**. It can also answer by itself — a **fixed response**, which serves a maintenance page with no machine behind it, or a **redirect**.

A **target group** can hold **instances**, plain **IP addresses**, or a **Lambda function** — so one balancer can front things that aren't servers at all. Three more settings live on it: **cross-zone** (spread evenly across zones), **stickiness** (one person returns to one machine), and **idle timeout** (how long a quiet connection is held). Access logs to S3 exist and are **off by default** — reading them is a later topic; knowing the setting exists is this one.

## A Load Balancer Does Not Go in Front of Your Database

Your two app servers are interchangeable — neither keeps anything, so a request sent to either gets the same answer, and spreading requests between them is safe. A database keeps the data. Put two behind a balancer and one purchase gets written to one of them; the other has never heard of it, and there's no longer a single true answer to "how many shares do I own." That's why one primary takes every write, and why the standby and read replica from last session aren't a way around it — the standby serves no traffic at all, and a read replica answers reads only.

## One Machine Registers First, So a Second Can't Hide a Problem

Targets register in order: one is added to the target group and has to clear the unhealthy threshold and reach **healthy** before the second is added. That way a healthy first machine can never mask a second one that never comes up.

## Proving Which Machine Answered

Both app servers run the same application and return the same page, so you can't tell which one answered from the response alone — unless the application says so:

```python
import socket

# on GET /health
return {"status": "ok", "server": socket.gethostname()}
```

```bash
curl http://<balancer-dns-name>/health
# {"status":"ok","server":"ip-10-0-1-42"}
curl http://<balancer-dns-name>/health
# {"status":"ok","server":"ip-10-0-2-17"}
```

Two different names in two calls is round robin, seen directly. It's also the quickest way to prove a machine has come off the list: **its name stops appearing.**

## Five Reasons a Target Goes Unhealthy, and the One Check for Each

All five are configuration, not bad luck, and each one has a single check that settles it:

| Why every target is unhealthy | The one check that tells you |
|---|---|
| The health path answers with a redirect | Ask for the path from off the machine and read the status |
| The application listens only on localhost | Check what address it is listening on |
| The security group doesn't let the balancer through | Check the rule from the balancer to the machine, not the reverse |
| The grace period is shorter than the boot | Time how long the machine takes to answer after it starts |
| The health check asks on one port and the application listens on another | Compare the four ports: listener, security group, health check, application |

While you're learning, keep **one port all the way across** — 80 on the listener, 80 in the security group, 80 on the health check, 80 in the application. A port that doesn't match is the most common of the five and the least interesting to debug.

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **Pull main and apply the balancer** — the `alb.tf` written in class is merged. Pull it, then change two things to your own before you apply: the S3 bucket in the backend block, and the key name on the instances.
- **Open the balancer's name, not an IP** — check the target group first. Both targets have to read **healthy** before the name answers. If one doesn't, it's one of the five reasons, and the port is the most likely.
- **Stop hard-coding the database address** — the endpoint was pasted in by hand in class. Take it from the database resource instead, so a rebuilt database doesn't leave the application pointing at an address that's gone.

**What you know now:** `for_each` repeats one resource block per entry in a set, and changing a resource's name — including turning a single instance into a set — makes Terraform propose destroying the old one and building new ones, which is safe here only because these app servers hold no data. An Application Load Balancer is one address, made of three named parts — **listener**, **rule**, **target group** — none of which is a machine the request passes through; it reads from HTTP and HTTPS, one of four kinds of load balancer alongside Network, Gateway, and Classic. The **target group** decides who's on the list, via its health check, and separately decides how to split traffic between them, via its **routing algorithm** — round robin by default, least outstanding requests when work is uneven. A balancer never goes in front of a database, because app servers are interchangeable and a database is not. And when a target goes unhealthy, it's always one of five configuration causes — a redirect on the health path, an address bound to localhost only, a security group blocking the balancer, a grace period shorter than boot time, or a port that doesn't match all the way across — never bad luck.

---

# Lesson 39: The Group That Keeps the Count — EC2 Auto Scaling

## Where We Left Off

Last session built the balancer: one address, three named parts, a health check deciding who's on the list. Two things it exposed were named but not explained — what the balancer actually does when *every* target fails the check, and what happens to a person's login when their next request lands on a different machine. Tonight closes both, then builds the piece that makes a second machine automatic instead of something you type by hand: the Auto Scaling group.

## The Balancer Fails Open — It Never Refuses Everything

| Situation | What happens |
|---|---|
| **Some targets unhealthy** | The balancer sends requests only to the healthy ones. The site keeps answering and nobody outside notices. |
| **All targets unhealthy** | The balancer **sends requests to all of them anyway**. It isn't allowed to refuse every request, so it tries. You see whatever a dead application produces — a **502** if the connection is refused, a **504** if it never answers. |
| **A real 503** | Means something different: the target group has **no registered targets at all**. Not unhealthy machines — no machines. |

AWS calls the middle row **failing open**. Refusing every request is worse than trying a machine that might still answer, so the balancer stops filtering. An unhealthy target is not the same thing as no target.

## `initial` Is Not a Failure — It's the Check Arriving Before the Machine Is Ready

Identical machines built from the same launch template can show different health for one reason: the check ran on one of them before its application finished starting.

**initial** — the target is registered and its first health check hasn't finished. This is not a failure. AWS gives it the reason code `Elb.InitialHealthChecking`.

| Setting | Where it lives, and what it controls | This deck's value |
|---|---|---|
| `interval` | Target group. Seconds between checks on one machine. Range 5–300. | 30 |
| `unhealthy_threshold` | Target group. Failures in a row before the machine is taken out. Range 2–10. | 2 |
| `health_check_grace_period` | Auto Scaling group. Seconds a new machine is left alone before the group judges it. | 300 |

Every machine in the group is built from the same launch template. A split result across two of them is the check arriving early on one, not two machines in different condition.

## An Unhealthy Target and an Error Page Are Two Different Problems

| | What it means |
|---|---|
| **Target unhealthy** | The machine is the problem. The request never reaches the application. |
| **Target healthy, error page** | Something the machine depends on is the problem — most often the database. |

If you still can't reach your own database, this is that same problem again, not a new one. Start by pasting the health status into Claude.

## One Person, One Machine, and the Next Request Lands Somewhere Else

You're not logged in. You put a T-shirt in a basket, close the browser, come back an hour later, and it's still there. Something remembered you, and it wasn't your account.

**stateless** — the machine keeps nothing that the next request needs. So it doesn't matter which machine gets that request.

With two app servers and a balancer choosing between them by round robin, a login held on one machine is invisible to the other. The next request just doesn't know you.

## Sticky Sessions Treats the Symptom. A Shared Session Store Fixes the Cause.

| | What it is |
|---|---|
| **Sticky sessions** | One setting on the target group. The same person keeps going back to the same machine. |
| **What it costs** | That machine failing now takes their session with it, and the machines stop being evenly loaded. |
| **The real fix** | A **shared session store** — the state moves off both machines into something both of them read. Named here; built in a later topic. |

**Connection pooling**, mentioned alongside it: several app servers each hold open connections, and the database allows only a finite number. The tool is **RDS Proxy**. Not built here.

## An Auto Scaling Group Keeps a Stated Number of Machines Running

**launch template** — the recipe a new machine is built from, so something other than a person can make one.

**Auto Scaling group (ASG)** — keeps a stated number of machines running, building each one from that template.

## A Launch Template Is a Definition. Nothing Runs Until Something Builds a Machine From It.

| | |
|---|---|
| **What it is** | Saved answers to the questions the EC2 launch screen asks. It costs nothing and it isn't running. |
| **What it isn't** | Not a machine, and not an AMI. A machine built from it is an ordinary EC2, the same as one launched by hand. |

Two different things build a machine from the same template:

```
# a person, in the console
Actions → Launch instance from template

# the Auto Scaling group, with nobody logged in
launch_template { id = aws_launch_template.app.id }
```

The template **holds** an AMI id. It isn't built from an AMI and it doesn't replace one.

## What a Launch Template Holds Is the Same List You'd Fill In for One EC2

```hcl
# launch-template.tf
resource "aws_launch_template" "app" {
  image_id      = data.aws_ami.al2023.id   # which operating system
  instance_type = var.instance_type        # how big
  key_name      = var.key_name             # which SSH key

  iam_instance_profile { ... }             # what it's allowed to read
  network_interfaces   { ... }             # public IP, security group
  user_data            = ...               # what it installs while booting
}
```

There's no subnet in it. The **Auto Scaling group** holds the subnets, because the group is the one deciding where each machine goes.

## Minimum, Desired and Maximum Are Three Separate Instructions, Not Three Levels

| | What it does |
|---|---|
| **Minimum** | Never go below this. The group builds a machine to stay at it. |
| **Desired** | The number it actually keeps right now. This is the one you change by hand. |
| **Maximum** | Never go above this, whatever else happens. |

Change desired from 2 to 3, and a third machine you never touched starts answering on the same address.

## Changing Desired by Hand Is Scaling — the Same Number a Policy Changes

| | |
|---|---|
| **You change it** | Edit desired in the console or in `asg.tf`. The group builds or removes machines to reach the new number. |
| **A policy changes it** | Same number, moved by a metric instead of a person. Nothing else about the group is different. |

Desired has to sit between the other two — the console refuses `minimum 2, desired 1` before it will create the group. With desired set to 4, two more machines start, register in the target group, pass the check, and take requests. **No policy is involved in any of it.**

## The Group Registers Every Machine It Builds Into the Target Group

```hcl
# asg.tf — the line that joins the two halves
resource "aws_autoscaling_group" "app" {
  target_group_arns = [aws_lb_target_group.app.arn]
}
```

Without that line, the group still builds machines and the balancer never sends them a request. The group registers each one, the health check runs, and only then does traffic arrive.

## When the Group Builds the Machines, the Instance Resource Comes Out of Your Code

| | |
|---|---|
| **Before** | `aws_instance` with `for_each`, plus one `aws_lb_target_group_attachment` for each machine. Two machines exist because the file says two. |
| **After** | `aws_autoscaling_group` with a desired capacity and `target_group_arns`. Machines exist because the group keeps that number. |

Keep both and you have two machines the group doesn't manage, running and billed beside the ones it does. Delete the instance block and the attachments, then apply.

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **Pull main, then point the backend at your own bucket** — `launch-template.tf` and `asg.tf` were pushed during class. The backend block in `providers.tf` still names the bucket used on screen, so `terraform init` fails on the state file until you put yours back.
- **Delete your own instance block** — the group builds the machines now. Leaving `aws_instance` in place leaves two machines running and billed that the group doesn't manage. The `aws_lb_target_group_attachment` resources go with it.
- **Terminate one machine and watch it come back** — the group builds a replacement to hold its desired count. Check the target group while it happens: the new machine reads **initial** first, and only takes requests once it has passed the check.

---

# Lesson 40: Closing the Unit — the Scaling Policy and the Certificate on the Balancer

## Where We Left Off

Last session built the Auto Scaling group: a stated count of machines held automatically, with the `aws_instance` block gone from the code for good. Two things it left sitting were named but not built — a policy that moves the desired count on its own instead of you typing a number, and a certificate that makes your own name answer over HTTPS instead of plain HTTP. Tonight builds both, and the unit is finished.

## The EC2 Status Check and Health Check Type ELB Answer Different Questions

| | What it checks |
|---|---|
| **EC2 status check** | Is the instance alive? The group always uses this. A dead application passes it **forever**. |
| **health check type ELB** | Adds the target group's answer **on top of** the status check. It is not a choice between the two. |

**saturation** — all of the CPU, or all of the RAM, fully used. The process is alive and stops answering anyway.

A machine can saturate while its application is still running, so the EC2 status check keeps passing it. Setting the Auto Scaling group's health check type to ELB gives it the target group's answer as well: that machine goes unhealthy, the group terminates it, and a replacement takes its place — the same replace-on-fail behavior from last session, now driven by whether the application answers instead of just whether the instance is alive.

## A Target Tracking Policy Holds One Number and Moves the Count Both Ways

| Setting | What it does |
|---|---|
| `ASGAverageCPUUtilization` | The predefined metric. Average CPU across the machines in the group. |
| Target value | The number the group holds the metric at. Higher works the machines harder and leaves less spare for a sudden increase. |
| Instance warmup | Seconds before a new machine is counted in that average, so a machine still booting doesn't drag it. |
| The other three | Step, simple and predictive. Scheduled scaling changes the count by clock time and is a scheduled action, not a policy. |

AWS creates and manages the CloudWatch alarms behind the policy. You do not write them, and you do not edit them.

One policy scales both ways: out above the target, in below it. Minimum and maximum still hold — a policy cannot take the group past either.

## The Certificate Goes on the Balancer, and Port 80 Redirects to It

| | |
|---|---|
| **ACM — AWS Certificate Manager** | The certificate is free. It lives in one region and has to be in the **balancer's** region. You validate it once with a DNS record, and it renews itself as long as that record stays. |
| **The redirect, and where HTTPS stops** | A **redirect action** on the port-80 listener sends a request without the `s` back as HTTPS. The balancer decrypts there and forwards to your machines over plain HTTP — **TLS termination**. |

The certificate never reaches your app servers. It sits on the balancer, and the balancer is where the encrypted connection ends.

## What You Can Do Now

| | |
|---|---|
| Tell running from answering | And know which of the two a load balancer can act on. |
| Read a health check | Its settings, and why a new machine is unhealthy at first. |
| Name the parts of an ALB | Listener, rule, target group. |
| Read a failed health check | Five causes, and the one check that tells you which one it is. |
| Say why a machine holds no state | Sticky sessions has a cost; a shared store is the real fix. |
| Keep a number of machines running | A launch template describes a machine; the group holds the count and replaces what stops answering. |

## Before the Next Class

- **Pull main, then put your own domain in** — the certificate and the HTTPS listener were built in the console in class and written to Terraform afterwards. `dns.tf` and `alb.tf` name the instructor's domain. Replace it with yours in the certificate, the validation record and the alias record before you apply, and put your own bucket back in the backend block.
- **Open your own site over http, not https** — type your name with `http://` in front of it. The browser should come back showing `https://` instead. If it stays on port 80 and reads not secure, the redirect action on the port-80 listener is missing. If nothing answers on 443 at all, the balancer's security group is the first thing to check, not the machines.
- **The scaling policy is not in the code** — it was created in the console in class and no `aws_autoscaling_policy` was pushed. Applying from main gives you the ELB health check and the certificate, and the count still only changes when you change `desired` yourself.

Getting stuck is normal. Do not wait for anyone. Read the error message, then Claude in your browser, then Claude in your terminal, then Slack.

**What you know now:** the group's health check can add the target group's answer on top of the EC2 status check, so a saturated machine that's still technically running gets replaced instead of left serving nothing. A target tracking policy holds one metric — usually average CPU — at one target value, moving the desired count both up and down on its own, inside the minimum and maximum you already set; step, simple, predictive and scheduled scaling are named but not built. A certificate from ACM lives on the balancer, not on any app server — it has to sit in the balancer's region, it renews itself off the DNS record that validated it, and a redirect action on the port-80 listener is what sends a plain HTTP request back as HTTPS, with TLS termination happening at the balancer and plain HTTP continuing on to the machines behind it.

**What you know now:** the balancer fails open — when every target is unhealthy it still tries to send requests, producing a 502 or 504, and a real 503 means the target group has no registered targets at all, not unhealthy ones. `initial` is the check arriving before a freshly built machine is ready, not a failure, and it's told apart from a real problem by five settings split across two resources — `interval` and `unhealthy_threshold` on the target group, `health_check_grace_period` on the Auto Scaling group. A target that's unhealthy and a target that's healthy but returning an error page are different problems — one is the machine, the other is usually the database behind it. Statelessness means the next request doesn't care which machine answers it; sticky sessions patches around a machine that isn't stateless, at the cost of uneven load and a session that dies with its machine, where the real fix is a shared session store. An Auto Scaling group keeps a stated number of machines running, built from a **launch template** — a definition that costs nothing until something builds from it — with minimum, desired and maximum as three separate instructions rather than a range, `target_group_arns` as the line that puts every machine the group builds onto the balancer's list, and the `aws_instance` block coming out of your code entirely once the group is what's building machines.

---

# Lesson 41: Metrics, Log Events & the Agent — Reading the System From Outside the Machine

## Where We Left Off

Last session closed out scaling: a policy that moves the machine count on its own, and a certificate that puts the site behind HTTPS. Both sessions leaned on the group replacing a machine that stops answering — but replacing a machine has a cost nobody named yet. Tonight names it: the disk goes with the machine, and CloudWatch is where what matters survives that.

## The Group Deletes a Machine's Disk When It Replaces the Machine

**root volume** — the disk a machine boots from and writes to. AWS deletes it when the instance is terminated, unless you ask for something else.

A machine the group replaces for saturation or a failed health check takes its root volume with it — and any log file the application wrote is gone at exactly the moment you most want to read it, because the machine was replaced for a reason. That is the problem the rest of tonight answers.

## A Metric Is a Number Over Time. A Log Event Is One Line From One Moment.

| | |
|---|---|
| **metric** | A name, and a series of numbers published against it over time. Each number carries a timestamp. You ask for a stretch of time and CloudWatch groups the numbers inside it. |
| **log event** | One record the application wrote when one thing happened. Usually a single line, carrying a time and a message. |

You have already read log events — every time you looked at an application's output after something went wrong, that's what you were reading.

## Metrics Add Up Cheaply. Log Events Keep the Detail.

| | A metric answers | A log event answers |
|---|---|---|
| **Question** | How many answers were errors, and when. | Which request failed, and what the application said about it. |
| **Cost** | Cheap to total, cheap to alarm on. | Keeps the detail, costs more to store and search. |

One failure, two records. Neither one answers the other's question, so you need both.

## Four Tools Do This Job, and Ours Is Already in the Account

| Tool | What it is |
|---|---|
| **Datadog** | A paid service you send metrics and logs to. Wide, polished, priced per host and per gigabyte. |
| **Grafana with Prometheus** | Prometheus collects and stores the numbers; Grafana draws them. Open source, and you run both yourself. |
| **The ELK stack** | Elasticsearch, Logstash and Kibana — built for searching large volumes of log events. You run it yourself. |
| **CloudWatch** | AWS's own. Holds both metrics and log events for the account. |

Ours is **CloudWatch**, for one reason worth saying plainly: it's already in the account and needs no server of its own. Every other option on this list is something else to run, pay for, and keep alive.

## Seven Metrics Already Exist, With Nothing Installed

| Name | What it counts | Published by |
|---|---|---|
| `RequestCount` | Requests the balancer handed to a target. | The balancer |
| `TargetResponseTime` | Seconds from the request leaving the balancer to the target starting to answer. | The balancer |
| `HTTPCode_Target_5XX_Count` | Server-error codes **your application** returned. | The balancer |
| `HTTPCode_ELB_5XX_Count` | Server-error codes **the balancer itself** produced. | The balancer |
| `HealthyHostCount` | Targets currently considered healthy. | The balancer |
| `UnHealthyHostCount` | Targets currently considered unhealthy. | The balancer |
| `CPUUtilization` | Percentage of the machine's CPU in use. | The instance |

The two 5xx names are different questions. Your application answered with an error, or the balancer couldn't get an answer to hand back. The fix is different in each case, so the metric is separate.

## A Metric Is Identified by Three Things. Ask for the Wrong One and Get Nothing Back.

- **namespace** — which service published it. The balancer's numbers live in `AWS/ApplicationELB`; the instance's live in `AWS/EC2`.
- **dimensions** — which particular thing the number is about, such as which balancer or which target group. A name/value pair, and part of the metric's identity.

Ask for a combination that was never published and CloudWatch returns an **empty result, not an error**. An empty graph usually means the dimensions are wrong, not that nothing happened. Dimensions are per metric, too — `HTTPCode_ELB_5XX_Count` is published against the load balancer only, never a target group, because no target was involved in producing those codes.

## RAM, Disk Space and Your Own Log File Are Invisible From Outside the Machine

AWS counts requests and CPU from **outside** the operating system, which is why they arrive with nothing installed. RAM used, disk space used, and whatever the application wrote to a file are known only **inside** the operating system — nothing outside can see them. The rule follows: anything measured inside the machine needs a program running inside the machine.

**CloudWatch agent** — a program that runs on the machine. It reads files you name and numbers measured inside the operating system, and sends both to CloudWatch. It does two jobs, not one — the room usually assumes it's a log tool, but it collects **files** and it collects **numbers**.

## A Log Group Holds the Settings; a Log Stream Is One Machine's Sequence

- **log group** — a named container for one application's log events. How long events are kept, and who may read them, are set on the group, not on individual events.
- **log stream** — one sequence of log events from one source. Each machine writes its own stream, and all of those streams live inside one log group.

What CloudWatch holds is a **copy**. The file is still on the machine, and the copy is still in CloudWatch after the instance is terminated — the answer to the problem this session opened with.

## Create the Log Group in Terraform First, With Its Retention Setting

```hcl
# cloudwatch.tf
resource "aws_cloudwatch_log_group" "app" {
  name              = "investment-app"
  retention_in_days = 14
}
```

Order matters here. If a machine starts sending before the group exists, **the agent creates the group itself** — and a later `apply` that declares the same name fails, because the group is already there and Terraform didn't make it. The group has to exist before anything writes to it.

## Log Storage Is Billed on What You Send and How Long You Keep It

| | |
|---|---|
| **Sent in** | Charged per gigabyte the moment it arrives — every line every machine writes. |
| **Kept** | Charged per gigabyte per month for as long as retention says to keep it. |
| **Default** | Keep forever. Leaving retention unset is a decision, not a neutral choice. |

This is the first bill in this course driven by **volume rather than resources**. Several machines writing many lines costs more every day without anyone launching anything. Set retention when you create the group.

## The Agent Can't Send Anything Until the Machine's Role Allows It

```hcl
# iam.tf — added to the role you already wrote
resource "aws_iam_role_policy_attachment" "cw_agent" {
  role       = aws_iam_role.app.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}
```

Without it, here's exactly what you see: the agent installs, starts, and **reports itself healthy** — and sends nothing. No error in the console, no data in CloudWatch. The only complaint is written into the agent's own log file on the machine, which is the one file you can't fetch yet, because sending is what's broken.

## The Agent's Configuration Names Which Files, Which Numbers, and Which Log Group

```json
{
  "logs": { "logs_collected": { "files": { "collect_list": [
      { "file_path": "/var/log/investment-app-install.log",
        "log_group_name": "investment-app",
        "log_stream_name": "{instance_id}" } ] } } },
  "metrics": { "metrics_collected": {
      "mem":  { "measurement": ["mem_used_percent"] },
      "disk": { "measurement": ["used_percent"] } } }
}
```

The application writes no log file of its own, so the file sent is the install log — adding an application log to `collect_list` so a buy or a sell shows up in CloudWatch is the practice task. `mem` is the agent's key for **RAM**. A JSON mistake here is a second way to get healthy machines and no data: the agent fails to start, and the only error is `cannot translate json` in the agent's own log on the machine.

## Install It, Point It at the Configuration, Start It

```bash
# install
sudo dnf install -y amazon-cloudwatch-agent

# point it at the configuration and start it
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json
```

Then the same two lines go into the **boot script in the launch template** and get merged to main, so every machine the group launches arrives with the agent already running. Nobody installs this by hand on a machine they intend to keep. A different distribution installs and starts services differently — find the two commands for yours: the package manager's install, and the agent control script. The paths above are Amazon Linux's.

## Finding One Machine's Log Events, in Three Steps

1. Open the **log group** for the application.
2. Pick the **stream** whose name is the instance id you care about.
3. Move to the **time** the problem happened, and read forward.

You don't log into anything to do this, and it still works after the machine that wrote those lines has been terminated and replaced.

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **Pull main, then point the backend at your own bucket** — `cloudwatch.tf` and the IAM attachment were pushed during class, naming the instructor's log group and bucket. Put your own in before you apply.
- **Add your application's own log to `collect_list`** — right now the agent only ships the install log. Point a second entry at whatever file your buy/sell code writes to, and confirm a new log stream appears with the events in it.
- **Terminate a machine and read its stream anyway** — pick a running instance, terminate it, and open CloudWatch afterward. The stream from that instance id is still there, holding everything it wrote before it died.

**What you know now:** replacing a machine deletes its **root volume**, so a log file written there goes with it — the reason CloudWatch exists is to hold a copy somewhere the group can't delete it. A **metric** is a named series of numbers over time, cheap to total and cheap to alarm on but blind to which request failed; a **log event** is one line from one moment, keeping the detail a metric throws away. Seven metrics — request count, response time, both flavors of 5xx, healthy and unhealthy host counts, and CPU — already exist with nothing installed, because the balancer and the instance publish them from outside the operating system; RAM, disk and your own log file are invisible from outside and need the **CloudWatch agent** running inside to collect and send them. A **log group** holds the retention and access settings for one application, and a **log stream** is one machine's own sequence inside it. The group has to exist in Terraform before anything writes to it, or the agent creates it first and a later `apply` fails; the agent's IAM policy and its JSON configuration are two separate ways to end up with a healthy machine sending nothing, and in both cases the only evidence is in the agent's own log on the machine that's failing to send logs anywhere else.

---

# Lesson 42: The Dashboard, the Alarm & Your Inbox — Reading the System From the Human Side

## Where We Left Off

Last session got metrics and log events off a machine and into CloudWatch, surviving the machine itself being replaced. But nothing yet stood between those numbers and a person — the seven metrics and everything the agent shipped just sat there, unwatched. Tonight closes that gap: a dashboard is one page of saved graphs, an alarm watches one metric against a threshold, and an SNS topic is how a firing alarm reaches an email address.

## A Dashboard Is One Page of Saved Graphs

**dashboard** — a saved page of graphs you chose. In practice: the page one person opens when a customer says the site is slow.

| Graph | Statistic | Why that one |
|---|---|---|
| **Request count** | `Sum` | You want the total for the period, not an average of it. |
| **Target response time** | `p95` | The number 95 out of every 100 requests came in under. An average hides the slow ones. |
| **5xx count** | `Sum` | How many errors, totalled. |
| **Healthy host count** | `Minimum` | The worst view any balancer node had, which is what catches a machine going bad. |
| **CPU** | `Average` | Across the machines, to see whether you are running enough of them. |

Each row picks its statistic on purpose. An average request count would hide a spike; a minimum on CPU would hide the machine that's struggling.

## The Dashboard Is a Terraform Resource, and Its Body Is JSON

```hcl
# dashboard.tf
resource "aws_cloudwatch_dashboard" "app" {
  dashboard_name = "investment-app"
  dashboard_body = jsonencode({
    widgets = [{
      type = "metric"
      properties = {
        metrics = [["AWS/ApplicationELB", "RequestCount", "LoadBalancer", aws_lb.app.arn_suffix]]
        stat   = "Sum"
        region = var.region
      }
    }]
  })
}
```

Its body is a document, not arguments — `jsonencode` lets Terraform check the shape. `region` is required inside the widget; leave it out and the apply fails with `should have required property region`.

## An Alarm Watches One Metric Against a Threshold

**alarm** — a rule attached to one metric. It compares the numbers to a threshold you set, and when the comparison holds for long enough, it acts.

## Four Settings Decide Whether Your Alarm Ever Fires

| Setting | What it decides |
|---|---|
| `period` | How long each single number covers. 60 means one number per minute. |
| `evaluation_periods` | How many of those numbers the alarm looks at. |
| `datapoints_to_alarm` | How many of the ones it looked at must be past the threshold. |
| `treat_missing_data` | What to do when a number does not exist at all. |

The last one is the trap. **The 5xx counts are published only when they are not zero**, so on a quiet stack there are no numbers — not zeroes. An alarm left on the default sits in `INSUFFICIENT_DATA` and never fires. Set `treat_missing_data = "notBreaching"` for a count. Healthy host count is different: it is published whenever targets are registered, so it always has numbers.

## Alarm a Person on What a Person Using the Site Would Notice

| Worth waking someone | Not worth waking someone |
|---|---|
| **Response time is up** — the site feels slow to a real person. | **CPU is at 90%** — nobody using the site can feel this. It might be fine. It might even be what you wanted, if you are paying for those machines. |
| **Errors are up** — requests are failing. | **But it is a good input for a scaling policy** — you have already seen one: a rule watching average CPU, adding and removing machines, with no person involved at any point. |
| **Healthy host count is down** — fewer machines are answering than you asked for. | |

Deciding **how many machines to run** and deciding **when to wake a person** are two different decisions. The same number can be right for one and wrong for the other.

## Being On Call Means You Are the Person the Alarm Reaches

**on call** — the named person who answers when an alarm fires, including at night and on weekends. The team shares the duty in a rotation — one week each on a team of four is one common arrangement, not a rule.

**escalation policy** — what happens when nobody answers. A paging tool — a program that rings a phone until someone acknowledges the alarm — calls the person on call, waits, calls again, and after that calls their manager.

You are **not on your own**. An outage big enough to wake someone usually reaches other teams too, and the developers who own the application are involved as well. This unit sends the alarm to an email address. Companies usually send it on to a paging tool instead — PagerDuty and Opsgenie are two.

## An SNS Topic Is a Named List That a Message Is Sent To

**SNS topic** (Simple Notification Service) — a named list. Something sends one message to the list, and everyone on the list receives it. The alarm does not know who is on it.

## A Subscription Is One Address on That List, and It Has to Confirm First

**subscription** — one destination on a topic — here, one email address. AWS creates it in a pending state and sends that address a confirmation link.

Until a person clicks that link, **no alarm mail is delivered**. A clean `apply` and a silent inbox is the expected result, not a bug. Check your mail before you debug anything, and check the spam folder — that is where the confirmation arrived in class.

## The SNS Topic and Subscription, in Terraform

```hcl
# alarms.tf
resource "aws_sns_topic" "alerts" {
  name = "app-alerts"
}

resource "aws_sns_topic_subscription" "email_alerts" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = "you@example.com"
}
```

The attribute is called `endpoint`. Here it means **the email address** — not a URL path, and not a hostname. Same word, third meaning.

## The Alarm, in Terraform, Pointed at That Topic

```hcl
# alarms.tf
resource "aws_cloudwatch_metric_alarm" "errors" {
  alarm_name          = "app-5xx"
  namespace           = "AWS/ApplicationELB"
  metric_name         = "HTTPCode_Target_5XX_Count"
  dimensions          = { LoadBalancer = aws_lb.app.arn_suffix }
  statistic           = "Sum"
  period              = 60
  evaluation_periods  = 5
  datapoints_to_alarm = 2
  threshold           = 5
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  ok_actions          = [aws_sns_topic.alerts.arn]
}
```

Beside every alarm, write **the action a person takes when it fires**. `ok_actions` sends the second mail saying it recovered.

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **Pull main, then confirm your own subscription** — `dashboard.tf` and `alarms.tf` were pushed during class naming the instructor's own email address and dashboard name. Put your own email in the subscription before you apply, and check your inbox — and your spam folder — for the confirmation link. No mail arrives until you click it.
- **Add a second alarm to the same topic** — pick `TargetResponseTime` or `HealthyHostCount` and point it at `aws_sns_topic.alerts.arn` alongside the 5xx alarm. Confirm `ok_actions` sends you the recovery mail too, not just the failure one.
- **Set `treat_missing_data` correctly for a count-based alarm** — leaving it on the default lets a quiet stack sit in `INSUFFICIENT_DATA` forever, never firing and never telling you why. Set it to `notBreaching` and check the alarm's history to see the difference.

**What you know now:** a **dashboard** is one saved page of graphs, built as a Terraform resource whose body is a JSON document checked by `jsonencode`, with each graph's statistic chosen on purpose — sums for counts, `p95` for response time, minimum for healthy host count, average for CPU. An **alarm** watches one metric against a threshold, and whether it ever fires comes down to four settings — `period`, `evaluation_periods`, `datapoints_to_alarm`, and `treat_missing_data`, the last of which hides a trap: a count metric published only on nonzero values sits in `INSUFFICIENT_DATA` on a quiet stack unless you set it to `notBreaching`. Alarming a person is a separate decision from scaling a group — response time, errors and healthy host count are worth waking someone for; CPU alone usually isn't, even though it's the right input for a scaling policy. Being **on call** means you're the one an **escalation policy** reaches first, with a manager as the fallback when nobody answers. An **SNS topic** is a named list a message goes to, and a **subscription** is one address on that list that has to confirm before any mail arrives — a clean apply and a silent inbox is the expected result until someone clicks that link. In Terraform, the topic, the subscription and the alarm are three separate resources, joined by `alarm_actions` and `ok_actions` pointing at the same topic ARN.

---

# Lesson 43: Testing the Alarm, Working an Outage & Getting a New Version Out

## Where We Left Off

Last session wired an alarm to an SNS topic so a threshold breach reaches an inbox. Tonight is that alarm proving itself, a fixed order for finding out why the site is down, and the mechanism that gets a new version onto every machine the group is already replacing for you — without anyone logging in.

## Prove the Alarm's Mail Arrives Without Waiting for a Real Failure

```bash
aws cloudwatch set-alarm-state \
  --alarm-name app-5xx \
  --state-value ALARM \
  --state-reason "testing the path"
```

| | |
|---|---|
| **What this proves** | The state changed, so the alarm ran its actions — SNS published, and mail reached every confirmed subscription. |
| **What it does not prove** | The metric, the threshold, or the missing-data setting. An alarm watching the wrong metric still sends this mail. |

All three flags are required. The forced state lasts only until the next real evaluation — usually seconds — and then the alarm returns to its real state, which sends the `ok_actions` mail too. Because the metric itself never breached, the change shows in the alarm's **History** tab, not on its graph.

`HTTPCode_Target_5XX_Count` counts a 5xx your application returned; `HTTPCode_ELB_5XX_Count` counts the 502 the balancer returns when it can't reach a target at all. Two different questions, not two names for the same failure.

## When the Site Is Down, Check the Path in One Fixed Order

Each check rules a layer out — that is the whole value of doing them in order, so you never guess twice about the same layer.

1. **Does the name resolve?** `host <your domain>`. If not, nothing after this matters.
2. **Does the listener answer?** `nc -vz <balancer dns name> 80` — the balancer is reachable and something is listening on the port.
3. **Does the target group hold a healthy target?** The target group's **Targets** tab. If it holds none, the balancer has nowhere to send.
4. **Does the health check path answer?** `curl -i <machine ip>/health` from somewhere that can reach it. Read what comes back.
5. **Read that machine's log events.** Now you know which machine, and CloudWatch has its stream.

## A Healthy Target Means One Endpoint Replied, Not That the Application Works

The health check path defaults to `/`. This repo sets `/health` and asks for it every 30 seconds, and the application answers it from its own process: `{"status": "ok"}`. That endpoint does not query the database and does not exercise any other route. Two failures in a row mark a target unhealthy; five successes in a row mark it healthy again.

| | |
|---|---|
| **Proven by a 200 on `/health`** | The process is up, the port is open, and it can answer one request. |
| **Not proven** | That the database is reachable. That a login works. That any other route returns anything at all. |

So a target reading **healthy** is a claim about one endpoint, not about your application. When the site misbehaves and every target is healthy, this is usually why. A health check that also asks the database catches more, and takes every target down whenever the database is down.

## A Deployment Strategy Is How a New Version Replaces a Running One

| Strategy | How | Cost / tradeoff |
|---|---|---|
| **Rolling replacement (ours)** | Replace a few machines at a time until all of them run the new version. | Needs no extra capacity beyond the few being replaced — the group already replaces machines, so this is the mechanism you have. |
| **Blue/green** | Run two complete sets, old and new, and move all traffic across at once. | Going back is instant. You pay for double the machines while both exist. |
| **Canary** | Send a small share of traffic to the new version first, watch it, then move the rest. | Catches a bad version with few people affected. |

Two things a screen will ask you: *how do you deploy without downtime*, and *how do you roll back*. These three answer the first. Rolling back is a separate question, answered below.

## Instance Refresh Replaces the Running Machines From a New Template Version

**instance refresh** — you tell the group its machines are out of date. It replaces them in batches, keeping enough healthy ones answering while it works.

Two settings decide whether that replacement breaks anything:

- **deregistration delay** (also called **draining**) — before a machine is shut down, the balancer stops sending it new requests and waits for the ones already sent, up to this many seconds. Default 300, and a maximum rather than a fixed wait — a target with no requests still open finishes at once. It belongs to the **target group**, not the Auto Scaling group: `deregistration_delay` on `aws_lb_target_group`, or **Attributes** in the console.
- **`health_check_type = "ELB"`** — the default is `EC2`, which asks only whether the instance is running, not whether your application answers. On the default, a refresh judges its replacements on the wrong question.

## Wire the Refresh onto the Group

```hcl
# asg.tf
resource "aws_autoscaling_group" "app" {
  launch_template {
    id      = aws_launch_template.app.id
    version = aws_launch_template.app.latest_version
  }
  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 50
      instance_warmup        = 120
    }
  }
}
```

AWS does not watch the launch template. `terraform apply` starts the refresh, and only when that apply changes the group's `launch_template` — which is why `version` points at `latest_version`. Publish a version in the console and nothing happens.

## Two Ways This Quietly Does Nothing, and Why a Successful Apply Is Not a Finished Deploy

| What you wrote | What happens |
|---|---|
| `version = "$Latest"` | Terraform sees no change. **No refresh starts.** Point at `latest_version` instead. |
| No `version` at all | Defaults to `$Default`. That group never refreshes either. |
| `apply` returns | It **started** the refresh. It did not wait for it, and it did not check it worked. |
| A second `apply` | A group allows one refresh at a time, so updating it again **cancels the refresh in flight** and starts another. |

```bash
aws autoscaling describe-instance-refreshes \
  --auto-scaling-group-name app
```

And what the template launches has to be **pinned**. If your boot script clones a branch, the refresh hands you new machines running whatever that branch holds at that moment — which is not a version, and not something you can roll back to.

## Stopping a Refresh, and Rolling Back to the Previous Version

| Option | What it does |
|---|---|
| **Cancel** | Stops a refresh that is still running. The machines it already replaced stay on the new version — cancel is not an undo. |
| **Roll back** | Replaces those machines again, from the version the group held before. Only while the refresh is still running, and only with a numbered template version. |
| **`auto_rollback`** | Does it for you when the refresh fails. Terraform names a rollback target only when you set this, which is why the console's **Roll back** is greyed out otherwise. |

And the part people get wrong in interviews: **rolling back the code often does not undo the deploy**. If the bad version changed the database, that change is already applied, and putting the old code back leaves it facing data it does not expect. Shipping a corrected version forward is frequently the safer move. Rollback is a decision, not a button.

---

# Lesson 44: Environments — One System, Three Roles & What a Second One Costs

## Where We Left Off

Last session closed the deploy: instance refresh replacing machines from a new launch template version, and a clean line between canceling a refresh and actually rolling one back. Tonight steps back from any single deploy to ask what you've been deploying into all along — right now, one system — and opens the unit on running more than one.

## Everything `terraform state list` Prints Is One System, and It's the Only One You Have

```bash
terraform state list     # every resource this repository is managing, read from remote state
```

One network, one load balancer, one database, one group of servers. One system, and everyone who visits your address reaches it.

## An Environment Is One Complete Running Copy of the System

**environment** — network, servers, load balancer, database. All of it, running at the same time.

Not a folder. Not a branch. Not an environment variable, and not the environment file your app reads. A whole system that is running.

## Production, Dev & Staging Are Roles Given to an Environment, Not Three Kinds of Thing

| Term | What it is |
|---|---|
| **production** | The copy real users reach. Its data is real data, belonging to real people. |
| **dev** | A copy engineers change freely. Its data is invented — nothing in it belongs to a real person, so a mistake here reaches nobody outside the team. |
| **staging** | A copy made to resemble production closely enough to be the last check before it. It usually still holds invented data, which is why it can't catch every failure. |

Close to production is not production. The data is usually where the difference is.

## The Same Resources, Fewer of Them

Copies hold the same resources. What differs is how many there are, how big each one is, and the data they hold. A lower environment costs less — fewer and smaller machines — but not nothing: a load balancer is charged for **each hour it's running**, used or not.

## With One Environment, Every Change Is Tried on the System Answering Real Traffic

| | |
|---|---|
| **What you have** | One environment. Every change you apply reaches the running system that answers your address. |
| **What you don't have** | Anywhere to put that same change and read the result before it's live. |

That's the problem. Companies run more than one environment because of it.

## The Rest of This Unit, in Five Parts

| Part | What it covers |
|---|---|
| **1 · What an environment is** | What counts as one, and the three names given to them: production, dev, staging. |
| **2 · Why a second environment exists** | The reasons, taken from companies rather than from your own account. |
| **3 · What separates two environments** | The AWS account, and what a boundary refuses that a name cannot. |
| **4 · Reaching a second account** | How a person gets into one, and how Terraform does. |
| **5 · The same code, two environments** | Modules, one directory per environment, and both of them applied. |

Tonight was part 1. The rest of the unit is still ahead.

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **Run `terraform state list` against your own repository** — read down the list and name, out loud, what would break if each entry disappeared. That list is your one environment, in full.
- **Sort your own app's data into real and invented** — for everything your database holds, decide which rows belong to a real person and which don't. That split is what will decide whether a copy of your system is allowed to be `dev` or has to stay `production`.
- **Price your own load balancer as a second environment** — it's charged by the hour whether it's used or not, so a second copy of it is never free, even at the smallest scale. Work out roughly what a second, minimal copy of your stack would add to the bill.

**What you know now:** an **environment** is one complete running copy of the system — network, servers, load balancer, database, all running at once — and it is not a folder, a branch, an environment variable, or the environment file your app reads. **Production**, **dev**, and **staging** are roles given to an environment, not three different kinds of thing: production is the copy real users reach with real data, dev is the copy engineers change freely with invented data, and staging resembles production closely enough to be the last check before it but usually still holds invented data, which is why it can't catch every failure. A lower environment costs less because it holds fewer and smaller copies of the same resources, but not nothing — a load balancer bills by the hour whether it's used or not. And with only one environment, there's nowhere to put a change and read the result before it reaches the system answering real traffic — which is the problem the rest of this unit, reaching a second AWS account and running the same code in both, is there to solve.

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **Force your own alarm into `ALARM` state** — use `set-alarm-state` against your own alarm name, confirm the mail arrives, and check that it shows in the alarm's **History** tab rather than on its graph, since the metric itself never breached.
- **Work the outage ladder against your own stack, in order** — resolve the name, check the listener, check the target group's targets, curl `/health` directly, then find that machine's log events. Don't skip a step even when you're sure you know the answer.
- **Wire `instance_refresh` onto your own Auto Scaling group** — point `version` at `latest_version`, not `$Latest` or nothing, push a change through `terraform apply`, and watch `describe-instance-refreshes` until it reports finished rather than assuming the `apply` returning means the deploy is done.
- **Set `auto_rollback` and try rolling back mid-refresh** — start a refresh, cancel it partway through, and check which machines actually went back to the old version versus which stayed on the new one.

**What you know now:** forcing an alarm's state with `set-alarm-state` proves the SNS publish and the subscription path work, but proves nothing about the metric, threshold, or `treat_missing_data` setting — and `HTTPCode_Target_5XX_Count` and `HTTPCode_ELB_5XX_Count` are different questions, not two names for the same failure. When the site is down, checking name resolution, the listener, the target group, the health check path, then log events, in that fixed order, rules a layer out at each step instead of guessing twice about the same one. A **healthy target** is a claim about one endpoint answering, not about the application working — the health check path defaults to `/` but this repo points it at `/health`, which never touches the database. A **deployment strategy** is how a new version replaces a running one — rolling replacement is ours, needing no extra capacity, while blue/green and canary trade capacity or exposure for a faster or safer rollback. **Instance refresh** replaces a group's machines in batches from a new launch template version, gated by **deregistration delay** (draining, a maximum wait on the target group) and `health_check_type = "ELB"` (so a refresh judges replacements on whether the application answers, not just whether the instance is running). Terraform only starts a refresh when an `apply` changes the group's `launch_template`, which is why `version` has to point at `latest_version`; a successful `apply` only starts the refresh; and **cancel**, **roll back**, and `auto_rollback` are three different things — with rolling back the code often not undoing a deploy that already changed the database.

---

# Lesson 45: Modules — One Description of the Infrastructure, Applied Twice

## Where We Left Off

Last session named the problem: with one environment, every change lands on the system answering real traffic, and there's nowhere to try it first. Tonight is part 5 of the unit — the same code, two environments — and it ends with a second environment actually applied, from your own repository.

## A Module Is a Directory of Terraform With Declared Inputs and Declared Outputs

**module** — a directory of Terraform with declared inputs and declared outputs, called from somewhere else by a relative path.

You already write one level of this:

```hcl
variable "instance_type" {
  type    = string
  default = "t3.micro"
}
```

A module is the same idea, one level of size up:

```hcl
module "network" {
  source = "../../network"
  cidr   = "10.0.0.0/16"
}
```

A `variable` is one description of **a value**. A `module` is one description of **a set of resources**. Both take their values from outside. The only new thing is `source` — a relative path to the directory being called.

## One Module, Called Twice With Different Values

A small module, three files:

```hcl
# variables.tf
variable "label" { type = string }

# main.tf — one resource, and it is free

# outputs.tf
output "id" { value = ... }
```

Called from two environment directories, with different values:

```hcl
module "first" {
  source = "../../first"
  label  = "production"
}

module "first" {
  source = "../../first"
  label  = "dev"
}
```

Nothing inside the module names either caller. That is what lets two different places call the same directory.

## Two Modules, Because an Output Needs Somewhere to Go

```hcl
# network/outputs.tf — a value going OUT
output "vpc_id" {
  value = aws_vpc.this.id
}
```

```hcl
# app/variables.tf — a value coming IN
variable "vpc_id" {
  type = string
}
```

The network module declares the VPC id as an output. The app module can't be built without it as an input. One module holding both would leave the output with nothing on the other side to hand the value to — so a VPC and the app that depends on it live in separate modules.

## The Environment Root Reads One Output and Passes It Into the Other — and "Root" Means Three Different Things

The network module declares the VPC id as an output. The **environment root** — the directory holding the provider block, the backend, and the calls to both modules — reads it by that name and passes it into the app module as an input. The value is recorded in that environment's state.

Three unrelated things get called root, and none of them is ever said bare:

| Term | What it is |
|---|---|
| **environment root** | The Terraform directory that calls the modules — `production/`, `dev/`, and so on. |
| **management account** | The AWS account at the top of an organization. |
| **root user** | The one login every AWS account starts with. |

## Reading Inside a Module Only Through What It Declares

```hcl
# modules/full-env/outputs.tf
output "db_endpoint" {
  value = aws_db_instance.main.address
}

# production/main.tf — reads the name the module declared
output "db_endpoint" {
  value = module.prod.db_endpoint   # plans and applies
}
```

```hcl
# production/main.tf — names a resource inside the module instead
output "db_endpoint" {
  value = module.prod.aws_db_instance.main.address   # Unsupported attribute
}
```

`module.prod` holds the names in that module's `outputs.tf` and nothing else. Moving a resource into a module puts it out of reach from outside, so every output that named it directly has to be rewritten to read the module's output instead.

## A Module Can Come From a Registry Instead of Your Own Repository

```hcl
# yours, by relative path
module "network" {
  source = "../modules/network"
  cidr   = "10.6.0.0/16"
}
```

```hcl
# somebody else's, by registry address
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 6.0"
  cidr    = "10.6.0.0/16"
}
```

`terraform init` downloads a registry module; `version` decides which release you get. The published ones are single pieces of infrastructure — a VPC, a load balancer, an S3 bucket — at `registry.terraform.io`, with AWS's own set published as the `terraform-aws-modules` GitHub organization. Your full-environment module stays yours, because the set of resources in it is yours.

## Four Ways to Run More Than One Environment, and Why Plain Directories Win

| Option | The tradeoff |
|---|---|
| **The directory duplicated per environment** | Every change has to be made twice. The day one copy is missed, the two environments stop matching. |
| **Terraform workspaces** | One configuration, several states. Named here, and not used. |
| **Terragrunt** | A separate tool that generates the repetition for you. Named here, and not used. |
| **A directory per environment, each its own Terraform root (ours)** | The repetition stays in the files, where you can read it. |

Each option differs on one axis — this isn't a ranking. The cost of the last one is real: a change to shared structure has to be made in each environment root. What keeps that small is the modules — the repetition that's left is a values file and a set of credentials, not the resources themselves.

## The Shape: Modules at the Top, One Directory Per Environment Beside Them

Module directories sit at the top level, named for what they build — `network`, `app`. Beside them, an `environments` directory holds one directory per environment — `production`, `dev` — each its own place Terraform is run, each with **one state per environment**.

## A Module Holds No Provider Block and No Backend

It inherits both from whichever environment root calls it. That's also why `terraform init` inside a module directory fails: a module has no backend, so there's nothing there for `init` to initialize. Terraform runs in the environment directory, never in a module directory.

## One Values File Inside Each Environment Root

| What it sets | production | dev |
|---|---|---|
| app servers | 3 | 1 |
| instance size | `t3.small` | `t3.micro` |
| database | across two zones | one zone |

(Sample sizes — the real numbers are yours to choose per environment.) The values file is not shared between environments, and it's not passed on the command line — it lives inside each environment root. `*.tfvars` is in the repository's `.gitignore` today; that line has to change, or the file stays on one machine.

## Building One Name Per Environment Out of a Shared Value

```hcl
# staging/variables.tf — the same in every root
variable "domain_name" {
  type    = string
  default = "inv-app.exchangeweb.net"
}
```

```hcl
# staging/main.tf — the one part that differs
module "staging" {
  source      = "../modules/full-env"
  domain_name = "staging.${var.domain_name}"
}
```

`var.domain_name` is that value, used where a value stands on its own. `${...}` puts it inside a string — the module receives `staging.inv-app.exchangeweb.net`. The variable needs its `default` for this to work: with no default and nothing passed in, there's no value to read, and the plan stops.

## One State Key Per Environment Root

One bucket per account, created by hand in that account, outside the configuration. In a single account, that's one bucket with a key for each environment root. An action in one account can't reach the other account's state. Copy every file from one environment root to build a second but leave the key alone, and `plan` reports **no changes** — both roots would be reading the one state, and everything in it already exists.

## Moving Into Modules Destroys and Recreates — Here, That's Acceptable

| | |
|---|---|
| **Moves into a module** | The network. The servers and the load balancer. |
| **Does not move** | The database. Its data is the whole reason, and it stays in the environment root. |

Your repository is one flat folder today; it moves into the two modules above. Terraform destroys and recreates everything that moves. Two reasons that's accepted here and wouldn't be at a company: the resources that move hold no data, and nobody is using your system yet.

## What the Plan Prints, and the One Line That Must Not Be In It

```diff
- aws_vpc.main                     # destroyed — its address changed
+ module.network.aws_vpc.this      # created at the new address

  aws_db_instance.main             # absent from the plan entirely
```

Say out loud what the plan will print before a file moves, then read the destroy count and confirm the database is not in it. `terraform init` inside a module directory still fails here for the same reason as before — a module has no backend, so there's nothing for it to initialize.

## The Second Environment, Applied

| | |
|---|---|
| **The same in both** | The two modules. The environment root that calls them. Every resource they create. |
| **Different in each** | The values file inside the environment root, and the credentials the apply runs as. Nothing else. |

An empty plan on a second, freshly-copied environment root is correct, not a broken module — it means the module produced exactly what already exists.

## In One Account, the Copy Fails on Every Name AWS Owns

| Refuses to create a second one | Why |
|---|---|
| Load balancer, target group | The name must be unique per region per account, and the balancer's address is built from it: `name-id.elb.region.amazonaws.com`. |
| IAM role, instance profile | IAM names are account-wide. There's no region to keep two of them apart. |
| Log group, DB subnet group, DB instance, DNS record | AWS finds each of these by the name you gave it. |
| Auto Scaling group | Unique per region per account, same rule as the load balancer. The instances it launches carry only a tag, which is why this one is easy to get wrong. |

The VPC, subnets, security groups, and route tables all create twice without complaint — their `Name` is a tag, and AWS never reads it. Two environments in two separate accounts hit none of this.

---

# Lesson 46 — Caching, and the Copy Nearest the User

## Where We Left Off

The last few sessions closed out the infrastructure-as-code arc: modules, environments, the same code applied twice. Tonight opens a new topic inside the Scale unit, and it starts from a plain fact about your own page: it does the whole job on every single request. The balancer routes it, Flask handles it, a call goes out to Finnhub for the quote, a query goes to Postgres, the page renders — and none of that work is kept from one request to the next. Tonight names the place a repeated answer can be kept instead. There turn out to be three such places, and by the end you can say which one holds any given answer on your own system.

## A Cache Is a Stored Copy of an Answer

**cache** — a stored copy of an answer. Instead of computing the answer again, the copy is handed back.

Your page asks Finnhub for the quote on every request. A cache would hand back the quote it fetched ten seconds ago instead of asking again. Most applications keep a copy of something. Yours, right now, keeps none.

## The First Place a Copy Can Live: Inside the Application

**local cache** — a copy inside the application process, kept on the machine it runs on. Each of your two Flask servers could keep the last Finnhub quote for a few seconds instead of asking Finnhub on every request.

That's the term. What it is not called: "the application's memory" — that phrase is reserved for a database's own memory, and a room full of people reaches for RAM the moment they hear it. The real term is local cache, and it names a copy inside the process, nothing more.

## The Origin Computes the Real Answer; a Hit or a Miss Says Whether It Was Asked

**origin** — the system that computes the real answer. For the quote on your page, the origin is Finnhub. For the whole page, the origin is your own servers. The origin does the work; a copy only repeats it.

(Not related to git's `origin`, which is a remote repository — same word, unrelated thing.)

| Term | What happens |
|---|---|
| **hit** | The quote is already in the Flask process. It's returned, and Finnhub is never called. |
| **miss** | No copy exists, or it has expired. Flask calls Finnhub, and the answer is stored on the way back. |

## The Key Is the Part of the Request That Selects the Copy

**key** — what the cache looks at to decide which copy you get. Same key, same copy.

- The quote's key is the ticker symbol: `AAPL` and `TSLA` are two keys, two copies, and everyone asking for `AAPL` gets the same one.
- A poster's key is the file's address: everyone asking for the same address gets the same copy.

A personal page has to carry the person in its key. Leave the account out of the key and everyone gets the same copy — one person sees another person's page.

## Time to Live: How Long a Copy Is Kept Before the Origin Is Asked Again

**time to live** (**TTL**) — how long a copy is kept before the origin is asked for a fresh answer.

You've already met this idea: your DNS record's TTL is 300 seconds, and a resolver keeps that answer for 300 seconds before asking Route 53 again. The same idea shows up on a web answer as one header line, set by the origin:

```
Cache-Control: max-age=300     # keep this copy for 300 seconds
```

## Stale: the Copy Still Holds the Old Answer

**stale** — the origin has a new answer, but the copy still holds the old one, and serves it until its time to live ends.

Finnhub has a new price; your Flask process still holds the old one for a few seconds. Nothing is broken — the copy is stale, and it stops being stale the moment its TTL runs out and the next request goes to the origin.

## The Limit of the First Place: N Machines Hold N Copies

Machine A stored a post's like count at 10:00:00 and shows 1,204. Machine B stored it at 10:00:40 and shows 1,219. Fine for likes — nobody is harmed and nobody notices two numbers for a minute. Not fine for a cart — a cart that differs between the two machines is a cart that loses items the moment the load balancer switches you to the other one.

Your two Flask processes could each keep the last Finnhub quote instead of asking every time, and for those seconds the two quotes would differ. That's the limit of the first place: **N machines hold N copies.**

## What a Local Cache Gives a Company

| What it gives | Why |
|---|---|
| **Fewer calls to the origin** | One Finnhub call serves every request for the next few seconds, instead of one call per request. |
| **A smaller bill** | External APIs bill per call and cap calls per minute. A copy keeps you under both. |
| **A faster answer** | A copy in the process answers in microseconds; a call across the internet takes tens of milliseconds. |

The limit stays: every machine keeps its own copy, so the copies can differ. Nothing to build here, and nothing to pay for — the process already had the memory.

## The Second Place: One Shared Store Every Server Reads

**shared store** (a **cache tier**) — a separate server whose only job is to hold copies. Every application server reads and writes the same one, so there is one copy, not N.

Your Amazon cart follows you from your phone to your laptop. It isn't kept on the machine that answered you — it's kept in a store every machine can reach.

## ElastiCache Is AWS Running a Cache Tier for You

**Amazon ElastiCache** — a cache server AWS runs for you inside your VPC, the same way RDS runs your database. Never public. Bills by the hour from creation. You're paying for RAM, and a gigabyte of RAM costs far more than a gigabyte of disk — which is why a cache holds what's asked for often, not everything the database holds.

| Engine | What it is |
|---|---|
| **Redis OSS** | The most widely used engine. Keys and values, held in RAM. |
| **Memcached** | The older, simpler engine. Keys and values only. |
| **Valkey** | A fork of Redis, kept open source. AWS's recommended engine for a new cache. |

ElastiCache runs any of the three. Named here; nobody creates one tonight.

## The Session Store Is Not a Cookie, and Not a Cache

In the load balancer topic, **sticky sessions** kept a user on one machine — a setting on the load balancer that sends you back to the same server every time, and it has to be configured on both the balancer and the application. The real fix moves who-is-logged-in off the machines entirely, into the shared store, so any machine can answer:

**session store** — the shared store holding who is logged in.

| Term | What it is |
|---|---|
| **sticky session** | A load-balancer setting solving the same problem a session store solves, at the cost of configuring both the balancer and the app. |
| **cookie** | Data the browser sends back with each request. A cookie can identify you with no login at all — the site stores an identifier in your browser and the browser sends it back on every visit. |
| **cache** | A stored answer, kept by a server or an app. Different word, different thing. |

Your application has no login, so it has nothing to put in a session store — explained here, not built.

## Some Answers Are Never a Copy

- **Your bank balance.** Your phone and the cash machine must show the same number, right now. A copy from a minute ago is a wrong balance.
- **The last seat on a flight.** Two people must not both buy it. The answer has to come from the one place that knows.
- **The cash figure on your page after a stock buy.** Computed on every request, from Postgres. Never stored anywhere else.

**The test:** if two screens may show different values for a minute, the answer *can* be a copy. If they may not, it *cannot*.

## Steam, 25 December 2015: the Key Left Out the Person

The Steam store was under a flood of requests. A caching change was deployed to cope with it, and it cached each store page **without the account in the key**. What people saw: other people's account pages — billing and email address, purchase history, the last two digits of a card. By Valve's own count, about 34,000 accounts were affected.

A personal page has the person in its key, or it is never a copy.

## What a Shared Store Gives a Company

| What it gives | Why |
|---|---|
| **One answer for every server** | The cart, the login, the count are the same whichever machine answers — the limit of the first place is gone. |
| **A database that does less** | Reads answered from the store never reach Postgres, so the same database serves many more users. Writes still go straight to Postgres; the application code decides which is which. |
| **Machines you can replace** | Nothing a user needs lives on the machine itself. A server can be replaced at any moment, which is exactly what the scaling group assumes. |

The cost: a server that bills by the hour from creation, inside the VPC, like RDS.

## Distance Costs Time

Light in fibre travels about 200 km per millisecond. Singapore to Virginia and back is at least 150 ms — before any server does a single thing. A page over HTTPS needs several such round trips before the first byte arrives. A video call across an ocean has a delay you can hear; the same delay is paid on every round trip a page makes.

## The Edge Location: a City Near the User

**edge location** — a small AWS data centre in a city, outside any region, that holds copies and answers requests from nearby users. There are hundreds of them, worldwide.

Netflix starts playing a film just as quickly in Chicago as in Warsaw, because a copy of the film sits in both cities. The edge is not the border of your network — it's a set of small data centres in cities, and it's the third place a copy can live.

## CloudFront Is AWS's Content Delivery Network

**Amazon CloudFront** (a **content delivery network**, **CDN**) — a set of edge locations that hold copies of your answers and serve them from the city nearest the user. It reads from a bucket, a load balancer, or any origin.

| CDN | What it is |
|---|---|
| **Cloudflare** | Its own edge network in front of any origin. Also sells the firewall and attack protection. |
| **Fastly** | Its own edge network. Used by large news and e-commerce sites. |
| **Akamai** | The oldest and largest. Runs inside internet providers. |
| **CloudFront** | AWS's. What this unit builds. |

## A Request Answered at the Edge Never Reaches the Region

| Step | What happens |
|---|---|
| **1 · First request from a city** | Miss. The edge location asks the origin, and stores the answer. |
| **2 · Every later request from that city** | Hit. Answered at the edge location, for everyone it serves. |
| **3 · Your servers** | Never see those requests at all. |

Faster, because the answer comes from nearby. Protected, because those requests never reach your servers. The copy is selected by the key, not by who asked — speed and protection are the same fact, seen from two sides.

## All Three Places, One Table

Real systems use all three places, for different answers:

| The answer | Where its copy lives |
|---|---|
| **Likes** | Inside the application. Two machines, two copies, and that's fine. |
| **The cart** | The shared store. One copy every server reads. |
| **A poster, a film** | The edge. A copy in every city that asked. |
| **The cash figure after a stock buy** | Nowhere. Read from Postgres on every request, never copied. |

Three places to keep a copy, and one answer that is never copied at all — the same test decides every row of this table: can two screens differ for a minute, or must they never?

## After Class

Optional practice and Q&A held after the main lecture — less structured, students stay to ask questions and work through exercises with the instructor:

- **Split your own repository into modules** — pull the network and the app/servers/load balancer into their own directories with declared inputs and outputs, and leave the database resource where it is. Read the plan before you apply it, and confirm the destroy count is what you expect and the database isn't in it.
- **Call the same module twice** — build a second environment directory from the first, change nothing but its values file and its state key, and get an empty plan on a re-apply of the original before you count it as working.
- **Break the read-through-outputs rule on purpose** — try `module.<name>.<some_resource>.<attr>` against a resource that only exists inside a module, read the exact error Terraform gives you, then fix it by adding the output and reading `module.<name>.<output>` instead.
- **Find your own account's naming collisions** — list the resources your repository creates and sort them into "named by you, found by AWS" versus "tagged only" — that split predicts exactly which ones would fail if applied twice in one account.

**What you know now:** a **module** is a directory of Terraform with declared inputs and declared outputs, called from somewhere else by a relative path — the same idea as a `variable`, one level of size up. An **environment root** is the directory that holds the provider block, the backend, and the calls to the modules; it is not the AWS **management account** and not an account's **root user**, three unrelated things that all get called root. A module holds no provider block and no backend, so it inherits both from whichever root calls it, and `terraform init` inside a module directory fails because there's nothing there to initialize. Everything read from a module has to come through a name it declared in its own `outputs.tf` — reaching in to name a resource directly fails with `Unsupported attribute`. Of the four ways to run more than one environment — a duplicated directory, Terraform workspaces, Terragrunt, or a directory per environment — plain directories keep the repetition visible and install nothing new, at the real cost of changing shared structure in more than one place, which the modules keep small. One state key lives per environment root, one bucket per account; moving resources into modules destroys and recreates them, accepted here because they hold no data and nobody is using the system yet — and once applied, two environments differ only in their values file and the credentials the apply runs as. In a single AWS account, that copy still fails on every resource AWS finds by a name it owns — a load balancer, an IAM role, a log group, an Auto Scaling group — while everything whose `Name` is only a tag creates twice without complaint.

---

# Lesson 47 — Building the Edge: the Distribution, Denial of Service & Reading What Shipped

## Where We Left Off

Last session named the three places a copy can live — inside the application, the shared store, the edge — and closed on the test that decides whether an answer can be a copy at all. Tonight starts from a failure your monitoring cannot see, builds the third place for real — a distribution in front of a private bucket — and then defends it: what a flood of requests looks like, and the two things that stop it before it reaches your servers.

## Slow Is a Failure, and It Is Not Down

**latency** — the time an answer takes to arrive. A game with 400 ms of lag is unplayable while its server is up and every health check passes. In trading, the same delay costs money.

| What your monitoring sees | During a slow hour |
|---|---|
| **Health checks** | Pass. The server answers. |
| **The 5XX alarm** | Does not fire. Nothing returned an error. |
| **Response time** | Never graphed. Your dashboard has request count. |

Your users are waiting, and nothing you built shows it.

## What the Edge Gives a Company

| What it gives | Why |
|---|---|
| **Requests that never reach the region** | A poster served from the edge costs no server, no database and no Finnhub call. The region only sees what the edge cannot answer. |
| **The same speed in every city** | The answer comes from the user's city, not from across an ocean. A film starts as fast in Warsaw as in Chicago. |
| **The peak absorbed** | A launch, a sale, a flood of requests: the edge answers most of it, and the region sees the rest. |

The same fact that makes it fast is what protects it: a flood stops at the edge.

## A Distribution Is One CloudFront Configuration

**distribution** — which origin it reads, which name and certificate it answers on, how long copies live.

Before, `www.` reached the load balancer. After, `movies.` reaches the edge, which reads the bucket.

## CloudFront Is Not a Load Balancer

| | |
|---|---|
| **The load balancer chooses a machine** | It sits in your region in front of the Auto Scaling group and spreads requests across the machines that are healthy. |
| **CloudFront chooses a city** | It answers from the edge location nearest the user, and reads the origin only when that location has no copy. |

- **The balancer keeps balancing** — CloudFront never picks a machine. Every request the edge cannot answer still reaches the balancer, which still spreads it.
- **The name and the certificate move** — the balancer answered on your name and carried the certificate. With a distribution in front, the distribution does, and the balancer keeps its own name behind it.
- **You do not always want one** — a distribution earns its place when users are far away, or when the same answer is asked for many times. An investment application needs neither.

A load balancer named as the origin is still a load balancer. CloudFront sits in front of it. It does not replace it.

## Only the Distribution May Read the Bucket

**origin access control** — a permission on the private bucket, naming the distribution as its only reader.

In Foundations you made a bucket public. Here nobody reaches the bucket directly, not even you. Every request goes through the edge.

## The Distribution's Certificate Must Live in us-east-1

Whatever region you chose, CloudFront reads its certificates from that one region. So one apply has to touch two regions, and a second `provider` block is what says so:

```hcl
# The second provider block carries a name — an alias — and the certificate points at it
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

resource "aws_acm_certificate" "movies" {
  provider = aws.us_east_1
  # ...
}
```

Every file in the room has this block, including the ones whose region is already `us-east-1`.

## The Build: a Private Bucket, a Distribution, a Certificate

Three resources, one Terraform root of its own, separate from the application's:

- **A private bucket** — holds the movie site: a poster grid, a page per film, two or three trailers. Only the distribution may read it.
- **A distribution** — reads the bucket, answers on `movies.` under your domain, and keeps a copy at every edge location that asks.
- **A certificate in us-east-1** — with its DNS validation record, and an alias record pointing `movies.` at the distribution.

```bash
terraform apply     # several minutes: the certificate first, then the distribution reaching every edge location
```

Every resource in the plan is one of the three above.

## An Attack Sends More Requests Than a Site Can Answer

**denial-of-service attack** (**DDoS** — distributed, from many machines at once) — a flood of requests sent to exhaust a site, so that real users cannot get through.

**Ticketmaster, 15 November 2022.** The Taylor Swift presale drew 3.5 billion requests, four times its previous peak. Ticketmaster attributed it to bot attacks and to fans who had no invite code. The public sale was cancelled.

A flood arrives first at whatever faces the internet. Today that is your load balancer. Put the edge in front of it, and the flood arrives at the edge.

## Shield Standard Absorbs the Flood at the Edge, and It Is Already On

| | |
|---|---|
| **Shield Standard** | On for every CloudFront distribution and every load balancer. Costs nothing. Absorbs floods of network traffic before they reach you. |
| **Shield Advanced** | $3,000 a month per organization, on a one-year commitment: a response team and cost protection. Named here; nobody creates it. |

## WAF Checks Each Request Against Rules

**AWS WAF** (**web application firewall**) — a list of rules attached to a distribution or a load balancer. Each request is checked against them before it goes on.

- **A rate-based rule** — too many requests from one address in five minutes, the default window, and that address is blocked. This is rate limiting.
- **A managed rule set** — rules AWS or a vendor writes for known attack patterns. You attach the list; you do not write it.
- **What it costs** — bills from creation, per rule set and per request checked. Not built in this unit.

## What WAF Rules Look Like in Practice

| Rule | What it checks | What it stops |
|---|---|---|
| **Rate-based** | More than 2,000 requests from one address in five minutes | Password guessing, scraping, one machine flooding the site |
| **SQL injection match** | `' OR 1=1` and similar in a query string or form field | Requests trying to change a database query |
| **Cross-site scripting match** | `<script>` in a form field | Requests trying to plant a script in a page other users see |
| **Known bad inputs** | Strings from published exploits, such as the Log4j `jndi:` pattern of 2021 | Automated scans for a known hole |
| **IP reputation list** | Addresses AWS has seen in botnets and anonymisers | Traffic from machines already known to be hostile |
| **Geographic match** | The country the request comes from | Traffic from countries where the company does no business |
| **Bot control** | Signs of a script pretending to be a browser | The bots in the presale, challenged instead of served |
| **Allow-list on `/admin`** | Is the address in the office range? | Everyone else reaching the admin pages |

The injection, scripting, bad-input and reputation rules are lists AWS writes; you attach them. The rate-based rule and the allow-list are the two a team writes itself.

## Cloudflare, 2 July 2019: One Rule Broke the Network for 27 Minutes

A new firewall rule held a regular expression that pushed CPU to 100% on every edge server it reached. Sites behind Cloudflare returned errors, worldwide.

| | |
|---|---|
| **What users saw** | 502 errors for 27 minutes. Traffic across Cloudflare's network dropped 82% at the worst point. |
| **What caused it** | One line in one rule, deployed to the whole network in one step, with no staged rollout. |

A rule meant to protect a site is code. It is deployed like code, and it fails like code.

## Reading What Was Built: dig on the New Name

```bash
dig movies.<your domain>     # the answer section: CloudFront addresses
dig www.<your domain>        # still the load balancer's addresses
```

`host` printed the same kind of answer in the DNS topic. `dig` prints it with more detail — the record type, the time to live, and the server that answered.

## The First Request Is a Miss. The Second Is a Hit.

```bash
# The same poster, twice — -I asks for the headers only
curl -I https://movies.<your domain>/posters/<one file>
x-cache: Miss from cloudfront                          # first time from this edge location

curl -I https://movies.<your domain>/posters/<one file>
x-cache: Hit from cloudfront
age: 12                                                 # seconds since the copy was stored
```

A request may land on a different edge location and miss again. That is correct, and so is a second miss at the same one: `x-amz-cf-pop` names a point of presence, not one machine, and each cache server inside it holds its own copy. `RefreshHit` means the copy was checked against the bucket and kept. `age` counts up to the cache policy's default time to live, **86400 seconds**, and then the next request goes to the origin. A `Cache-Control` header from the origin overrides it.

A trailer is tens of megabytes. Its second play is where the edge shows.

## A Replaced Poster Still Shows the Old Picture

```bash
# Change the origin, then ask the edge again
aws s3 cp new-poster.jpg s3://<bucket>/posters/<one file>     # the bucket now holds a different picture

curl -I https://movies.<your domain>/posters/<one file>
x-cache: Hit from cloudfront                                   # still the old copy
age: 340
```

The copy at the edge is stale. It serves until its time to live ends — and the browser shows the old poster.

## Removing a Copy Before Its Time to Live Ends Is Invalidation

**invalidation** — you tell the edge location to drop its copy now, instead of waiting for its time to live.

The next request for that key is a miss. It goes to the bucket, and a fresh copy is stored at the edge.

```bash
# Drop the copy now, instead of waiting for its time to live
aws cloudfront create-invalidation --distribution-id <id> --paths "/posters/<one file>"
                                                          # the id is a Terraform output
curl -I https://movies.<your domain>/posters/<one file>
x-cache: Miss from cloudfront                            # fetched from the bucket again
```

The next request is a miss. The edge reads the bucket, stores the new copy, and the browser shows the new poster.

## Cost: Free at This Size, and a Slower Destroy

| | |
|---|---|
| **CloudFront, always free up to** | 1 TB out and 10 million requests a month. The bucket holds a few files. |
| **`terraform destroy`** | Disables the distribution, waits for that to reach every edge location, then deletes it. Longer than usual. It completes. |
| **Bills from creation** | ElastiCache and WAF. Neither is built in this unit. Shield Advanced: $3,000 a month. |

The distribution costs nothing at this size. Destroy it anyway, like everything else built in this course.

## The Assignment Is the Hands-On, on Your Own Application

- **Assignment 07, already in your repository** — a distribution in front of your own balancer. The trade button, the cash figure and the redirect each break in a different way: predict, read the header, fix it in the file it belongs in. Then one invalidation, and a timed `terraform destroy`.
- **What it does not build** — the copy inside the application, and the shared store. Assignment 07 builds the third place only. ElastiCache is the ungraded bonus at the end of its README.
- **Three places to name** — inside the application, the shared store, the edge. Never "the cache" alone.

Some answers are never a copy: if two screens may show different values for a minute, it can be a copy; if they may not, it cannot. A request answered at the edge never reaches your servers — that is why the edge is both the speed and the protection.

---

# Lesson 48 — Serverless: Code That Runs Only When Something Happens

## Where We Left Off

Last session finished the edge unit: a distribution in front of a private bucket, and Shield and WAF absorbing a flood before it reaches your servers. Tonight opens a new unit inside Scale, and it starts from a fact about everything built so far: your instance, your Flask app under systemd, nginx, Postgres, cron — every one of them is a program that starts, waits, and is billed for every hour it waits, whether or not anyone asks anything of it. Your news bot runs for under a minute once a day. The `t3.micro` under it is billed for the other twenty-three hours anyway. Tonight names the other shape a running program can take, and builds one for real.

## A Daemon Waits for Work, Billed for Every Hour It Waits

**daemon** — a program that waits for work. It starts when the machine boots and runs until it is stopped, waiting the whole time. It is billed for every hour it waits, whether or not any work arrives.

The logging topic called this the background process. You already run several: the Flask app under systemd, nginx, Postgres, and cron itself — the daemon that starts your news bot's script at 09:00 and then goes back to waiting.

## An Event Is One Thing That Happened, Written Down as Data

**event** — one thing that happened, written down as data a program can read. A request arrived, a file landed in S3, the clock reached 09:00, a message was sent to a bot — each one is an event.

The logging topic defined a **log event** as what the application wrote when something happened. Same word, same sense.

## Event-Driven Code Runs on an Event, Handles It, and Stops

**event-driven** — code that runs on an event. It starts when the event arrives, handles that one event, and stops. Your news bot's script at 09:00. A Telegram bot answering a message. A push notification when a card is charged.

One order placed in a phone app fans out into three separate runs: charge the card, print the kitchen ticket, send the confirmation. Three events from one order, not one program handling all three.

## The Same Day, Run Both Ways

| | Billed |
|---|---|
| **A daemon** | Running from midnight to midnight. Billed for every hour, however many requests arrive. |
| **Event-driven code** | Running only where a mark is. Billed for each run, and for nothing in between. |

Your news bot's script is event-driven. The daemon is the machine under it, and cron on it, waiting all day so the script can start on time.

## A Function Is a Named Block of Code — the First `def` in the Course

**function** — a named block of code. It is called by its name with an input, and it gives an output back.

Foundations taught variables, lists, loops and conditions. It never taught how to define one. This is the first `def` in the course:

```python
def quote(symbol):
    price = fetch_price(symbol)
    return f"{symbol}: {price}"

quote("AAPL")
quote("MSFT")
```

`def` names it. The name is `quote`. `symbol` is the input. `return` gives the output back. Called twice here, with a different input each time. `fetch_price` is another function, written somewhere else.

## Serverless: You Upload the Code, and AWS Runs It on Its Own Machines

**serverless** — you upload the code; AWS runs it on its own machines. When an event arrives, AWS runs your code on a machine it chose and bills you for the milliseconds it ran. When nothing arrives, nothing runs and nothing is billed.

**Lambda** — AWS's service for this. You give it the code and the events that trigger it.

**handler** — the named function Lambda calls, with the event as its input. You say which one it is.

## There Is a Server. You Just Never Choose It, Patch It, or Pay for It Waiting.

- **You never choose it** — no instance type, no image, no boot script. AWS picks the machine for each run.
- **You never patch it** — the operating system and the Python runtime are AWS's to update.
- **You never pay for it waiting** — billing starts when your code starts running and stops when it returns.

What your code prints goes to CloudWatch Logs, into a log group — the same kind of log group the logging topic taught. Nothing is installed on anything to make that happen.

## What the Same Stack Costs at Zero Traffic

| What is running | Rate | A month |
|---|---|---|
| The instance, one `t3.micro` | $0.0104 an hour | about $7.50 |
| The load balancer | $0.0225 an hour before any traffic | about $16 |
| The database, one `db.t3.micro` Postgres in one zone | $0.017 an hour before storage | about $12 |
| The same page on Lambda, at your traffic | inside the free allowance of 1 million requests and 400,000 GB-seconds a month | $0 |

*List prices, not a bill — us-east-1, on-demand, per month, at zero traffic.*

This is not an argument for cheapness. Instances behind a balancer are the correct design for a page that must answer immediately and hold a database connection. The question the rest of tonight answers is which jobs fit a function.

## One Function, Run Twice From the Console

```
REPORT Duration: 412.35 ms  Billed Duration: 413 ms        ← first run
       Memory Size: 128 MB  Max Memory Used: 41 MB  Init Duration: 187.22 ms

REPORT Duration: 2.11 ms  Billed Duration: 3 ms            ← second run
       Memory Size: 128 MB  Max Memory Used: 41 MB
```

**Duration / Billed Duration** — how long your code ran, and what is charged, rounded up to the millisecond. **Memory Size / Max Memory Used** — the RAM you gave the function, and the RAM it actually used; those are the console's own words for it. **Init Duration** appears on the first line only. The second run has no such field.

## The Sentence: Between Events, Nothing of Yours Is Running

> Between events, nothing of yours is running, and the environment the last run used is gone.

**environment** — the place one run happens: your uploaded code with the Python runtime started under it, on a machine AWS chose.

The package you uploaded stays uploaded. The environment that ran it does not. That difference is why the first `REPORT` line above carries an `Init Duration` and the second one doesn't — the first had to build a fresh environment before it could run at all.

## Five Questions, Answered From What Was Already on the Screen

### Where is a copy your code kept, when the next request arrives?

If your function kept a copy inside itself the way the caching topic taught — to hand back on the next request instead of asking Finnhub again — that copy is gone the moment the environment is. Anything held in a variable, and anything written to the function's own disk (**ephemeral storage**, 512 MB by default and up to 10 GB), goes with it. Only something written outside the function — S3, your RDS database, another store — survives to the next run.

The local cache from the caching topic cannot exist here. Statelessness was a discipline in the autoscaling topic; here it is enforced.

### Why was the first run slower than the second?

**cold start** — starting a fresh environment before the code runs: download the package, start the Python runtime, then call the handler. A few hundred milliseconds. `Init Duration` on the first `REPORT` line above is that number. Booting a replacement instance from user data in the autoscaling topic took minutes; a cold start starts a process, not a machine. AWS does not publish how long an environment stays warm — the next day's call is cold again.

### What happens when two requests arrive at the same moment?

They run the function twice, in two environments. No queue behind one process, no scaling policy, no minimum, no desired capacity. A thousand orders at lunch are a thousand events or more, each in its own environment. A thousand runs at 200 milliseconds each is 200 seconds of billed time, so the bill is not the risk. The limit is 1,000 running at once per region by default, and AWS will raise it on request.

### What do a thousand of them at once do to one Postgres?

Each environment opens its own connection. None of them shares a running process, so none of them shares a set of open connections — one Postgres instance is asked for a thousand connections at the same moment. That's the risk, and it's why the database that belongs beside a function is one reached over HTTPS, with no connection to hold.

**DynamoDB** — AWS's managed key-value database. Nothing to run, billed per request, reached over HTTPS. A thousand functions calling it do not hold a thousand connections open. **Key-value** means you store a value under a key and read it back by that key — there's no query across the whole table the way there is in Postgres. It's the database most often paired with Lambda, for exactly this reason.

### A failed event is retried. What does that mean for your code?

**idempotent** — doing the same work twice does no damage; running it once and running it twice leave the same result.

| | |
|---|---|
| **Writing a row with the same key twice** | Fine. The second write replaces the first with the same value. |
| **Charging a card twice** | Not fine. The customer paid twice, and nothing about the second charge looks wrong. |

A retried event runs the same work again, and the run that failed left nothing behind to tell the second attempt that. So the code has to be idempotent.

## The Execution Role: the Function Runs as a Role, and Nothing Else

**execution role** — the IAM role the function runs as. What the function may touch, it touches through this role, and nothing else. It's the same kind of role as the instance role from Foundations — its trust policy names Lambda as the trusted entity, Foundations' phrase for who may use this role.

## Two Settings Are the Whole Sizing Model

- **RAM** — from 128 MB to 10,240 MB. The console labels this field `Memory`. CPU is given in proportion to it, and is not a separate setting.
- **timeout** — from 1 second to 900 seconds. 900 seconds is fifteen minutes, and it is the maximum there is.

The runtime — Python, Node.js, Java, Go, C# or Ruby — is a separate choice, made from a list, and it isn't part of the sizing. Foundations chose an instance family and a size from a table of them. Here there are two numbers, and no table.

## API Gateway Turns an HTTP Request Into an Event

**API Gateway** — it turns an HTTP request into an event. It receives the request, picks the function by path and method, calls it with the request written as the event, and returns the answer. A browser does not call a function directly.

Your load balancer forwards to machines already running. API Gateway calls code that is not running until the request arrives.

## Other Ways to Start a Function

| Trigger | What it is |
|---|---|
| **A function URL** | One address that goes straight to one function. No routes, no paths, nothing to configure between them. |
| **Your own load balancer** | It can send a path to a function as a target, the same way it sends a path to an instance. |
| **An EventBridge rule** | A schedule, not a request — every day at 09:00, Monday to Friday, run this function. That is your news bot, with no machine under it. |

API Gateway is the one used tonight.

## Inside the VPC or Outside It — Lambda's Networking Is a Choice You Make

- **Outside the VPC** (the default, nothing to configure) — the function reaches the public internet. It cannot reach a database in a private subnet.
- **Inside the VPC** (you give it subnets and a security group) — it reaches your private database, and reaches nothing public unless that subnet has a NAT gateway.

A function in a private subnet with no NAT gateway can read your RDS instance and cannot call Finnhub. Tonight's function needs both, so it runs in a subnet that has a NAT gateway.

## The Invoke Permission: Who May Call the Function, Not What It May Touch

**the invoke permission** — attached to the function, naming who may call it. API Gateway may not call your function unless a permission on the function says it may. In Terraform this is `aws_lambda_permission`, naming `apigateway.amazonaws.com` as who may call.

You've seen this shape before: the trusted entity on a role, and the policy Foundations wrote on the public S3 bucket. The role says what the function may touch; this says who may call the function — two different questions, two different attachments.

## Without the Permission, Every Request Is a 500

```
{"message":"Internal Server Error"}
```

The function's log group shows no invocation at all. A 500 with an empty log group is the diagnosis: the function was never called. Lambda answers API Gateway with a 403; API Gateway can't complete the request, so the browser is handed a 500. This is the most common cause of a 500 when a function sits behind API Gateway — verified live in the cohort's own account, where adding the missing `aws_lambda_permission` turned the same route from a 500 into a 200 with nothing else changed.

## Four Resources, and a URL That Returns a Stock Quote

- The execution role
- The function, fetching the Finnhub quote
- The API Gateway route
- The invoke permission

Its own Terraform root, with its own state key, separate from the three environment roots:

```hcl
resource "aws_iam_role" "lambda_exec" {
  name               = "quote-function-exec"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust.json   # trusts lambda.amazonaws.com
}

resource "aws_lambda_function" "quote" {
  function_name = "quote"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "app.handler"
  runtime       = "python3.13"
  memory_size   = 128
  timeout       = 10
}

resource "aws_apigatewayv2_api" "quote" {
  name          = "quote-api"
  protocol_type = "HTTP"
}
# one route, integrated to aws_lambda_function.quote

resource "aws_lambda_permission" "apigw" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.quote.function_name
  principal     = "apigateway.amazonaws.com"
}
```

## Claude Code Writes It, Applies It, Calls the URL, Destroys It

Claude Code wrote the Terraform live: the IAM role trusting `lambda.amazonaws.com`, the function naming its handler, runtime, RAM and timeout, the HTTP API and its one route integrated to the function, and the permission naming `apigateway.amazonaws.com` as who may call it. The URL, called once after a cold start and once straight after, produced the same two `REPORT` lines as the console demo — one with an `Init Duration`, one without. Then `terraform destroy`.

## Code Written for a Server Doesn't Move to Lambda in Its Current Shape

Moving to Lambda means the code has to change shape first:

- **Shaped as a handler** — one named function, called with the event as its input.
- **No state in the process** — nothing held from one request to the next, because the environment doesn't survive.
- **Finished inside the timeout** — fifteen minutes at most, and usually far less.

Those changes are the developers' work. The platform engineer has to know they exist, and has to say so before a migration is planned around them. Your news bot can't move as it is either — the Claude command-line tool doesn't run inside Lambda. A function version would have to call the APIs directly from Python.

## Two Questions Decide Whether a Job Fits: How Often, and How Long

- **How often it runs** — once a day, once an hour, every second.
- **How long one run takes** — under a second, a few minutes, over fifteen.

A run longer than fifteen minutes cannot run on Lambda at all. A job that's busy all the time costs more than the instance it would replace. What's left — a job that runs rarely and finishes quickly — fits a function.

## Six Jobs, Placed on the Two Axes

| Job | How often | How long | Fits? |
|---|---|---|---|
| Your news bot | Once a day | Seconds to minutes | Fits |
| A report at midnight | Once a day | Seconds to minutes | Fits |
| A thumbnail made when a photo is uploaded | A few times an hour | Under a second | Fits |
| A webhook from a payment provider | A few times an hour | Under a second | Fits |
| Your page at steady traffic | Constant | — | Costs more than the instance |
| Your trading path | Constant | — | Costs more than the instance |

The two that don't fit aren't rare or slow — they're busy all the time, which is exactly the shape a daemon behind a balancer is built for, and exactly the shape a function is billed against.

## The Question to Answer in Your Own Account

Two sentences, a number in each: one job in your account that should become a function, and what it costs today running as a daemon; one that should stay on the instance, and why.

**What you know now:** a **daemon** waits for work and is billed for every hour it waits, whether work arrives or not — your Flask app, nginx, Postgres and cron are all daemons. **Event-driven** code runs only on an **event**, one thing that happened written as data, and a **function** is a named block of code called with an input and returning an output — the first `def` in this course. **Serverless** means you upload the code and AWS runs it on a machine it chooses, billed for the milliseconds it ran; there is a server, you simply never choose it, patch it, or pay for it waiting. The sentence to carry forward, always in full: between events, nothing of yours is running, and the environment the last run used is gone — the package you uploaded stays uploaded, the environment that ran it does not. That single fact answers all five questions: state has to live outside the function, since **ephemeral storage** and anything held in a variable don't survive between runs; the first call after downtime pays a **cold start** while a fresh environment is built; concurrent requests each get their own environment, with no queue and no scaling policy behind them; a thousand of them at once means a thousand database connections, which is why **DynamoDB** — billed per request, reached over HTTPS, no connection to hold — is the database usually paired with Lambda; and a retried event means the code has to be **idempotent**, since the failed run left nothing behind to say it already tried. Around the function itself: an **execution role** decides what it may touch, RAM and timeout are the whole sizing model, **API Gateway** turns an HTTP request into an event a function can receive, and **the invoke permission** decides who may call the function at all — leave it off and every request comes back a 500 with an empty log group, because Lambda answered API Gateway with a 403 and API Gateway couldn't complete the request. Whether a job belongs here comes down to two questions — how often it runs, and how long one run takes — with anything over fifteen minutes ruled out entirely and anything busy all the time costing more than the instance it would replace; a news bot and a midnight report fit, a steady-traffic page and a trading path don't.

---

# Lesson 49 — Where Serverless Doesn't Fit, and the Third Way to Run Code

## Where We Left Off

Last session ended on the decision framework: how often a job runs, and how long one run takes, six jobs placed on those two axes, and a question left for your own account — one job that should become a function, one that should stay on the instance. Tonight fills in the edges of that framework with the four concrete places a function is the wrong choice, four real companies who ran into exactly those edges, a wider view of what AWS itself calls serverless beyond Lambda alone, and the third way to run code that sits between an instance you own and a function AWS owns entirely: a container.

## Four Places a Function Is the Wrong Choice

| Reason | Why |
|---|---|
| **Work longer than fifteen minutes** | The timeout is the maximum there is. A job that takes an hour cannot run as a function. |
| **Steady high traffic** | A function kept busy all month costs more than the instance that would have served the same requests. |
| **A request that cannot wait for a cold start** | The stock buy on your own page: the price can move in the few hundred milliseconds the environment takes to start. |
| **Moving to another cloud** | Your Python code moves. The triggers, the roles and the permissions are AWS's own, and have to be written again for the other cloud. |

## Amazon Prime Video: The Case Against Steady High Volume

March 2023. A tool inside Prime Video checks every stream for picture and sound defects — frozen frames, audio out of sync with the video. This is not monitoring in the sense the logging topic taught: it looks at the picture and the sound themselves.

| | |
|---|---|
| **What it ran on** | Step Functions, AWS's service that runs steps in order, and Lambda, passing each video frame between steps through S3. At the volume of every stream, the bill was the state transitions and the S3 calls. |
| **What they changed** | The team packed the steps into one process on ECS and EC2, and cut that tool's infrastructure cost by over 90 percent. |

One internal tool, not Prime Video itself — the case for steady high volume being the wrong fit, published by an Amazon team.

## The LEGO Group: Built for a Spike, Not a Steady Load

| | |
|---|---|
| **2017** | Peak traffic overwhelmed the on-premises commerce back ends behind lego.com, and shoppers got 503 errors. A 503 is the server saying it cannot take the request right now — an overloaded back end returns one, and so does a load balancer with no healthy target. |
| **The rebuild** | The shop was rebuilt on Lambda, API Gateway, DynamoDB, and three AWS services that pass work between functions: SQS (queues), SNS (notifications) and Step Functions (steps in order). shop.LEGO.com switched over on 10 July 2019. |
| **The load** | Sales events drive transactions up to 200 times normal for a few hours. |

The commerce back ends, not the whole company — the case for spikes: idle for most of the month, and very large for one afternoon.

## Coca-Cola: Working Out the Break-Even

The vending backend, 2016 — the service that handles a phone tap at a vending machine.

| | A year |
|---|---|
| On six EC2 instances | about $12,900 |
| On API Gateway and Lambda, at 30 million requests a month | about $4,500 |
| The architect's break-even | about 80 million calls a month |

One small service, not Coca-Cola's infrastructure. Above the break-even the instances cost less. The number is theirs. The lesson is that every job has a break-even, and it can be worked out before choosing.

## iRobot: A Company's Main Product, Run by Fewer Than Ten People

| | |
|---|---|
| **The connections** | AWS IoT Core takes the robots' connections. Lambda runs the code behind them, with DynamoDB for state. |
| **What they run** | Over a hundred functions, and no EC2 instance they manage. |
| **The size of it** | About two million connected robots by 2018, run by fewer than ten people. |

The robot backend, not iRobot's whole business — the case for a company's main product running this way.

## Serverless Is Wider Than Lambda

AWS calls DynamoDB, Aurora Serverless, Fargate, S3 and SQS all serverless. They share three things: no instances to choose or count, billing by use, and scaling down to zero when nothing arrives.

| Cloud | Their name for it |
|---|---|
| Microsoft Azure | Azure Functions. |
| Google Cloud | Cloud Functions, and Cloud Run for a container. |
| Cloudflare | Cloudflare Workers, which is a product name, running at the kind of edge locations the edge topic taught. |

## Three Ways to Run Code

- **Instances you own** — an image, an Auto Scaling group and a balancer in front of them. Everything built so far in Scale.
- **A function AWS runs** — a package and an environment AWS starts for one event, and stops.
- **A container** — a boxed package that runs unchanged in more than one place: a laptop, EC2, Fargate, or Kubernetes.

Fargate sits on the line between the second and third of these: it runs a container on a machine AWS owns. The container is the next stage.

## The Assignment, and the Sentence Carried Forward

Nothing from this unit is running in your account, so there is nothing to destroy — the assignment is where you build one. Two sentences, a number in each: one job in your account that should become a function, and what it costs today; one that should stay on the instance, and why. The four real cases are posted with their scopes and their sources.

Between events, nothing of yours is running, and the environment the last run used is gone. Everything else in this unit came from that.

**What you know now:** four concrete places rule a function out — longer than fifteen minutes, steady high traffic, a request that can't wait for a **cold start**, or moving to another cloud whose triggers and roles aren't AWS's — and each is backed by a real company, not a hypothetical. **Amazon Prime Video** paid Step Functions' per-transition billing at the volume of every stream and cut one internal tool's cost by over 90 percent by packing the steps into one process on ECS and EC2 — the case against steady high volume. **The LEGO Group**'s on-premises commerce back ends returned 503s under 2017's peak traffic and were rebuilt on Lambda, API Gateway, DynamoDB, SQS, SNS and Step Functions to absorb sales spikes up to 200 times normal — the case for a load that is idle most of the month and very large for one afternoon. **Coca-Cola**'s vending backend had a real break-even, about 80 million calls a month, above which six EC2 instances cost less than API Gateway and Lambda — proof that every job's break-even can be worked out before choosing. And **iRobot** runs its entire connected-robot backend — AWS IoT Core, over a hundred Lambda functions, DynamoDB for state — for about two million robots with fewer than ten people, the case for a company's main product running this way. Serverless itself is wider than Lambda: DynamoDB, Aurora Serverless, Fargate, S3 and SQS all share three traits — no instances to choose or count, billing by use, and scaling to zero — and every other cloud has its own name for the same idea, Azure Functions, Google Cloud Functions and Cloud Run, Cloudflare Workers. Everything built in Scale up to tonight is the first of three ways to run code — instances you own, behind a balancer; a function AWS runs, started fresh for one event and gone; and a container, a boxed package that runs unchanged on a laptop, EC2, Fargate or Kubernetes. Fargate itself already runs a container on a machine AWS owns, and the container is the next stage.
