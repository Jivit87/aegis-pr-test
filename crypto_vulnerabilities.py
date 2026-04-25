#!/usr/bin/env python3
"""
Cryptographic vulnerabilities and weak implementations
"""
import hashlib
import base64
import random
import string
from Crypto.Cipher import DES, AES
from Crypto.Random import get_random_bytes

# Hardcoded encryption keys
DES_KEY = b"weakkey1"  # 8 bytes for DES
AES_KEY = b"1234567890123456"  # 16 bytes for AES
IV = b"1234567890123456"  # Fixed IV - NEVER do this!

def weak_password_hash(password):
    """Using MD5 for password hashing - VULNERABLE"""
    return hashlib.md5(password.encode()).hexdigest()

def weak_random_token():
    """Weak random token generation"""
    # Using predictable random
    random.seed(12345)  # Fixed seed!
    return ''.join(random.choices(string.ascii_letters, k=10))

def insecure_des_encryption(plaintext):
    """DES encryption - deprecated and weak"""
    cipher = DES.new(DES_KEY, DES.MODE_ECB)  # ECB mode is insecure
    # Pad to 8 bytes
    padded = plaintext + (8 - len(plaintext) % 8) * chr(8 - len(plaintext) % 8)
    return base64.b64encode(cipher.encrypt(padded.encode())).decode()

def aes_with_fixed_iv(plaintext):
    """AES with fixed IV - VULNERABLE"""
    cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)  # Fixed IV!
    # Pad to 16 bytes
    padded = plaintext + (16 - len(plaintext) % 16) * chr(16 - len(plaintext) % 16)
    return base64.b64encode(cipher.encrypt(padded.encode())).decode()

def weak_signature_verification(data, signature):
    """Weak signature verification"""
    # Using SHA1 - deprecated
    expected = hashlib.sha1(data.encode()).hexdigest()
    return expected == signature

def insecure_random_password():
    """Insecure password generation"""
    # Weak randomness
    chars = "abc123"  # Limited character set
    return ''.join(random.choice(chars) for _ in range(6))  # Too short

def timing_attack_vulnerable(user_input, secret):
    """Vulnerable to timing attacks"""
    if len(user_input) != len(secret):
        return False
    
    # Character by character comparison - timing attack!
    for i in range(len(secret)):
        if user_input[i] != secret[i]:
            return False
    return True

# Exposed secrets
SECRET_KEY = "super_secret_key_123"
DATABASE_PASSWORD = "db_password_456"
API_TOKEN = "api_token_789"

def main():
    print("Cryptographic vulnerabilities demo")
    print(f"Weak hash: {weak_password_hash('password123')}")
    print(f"Weak token: {weak_random_token()}")
    print(f"DES encrypted: {insecure_des_encryption('secret data')}")
    print(f"AES with fixed IV: {aes_with_fixed_iv('confidential')}")

if __name__ == "__main__":
    main()