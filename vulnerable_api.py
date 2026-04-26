"""
VULNERABLE: Mixed API vulnerabilities (SQLi + secrets + misc) for security swarm testing.
This file is intentionally vulnerable for automated security testing.
"""

import os
import sqlite3
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# VULN: hardcoded secret used to sign sessions
app.secret_key = "hardcoded-flask-secret-1234"

# VULN: hardcoded internal service token
INTERNAL_API_TOKEN = "tok_internal_abc123xyz"


# ----------------------------------------------------------------
# VULNERABILITY 1: SQLi + hardcoded DB path exposed via API
# ----------------------------------------------------------------
@app.route("/api/users")
def api_get_user():
    uid = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    # VULN: unsanitized uid injected directly
    cur.execute(f"SELECT id, username, email FROM users WHERE id = {uid}")
    row = cur.fetchone()
    conn.close()
    return jsonify(row)


# ----------------------------------------------------------------
# VULNERABILITY 2: Auth bypass via SQL injection in login
# ----------------------------------------------------------------
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    # VULN: classic auth bypass — username: admin'--
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cur.execute(query)
    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "ok", "token": INTERNAL_API_TOKEN})
    return jsonify({"status": "fail"}), 401


# ----------------------------------------------------------------
# VULNERABILITY 3: Command injection via unsanitized input
# ----------------------------------------------------------------
@app.route("/api/ping")
def api_ping():
    host = request.args.get("host", "localhost")
    # VULN: attacker can pass: localhost; cat /etc/passwd
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return result.decode()


# ----------------------------------------------------------------
# VULNERABILITY 4: Sensitive env vars returned in response
# ----------------------------------------------------------------
@app.route("/api/debug")
def api_debug():
    # VULN: dumps all environment variables including secrets
    return jsonify(dict(os.environ))


if __name__ == "__main__":
    # VULN: debug=True in production exposes interactive debugger
    app.run(debug=True, host="0.0.0.0", port=5000)
