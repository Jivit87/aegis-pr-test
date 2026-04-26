"""
VULNERABLE: SQL Injection test cases for security swarm testing.
This file is intentionally vulnerable for automated security testing.
"""

import sqlite3
import mysql.connector


# ----------------------------------------------------------------
# VULNERABILITY 1: Raw string formatting in SQL (classic SQLi)
# ----------------------------------------------------------------
def get_user_by_name(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # VULN: attacker can pass: ' OR '1'='1
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()


# ----------------------------------------------------------------
# VULNERABILITY 2: f-string interpolation in SQL
# ----------------------------------------------------------------
def get_order(order_id):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # VULN: attacker can pass: 1; DROP TABLE orders--
    query = f"SELECT * FROM orders WHERE id = {order_id}"
    cursor.execute(query)
    return cursor.fetchone()


# ----------------------------------------------------------------
# VULNERABILITY 3: Dynamic table/column name (no parameterization possible
#                  but still unsanitized)
# ----------------------------------------------------------------
def get_report(table_name, column):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # VULN: table and column names cannot use ? placeholders — must sanitize manually
    query = f"SELECT {column} FROM {table_name}"
    cursor.execute(query)
    return cursor.fetchall()


# ----------------------------------------------------------------
# VULNERABILITY 4: LIKE clause injection
# ----------------------------------------------------------------
def search_products(keyword):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # VULN: attacker can escape the LIKE and inject arbitrary SQL
    query = "SELECT * FROM products WHERE name LIKE '%" + keyword + "%'"
    cursor.execute(query)
    return cursor.fetchall()


# ----------------------------------------------------------------
# VULNERABILITY 5: Second-order injection (stored then executed)
# ----------------------------------------------------------------
def update_email(user_id, new_email):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # VULN: email stored unsanitized, later used in another raw query
    cursor.execute(f"UPDATE users SET email = '{new_email}' WHERE id = {user_id}")
    conn.commit()
