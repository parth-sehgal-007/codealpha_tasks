# Intentionally VULNERABLE demo app - for the code review only. Never deploy.
import sqlite3, subprocess, hashlib, pickle, os
from flask import Flask, request

app = Flask(__name__)
SECRET_KEY = "admin123"                      # hardcoded secret
db = sqlite3.connect("users.db", check_same_thread=False)

@app.route("/login", methods=["POST"])
def login():
    u, p = request.form["user"], request.form["pass"]
    pw = hashlib.md5(p.encode()).hexdigest()  # weak hash, no salt
    q = f"SELECT * FROM users WHERE name='{u}' AND pw='{pw}'"   # SQL injection
    return "ok" if db.execute(q).fetchone() else "denied"

@app.route("/ping")
def ping():
    host = request.args.get("host")
    return subprocess.check_output("ping -c 1 " + host, shell=True)  # command injection

@app.route("/hello")
def hello():
    return "<h1>Hello " + request.args.get("name", "") + "</h1>"   # reflected XSS

@app.route("/file")
def file():
    return open("uploads/" + request.args.get("f")).read()       # path traversal

@app.route("/load", methods=["POST"])
def load():
    return str(pickle.loads(request.data))                        # insecure deserialization

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")      # debug console exposed to the network
