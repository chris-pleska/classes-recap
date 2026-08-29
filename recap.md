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

---

## Lesson 22: HTTP — Requests, Responses & the Network Tab
A **protocol** is an agreed set of rules two programs follow so they can talk without ever having met — SSH, DNS, and HTTP are all protocols already in use. **HTTP** (HyperText Transfer Protocol) is the protocol pages travel by: a **client** sends a request, a **server** sends back a response. Whoever asks is the client, whoever answers is the server — the same machine can be either, depending on the protocol (your Mac is the client over SSH into your EC2, but the server for HTTP requests it answers).

**A URL, left to right:** `http://server.aigul.click/portfolio` — protocol, then domain (DNS turns it into an IP), then path. HTTP arrives at **port 80**, HTTPS at **443**, beside SSH's **22**.

**The request, raw — a request line then headers (labeled facts):**
```
GET /portfolio HTTP/1.1
Host: server.aigul.click
User-Agent: ...
```

**The response, raw — status line, headers, one empty line, then the body (the HTML itself):**
```bash
curl http://<domain>/portfolio      # prints just the body
curl -i http://<domain>/portfolio   # -i: status line + headers too
```

**Status code families:**
- `2xx` = it worked (200 OK)
- `3xx` = go elsewhere — a redirect the browser follows on its own
- `4xx` = the request is wrong (404 Not Found)
- `5xx` = the server broke

Chrome's **Network tab** (`⌥⌘I` → Network) shows one row per request/response. Loading one page is rarely one row: Chrome parses the HTML, finds every `<link>`/`<script>`/`<img>` reference, and requests each on its own — sometimes from a different machine entirely (e.g. a logo served from S3, not your EC2).

**Under the hood:** TCP opens a connection first (a three-way handshake), then carries the HTTP text in order, both directions. Plain HTTP is a postcard — any machine in between can read it. HTTPS is the same conversation, encrypted before it leaves — same shape, port 443 instead of 80.

---

## Lesson 23: Static Hosting — nginx & S3
**Hosting** = files on a machine that is always on, has a public IP, and runs a program listening on port 80 that reads each request's path, finds the file, and answers. Your Mac fails this: private IP, sleeps when closed.

**nginx** (say "engine-x") is the web server — a program whose whole job is that list. Install and start it:
```bash
sudo dnf install nginx
sudo systemctl enable --now nginx   # start now + on every reboot
```
Before install: `curl http://<ip>` → *connection refused* (port open, nobody listening). After: `curl -i http://<ip>` → `200 OK`.

**The one rule everything rests on: this address → this file.** The request's path names a file under one root folder — nothing outside it is reachable. Three settings in `/etc/nginx/nginx.conf` carry the whole story:
```
listen 80;                    # answer on port 80 (IPv4)
listen [::]:80;               # same port, IPv6
root /usr/share/nginx/html;   # every path is found under here
index index.html;             # for /, hand back index.html
```
A path starting with `/` in an `<img src="/images/x.png">` is absolute to that root folder, e.g. `/usr/share/nginx/html/images/x.png` — not the filesystem root.

**Deploy files onto the server:**
```bash
git clone https://github.com/<user>/menu.git
sudo cp -r menu/* /usr/share/nginx/html/
```
Copy into the default root, not a home folder — nginx can't read a home folder's permissions, and you'll get `403 Forbidden`.

**Static site** = every answer already existed as a file before the request came — same bytes, every time, for everyone.

**S3 as a second way to host — no server at all.** A bucket already satisfies hosting's three requirements: AWS's machines are always on, a bucket gets a public website endpoint, and "ask for a file by name, get it back" is the same this-address-to-this-file rule.
1. Create a bucket, upload the files.
2. Turn **off** "Block public access" (a master override — expected here, since this bucket is public on purpose).
3. Add a bucket policy allowing public `s3:GetObject` (read-only).
4. Properties → Static website hosting → on, index document `index.html`.
5. Open the website endpoint URL.

**Your own server vs S3:**
| | own EC2 + nginx | S3 static |
|---|---|---|
| control | full | limited to AWS's rules |
| HTTPS | possible (certbot) | no — needs CloudFront |
| cost (small site) | ~$108/yr | ~$10/yr |
| upkeep | patch/keep the machine alive | nothing to run |

---

## Lesson 24: Dynamic & the API — Backend, Frontend, Database
**Static** fails the moment an answer doesn't exist yet as a file — a stock price moves, a buy changes the page, a trade is work to *do* (check price, move cash, record trade), not a page to serve. **Dynamic** = the response is composed at the moment of asking, from what's true right now — same address, different answer, depending on state.

```bash
curl http://<ip>/     # read cash + holdings
# ...make a trade in the browser...
curl http://<ip>/     # same address — the numbers moved, nobody edited a file
```
What comes back is still ordinary HTML — a program filled blanks in a template moments ago; the template is a file, the finished page never is.

**Who answers on the server:**
```bash
sudo ss -tlnp   # -t TCP, -l listening only, -n numeric, -p show program
```
`gunicorn` — not nginx — holds port 80 for a dynamic app. **Flask** is the ready-made Python web plumbing your code is built from; **gunicorn** is the always-on runner that executes that code for every request (like typing `python3`, but never stops). gunicorn runs multiple copies of your code at once — nobody waits in line. Both are choices, not standards — HTTP, ports, and HTML are standards every app shares; Python/Flask/gunicorn/Postgres are just this build's picks. "Server" now names a program too, not just the machine — read from context which one is meant.

**The three tiers:**
- **Frontend** — HTML/CSS/JS rendered in the browser, on your machine (**client-side**). What you see.
- **Backend** — your Flask code, run by gunicorn, on the server. No screen, no buttons, never seen — composes every answer from the database beside it.
- **Database** — the backend's memory (cash, holdings, prices). The backend is the *only* path in — your browser can never query it directly, so it alone decides what can be asked.

