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
    
    # VULNERABILITY: Direct string concatenation in SQL query
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL Injection here!
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    
    return {"user": result}

@app.route('/search')
def search():
    """VULNERABLE: SQL Injection in LIKE clause"""
    term = request.args.get('q', '')
    
    # VULNERABILITY: Unsanitized input in LIKE clause
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name LIKE '%" + term + "%'"  # SQL Injection!
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    return {"results": results}

if __name__ == '__main__':
    app.run(debug=True)
