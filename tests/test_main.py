import os
import tempfile
import subprocess
import pytest
import sqlite3
from main import get_user_score, run_system_command, calculate, read_file

# -------------------------------
# Fixture: Temporary SQLite DB
# -------------------------------
@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp_db:
        conn = sqlite3.connect(tmp_db.name)
        cur = conn.cursor()
        cur.execute("CREATE TABLE users (name TEXT, score INTEGER);")
        cur.execute("INSERT INTO users VALUES (?, ?)", ("alice", 100))
        conn.commit()
        conn.close()
        yield tmp_db.name

# -------------------------------
# Test get_user_score
# -------------------------------
def test_get_user_score(temp_db):
    score = get_user_score(temp_db, "alice")
    assert score[0] == 100

# -------------------------------
# Test run_system_command
# -------------------------------
def test_run_system_command():
    output = run_system_command("echo hello")
    assert output.decode().strip() == "hello"

# -------------------------------
# Test calculate
# -------------------------------
def test_calculate():
    assert calculate("2 + 3") == 5
    assert calculate("10 - 4") == 6
    assert calculate("2 * 3") == 6
    assert calculate("8 / 4") == 2
    with pytest.raises(ValueError):
        calculate("__import__('os').system('ls')")  # unsafe input

# -------------------------------
# Test read_file
# -------------------------------
def test_read_file(tmp_path, monkeypatch):
    # Create a "safe" directory inside tmp_path
    safe_dir = tmp_path / "safe_data"
    safe_dir.mkdir()
    safe_file = safe_dir / "test.txt"
    safe_file.write_text("Hello World")

    # Monkeypatch the BASE_DIR in main.py
    monkeypatch.setattr("main.BASE_DIR", str(safe_dir))

    # Valid file access
    content = read_file(str(safe_file))
    assert content == "Hello World"

    # Access outside safe directory should raise error
    outside_file = tmp_path / "unsafe.txt"
    outside_file.write_text("This should fail")
    with pytest.raises(ValueError):
        read_file(str(outside_file))
