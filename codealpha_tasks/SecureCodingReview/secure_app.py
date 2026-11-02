# Fixed version of vulnerable_app.py
import os, re, json, sqlite3, subprocess
from flask import Flask, request, abort
from markupsafe import escape
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["APP_SECRET_KEY"]       # from environment
db = sqlite3.connect("users.db", check_same_thread=False)
UPLOADS = os.path.realpath("uploads")
HOST_RE = re.compile(r"^[A-Za-z0-9.-]{1,253}$")

@app.route("/login", methods=["POST"])
def login():
    u, p = request.form["user"], request.form["pass"]
    row = db.execute("SELECT pw_hash FROM users WHERE name=?", (u,)).fetchone()  # parameterised
    return "ok" if row and check_password_hash(row[0], p) else "denied"           # salted hash

@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    if not HOST_RE.fullmatch(host):
        abort(400)
    out = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True, timeout=5)  # no shell
    return out.stdout

@app.route("/hello")
def hello():
    return f"<h1>Hello {escape(request.args.get('name', ''))}</h1>"                # output encoding

@app.route("/file")
def file():
    path = os.path.realpath(os.path.join(UPLOADS, request.args.get("f", "")))
    if not path.startswith(UPLOADS + os.sep):
        abort(403)
    with open(path) as fh:
        return fh.read()

@app.route("/load", methods=["POST"])
def load():
    return str(json.loads(request.data))                                           # data-only format

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1")
