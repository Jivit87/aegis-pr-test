#!/usr/bin/env python3
import os
import subprocess
import sqlite3
import pickle
import yaml
import xml.etree.ElementTree as ET
from flask import Flask, request, session, redirect, render_template_string

app = Flask(__name__)
app.secret_key = "hardcoded_secret_key_123"

# Hardcoded database credentials
DB_HOST = "prod-db.company.com"
DB_USER = "admin"
DB_PASS = "SuperSecret123!"
API_KEY = "sk-live-1234567890abcdef"
JWT_SECRET = "jwt_secret_key"

@app.route('/rce')
def remote_code_execution():
    """Remote Code Execution via eval()"""
    code = request.args.get('code', '')
    return str(eval(code))

@app.route('/cmd')
def command_injection():
    """Command Injection"""
    cmd = request.args.get('cmd', 'ls')
    result = os.system(f"echo 'Running: {cmd}' && {cmd}")
    return f"Command executed: {cmd}"

@app.route('/shell')
def shell_injection():
    """Shell Injection via subprocess"""
    user_input = request.args.get('input', '')
    subprocess.call(f"echo {user_input} | grep something", shell=True)
    return "Done"

@app.route('/sqli/<table>')
def sql_injection(table):
    """SQL Injection in dynamic table name"""
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM {table} WHERE active = 1"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return {"data": results}

@app.route('/blind_sqli')
def blind_sql_injection():
    """Blind SQL Injection"""
    user_id = request.args.get('id', '1')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT username FROM users WHERE id = {user_id} AND password = 'secret'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        return "User exists"
    return "User not found"

@app.route('/file')
def path_traversal():
    """Path Traversal / Directory Traversal"""
    filename = request.args.get('file', 'default.txt')
    try:
        with open(f"/app/files/{filename}", 'r') as f:
            return f.read()
    except:
        return "File not found"

@app.route('/template')
def ssti():
    """Server-Side Template Injection"""
    name = request.args.get('name', 'World')
    template = f"Hello {name}!"
    return render_template_string(template)

@app.route('/deserialize')
def unsafe_deserialization():
    """Unsafe Deserialization"""
    data = request.args.get('data', '')
    try:
        obj = pickle.loads(data.encode('latin1'))
        return str(obj)
    except:
        return "Deserialization failed"

@app.route('/yaml')
def yaml_load():
    """YAML Deserialization"""
    yaml_data = request.args.get('yaml', 'key: value')
    try:
        result = yaml.load(yaml_data, Loader=yaml.Loader)
        return str(result)
    except:
        return "YAML parsing failed"

@app.route('/xml')
def xxe():
    """XML External Entity (XXE) Injection"""
    xml_data = request.args.get('xml', '<root>test</root>')
    try:
        root = ET.fromstring(xml_data)
        return ET.tostring(root).decode()
    except:
        return "XML parsing failed"

@app.route('/redirect')
def open_redirect():
    """Open Redirect"""
    url = request.args.get('url', '/')
    return redirect(url)

@app.route('/xss')
def reflected_xss():
    """Reflected XSS"""
    user_input = request.args.get('input', '')
    return f"<h1>Hello {user_input}</h1>"

@app.route('/stored_xss', methods=['POST'])
def stored_xss():
    """Stored XSS"""
    comment = request.form.get('comment', '')
    # Simulate storing in database
    with open('comments.txt', 'a') as f:
        f.write(f"{comment}\n")
    return f"Comment saved: {comment}"

@app.route('/csrf')
def csrf():
    """CSRF - No CSRF protection"""
    if request.method == 'POST':
        # Dangerous action without CSRF token
        user_id = request.form.get('user_id')
        new_password = request.form.get('password')
        # Change password without verification
        return f"Password changed for user {user_id}"
    return '<form method="post"><input name="user_id"><input name="password"><button>Change Password</button></form>'

@app.route('/info')
def information_disclosure():
    """Information Disclosure"""
    return {
        "database_url": f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/prod",
        "api_key": API_KEY,
        "jwt_secret": JWT_SECRET,
        "debug_info": {
            "python_version": os.sys.version,
            "environment": dict(os.environ),
            "current_user": os.getlogin(),
            "working_directory": os.getcwd()
        }
    }

@app.route('/weak_crypto')
def weak_cryptography():
    """Weak Cryptography"""
    import hashlib
    password = request.args.get('password', '')
    # Using MD5 for password hashing
    hashed = hashlib.md5(password.encode()).hexdigest()
    return f"MD5 Hash: {hashed}"

@app.route('/race_condition')
def race_condition():
    """Race Condition"""
    global counter
    if 'counter' not in globals():
        counter = 0
    counter += 1
    # Simulate some processing time
    import time
    time.sleep(0.1)
    return f"Counter: {counter}"

@app.route('/memory_leak')
def memory_leak():
    """Memory Leak"""
    global memory_hog
    if 'memory_hog' not in globals():
        memory_hog = []
    # Keep adding data without cleanup
    memory_hog.append('x' * 1000000)  # 1MB per request
    return f"Memory usage increased. Total items: {len(memory_hog)}"

def vulnerable_function(user_data):
    """Function with multiple vulnerabilities"""
    # Buffer overflow simulation
    if len(user_data) > 1000:
        return "Data too long"
    
    # Unsafe eval
    result = eval(f"len('{user_data}')")
    
    # SQL injection
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute(f"SELECT '{user_data}' as data")
    
    return result

if __name__ == '__main__':
    # Running in debug mode with all interfaces exposed
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)