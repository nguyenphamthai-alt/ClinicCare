# ClinicCare Mini EMR Backend

This project exposes the FastAPI backend for the ClinicCare Mini EMR.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and provide the required values, including `SECRET_KEY`.

## Run locally

```bash
uvicorn app.main:app --reload
```

The app reads the SQLite database from `database/cliniccare.db` by default, unless `CLINICCARE_DB_PATH` is set for tests.

## Database

The database schema and seed files live in the `database/` folder:

- `schema.sql`
- `seed.sql`
- `seed_diagnosis.sql`

The app initializes the database on startup and re-creates the local SQLite file. Test runs use an isolated temporary database file.
