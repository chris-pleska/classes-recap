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

---

## Lesson 17: Virtualization, Your Slice & Ports/Firewall
An EC2 instance is a **virtual machine** — no single physical box IS your box. A **hypervisor** (AWS uses the Nitro System, built on Linux's KVM) runs on real hardware and carves it into many VMs, each with its own OS.

**Look inside your box:**
```bash
sudo dnf install htop   # Amazon Linux (Ubuntu: sudo apt install htop)
htop                    # vCPUs and RAM moving in real time
nproc                   # count the vCPUs
free -h                 # RAM slice, human units
df -h                   # disk, seen from inside
uname -a                # OS and kernel
```

**Decode an instance type, e.g. `t3.micro`:** family (`t` = burstable/general purpose) · generation (`3` = hardware era) · size (`micro` = 2 vCPU, 1 GB RAM). Families: `t`/`m` = balanced, `c` = compute-heavy, `r` = RAM-heavy, `g`/`p` = GPU.

**Reserved vs on-demand:** committing 1-3 years can cut the price ~40% — a real lever (FinOps) at company scale.

**AMI** = Amazon Machine Image — the frozen disk your box was copied from at launch (Amazon Linux 2023 → `dnf`/`ec2-user`; Ubuntu → `apt`/`ubuntu`). A **golden AMI** is one you snapshot yourself to launch identical copies later.

**Ports & firewall:**
- A port is a numbered door (0–65535); a program **listens** on one. Port 80 = web, 22 = SSH.
```bash
sudo ss -tlnp    # -t TCP, -l listening only, -n numeric, -p show program
```
- The **security group** is AWS's firewall — checked before traffic ever reaches your machine's ports. Removing the port-80 rule doesn't kill the server or the app (`gunicorn` keeps listening) — it just blocks traffic from getting there.
- **Inbound** vs **outbound**: replies don't need their own rule — a security group is **stateful**, it remembers the connection a visitor opened and lets the reply ride back.
- SSH rule source `0.0.0.0/0` = anyone may try to connect (your key still guards the login); locking source to your own IP is safer but breaks if your IP changes.

---

## Lesson 18: The Neighborhood — IPs, CIDR, VPCs & Route Tables
A **network** = computers that can pass messages to each other, each with an address. Your box has **two** addresses: a public IP (reachable from the internet) and a private IP (only means something inside its own fence).

**IP anatomy:** four slots, each 0–255 (one byte = 8 switches, 256 combos). 4 slots × 256 = ~4.3 billion addresses total — that's a **32-bit address**, and it's why IPv4 ran out.

**Private ranges** (reusable behind any fence, never routable on the internet):
```
192.168.x.x     # home routers
172.16–31.x.x   # AWS hands your box its 172.31... from here
10.x.x.x        # big companies
```

```bash
ip addr    # see your box's private IP from inside it
```

**Elastic IP:** your public IP is normally borrowed — stop/start the box and you get a new one, breaking DNS. An Elastic IP is reserved for your account and survives stop/start. Costs ~$0.005/hr (~$3.65/mo), even while idle/unattached — release it when unused.

**CIDR — `/number` decodes a block:** the number = how many of the 32 switches are locked (fixed); the rest are free and determine block size.
```
10.0.0.0/8      # 1 slot locked  → 16,777,216 addresses
172.31.0.0/16   # 2 slots locked → 65,536 addresses (your VPC)
192.168.0.0/24  # 3 slots locked → 256 addresses
x.x.x.x/32      # all locked     → exactly 1 address
0.0.0.0/0       # 0 locked       → every address — "anyone" in a firewall rule
```

**VPC** (Virtual Private Cloud) = your fenced-off patch of AWS's network — yours owns `172.31.0.0/16` by default. A **subnet** is a smaller block cut from the VPC's block; a machine always launches into a subnet, never "into the VPC" directly.

**Route tables** = each subnet's directions: "traffic going THERE → send it THIS way."
```
172.31.0.0/16 → local              # stays inside the fence
0.0.0.0/0     → igw-0a1b2c...      # everywhere else → internet gateway
```
More-locked rows win ties (a `/16` beats `/0`), so neighborhood traffic never accidentally leaves. A subnet is **public** if its route table has the `0.0.0.0/0 → igw` row, **private** if that row is simply missing — one missing row is the entire difference.

**Full request path:** name → DNS → public IP → internet gateway → public subnet → security group check → port 80 → app answers.

---

## Lesson 19: Data Storage — EBS Volumes, Snapshots & S3
All data is bytes — bit → byte → KB → MB → GB → TB. Your server's disk is really an **EBS volume**: separate storage hardware attached to your server over the network, not something physically inside it. Killing the server doesn't touch it — except the **root disk**, which is set to delete with the server by default.

**Inspect and attach a disk:**
```bash
lsblk                              # list disks the server can see
sudo mkfs -t ext4 /dev/nvme1n1      # format a blank disk
sudo mount /dev/nvme1n1 /mnt/spare  # plug it into a folder
df -h /                            # size, used, available, use% for the root volume
sudo du -sh /* | sort -h            # find what's eating the disk
```

**Backups:** a **snapshot** is AWS's backup of a whole EBS volume — kept away from your server, one click in the console. A copy on the same disk isn't a backup; if the disk dies, both copies die together.

**Restore:** create a new volume from a snapshot → attach it to any server → mount it. Backup + new disk + any server = a restore.

**S3 — storage that isn't a disk:**
- **bucket** = a named container you create
- **object** = one file in it, fetched by name, replaced whole (never edited in place)
- Every object has a web address: `bucket-name.s3.region.amazonaws.com/object-name`
- New buckets are **private by default** — nothing is public unless you decide it

**Disk vs S3:** a volume is a rented disk — pick a size, pay for all of it, serves one server. A bucket is bottomless — pay per GB actually stored, served to anyone you allow, no server of yours required. Backups, logs, and images that grow forever belong in S3; files a server needs to run belong on its disk.

**The map:** RAM (working space, wiped on reboot) → the EBS volume (server's disk — OS, app, Postgres's files; backed up via snapshot) → S3 (files served by web address). Postgres isn't a third place — it's a program whose files live on the disk.

---

## Lesson 20: The Database — Postgres, Tables & SQL
A **database** = a separate program whose only job is records: keep them safe, answer questions fast, serve many clients at once, never lose a fact. A file (`trades.txt`) fails this: half-written on a crash, slow to search line by line, and two writers at once clobber each other.

**Relational** = records live in **tables** (one kind of fact per table; rows = facts, columns = details), and tables **point at each other by id** instead of copying data — e.g. a transaction stores `company_id = 1` rather than repeating NVIDIA's name/price. Postgres, MySQL, SQLite, SQL Server, Oracle are all relational and all speak **SQL**. NoSQL (MongoDB, Redis, DynamoDB) skips tables entirely — different shape, not better/worse.

**Install Postgres from scratch:**
```bash
sudo dnf install postgresql16-server
sudo postgresql-setup --initdb
sudo systemctl enable --now postgresql
sudo ss -tlnp | grep 5432                 # confirm it's listening
echo 'host all all 127.0.0.1/32 md5' | sudo tee -a /var/lib/pgsql/data/pg_hba.conf
sudo systemctl restart postgresql
```

**Create a user + database (as the `postgres` admin):**
```bash
sudo -u postgres psql
CREATE USER app_user WITH PASSWORD '...';
CREATE DATABASE investapp OWNER app_user;
```
Grant a read-only user access to someone else's database:
```sql
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_user;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;
```

**psql — the terminal client for Postgres:**
```bash
psql -U app_user -d investapp   # connect: which user, which database
\dt                              # list tables
\d companies                     # describe a table's columns/types
```

**Schema** = the full plan (tables, columns, types) — a contract the database enforces; a row that doesn't fit is refused. Types: `text` (str), `integer` (int), `numeric` (money — exact decimals; **never use float for money**, `0.1 + 0.2` ≠ `0.3`), `timestamp`. Every row also gets a **primary key** (`id`) — how other rows point at it.

**SQL — ask the database questions:**
```sql
SELECT * FROM companies;                       -- show me everything
SELECT * FROM companies WHERE price < 100;      -- numbers compare bare
SELECT * FROM companies WHERE symbol = 'NVDA';  -- text goes in 'quotes'
```

**Backup and restore — `pg_dump` writes the whole database out as a readable `.sql` file:**
```bash
pg_dump -U app_user investapp > backup.sql   # back it up (store off the same disk, e.g. S3)
psql -U app_user -d investapp < backup.sql   # restore: feed the dump back in
```
A plain `pg_dump` carries tables + rows but not users/roles — those must be recreated by hand (or use `pg_dumpall --globals-only`).

---

## Lesson 21: HTML — Labels, References & the Three Languages of a Page
A web page is a text file. **HTML** (HyperText Markup Language) is a markup language — its statements **label** content (what things ARE). Unlike Python, it can't compute: no variables, no `if`, no loops. That's on purpose — a label only describes, it can't crash.

**The one page shape, every page on earth:**
```html
<html>
  <head>
    <title>Plov House</title>   <!-- what the browser tab shows -->
  </head>
  <body>                        <!-- the page itself, what the visitor sees -->
    <h1>Plov House</h1>
    <p>Plov — rice, carrots, lamb. $12</p>
  </body>
</html>
```

**Element anatomy:** opening tag + content + closing tag = an element, e.g. `<h1>Plov House</h1>`.

**Reference = one file pointing at another, by path.** Same idea, paid four times:
```html
<img src="images/plov.png">               <!-- a picture -->
<a href="drinks.html">Drinks</a>          <!-- another page -->
<link rel="stylesheet" href="style.css"> <!-- CSS — the looks -->
<script src="menu.js"></script>          <!-- JavaScript — instructions -->
```
A website is just files pointing at files. Break one reference (rename the image) and only that part fails — everything else on the page still renders; diagnose by eye (the broken-image icon marks the spot).

**Three languages, three verbs:**
- HTML = what things ARE (rendered)
- CSS = how they LOOK (rendered)
- JavaScript = what to DO (executed, after render — folding menus, form validation, feeds that grow with no reload)

Chrome's rendering engine is **Blink**; its JavaScript engine is **V8**.

**Markdown** is a different markup — not for browsers. It's for humans (and AI) reading docs/READMEs directly; GitHub renders it, but no browser ever does.
