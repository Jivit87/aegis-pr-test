#!/usr/bin/env python3
"""
Vulnerable Flask application with SQL injection
"""

import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/user')
def get_user():
    """VULNERABLE: SQL Injection"""
    user_id = request.args.get('id', '')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return {"user": result}

@app.route('/search')
def search():
    """VULNERABLE: SQL Injection in LIKE clause"""
    term = request.args.get('q', '')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (f"%{term}%",))
    results = cursor.fetchall()
    conn.close()
    
    return {"results": results}

if __name__ == '__main__':
    app.run(debug=True)