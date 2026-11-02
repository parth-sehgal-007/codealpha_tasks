# Secure Code Review Report - vulnerable_app.py (Python / Flask)
Method: manual inspection plus `audit.py` (pattern scanner). Recommended extra tools: `bandit -r .` and `semgrep`.

| # | Vulnerability | Location | Severity | Risk | Fix (in secure_app.py) |
|---|---|---|---|---|---|
| 1 | SQL injection (CWE-89) | /login | High | `' OR '1'='1` bypasses login, dumps data | Parameterised query `?` |
| 2 | Command injection (CWE-78) | /ping | Critical | `host=8.8.8.8;cat /etc/passwd` runs commands | Validate input, `subprocess.run([...])` without shell |
| 3 | Insecure deserialization (CWE-502) | /load | Critical | Crafted pickle gives remote code execution | Use JSON |
| 4 | Hardcoded secret (CWE-798) | SECRET_KEY | High | Leaks via source control | Environment variable / secret manager |
| 5 | Weak password hashing (CWE-327) | /login | Medium | MD5 is fast and unsalted, easy to crack | `werkzeug.security` (scrypt/PBKDF2) |
| 6 | Reflected XSS (CWE-79) | /hello | Medium | Script runs in victim's browser | Escape output |
| 7 | Path traversal (CWE-22) | /file | High | `f=../../etc/passwd` reads any file | `realpath` + base-directory check |
| 8 | Debug mode, bind 0.0.0.0 (CWE-489) | main | Medium | Werkzeug console gives remote code execution | `debug=False`, bind 127.0.0.1 behind a proper server |

## General best practices
Validate input on the server, never build queries or commands from strings, least privilege, keep dependencies updated, no secrets in code, log security events, add tests for each fix.
