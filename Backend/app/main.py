import logging
import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth, consultations, diagnosis, patients
from app.core.db import init_db
from app.core.error_handlers import register_error_handlers

logger = logging.getLogger("cliniccare.api")
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Reinitialize the local SQLite database on startup so the demo app always starts from a known state.
    init_db()
    yield


app = FastAPI(title="ClinicCare Mini EMR", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)

for r in (auth.router, diagnosis.router, patients.router, consultations.router):
    app.include_router(r)
