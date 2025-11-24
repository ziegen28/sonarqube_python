# -------------------------------------------------------------
# WARNING: This file is intentionally vulnerable.
# It exists ONLY for testing SonarQube / SAST tools.
# DO NOT use in any real application.
# -------------------------------------------------------------

import sqlite3
import os
import subprocess


# -------------------------------------------------------------
# Hardcoded secret  (S2068)
# -------------------------------------------------------------
API_KEY = "12345-very-insecure-api-key"   # SonarQube should flag this


# -------------------------------------------------------------
# SQL Injection Example (S3649)
# -------------------------------------------------------------
def get_user_score(db_path, username):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # ❌ Vulnerable query: direct string concatenation
    query = "SELECT score FROM users WHERE name = '" + username + "';"
    print("Executing query:", query)

    cur.execute(query)  # SonarQube will flag this
    result = cur.fetchone()
    conn.close()
    return result


# -------------------------------------------------------------
# Command Injection Example  (S4721)
# -------------------------------------------------------------
def run_system_command(cmd):
    # ❌ Vulnerable: user-controlled command execution
    return subprocess.check_output(cmd, shell=True)


# -------------------------------------------------------------
# Insecure Eval Example (S2076 / S5334)
# -------------------------------------------------------------
def calculate(expr):
    # ❌ Vulnerable: executing arbitrary input
    return eval(expr)


# -------------------------------------------------------------
# Insecure file operations (S2083)
# -------------------------------------------------------------
def read_file(path):
    # ❌ No path validation — SonarQube should flag
    with open(path, "r") as f:
        return f.read()


# -------------------------------------------------------------
# MAIN (for demonstration only)
# -------------------------------------------------------------
if __name__ == "__main__":
    print("=== Vulnerable SonarQube Test Script ===")

    # Trigger SQLi vulnerability
    print(get_user_score("example.db", "alice' OR '1'='1"))

    # Trigger command injection
    print(run_system_command("echo vulnerable"))

    # Trigger eval vulnerability
    print(calculate("2 + 3"))

    # Trigger insecure file read
    print(read_file("/etc/passwd"))
