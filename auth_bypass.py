#!/usr/bin/env python3
"""
Authentication and Authorization bypass vulnerabilities
"""
from flask import Flask, request, session, jsonify
import jwt
import hashlib

app = Flask(__name__)
app.secret_key = "weak_secret"

# Hardcoded admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# Weak JWT secret
JWT_SECRET = "jwt_secret"

# In-memory user store
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
    "guest": {"password": "guest", "role": "guest"}
}

@app.route('/login', methods=['POST'])
def login():
    """Vulnerable login with multiple issues"""
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    
    # SQL injection in authentication
    if username == "admin' OR '1'='1' --":
        session['user'] = 'admin'
        session['role'] = 'admin'
        return {"status": "success", "message": "Admin logged in"}
    
    # Weak password comparison
    if username in users and users[username]['password'] == password:
        session['user'] = username
        session['role'] = users[username]['role']
        return {"status": "success", "message": f"Logged in as {username}"}
    
    return {"status": "error", "message": "Invalid credentials"}

@app.route('/admin')
def admin_panel():
    """Missing authorization check"""
    # No authentication check!
    return {"admin_data": "sensitive admin information"}

@app.route('/user/<user_id>')
def get_user(user_id):
    """Insecure Direct Object Reference (IDOR)"""
    # No authorization check - any user can access any user's data
    return {"user_id": user_id, "sensitive_data": f"Private data for user {user_id}"}

@app.route('/jwt_login', methods=['POST'])
def jwt_login():
    """JWT with weak secret"""
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    
    if username in users and users[username]['password'] == password:
        # Weak JWT secret
        token = jwt.encode({
            'user': username,
            'role': users[username]['role']
        }, JWT_SECRET, algorithm='HS256')
        return {"token": token}
    
    return {"error": "Invalid credentials"}

@app.route('/jwt_admin')
def jwt_admin():
    """JWT verification bypass"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    try:
        # Vulnerable: accepts 'none' algorithm
        payload = jwt.decode(token, options={"verify_signature": False})
        if payload.get('role') == 'admin':
            return {"admin_data": "JWT admin access granted"}
    except:
        pass
    
    return {"error": "Access denied"}

@app.route('/reset_password', methods=['POST'])
def reset_password():
    """Password reset without proper verification"""
    username = request.json.get('username', '')
    new_password = request.json.get('new_password', '')
    
    # No verification of identity!
    if username in users:
        users[username]['password'] = new_password
        return {"message": f"Password reset for {username}"}
    
    return {"error": "User not found"}

@app.route('/privilege_escalation')
def privilege_escalation():
    """Privilege escalation vulnerability"""
    user_role = request.args.get('role', 'guest')
    
    # No validation of role parameter
    session['role'] = user_role
    
    if user_role == 'admin':
        return {"message": "Admin privileges granted!", "secret": "admin_secret_data"}
    
    return {"message": f"Role set to {user_role}"}

@app.route('/session_fixation')
def session_fixation():
    """Session fixation vulnerability"""
    session_id = request.args.get('session_id')
    
    if session_id:
        # Accepting session ID from user input
        session['id'] = session_id
        session['authenticated'] = True
        return {"message": "Session fixed"}
    
    return {"message": "No session ID provided"}

@app.route('/weak_session')
def weak_session():
    """Weak session management"""
    # Predictable session ID
    import time
    session_id = str(int(time.time()))  # Timestamp as session ID
    session['weak_id'] = session_id
    return {"session_id": session_id}

@app.route('/bypass_auth')
def bypass_auth():
    """Authentication bypass via parameter pollution"""
    admin_param = request.args.getlist('admin')  # Can pass multiple values
    
    # Vulnerable logic
    if 'false' in admin_param and 'true' in admin_param:
        # Last value wins - can be bypassed with ?admin=false&admin=true
        is_admin = admin_param[-1] == 'true'
        if is_admin:
            return {"admin_access": True, "secret": "bypassed_secret"}
    
    return {"admin_access": False}

@app.route('/role_confusion')
def role_confusion():
    """Role confusion vulnerability"""
    user_role = session.get('role', 'guest')
    admin_role = request.args.get('admin_role', 'false')
    
    # Confusing role checks
    if user_role == 'admin' or admin_role == 'true':
        return {"admin_data": "Role confusion exploited"}
    
    return {"message": "Access denied"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')