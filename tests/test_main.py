import os
import tempfile
import subprocess
import pytest
from main import get_user_score, run_system_command, calculate, read_file

# -------------------------------
# Test get_user_score
# -------------------------------
def test_get_user_score():
    # Create a temporary SQLite DB
    import sqlite3
    with tempfile.NamedTemporaryFile() as tmp_db:
        conn = sqlite3.connect(tmp_db.name)
        cur = conn.cursor()
        cur.execute("CREATE TABLE users (name TEXT, score INTEGER);")
        cur.execute("INSERT INTO users VALUES (?, ?)", ("alice", 100))
        conn.commit()
        conn.close()

        # Test fetching user score
        score = get_user_score(tmp_db.name, "alice")
        assert score[0] == 100


# -------------------------------
# Test run_system_command
# -------------------------------
def test_run_system_command():
    output = run_system_command("echo hello")
    assert output.strip() == b"hello"


# -------------------------------
# Test calculate
# -------------------------------
def test_calculate():
    assert calculate("2 + 3") == 5
    assert calculate("10 - 4") == 6
    assert calculate("2 * 3") == 6
    assert calculate("8 / 4") == 2
    with pytest.raises(ValueError):
        calculate("__import__('os').system('ls')")  # unsafe


# -------------------------------
# Test read_file
# -------------------------------
def test_read_file():
    # Create a temporary safe directory
    with tempfile.TemporaryDirectory() as tmpdir:
        BASE_DIR = "/safe/data/"
        os.makedirs(BASE_DIR, exist_ok=True)
        safe_file_path = os.path.join(BASE_DIR, "test.txt")
        with open(safe_file_path, "w") as f:
            f.write("Hello World")

        content = read_file(safe_file_path)
        assert content == "Hello World"

        # Access outside safe dir should raise error
        with pytest.raises(ValueError):
            read_file(tmpdir + "/file.txt")
