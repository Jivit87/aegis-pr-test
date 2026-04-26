"""
VULNERABLE: Hardcoded secrets and env misuse test cases for security swarm testing.
This file is intentionally vulnerable for automated security testing.
"""

import os
import requests
import boto3
import jwt


# ----------------------------------------------------------------
# VULNERABILITY 1: Hardcoded AWS credentials
# ----------------------------------------------------------------
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "us-east-1"

def upload_to_s3(file_path, bucket):
    # VULN: credentials hardcoded above instead of using IAM roles / env vars
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    s3.upload_file(file_path, bucket, file_path)


# ----------------------------------------------------------------
# VULNERABILITY 2: Hardcoded database password
# ----------------------------------------------------------------
DB_HOST = "prod-db.internal"
DB_USER = "root"
DB_PASS = "SuperSecret123!"   # VULN: plaintext password in source

def get_db_connection():
    import mysql.connector
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database="production",
    )


# ----------------------------------------------------------------
# VULNERABILITY 3: Hardcoded JWT secret
# ----------------------------------------------------------------
JWT_SECRET = "my_super_secret_key_do_not_share"  # VULN: weak, hardcoded

def create_token(user_id):
    return jwt.encode({"user_id": user_id}, JWT_SECRET, algorithm="HS256")

def verify_token(token):
    # VULN: no expiry check, no audience/issuer validation
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])


# ----------------------------------------------------------------
# VULNERABILITY 4: API key in code
# ----------------------------------------------------------------
STRIPE_SECRET_KEY = "sk_live_FAKE_KEY_FOR_TESTING_ONLY_NOT_REAL"   # VULN: hardcoded key (dummy value)
SENDGRID_API_KEY  = "SG.FAKE_SENDGRID_KEY_FOR_TESTING_ONLY_NOT_REAL"

def charge_customer(amount, token):
    # VULN: live Stripe key hardcoded
    import stripe
    stripe.api_key = STRIPE_SECRET_KEY
    return stripe.Charge.create(amount=amount, currency="usd", source=token)


# ----------------------------------------------------------------
# VULNERABILITY 5: Env var with insecure fallback default
# ----------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-hardcoded-secret")  # VULN: insecure default

def get_admin_token():
    # VULN: if SECRET_KEY env var is not set, falls back to known string
    return jwt.encode({"role": "admin"}, SECRET_KEY, algorithm="HS256")


# ----------------------------------------------------------------
# VULNERABILITY 6: Credentials logged to stdout
# ----------------------------------------------------------------
def authenticate(username, password):
    print(f"[DEBUG] Authenticating user={username} password={password}")  # VULN: password in logs
    return username == "admin" and password == "admin123"
