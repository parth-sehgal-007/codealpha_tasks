#!/usr/bin/env python3
"""Tiny static analyzer: flags risky patterns line by line. Usage: python audit.py vulnerable_app.py"""
import re, sys 
RULES = [
 (r"f[\"'].*(SELECT|INSERT|UPDATE|DELETE).*\{|[\"']\s*\+.*(SELECT|WHERE)|(SELECT|WHERE).*[\"']\s*\+", "HIGH", "SQL injection: string-built query"),
 (r"shell\s*=\s*True|os\.system\(", "HIGH", "Command injection risk"),
 (r"pickle\.loads?\(|yaml\.load\(|eval\(|exec\(", "HIGH", "Unsafe deserialization / code execution"),
 (r"hashlib\.(md5|sha1)\(", "MEDIUM", "Weak hash for passwords"),
 (r"(SECRET|PASSWORD|API_KEY|TOKEN)\w*\s*=\s*[\"'][^\"']+[\"']", "HIGH", "Hardcoded secret"),
 (r"debug\s*=\s*True", "MEDIUM", "Debug mode enabled"),
 (r"open\(\s*[\"'][^\"']*[\"']\s*\+", "HIGH", "Possible path traversal"),
 (r"return\s+[\"']<.*[\"']\s*\+", "MEDIUM", "Possible XSS: unescaped HTML concatenation"),
]
def main(path):
    n = 0
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        for rx, sev, msg in RULES:
            if re.search(rx, line, re.I):
                n += 1
                print(f"{path}:{i} [{sev}] {msg}\n    {line.strip()}")
    print(f"\n{n} finding(s)")
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "vulnerable_app.py")
