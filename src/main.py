import os
import sqlite3
import subprocess

# -------------------------------
# Module-level safe directory
# -------------------------------
BASE_DIR = "/safe/data"  # default safe directory

# -------------------------------
# Environment variable check
# -------------------------------
API_KEY = os.environ.get("API_KEY")
if API_KEY is None:
    raise RuntimeError("Missing environment variable: API_KEY")

# -------------------------------
# Functions
# -------------------------------

def get_user_score(db_path, username):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT score FROM users WHERE name=?", (username,))
    result = cur.fetchone()
    conn.close()
    return result

def run_system_command(cmd):
    return subprocess.check_output(cmd, shell=True)

def calculate(expr):
    allowed_chars = "0123456789+-*/(). "
    if any(c not in allowed_chars for c in expr):
        raise ValueError("Unsafe expression")
    return eval(expr)

def read_file(file_path):
    if not file_path.startswith(BASE_DIR):
        raise ValueError("Access denied")
    with open(file_path, "r") as f:
        return f.read()
