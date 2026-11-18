# ClinicCare Mini EMR

ClinicCare Mini EMR is a small clinic management application for doctors to search ICD-10 diagnosis codes, review patient consultation history, and create consultation records with diagnosis assignments.

## Technologies

- Backend: Python, FastAPI, SQLite, Pydantic, JWT
- Frontend: Nuxt 3, Vue 3, TypeScript

## Features

- Authentication and doctor login
- Patient search and inline patient creation during consultation entry
- ICD-10 diagnosis lookup by code or description
- Consultation creation and listing
- Search across consultation records by patient, diagnosis, or note content

## Project structure

```text
ClinicCare/
├── Backend/
│   ├── app/
│   ├── database/
│   ├── tests/
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   └── venv/
├── Frontend/
│   └── cliniccare-frontend/
│       ├── app/
│       ├── components/
│       ├── composables/
│       ├── middleware/
│       ├── pages/
│       ├── public/
│       ├── types/
│       ├── package.json
│       ├── nuxt.config.ts
│       └── README.md
├── README.md
└── .git/
```

## Prerequisites

The project was validated in this environment with:

- Python 3.12.8
- Node.js 24.14.1
- npm 11.11.0

## Quick start

### 1. Clone the repository

```bash
git clone <repo-url>
cd ClinicCare
```

### 2. Backend setup

```bash
cd Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set the required backend environment variable before starting the server:

```bash
export PYTHONPATH=$PWD
export SECRET_KEY="replace-with-a-secure-secret"
```

Start the API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend setup

```bash
cd ../Frontend/cliniccare-frontend
npm install
npm run dev -- --host 0.0.0.0
```

The frontend runs at http://localhost:3000 and expects the API at http://localhost:8000.

## Environment variables

The application uses the following environment values.

| Name | Required | Purpose | Example |
|---|---|---|---|
| `SECRET_KEY` | Yes | Signing key for JWT tokens | `change-me` |
| `CLINICCARE_DB_PATH` | No | Override the SQLite database file location | `/tmp/cliniccare.db` |
| `NUXT_PUBLIC_API_BASE` | No | Backend URL used by the frontend | `http://localhost:8000` |

The backend example file is at `Backend/.env.example`.

## API endpoints

The backend exposes the following routes.

### Authentication

- `POST /auth/login` — doctor login with username/password; returns the doctor name and sets HttpOnly access/refresh cookies. Tokens are not exposed in the response body.
- `POST /auth/refresh` — refresh the active session using the refresh cookie.
- `POST /auth/logout` — clears the current auth cookies and invalidates the refresh token.
- `GET /auth/me` — returns the current logged-in doctor profile when a valid session is present.

### Diagnosis

- `GET /diagnosis` — search ICD-10 diagnosis codes by code or description.

### Patients

- `GET /patients` — search patient records by name.

### Consultations

- `GET /consultation` — list queryable consultation records with filters such as patient id, patient name, doctor id, diagnosis code, and general search text.
- `POST /consultation` — create a consultation for an authenticated doctor.

## Database and seed data

The backend stores its SQLite database in the default path:

```text
Backend/database/cliniccare.db
```

This location can be overridden with the `CLINICCARE_DB_PATH` environment variable.

The database is initialized by `Backend/app/core/db.py`. The app creates the local SQLite file if it does not already exist and keeps existing records when the database is already present. The schema and seed files live in:

- `Backend/database/schema.sql`
- `Backend/database/seed.sql`
- `Backend/database/seed_diagnosis.sql`

The diagnosis seed file contains 100 ICD-10 records and is loaded during initialization.

## Authentication and demo account

The backend uses JWT authentication with HttpOnly cookies for session handling. Access and refresh tokens are not exposed to JavaScript or stored in browser storage. The frontend uses `fetch(..., { credentials: 'include' })`; when `/auth/me` reports an expired access token, the client refreshes the session once with the HttpOnly refresh cookie. Route middleware waits for this restoration before deciding whether to redirect to login, so valid sessions survive page reloads on the current route.

During local validation, the seeded doctor login was verified as:

- Username: `doctor01`
- Password: `@Admin123`

## Running tests

Run the backend tests from the backend directory:

```bash
cd Backend
source venv/bin/activate
export PYTHONPATH=$PWD
pytest tests/test_consultation_search.py -q
```

Run the frontend production build:

```bash
cd Frontend/cliniccare-frontend
npm run build
```

## Troubleshooting

### Backend port already in use

Stop the process already bound to port 8000, then restart the API.

### Missing environment variables

Make sure `SECRET_KEY` is defined in the backend `.env` file before running the app.

### Frontend cannot reach backend

Confirm the backend is running on http://localhost:8000 and that CORS is enabled for http://localhost:3000.

### Database initialization issues

If the database path is invalid or the folder does not exist, ensure the directory exists and that `CLINICCARE_DB_PATH` points to a writable location.

## Notes

This project is intentionally scoped to a small clinical workflow: doctor authentication, patient lookup and inline creation, diagnosis search, and consultation recording.
