#!/usr/bin/env python3
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.db import connect, get_db_path
from app.core.security import hash_password

reset_db = "--reset" in sys.argv
if reset_db:
    sys.argv.remove("--reset")

if len(sys.argv) != 4:
    sys.exit(
        'Usage: python create_doctor.py [--reset] <username> <password> "<full name>"'
    )

username, password, full_name = sys.argv[1:]

if reset_db:
    from app.core.db import init_db
    init_db()

conn = connect()
try:
    conn.execute(
        "INSERT INTO doctors (id, username, password_hash, full_name) VALUES (?,?,?,?)",
        (str(uuid.uuid4()), username, hash_password(password), full_name),
    )
    conn.commit()
    print(f"Created doctor '{username}' in {get_db_path()}")
finally:
    conn.close()