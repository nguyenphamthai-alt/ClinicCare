import os
import sqlite3
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_DIR = BASE_DIR / "database"


def get_db_path() -> Path:
    return Path(os.environ.get("CLINICCARE_DB_PATH", str(DB_DIR / "cliniccare.db")))


SCHEMA = DB_DIR / "schema.sql"
SEED = DB_DIR / "seed.sql"
SEED_DIAGNOSIS = DB_DIR / "seed_diagnosis.sql"


def new_uuid() -> str:
    return str(uuid.uuid4())


def connect() -> sqlite3.Connection:
    # Create the database directory before opening SQLite so a fresh environment does not fail at startup.
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_db():
    conn = connect()
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    needs_creation = not db_path.exists()
    conn = connect()
    try:
        if needs_creation:
            conn.executescript(SCHEMA.read_text(encoding="utf-8"))
            for seed_path in (SEED_DIAGNOSIS, SEED):
                if seed_path.exists():
                    conn.executescript(seed_path.read_text(encoding="utf-8"))
            conn.commit()
        else:
            # Preserve existing records and keep schema initialization idempotent for the live SQLite file.
            conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='doctors' LIMIT 1")
            conn.commit()
    finally:
        conn.close()