**API — Application Programming Interface:** the agreed list of requests a program offers other programs. Making one is an **API call**. Programs talk to programs with no screen involved — your news bot calling Anthropic's API and Telegram's Bot API is the same shape as a taxi app's backend calling a maps API and a payments API. Your own app's API: `GET /` (check portfolio), buy a stock, sell a stock — offered to the frontend; when a saved price goes stale, your backend becomes the *client* and calls the price service's API.

In Chrome's Network tab (Preserve log ON), a stock buy shows as `POST` → `302` (backend did the work, then redirected) → `GET /` → `200` (fresh composed page) — versus `style.css`/`logo.png` which are plain finished-file fetches, not API calls.

**Skipped on purpose:** login/**authentication** — the backend's check of *who* is asking, before it answers. One server, one owner here; a real multi-user app checks this on every request.

---

## Lesson 25: Data to the Backend — Payloads, Dicts & Routes
A stock buy isn't a plain page fetch — clicking Buy **sends** something (which stock, how many shares) along with the request. Chrome's Network tab (Preserve log ON) shows it in the row's **Payload** panel: labeled values, key:value pairs — the same shape as a database row.

**The dict — Python's type for key:value, read by name instead of position:**
```python
order = {"symbol": "AAPL", "shares": 2}   # braces make a dict, comma-separated pairs
order["symbol"]          # → 'AAPL' — read by NAME (a list reads by position: classes[0])
order["shares"] = 3      # change a value by name
order["price"] = 202.50  # a new name adds a pair
order["ticker"]          # KeyError: 'ticker' — no such name, the dict's 404
```

**JSON** = the same key:value shape, written as text so it can cross the wire between programs. A dict lives inside a running Python program; JSON is what travels: `{"symbol": "NVDA", "price": 184.32}`. Every language reads and writes it — it belongs to none of them.

**GET vs POST — the first word of the request line:**
- `GET` = looking, safe to repeat
- `POST` = sending something in, to change things

What you send rides in different places:
```
GET /search?q=nvidia+stock HTTP/1.1     # a little rides in the address — the query string

POST /buy HTTP/1.1
Host: <the-app-ip>
                                         # the blank line
symbol=NVDA&shares=1                    # the payload rides in the body
```

**The form gives the payload its labels** — `<input name="symbol">` is why the panel, the body, and the code all use the same word:
```html
<form action="/buy" method="POST">
  <input name="symbol">
  <input name="shares">
  <button>Buy</button>
</form>
```

**Refresh after a buy — does it buy again?** Refresh repeats the *last* request. If that's the POST, it buys again (the browser's "Confirm Form Resubmission" warning is exactly this). The fix is **POST-redirect-GET**: answer every POST with "done — go look over there," so the last request becomes a harmless GET.

**Inside the code — a function is a named block, a route matches a verb+path to it:**
```python
@app.route("/buy", methods=["POST"])   # "when a POST arrives at /buy, run buy()"
def buy():
    symbol = request.form["symbol"]    # the payload, read by name — the dict move
    ...                                # talks to the database
    return redirect("/")               # "done — ask over there" — POST-redirect-GET
```

**Flask** is the framework — pre-written plumbing (reads raw HTTP, matches routes, assembles responses) so your own code only has to hold routes and decisions. `gunicorn` holds the port and hands each request to Flask. Django (Python, batteries-included) and Express (JavaScript) do the same job in other stacks.

---

## Lesson 26: Where the Backend Lives — systemd, nginx & HTTPS Renewal
A backend needs a computer with a runner — S3 only hands files over (the bucket test: the same `.py` file is inert text in a browser, but runs with `python3 order.py` on a machine). That's why the frontend borrows the visitor's laptop but the backend gets its own EC2, database beside it.

**Nobody starts the app by hand — `systemd` does.** It's the machine's supervisor: starts services at boot, tracks them, restarts them per their settings.
```bash
sudo systemctl status <the-app-service>   # is it running? since when? what PID?
sudo systemctl enable --now <service>     # start now + on every reboot
sudo kill -9 <pid>                        # kill test — watch systemd bring it back in seconds
```

**The unit file — a service's settings, plain text:**
```
/etc/systemd/system/<the-app-service>.service

[Service]
ExecStart=/usr/bin/gunicorn --bind 127.0.0.1:8000 app:app   # the command, and where it binds
Restart=always                                              # the comeback after a kill
```
`--bind 0.0.0.0:80` = gunicorn faces the world itself (shape 1). `--bind 127.0.0.1:8000` = gunicorn answers only its own machine, with nginx taking the front door (shape 2, most builds already this way).

**localhost / 127.0.0.1** = every computer's name for itself. Postgres and (in shape 2) gunicorn both bind here on purpose — only a program standing on the same machine can reach them.

**nginx in front = a reverse proxy** — faces the internet, handles the certificate, passes each request inward to gunicorn on `127.0.0.1`.
```bash
sudo ss -tlnp
# 0.0.0.0:80      nginx      ← faces the world
# 127.0.0.1:8000  gunicorn   ← the app, inside only
# 127.0.0.1:5432  postgres   ← inside only
```

**HTTPS, for real this time — certbot runs on the server, not your Mac:**
```bash
sudo dnf install certbot python3-certbot-nginx   # Amazon Linux (Ubuntu: apt)
sudo certbot --nginx -d your-domain.com          # proves the name on port 80, writes nginx's config itself
sudo systemctl enable --now certbot-renew.timer  # Amazon Linux (Ubuntu: certbot.timer)
systemctl list-timers                            # confirm the renewal is scheduled
```
Certificate = the server's public key + name, signed by a Certificate Authority (Let's Encrypt) every browser already trusts. The private key (`privkey.pem`) never leaves the server — that's the whole trick. Certs are short-lived (~3 months) on purpose, so the renewal timer replaces the old manual fix-it-by-hand routine.

---

## Lesson 27: Database Internals — Logging, SQL Injection, Migrations & Moving the Database

Five separate topics on the database you already query by hand, then the first half of giving it its own server.

**Logging** — off by default; turn it on to see every query the app sends, then watch it beside a browser click:
```bash
sudo -u postgres psql -c "ALTER SYSTEM SET log_statement = 'all'"
sudo -u postgres psql -c "SELECT pg_reload_conf()"
sudo tail -f /var/log/postgresql/postgresql-*.log
```
Nobody reads logs this way at work — they ship to Datadog, CloudWatch, Grafana, or Dynatrace instead.

**SQL injection** — user input glued straight into a SQL string lets a stray quote turn data into commands:
```sql
-- normal input:  SELECT * FROM companies WHERE symbol = 'AAPL'
-- ' OR '1'='1 :  SELECT * FROM companies WHERE symbol = '' OR '1'='1'
```
The fix is a **parameterized query** — the value rides in separately instead of getting pasted into the sentence:
```python
cur.execute("... WHERE symbol = %s", (user_input,))
```

**Connecting** — the app's connection string packs the same four facts `psql` takes as flags:
```
psql -U app_user -d investapp -h localhost
postgresql://app_user:...@localhost:5432/investapp
```
who · which machine (an RDS **endpoint** replaces `localhost` once it's off this box) · which port · which database. Moving the database changes exactly one of these four.

**Migrations** — a table's shape should come from numbered, ordered `.sql` files (`001_create_companies.sql`, `002_...`), run once each, not hand-edits on the live database. Ask Claude how your own tables got their shape — some builds (ours included) skip the folder and Claude just built the tables directly.

**Money data rules** — a ledger is **append-only** (a mistake gets a new offsetting row; nothing is edited or deleted) and stores no balance — the balance is always a fresh sum:
```sql
SELECT SUM(amount) FROM ledger;
```

**Moving the database to its own server — one tier becomes two.** Steps 1–5 of a 12-step move:
```bash
# 1. back up first, always
sudo -u postgres psql -l
sudo -u postgres pg_dump investapp > investapp.sql

# 5. reach the new server in two hops — laptop -> app server -> db server
scp -i key.pem key.pem ubuntu@<app-public>:~
ssh -i key.pem ubuntu@<app-public>
ssh -i key.pem ubuntu@<db-private-ip>
```
Step 2 makes a new subnet in the same VPC, with auto-assign public IP left **off**. Step 3 gives that subnet its own route table with no `0.0.0.0/0` row to the internet gateway — that one missing row is what "private" means. Step 4 launches the database server into it, firewalled to accept port 5432 and 22 only from the app server's security group (a security group, not an address, as the source).

Hit the wall right after: a private subnet has no way out to install anything (`apt update`/`dnf install` hangs at 0%). Wednesday's fix is a NAT gateway — step 6.

---

## Lesson 28: Finishing the Database Move — NAT Gateway, Cutover & Order
Picking up right where Lesson 27's wall left off. Two separate walls, not one: the route table has no internet row, **and** an internet gateway only carries traffic for a machine with a public address — this server has none on purpose. Adding the row back alone doesn't fix it.

**NAT gateway** — sits in a public subnet, makes outbound calls on the private server's behalf; the server keeps its private address and stays unreachable from outside. ~5¢/hr (~$36/mo) if left running — for class: create it, use it, delete it.
```bash
# one new row in the DATABASE subnet's route table
0.0.0.0/0 → nat-...    # not the internet gateway

sudo apt update    # now succeeds
```

**Install Postgres + open it to the network:**
```bash
sudo -u postgres createuser --pwprompt app_user
sudo -u postgres createdb -O app_user investapp

# postgresql.conf
listen_addresses = '*'
# pg_hba.conf
host  investapp  app_user  0.0.0.0/0  scram-sha-256
sudo systemctl restart postgresql
```
`pg_hba.conf` is read top to bottom — **first match wins**. A rule appended at the end never fires if a shipped `peer`/`ident` line above it matches first — the error reads like a bad password, but the password was never the problem. Move your line above the shipped ones.

**Copy the backup over, restore, verify:**
```bash
# from the app server, over the private network
scp -i key.pem investapp.sql ubuntu@<db-private-ip>:~

# on the db server
psql -U app_user -d investapp -f investapp.sql
GRANT ALL ON ALL TABLES IN SCHEMA public TO app_user;

# row counts must match on both sides
psql -d investapp -c "SELECT count(*) FROM ledger;"
psql -h <db-private-ip> -U app_user -d investapp -c "SELECT count(*) FROM ledger;"
```

**Cutover** — only the address in the connection string changes (same user/password/db name); restart the app, then prove it with a real buy. Leave the old database running until the new one's proven — that's the way back.
```bash
sudo grep -rl DATABASE_URL /etc /opt /srv /home 2>/dev/null
sudo systemctl restart gunicorn
```

**Close the door** — delete the `0.0.0.0/0` route row, delete the NAT gateway, release its Elastic IP, in that order (the address stays greyed out until the gateway finishes deleting). The database never needs the internet again.

**Getting in later** — through the app server as a jump host (bastion):
```bash
ssh -i key.pem -J ubuntu@<app-public> ubuntu@<db-private-ip>
```
`-J` = jump via, both hops in one command, no key left behind on the app server.

**Why the order mattered:** back up first, create the login before the restore needs it, count rows before pointing the app anywhere, keep the old database running until a real buy proves the new one, one change at a time, close the way out last. Every stopping point was safe to pause at — that's how you change something people depend on.

**At a real job:** split further into three tiers (frontend/backend/db, each its own team) or hand it to RDS — same steps, but a button instead of `pg_dump` + `scp` + restore by hand.

---

## Lesson 29: Many Engineers, Same Code — Branches, PRs & Merging
Two people changing the same file at once is new territory — everything so far was solo. A shared push isn't rejected because content clashes; it's rejected because the line of saves (`main`) moved on GitHub while you were working and your copy hasn't seen it (`fetch first`).

**A branch is a second line of saves, with its own name** — not a copy, not a backup, not a separate repo. It starts from the commit you're on; `main` doesn't move while you work. Git's word for the branch you're standing on is `HEAD`.
```bash
git switch -c color-fix     # create + stand on it (older: git checkout -b)
git branch                  # * marks the one you're on
git switch main              # swap files to main's version
git switch color-fix         # swap back — nothing was ever lost
git log --oneline            # shows (HEAD -> color-fix), (origin/main, main)...
```

**Pushing a branch** — until you push it, it only exists on your machine:
```bash
git push -u origin color-fix   # -u links it, so plain `git push` works after
```

**Pull request** = "here's my line of saves, please add it to main." Nothing merges until someone presses Merge. Git itself has no concept of a PR — that's GitHub (GitLab calls it a merge request). A diff is the same +/- list as `git diff`, drawn as a web page. GitHub won't let you approve your own PR.

**Merging** joins two lines into one; the source branch isn't harmed, it just stops being ahead:
```bash
git merge <branch>         # terminal equivalent of the Merge button
git branch -d color-fix    # safe after merge — the saves live in main now
```

**Conflicts** — Git decides on its own when two edits touch different lines; it stops and asks only when the *same* line changed on both sides. Not an error, just Git refusing to guess:
```bash
git switch main && git pull
git switch add-button
git merge main
# CONFLICT (content): Merge conflict in index.html
```
Git writes three markers into the file: `<<<<<<< HEAD`, `=======`, `>>>>>>> main`. Delete all three once you've chosen what stays — committing with `=======` still in the file is the classic mistake. Claude is fine at resolving these; hand it the conflicted file and say what to keep, then read the result yourself.

**Keep your branch caught up with main** — same four commands as a normal pull, just the other direction (main gives, your branch receives). Do it before you push, not as recovery:
```bash
git switch main && git pull
git switch add-button
git merge main
```

**.gitignore** — one file listing what Git should never save:
```
.env            # your API keys
*.pem           # key files
__pycache__/    # Python leftovers
.DS_Store       # macOS junk
```
It only stops a file from being saved *going forward* — a key already pushed has to be rotated, not just ignored.

**Named for later, not taught yet:** `rebase` (moves your saves onto main's tip instead of joining them — one straight line, no merge commit) and `revert` (undoes an already-merged PR by adding a new PR, not erasing history). `git fetch` is the download-only half of `git pull`.

---

## Lesson 30: Infrastructure as Code — Terraform

A click can't do three things: **repeat** it exactly, **review** it before it happens, or **rebuild** it once it's gone. **Infrastructure as code** = write the infrastructure you want into files, keep those files like code, and a program reads them and makes reality match. A script performs steps in order; this describes a destination and works out the steps itself.

**The field, one difference each:** CloudFormation (AWS's own, AWS-only) · Pulumi/CDK (a real language — Python, TypeScript — produces the infra) · Ansible (not IaC at all — **configuration management**, for machines that already exist) · **Terraform** (describes what should exist, against any cloud — what this course teaches). Terraform's license changed in Aug 2023 (now IBM's, not open source); OpenTofu is the community fork. Still free to use for learning and work — you just can't resell a product that is Terraform.

**Two new words that aren't commands:**
- **provider** — a plug-in that speaks to one cloud; Terraform itself knows nothing about AWS until it's handed one.
- **resource** — one thing that should exist (a network, a server, a firewall rule). Written as `resource "type" "name"` — the **type** is fixed by the provider, the **name** is yours alone and must be unique per type (copy-paste-forget-to-rename is the classic "Duplicate resource" error).

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "scratch" {
  cidr_block = "10.99.0.0/16"
}
```

**The four commands:**
```bash
terraform init      # download the providers this folder needs — nothing created, nothing costs money
terraform plan       # ask AWS what exists, compare to the file, print what it WOULD do — changes nothing
terraform apply       # do what the plan said — shows the plan again, asks once, then changes your account
terraform destroy     # delete everything this folder made, and nothing else — asks once
```

**Reading a plan — the last line first:**
```
Plan: 1 to add, 0 to change, 0 to destroy.
```
Symbols: `+` create · `-` destroy · `~` change in place · `-/+` destroy then recreate (read left to right — that's the order) · `+/-` create replacement first, then destroy old · `<=` read without touching · no symbol = not changing (most lines of a long plan). Stop and look if the destroy count isn't what you expected.

**Install (macOS):**
```bash
brew tap hashicorp/tap && brew install hashicorp/tap/terraform
terraform version                    # confirms it's installed
aws sts get-caller-identity          # Terraform borrows the same aws credentials you already set up
```

---

## Lesson 31: Terraform — The Real Network, State & for_each
Building the real VPC network resource by resource, then the two things every real Terraform setup depends on: state and saying things once.

**Seven resources, one network:** `aws_vpc`, `aws_subnet` ×2, `aws_internet_gateway`, `aws_route_table`, `aws_route_table_association` ×2. `10.0.0.0/16` for the network, `10.0.1.0/24` and `10.0.2.0/24` for the subnets — both public here, so `public_a`/`public_b`, never `private`. AWS creates a **main route table** with every VPC on its own; Terraform didn't make it, so it never shows in a plan and can't be deleted — seeing it in the console isn't a sign anything's wrong.

```hcl
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"   # anywhere outside this network — not a narrow range
    gateway_id = aws_internet_gateway.gw.id
  }
}
```

Build one resource at a time: say it in a sentence, write it, `plan`, `apply`. Nothing in the file states an order — the subnet block *mentions* `aws_vpc.main.id`, so Terraform's **dependency graph** works the order out itself (and reads it backwards to delete safely).

**Change vs. outage — one symbol decides which:** `~` changes something in place (e.g. a tag); `-/+` destroys and rebuilds (e.g. a subnet's CIDR) — safe here only because the subnets are empty. In the console the same edit just happens; Terraform is the one that tells you first.

**Drift** = reality has moved away from what your file says, usually a console edit. Plain `terraform plan` finds it unasked ("Objects have changed outside of Terraform") and offers to put it back — nothing changes until someone runs `apply`.

```bash
terraform apply -auto-approve   # skips the plan and the yes/no prompt — for pipelines, not yet
```

**State — `terraform.tfstate` is Terraform's memory file:** for each resource it stores the name from your file beside the real AWS id. Move the file aside and `plan` wants to build everything again (`7 to add`) even though AWS is untouched; put it back and it remembers. Delete it for real and your infrastructure is still there, running and billing — Terraform has just forgotten it, so the next `apply` builds a second copy beside the first. State also stores every value AWS returns, including ones you wouldn't want stored — a database password lands in it in plain text, no extra step required.

```bash
# .gitignore
.terraform/
*.tfstate
*.tfstate.*
*.tfvars
# NOT .terraform.lock.hcl — commit that one, it pins your provider version
```

**Remote state** keeps that memory in shared storage (S3, Azure storage, or Terraform Cloud) instead of one laptop, so it survives and more than one machine can use it:

```hcl
terraform {
  backend "s3" {
    bucket = "your-unique-bucket-name"   # this block is read before anything else — no variables allowed
    key    = "unit1/terraform.tfstate"
    region = "us-east-1"
  }
}
```
```bash
terraform init                # first time: asks to copy existing state to the new backend
terraform init -reconfigure   # every later change to this block
```
The bucket has to exist first — Terraform won't make it. `backend.tf` itself is committed to git; it holds the address of the memory, not the memory.

**State locking** stops two people applying at once and silently clobbering each other's record. Off by default — add `use_lockfile = true` to turn it on, and nothing warns you it's missing.

**Variables and outputs — say a value once:**
```hcl
variable "region" {
  type    = string
  default = "us-east-1"
}

availability_zone = "${var.region}a"   # ${ } required inside quotes, or AWS gets literal "var.region"

output "subnet_a_id" {
  value = aws_subnet.a.id
}
```
A variable is a value going in; an output is a value Terraform prints back out (`terraform output`).

**`for_each` — write the description once, not once per resource:**
```hcl
variable "subnets" {
  type = map(string)
  default = {
    "us-east-1a" = "10.0.1.0/24"
    "us-east-1b" = "10.0.2.0/24"
  }
}

resource "aws_subnet" "main" {
  for_each          = var.subnets
  vpc_id            = aws_vpc.main.id
  availability_zone = each.key
  cidr_block        = each.value
}
```
Not a loop — no order, both made at once. Converting existing resources to `for_each` destroys and rebuilds them (the names changed), and breaks anything that referenced the old names — `Reference to undeclared resource`, then `Missing resource instance key`. Fix by moving references the same way:
```hcl
resource "aws_route_table_association" "main" {
  for_each       = aws_subnet.main
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}
```

---

## Lesson 32: Terraform — Describing a Server
Nobody configures a real environment by hand — people slip, it can't be reproduced, and real companies run thousands of machines at once. Describing one server means deciding five things: which OS, how big, where in the network, who may reach it, what it may do in AWS (the fifth is next session).

**Decision 1 — the OS, via a data source instead of a pasted id.** An id is never worth writing down: it differs per region and Amazon replaces it whenever a newer image ships. A `data` block *reads* a fact from AWS; it creates nothing.
```hcl
data "aws_ami" "linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}
# read it as: data.aws_ami.linux.id
```
A wrong filter doesn't guess — `Your query returned no results` means the filter is wrong, not that the image is missing.

**Decisions 2–3 — size and placement, both already familiar:**
- **instance type** (`t3.micro`) — family (`t3`) + size (`micro`): family is what it's built for, size is how much of it. Bills by the hour from the moment it exists, whatever size.
- **subnet** — which part of the network already built in Terraform it lands in.

**Decision 4 — who may reach it, via a security group.** A machine created by code gets no outbound access unless you write it — unlike one clicked into existence. Without an egress rule the machine starts, lets you in, and installs nothing.
```hcl
resource "aws_security_group" "app" { vpc_id = aws_vpc.main.id }

resource "aws_vpc_security_group_ingress_rule" "ssh" {
  security_group_id = aws_security_group.app.id
  from_port = 22 , to_port = 22 , ip_protocol = "tcp"
  cidr_ipv4 = "0.0.0.0/0"
}

resource "aws_vpc_security_group_egress_rule" "out" {
  security_group_id = aws_security_group.app.id
  ip_protocol = "-1" , cidr_ipv4 = "0.0.0.0/0"
}
```
One rule per port, each naming its group. Use `vpc_security_group_ids` in your own VPC — the other argument, `security_groups`, is for the default VPC only, and using it here makes Terraform destroy and rebuild the machine every time the group changes.

**The machine, one block, four decisions in it:**
```hcl
resource "aws_instance" "app" {
  ami                    = data.aws_ami.linux.id       # 1 which OS
  instance_type          = "t3.micro"                  # 2 how big
  subnet_id              = aws_subnet.public.id        # 3 where in the network
  vpc_security_group_ids = [aws_security_group.app.id] # 4 who may reach it
  # iam_instance_profile = ...                          # 5 what it may do — next session

  key_name                    = "my-key"
  associate_public_ip_address = true   # or there's no address to SSH to
}
```
Read the plan before saying yes — changing `associate_public_ip_address` or the security-group argument on a machine that already exists makes Terraform destroy it and build another.

**Two arguments any block can be told:**
- `depends_on = [aws_subnet.public]` — spells out ordering by hand for the rare case Terraform can't work it out from one block naming another.
- `lifecycle { ignore_changes = [tags] }` — tells Terraform to leave one value alone (set outside the file) while still managing the rest.

**Outputs, revisited** — a variable is a value going in, an output is one Terraform prints back out, usually a real AWS id only it can tell you:
```hcl
output "subnet_a_id" {
  value     = aws_subnet.a.id
  sensitive = false   # true for a password: prints (sensitive value)
}
```
```bash
terraform output   # prints the real ids, ready to paste
```

**SSH onto it — and there's nothing there:**
```bash
ssh ec2-user@<the new machine>
```
No app, no packages, no database — a machine described in five lines, created by `apply`, and empty. Next: what puts the app on it.

---

## Lesson 33: One Server, Built From Code — Identity, Installing & Disposability
Decision five, then how the app actually lands on the empty machine, then what it means that the machine can now be thrown away.

**Decision 5 — what it may do in AWS.** The app has to read a secret out of Secrets Manager, so the machine needs an identity of its own. Your own access keys never go onto it — they're one person's, have to be copied on by hand, and expire. A **role** is an identity with permissions attached; an **instance profile** is the object AWS actually attaches to a machine — a machine can't hold a role directly.
```hcl
resource "aws_iam_role" "ec2_role" {                # 1 the identity
  assume_role_policy = jsonencode({ ... })           # who may assume this role — the EC2 service
}
resource "aws_iam_role_policy" "ec2_policy" {        # 2 what it may do
  role   = aws_iam_role.ec2_role.id
  policy = jsonencode({ ... })                       # e.g. secretsmanager:GetSecretValue only
}
resource "aws_iam_instance_profile" "ec2_profile" {  # 3 the object AWS attaches
  role = aws_iam_role.ec2_role.name
}
```
```hcl
# on the instance itself
iam_instance_profile = aws_iam_instance_profile.ec2_profile.name
```
Proof it worked: `aws sts get-caller-identity` on the machine answers `assumed-role/ec2_role/i-0a1b2c3d` — the machine, not you. No keys anywhere on disk, nothing to rotate.

**Two ways to get the app onto a fresh machine:**
```hcl
# 1. Amazon's image + a script that installs at boot
resource "aws_instance" "app" {
  ami                          = data.aws_ami.linux.id
  user_data                    = file("install.sh")   # runs once, on first boot, as root
  user_data_replace_on_change  = true                 # edit the script → build a new machine
}
```
```bash
aws ec2 create-image --instance-id <the machine you built> --name "app-with-everything-on-it"
# 2. your own image — a machine launched from it installs nothing
```
The script installs packages, installs and starts the database, gets the code, writes the service file, starts the web server — every step you've already done by hand; the change is who types them. Pick by how often the company ships: frequent deploys favor install-at-boot (always current, slower to launch); rare/regulated deploys favor a pre-built image (fast to launch, only as current as the last rebuild).

**The script can't hold the secret** — it's a file in the repo. Instead the machine fetches it at boot, using the identity from decision 5:
```bash
DB_PASSWORD=$(aws secretsmanager get-secret-value \
  --secret-id app/db --query SecretString --output text)
```
The script's only job is to write that value where the app already looks — an environment variable, the same way it always read its config.

**Disposable, proven:**
```bash
terraform destroy    # the machine is gone
terraform apply      # a new one, and the app answers on it
```
The second machine isn't a copy of the first — both were built from the same file. That's what lets a machine be replaced instead of repaired, which means the app itself owes five things: start on boot, listen on a known port, take config from the environment (three already true), answer "are you working?", and ship its logs somewhere that outlives the machine (the two still open).

**Health endpoint** (usually `/health`): answers only when the app can actually do its job — the only way to tell "running" from "working" from outside. It must not check the database — one database wobble would report every machine dead over a problem none of them had; check only what this machine is responsible for.

---

## Lesson 34: The Data Tier — Moving to Amazon RDS
Your database moves off the app server to Amazon RDS, by hand, once. The point stays the same as Lesson 27/28's move: a server built from code can be destroyed and rebuilt — nothing rebuilds the data that was on it.

**Five jobs any database needs done, wherever it lives:** install and patch the engine · back up and prove the restore · keep serving when the machine dies · hold the password out of the code · report whether it's healthy. You already did four of these by hand — the third (surviving the machine dying) had no answer, because the database and the app server were the same machine.

**"Managed" means AWS does jobs off that list, and you cannot log in to the machine.** What it costs: no superuser, no OS access (no SSH, no shell), no `postgresql.conf` (settings go through a parameter group instead), and the same size machine costs more per hour.

**An RDS instance is not an EC2 instance** — no SSH, no shell, just a hostname (the **endpoint**) plus port/user/password, the same things `psql` always wanted.

**Networking:** hand RDS a **DB subnet group** spanning two availability zones (AWS requires two); the database itself still runs in one. No route to the internet, no NAT gateway, no public address — a database needs nothing from the internet. Only the app servers' security group may reach port 5432 (name the group, not an address range — servers get replaced, the group doesn't).

**The master password lands in the Terraform state file as plain text**, however you produced it. Either protect the state file (encrypt the bucket, restrict who can read it) or skip storing it entirely with `manage_master_user_password`, which hands the password to Secrets Manager instead.

**Prove you can reach it before moving any data, from the app server, in this order:**
```bash
nc -vz <the endpoint> 5432

psql 'host=<the endpoint> port=5432 dbname=investment_app user=investment_app sslmode=require' \
  -c "SELECT version();"
```
`nc` fails → nothing's listening (security group or network). `nc` works, `psql` fails → it's the user, password, or database name.

**The connection** — host, port, user, password, database name — lives entirely in the app's secret; Terraform writes the host in because it created the database and knows the address. A hostname isn't secret; it's there because that's where the rest of the connection already is.

**Move the data once, by hand:**
```bash
pg_dump -h 127.0.0.1 -U investment_app -d investment_app -f app.sql

psql 'host=<the endpoint> port=5432 dbname=investment_app user=investment_app sslmode=require' \
  -f app.sql
```
`-h 127.0.0.1` matters — without it `pg_dump` uses the local socket, which requires your Linux username to match the database username.

**Then remove Postgres from the app server for good** (keep just the client) and rebuild:
```bash
# boot script: drop postgresql16-server / initdb / enable --now postgresql
# keep:        dnf install -y postgresql16   (the psql client only)

terraform destroy   # then   terraform apply
```

**Health checks must not query the database** — if they do, one slow database makes every app server report itself dead at the same moment.

**Two questions decide the rest of the session:** how much data can you afford to lose (**RPO**, recovery point objective), and how long can you afford to be down (**RTO**, recovery time objective). The numbers come from the business; the engineering follows them.

**Backups, snapshots, and point-in-time recovery are three different things:** automated backups run on a schedule you set and expire after N days; a snapshot is one copy you take that stays until you delete it; point-in-time recovery goes back to a moment inside the retention window. Restoring any of them gives you a **new database with a new hostname**, never the old one back in place — which is why the hostname lives in the secret, not in a file that rebuilds the server.

**A standby** (job 3, the one with no answer on your own server) is a synchronous second copy in the other zone; if the machine dies, the standby takes over and **the hostname does not change**. Roughly doubles the price — turn it on to prove it, then off. **A read replica** is different: its own hostname, readable, and it lags — a value you just wrote may still show old there.

**Never destroy a production database.** Stop it (up to 7 days, then it restarts itself) or snapshot it and delete it — deleting always asks for a final snapshot first; skip that only on scratch/dev databases.

---

## Lesson 35: The Data Tier — Reading Route Tables & the Cutover
Continuing Lesson 34's move to RDS: how to tell a subnet's network posture from the route table alone, then the actual cutover from the app server's own Postgres to the new database.

**Only the route table tells you whether a subnet is public or private** — not the name (you can call a subnet `public-a` and still give it no way out) and not the address range (every subnet sits inside the VPC's block regardless). Read the `0.0.0.0/0` line: pointing at an internet gateway means public; pointing at a NAT gateway means still private (a server here can reach out, nothing can reach in); no such line at all means private — what the database subnets are. Every route table also carries a `local` line AWS adds and you can't remove — it means "stays inside this VPC," not a route to the internet.

**The connection is five pieces — host, port, user, password, database name** — read from one file the boot script writes and the app reads once, at startup:
```
# /etc/investment-app.env, written by the boot script
DB_HOST=127.0.0.1          # the only line that changes
DB_PORT=5432
DB_NAME=investment_app
DB_USER=investment_app
DB_PASSWORD=...            # fetched from Secrets Manager at boot
```

**The cutover — edit the file, then restart, because the app only reads it once at startup:**
```bash
sudo vi /etc/investment-app.env   # DB_HOST=127.0.0.1  ->  DB_HOST=<the endpoint>
sudo systemctl restart investment-app
```
Prove it by buying one more share: the new database gets the new row, and the database still sitting on the app server is frozen with whatever it had at cutover — it will never change again.

**The host belongs in the same secret as the password** — Terraform put it there because it created the database and knows the address. A hostname isn't secret; it goes there so there's one place to change when the database moves again. The boot script doesn't read it from there yet — today's edit was by hand, and a rebuilt server would go right back to looking for `127.0.0.1` until that gap is closed.

**Removing Postgres from the app server for good:** drop `postgresql16-server`, `initdb`, and `enable --now postgresql` from the boot script; keep just `postgresql16` for the `psql` client. Then `terraform apply` alone — not `destroy` then `apply`. `database.tf` now lives in the same folder with `skip_final_snapshot = true`, so a `destroy` here would delete the database you just migrated data into. `user_data_replace_on_change = true` is what gets you a rebuilt server from `apply` by itself.

---

## Lesson 36: The Data Tier, Finished — Health Checks & Running vs. Answering

Closes out the data tier (jobs 2 and 3 — backups and the standby, both recapped) and opens the next arc: a machine can be running and still unable to answer a request, which is what a health check exists to catch.

**Health checks must never query the database** — if they do, one slow database makes every app server report itself dead at the same moment, turning one problem into a total outage. A health check answers exactly one question: is *this* server able to serve, not whether something farther away is fine.

**Two questions decide the rest of the data tier, for your app specifically, not in general:** how much data can you afford to lose (**RPO**, recovery point objective — decides how often backups run) and how long can you afford to be down (**RTO**, recovery time objective — decides what you build). The numbers come from the business; the engineering follows them.

**Restoring a backup, snapshot, or point-in-time recovery always gives you a new database with a new hostname** — never the old one back in place. Recovery is three steps: restore it, check it's right, then point the app at the new hostname — why the hostname lives in the secret.

**Running and able to answer are two different facts about one machine.** EC2 answers the first; only the application can answer the second:
```bash
# is the service running? — EC2's view of the machine
sudo systemctl is-active investment-app

# can it answer a request? — the application's own view
curl -i localhost:PORT/HEALTH_PATH
```
An application can die (`sudo systemctl stop investment-app`) while its instance state stays `running` — the console never notices.

**Health endpoint vs. health check:** the endpoint is a small path the application serves for one purpose, to say it's working; the check is something outside the machine asking for that path on a timer and keeping score.

**Five settings, and nothing else decides whether a machine is on the list or off it:** path (default `/`), interval (30s), timeout (5s), unhealthy threshold — consecutive failures before removal (2), healthy threshold — consecutive successes before it's added back (5). A check that **times out counts as a failure**, same as a bad status code. Only `200` passes by default — a redirect fails the check (`Target.ResponseCodeMismatch`) exactly like silence does (`Target.Timeout`).

**An application has to listen on every address the machine has, not just its own:**
```bash
ss -tulnp
# 0.0.0.0:80     -> every address this machine has; a check from outside reaches it
# 127.0.0.1:5432 -> this machine only; nothing outside can reach it
```
A check always comes from outside the machine, so an app bound only to `127.0.0.1` fails every check while looking perfectly healthy from a shell on the box.

**Homework:** turn on automated backups with a retention period and a maintenance window in your app's quiet hours; add `multi_az = true` once to see the standby, then turn it back off (it roughly doubles the price); and on your own server, run `systemctl is-active` then `curl -i localhost:80`, break the app on purpose, watch the two answers disagree, then fix it.

---

## Lesson 37: More Than One App Server — the Load Balancer & Target Group

Two machines have two addresses; a customer types one name. `for_each` turns a single resource block into one repeated per named entry — add a line, get a machine; delete a line, Terraform destroys only that one. Ours has two entries, one per public subnet, so the two app servers land in two availability zones. Terraform identifies a resource by its name, so changing one machine into a set makes it propose destroying the old one and building new — fine here only because the database already moved off the app servers.

```hcl
for_each = {
  frontend = "red"
  backend  = "green"
  worker   = "blue"
}

name = each.key                 # frontend, backend, worker
tags = { color = each.value }   # red, green, blue
```

**An Application Load Balancer (ALB) is one address that hands each request to a machine that can answer.** Not a machine — nothing to SSH into, no address you keep, only a DNS name AWS owns. It bills by the hour plus LCUs (Load Balancer Capacity Units), not per request. Elastic Load Balancing has four kinds; you'll meet two of them:

| Kind | Works on | Used for |
|---|---|---|
| Application | HTTP/HTTPS | Reads the request, routes on host or path. **Ours.** |
| Network | TCP | Faster, doesn't read the request. |
| Gateway | passthrough | Sends to inspection appliances. Rare. |
| Classic | — | Old kind, inherited accounts only. |

**A balancer has three parts:** a **listener** (the port/protocol it accepts on), a **rule** (what the listener consults to pick a target group — routes on host name or path, or answers itself with a fixed response or redirect), and a **target group** (the list of machines plus the health check that decides who's on the list). None of the three is a machine the request passes through — the listener and rule are inside the balancer; the target group is just a list it reads. A target group can hold instances, plain IP addresses, or a Lambda function.

**Routing algorithm is a target-group setting, not a balancer setting.** Round robin (the default — first request to the first machine, second to the second) is right when machines are interchangeable, which two copies of the same app are. Least outstanding requests sends to whichever machine has fewest requests in flight — worth it only when request times vary a lot. Neither ever picks a machine that's off the list; the health check decides who's on it.

**A load balancer never goes in front of a database.** App servers are interchangeable and keep no state, so spreading requests is safe. A database holds state — put two behind a balancer and one write lands on one of them while the other never hears about it. One primary always takes every write; a standby serves no traffic and a read replica answers reads only.

**Prove round robin directly** by having the health path report which machine answered:

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

Two different names in two calls is round robin, seen directly — and a machine's name disappearing from the responses is the quickest sign it came off the list.

**Five reasons a target goes unhealthy, and the one check that settles each:**

| Cause | The check |
|---|---|
| Health path answers with a redirect | Ask for the path from off the machine, read the status |
| App listens only on `localhost` | Check what address it's actually listening on |
| Security group doesn't let the balancer through | Check the rule balancer → machine, not the reverse |
| Grace period shorter than boot time | Time how long the machine takes to answer after it starts |
| Health check hits one port, app listens on another | Compare all four ports: listener, security group, health check, app |

While learning, keep one port all the way across — 80 on the listener, security group, health check, and app. A port mismatch is the most common of the five and the least interesting to debug.

**Before next class:** pull main and apply the balancer (`alb.tf`) — change the S3 bucket in the backend block and the key name to your own first. Open the balancer's DNS name, not an IP — both targets must read healthy before it answers. Stop hard-coding the database address — take the endpoint from the database resource instead of pasting it in by hand, so a rebuilt database doesn't leave the app pointing at a hostname that's gone.

---

## Lesson 38: The Group That Keeps the Count — Health, Statelessness & Auto Scaling

**A target failing open explains the 502/504 you see when every target is unhealthy.** The balancer only filters to healthy targets when some are still healthy; refusing every request outright is worse than trying one that might still answer, so with none healthy it sends the request anyway — a 502 if the connection is refused, a 504 if it never answers. A real 503 means something different: the target group has no registered targets at all, not unhealthy ones. `initial` (reason code `Elb.InitialHealthChecking`) isn't a failure either — it just means the first check hasn't finished yet, which is why identical machines can briefly show different health.

| Setting | Where it lives | Controls |
|---|---|---|
| `interval` | Target group | Seconds between checks on one machine (5–300) |
| `unhealthy_threshold` | Target group | Failures in a row before removal (2–10) |
| `health_check_grace_period` | Auto Scaling group | Seconds a new machine is left alone before being judged |

An unhealthy target and an error page are two different problems: unhealthy means the machine itself is the problem and the request never reaches the application; healthy-but-erroring means something the machine depends on — usually the database — is the problem.

**Stateless means the machine keeps nothing the next request needs**, so it doesn't matter which one answers. Sticky sessions (one target-group setting) fake statefulness by always sending the same person back to the same machine — but that machine dying now takes their session with it, and load stops being even. The real fix is a shared session store that moves state off both machines into something both can read.

**An Auto Scaling group (ASG) keeps a stated number of machines running**, building each from a launch template. The template is just saved answers to the EC2 launch questions — it costs nothing and isn't running until something builds a machine from it, whether that's a person in the console or the ASG with nobody logged in. It holds an AMI id but isn't built from one. Minimum, desired, and maximum are three separate instructions, not three levels: minimum is a floor the group builds up to, maximum is a ceiling it won't cross, and desired — which must sit between them — is the number you actually change, by hand or by a scaling policy; either way it's the same number.

```hcl
resource "aws_autoscaling_group" "app" {
  target_group_arns = [aws_lb_target_group.app.arn]
}
```

That line is what joins the two halves — without it the group still builds machines, but the balancer never sends them a request. Moving to an ASG means `aws_instance` (with its `for_each`) and the per-machine `aws_lb_target_group_attachment` resources come out of the code entirely; leaving them in means paying for machines the group doesn't manage.

**Before next class:** pull main, then point the backend block in `providers.tf` at your own S3 bucket. Delete your own `aws_instance` block and its `aws_lb_target_group_attachment` resources — the group builds machines now. Terminate one machine and watch the group replace it: the new one reads `initial` first and only takes requests once it passes the health check.
