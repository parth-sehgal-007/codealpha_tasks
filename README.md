# CodeAlpha Cyber Security Internship Projects

Three projects completed for the CodeAlpha Cyber Security Internship: a network packet sniffer, a phishing awareness training module, and a secure code review.

Author: Parth Sehgal

---

## Table of Contents

1. [Repository Structure](#repository-structure)
2. [Tasks Completed](#tasks-completed)
3. [Project 1: Network Sniffer](#project-1-network-sniffer)
4. [Project 2: Phishing Awareness Training](#project-2-phishing-awareness-training)
5. [Project 3: Secure Coding Review](#project-3-secure-coding-review)
6. [Legal and Ethical Use](#legal-and-ethical-use)
7. [What I Learned](#what-i-learned)

---

## Repository Structure

```
CodeAlpha_NetworkSniffer/
|-- sniffer.py            Main packet sniffer
|-- find_iface.py         Finds the network adapter that carries traffic
|-- requirements.txt      Dependency list (scapy)

CodeAlpha_PhishingAwareness/
|-- index.html            Training module and quiz in one file

CodeAlpha_SecureCodingReview/
|-- vulnerable_app.py     App under review (intentionally insecure)
|-- secure_app.py         Fixed version of the app
|-- audit.py              Simple static analyzer
|-- REPORT.md             Audit report
```

---

## Tasks Completed

| Task | Project | Technology | What it shows |
|---|---|---|---|
| Task 1 | Basic Network Sniffer | Python, Scapy | How data travels across a network |
| Task 2 | Phishing Awareness Training | HTML, CSS, JavaScript | How attackers trick people |
| Task 3 | Secure Coding Review | Python, Flask | How insecure code gets exploited and how to fix it |

---

# Project 1: Network Sniffer

A Python program that captures network packets, splits each one into its protocol layers, and prints the source and destination IPs, ports, protocol, TCP flags, DNS queries and a payload preview.

## Background

When you open a website, data is cut into small pieces called packets. Each packet is wrapped in layers like nested envelopes:

```
Ethernet  : which device on the local network
  IP      : source address -> destination address
    TCP/UDP : ports and flags
      Payload : the actual data
```

Key ideas:

- **Ports** identify services: 53 is DNS, 80 is HTTP, 443 is HTTPS.
- **TCP** is reliable and sets up a connection first. **UDP** is faster with no guarantee.
- **TCP handshake:** SYN (flag `S`), then SYN-ACK (`SA`), then ACK (`A`).
- **DNS** converts names like example.com into IP addresses, over UDP port 53.
- **HTTPS** encrypts the payload, so only metadata is visible. HTTP payloads can be readable text.

## Features

- Live packet capture on a chosen interface
- Shows time, protocol, source IP and port, destination IP and port, length and TCP flags
- Extracts domain names from DNS queries
- Readable preview of the first 60 bytes of each payload
- Protocol summary at the end
- Options for interface, packet count, time limit and BPF filter
- Helper script to find the correct network adapter

## Requirements

- Python 3.8 or newer
- Scapy: `pip install scapy`
- Windows: Npcap from https://npcap.com (tick "WinPcap API-compatible mode")
- Linux: libpcap (`sudo apt install libpcap-dev` if missing)
- Administrator rights on Windows, or root rights on Linux and macOS

## Usage

Windows: open the terminal as Administrator. Linux and macOS: put `sudo` in front.

```
python -u sniffer.py -c 20
```

| Option | Meaning | Example |
|---|---|---|
| `-c N` | Stop after N packets | `-c 20` |
| `-t N` | Stop after N seconds | `-t 15` |
| `-i NAME` | Network interface | `-i "Wi-Fi"` |
| `-f FILTER` | BPF filter | `-f "tcp port 80"` |

The `-u` flag makes Python print each line immediately.

If nothing prints, the program may be listening on the wrong adapter. Run `python -u find_iface.py`, which tests each adapter for three seconds, and use the one with the most packets as the `-i` value.

## Example Output

This is an illustration of the format. Your values will differ.

```
[14:32:10] UDP   192.168.1.5:60321 -> 192.168.1.1:53 len=74 flags= DNS query: example.com.
[14:32:10] TCP   192.168.1.5:51234 -> 93.184.216.34:80 len=66 flags=S
[14:32:10] TCP   93.184.216.34:80 -> 192.168.1.5:51234 len=66 flags=SA
[14:32:10] TCP   192.168.1.5:51234 -> 93.184.216.34:80 len=54 flags=A

Summary: {'UDP': 1, 'TCP': 3}
```

Reading it: a DNS lookup, then the three-way handshake (`S`, `SA`, `A`), then data transfer.

## How the Code Works

1. `sniff()` from Scapy captures packets and calls `handle()` on each one.
2. `handle()` ignores non-IP packets, reads the IP layer for addresses and protocol number, then reads TCP or UDP for ports and flags.
3. It checks for a DNS layer and extracts the queried name.
4. `payload_preview()` takes the first 60 bytes of the raw data and shows printable characters, replacing the rest with dots.
5. The main loop calls `sniff()` in one-second slices. This lets Python notice Ctrl+C on Windows and check the packet and time limits.

## Troubleshooting

| Problem | Fix |
|---|---|
| `No libpcap provider available` | Install Npcap with WinPcap compatibility, then restart |
| Permission error | Run as Administrator (Windows) or with `sudo` |
| `No module named scapy` | `pip install scapy` for the same Python you run |
| Runs but prints nothing | Run `find_iface.py` and use `-i` with the right adapter, and browse while capturing |
| Ctrl+C does not stop it | Use `-c` or `-t` to stop automatically |
| Output appears late | Run with `python -u` |
| Capture blocked | Antivirus, VPN or a managed laptop may block it |

## Limitations

- Only sees traffic that reaches the machine it runs on
- HTTPS payloads are encrypted, so only metadata is visible
- IPv6 packets show as protocol "Other"
- Does not save captures to a file or reassemble TCP streams

---

# Project 2: Phishing Awareness Training

An interactive training page that teaches how to recognise phishing, explains social engineering, gives real-world examples, and tests the learner with a quiz that explains each answer. It is a single HTML file with no dependencies.

## How to Run

Open `index.html` in any browser. To get a live link, enable GitHub Pages: repository Settings, then Pages, then deploy from the `main` branch.

## Content Covered

**Red flags in an email**

- Sender mismatch: the display name says a bank but the address is a look-alike domain
- Urgency or fear: "account blocked in 24 hours"
- Suspicious links: `paypa1.com`, or `amazon.com.verify-now.net` where the real domain is `verify-now.net`
- Requests for passwords, PINs or OTPs
- Unexpected attachments such as `invoice.pdf.exe`
- Generic greetings and poor language

**Fake websites**

- Check the full domain, not only the padlock. HTTPS means encrypted, not trustworthy.
- Watch for look-alike spellings and unusual endings
- Type the address yourself or use bookmarks for banking and work logins

**Social engineering tactics**

- Authority, urgency, curiosity and greed, and pretexting (a believable made-up story)
- Variants: smishing (SMS), vishing (calls), spear phishing (targeted) and QR code phishing

**Real-world examples**

- Fake KYC or account-suspension SMS with a link to a counterfeit bank page
- Business email compromise: a spoofed executive or supplier email asking for a payment or a change of bank details
- Credential harvesting through a fake "password expires today" login page

**Best practices**

- Stop and check the sender and the link
- Verify through a second channel, such as the company's official phone number
- Use multi-factor authentication and a password manager
- Keep software updated and report suspicious messages
- If you clicked: change the password, tell IT, and monitor your accounts

## The Quiz

Five sample emails, each answered with Phishing or Legitimate. After each answer the page shows an explanation of the clues, then a final score with a Retry button.

| # | Email | Answer | Clues |
|---|---|---|---|
| 1 | "Netflix" billing from a look-alike domain | Phishing | Wrong domain, urgency, generic greeting |
| 2 | HR holiday calendar from the company domain | Legitimate | Internal sender, no link or request |
| 3 | "IT Helpdesk" password expiry from an external domain | Phishing | Look-alike domain, urgent password link |
| 4 | Amazon shipping update pointing to the app | Legitimate | Matches a real order, no suspicious link |
| 5 | "CEO" asking for gift cards from a free email | Phishing | Authority, secrecy, gift cards, free email address |

Two of the five are legitimate on purpose, so learners practise judgement instead of distrusting all email.

**How it works in code:** the questions live in a JavaScript array `Q`. Each item has `from`, `subj`, `body`, `phish` (true or false) and `why`. A loop builds a card for each question. A button click compares the choice with `phish`, updates the score and shows the explanation. Links inside the sample emails are disabled.

**Adding a question:** add an object to `Q` in `index.html`:

```javascript
{
  from: "Bank Alerts &lt;alerts@bank-secure-update.co&gt;",
  subj: "Your card has been locked",
  body: "Dear customer, <a href='#' onclick='return false'>verify your card now</a>.",
  phish: true,
  why: "Look-alike domain, generic greeting and pressure to click a link."
}
```

## Limitations

- Only five fixed questions, so they can be memorised
- Scores are not saved between sessions
- Text-based examples only, with no screenshots

---

# Project 3: Secure Coding Review

A security review of a small Flask application. It contains a deliberately vulnerable app, a simple static analyzer, an audit report, and a fixed version of the app.

> **Warning:** `vulnerable_app.py` contains intentional flaws. Use it only for learning, only on your own machine, and never deploy it.

## The Core Idea

Almost every flaw here comes from one mistake: the program treats data from a user as if it were instructions.

| Vulnerability | What should be data | What it gets treated as |
|---|---|---|
| SQL injection | A username | Part of a database command |
| Command injection | A host name | Part of an operating system command |
| Cross-site scripting | A visitor's name | Code the browser runs |
| Path traversal | A file name | A way out of the allowed folder |
| Insecure deserialization | Received bytes | Code that runs while loading |

The fix is the same each time: never trust user input, and keep data as data.

## Methodology

1. Select the target: a small Flask app with a login, a ping tool, a greeting page, a file reader and a data loader
2. Run `audit.py` to flag risky patterns
3. Review each route manually: where does input enter, where does it end up, is it checked on the way?
4. Classify each issue by severity and CWE (the standard ID for a weakness type)
5. Fix each issue in `secure_app.py`
6. Document everything in `REPORT.md`

## Summary of Findings

| # | Vulnerability | CWE | Location | Severity |
|---|---|---|---|---|
| 1 | SQL injection | CWE-89 | `/login` | High |
| 2 | Command injection | CWE-78 | `/ping` | Critical |
| 3 | Insecure deserialization | CWE-502 | `/load` | Critical |
| 4 | Hardcoded secret | CWE-798 | `SECRET_KEY` | High |
| 5 | Weak password hashing | CWE-327 | `/login` | Medium |
| 6 | Reflected cross-site scripting | CWE-79 | `/hello` | Medium |
| 7 | Path traversal | CWE-22 | `/file` | High |
| 8 | Debug mode on, open to all interfaces | CWE-489 | `app.run` | Medium |

## Detailed Findings and Fixes

### 1. SQL injection at `/login`

Vulnerable:
```python
q = f"SELECT * FROM users WHERE name='{u}' AND pw='{pw}'"
```
Entering `' OR '1'='1' --` as the username makes the condition always true, so the attacker logs in without a password.

Fix: a parameterised query.
```python
db.execute("SELECT pw_hash FROM users WHERE name=?", (u,))
```
The database receives the command and the data separately, so input cannot change the command.

### 2. Command injection at `/ping`

Vulnerable:
```python
subprocess.check_output("ping -c 1 " + host, shell=True)
```
A request with `host=8.8.8.8; cat /etc/passwd` runs the attacker's second command.

Fix: validate the input and avoid the shell.
```python
HOST_RE = re.compile(r"^[A-Za-z0-9.-]{1,253}$")
if not HOST_RE.fullmatch(host):
    abort(400)
subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True, timeout=5)
```

### 3. Insecure deserialization at `/load`

Vulnerable: `pickle.loads(request.data)`. A crafted pickle can run code while it loads.

Fix: `json.loads(request.data)`. JSON can only carry plain data.

### 4. Hardcoded secret

Vulnerable: `SECRET_KEY = "admin123"`. Anyone who sees the code has the key.

Fix: `os.environ["APP_SECRET_KEY"]`. Generate a strong value with `python -c "import secrets; print(secrets.token_hex(32))"`.

### 5. Weak password hashing

Vulnerable: `hashlib.md5(...)`. MD5 is very fast, so attackers can test billions of guesses per second, and it has no salt.

Fix: `check_password_hash(...)` from Werkzeug, which uses a salted, slow algorithm. Store `generate_password_hash(password)` when creating accounts.

### 6. Reflected cross-site scripting at `/hello`

Vulnerable:
```python
return "<h1>Hello " + request.args.get("name", "") + "</h1>"
```
`name=<script>alert(1)</script>` runs a script in the victim's browser.

Fix: `escape(...)` from `markupsafe`, which turns `<` into harmless text.

### 7. Path traversal at `/file`

Vulnerable: `open("uploads/" + f)`. With `f=../../etc/passwd` the attacker reads any file.

Fix:
```python
path = os.path.realpath(os.path.join(UPLOADS, f))
if not path.startswith(UPLOADS + os.sep):
    abort(403)
```
`realpath` resolves every `../`, and the check confirms the result is still inside the allowed folder.

### 8. Debug mode exposed

Vulnerable: `app.run(debug=True, host="0.0.0.0")`. The interactive debugger can run code, and the app is reachable from the whole network.

Fix: `app.run(debug=False, host="127.0.0.1")`, and use a proper WSGI server in production.

## The Static Analyzer

`audit.py` reads a file line by line and tests each line against regular expressions that describe risky patterns. When a line matches, it prints the line number, severity and description.

```python
RULES = [
 (r"shell\s*=\s*True|os\.system\(", "HIGH", "Command injection risk"),
 (r"hashlib\.(md5|sha1)\(",         "MEDIUM", "Weak hash for passwords"),
 ...
]
```

| Pattern | Severity | Finding |
|---|---|---|
| String-built SQL queries | High | SQL injection |
| `shell=True`, `os.system(` | High | Command injection |
| `pickle.load(s)`, `yaml.load(`, `eval(`, `exec(` | High | Unsafe deserialization or code execution |
| `hashlib.md5(`, `hashlib.sha1(` | Medium | Weak hashing |
| SECRET, PASSWORD, API_KEY or TOKEN set to a string literal | High | Hardcoded secret |
| `debug=True` | Medium | Debug mode |
| `open("..." +` | High | Possible path traversal |
| HTML returned with a concatenated variable | Medium | Possible XSS |

## Running the Review

```
python audit.py vulnerable_app.py
python audit.py secure_app.py
```

On the vulnerable app it reports 8 findings, one for each issue above. On the fixed version it reports 0 findings. A clean scan only means none of the simple patterns matched. It does not prove the code is secure, which is why manual review is still needed.

To run the fixed app locally:

```
pip install flask
```

Windows PowerShell:
```
$env:APP_SECRET_KEY = "replace-with-a-long-random-value"
python secure_app.py
```

Linux and macOS:
```
export APP_SECRET_KEY="replace-with-a-long-random-value"
python3 secure_app.py
```

The apps expect a SQLite `users.db` and an `uploads` folder. Run the vulnerable app only on your own machine, and only while testing.

## Professional Tools

| Tool | Purpose | Example |
|---|---|---|
| Bandit | Security linter for Python | `bandit -r .` |
| Semgrep | Rule-based static analysis | `semgrep --config auto .` |
| pip-audit | Finds vulnerable dependencies | `pip-audit` |
| OWASP ZAP | Tests a running web app | Run against a local test instance |

## Secure Coding Best Practices

1. Validate all input on the server, and prefer allow-lists
2. Separate data from commands: parameterised queries, argument lists, no shell
3. Encode output for its context
4. Never hardcode secrets
5. Hash passwords with scrypt, bcrypt or Argon2
6. Avoid `eval`, `exec`, `pickle` and `shell=True` with untrusted input
7. Apply least privilege
8. Show users generic errors, log details privately, and never run debug mode in production
9. Keep dependencies updated
10. Log and monitor security events
11. Test the fixes with the malicious inputs shown above
12. Combine automated tools with human review

## Limitations

- The target app was written for this review, and a real application is far larger
- The analyzer matches text patterns, so it can give false positives and false negatives
- Authorisation logic, session handling, CSRF, rate limiting and dependencies are not covered
- The fixed app has not been through penetration testing

---

## Legal and Ethical Use

Capture network traffic only on networks you own or have permission to monitor. Run the vulnerable app only on your own machine. These projects are for learning and for the CodeAlpha internship submission.

---

## What I Learned

- How packets are layered, how TCP handshakes and DNS lookups look on the wire, and why HTTPS matters
- That phishing works by exploiting urgency, fear and trust, and that specific checkable clues teach better than general warnings
- That most vulnerabilities come from trusting user input, and the fixes are small and standard
- How to classify findings by severity and CWE, and write a remediation report
- How to debug practical problems such as drivers, privileges and adapter selection

---

Author: Parth Sehgal
CodeAlpha Cyber Security Internship
