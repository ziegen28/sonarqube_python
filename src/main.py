# -------------------------------------------------------------
# SAFE VERSION — Vulnerabilities Removed
# -------------------------------------------------------------

import sqlite3
import os
import subprocess
import shlex


# -------------------------------------------------------------
# Secure API Key Handling (Fix for S2068)
# -------------------------------------------------------------
# Do NOT hardcode secrets — load from environment instead.
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("Missing environment variable: API_KEY")


# -------------------------------------------------------------
# Safe SQL Query (Fix for S3649)
# -------------------------------------------------------------
def get_user_score(db_path, username):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # ✔ Use parameterized queries
    query = "SELECT score FROM users WHERE name = ?;"
    print("Executing query (safe):", query, username)

    cur.execute(query, (username,))
    result = cur.fetchone()
    conn.close()
    return result


# -------------------------------------------------------------
# Safe Command Execution (Fix for S4721)
# -------------------------------------------------------------
def run_system_command(cmd):
    # ✔ Avoid shell=True + sanitize
    if not isinstance(cmd, list):
        cmd = shlex.split(cmd)

    return subprocess.check_output(cmd)


# -------------------------------------------------------------
# Safe Expression Evaluation (Fix for S2076 / S5334)
# -------------------------------------------------------------
def calculate(expr):
    # ✔ No eval — allow only arithmetic using Python’s AST
    import ast
    import operator

    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
    }

    class SafeEval(ast.NodeVisitor):
        def visit_BinOp(self, node):
            if type(node.op) not in allowed_ops:
                raise ValueError("Operation not allowed")
            left = self.visit(node.left)
            right = self.visit(node.right)
            return allowed_ops[type(node.op)](left, right)

        def visit_Num(self, node):
            return node.n

        def generic_visit(self, node):
            raise ValueError("Invalid expression")

    tree = ast.parse(expr, mode="eval")
    return SafeEval().visit(tree.body)


# -------------------------------------------------------------
# Safe File Reading (Fix for S2083)
# -------------------------------------------------------------
def read_file(path):
    # ✔ Restrict allowed directory
    BASE_DIR = "/safe/data/"

    abs_path = os.path.abspath(path)
    if not abs_path.startswith(os.path.abspath(BASE_DIR)):
        raise ValueError("Access outside allowed directory is forbidden")

    with open(abs_path, "r") as f:
        return f.read()


# -------------------------------------------------------------
# MAIN (demo)
# -------------------------------------------------------------
if __name__ == "__main__":
    print("=== Secure SonarQube Test Script ===")

    print(get_user_score("example.db", "alice"))
    print(run_system_command("echo secure"))
    print(calculate("2 + 3"))
