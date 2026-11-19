-- ==========================================
-- CLINICCARE MINI EMR DATABASE
-- Schema Definition
-- NOTE: timestamps are stored in UTC; convert to local time in the frontend.
-- NOTE: PRAGMA foreign_keys must also be enabled on every connection in app code.
-- ==========================================

PRAGMA foreign_keys = ON;

-- ==========================================
-- 1. PATIENTS
-- ==========================================

CREATE TABLE IF NOT EXISTS patients (
    id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    date_of_birth TEXT,
    sex TEXT NOT NULL
        CHECK (sex IN ('Male', 'Female')),
    phone TEXT,
    email TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 2. DOCTORS
-- ==========================================

CREATE TABLE IF NOT EXISTS doctors (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    refresh_token_hash TEXT,
    refresh_token_expires_at TEXT
);

-- ==========================================
-- 3. DIAGNOSIS CODES (ICD-10)
-- ==========================================

CREATE TABLE IF NOT EXISTS diagnosis_codes (
    code TEXT PRIMARY KEY,
    description TEXT NOT NULL
);

-- ==========================================
-- 4. CONSULTATIONS
-- ==========================================

CREATE TABLE IF NOT EXISTS consultations (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    doctor_id TEXT NOT NULL,
    consultation_date TEXT DEFAULT (date('now')),
    treatment_notes TEXT NOT NULL,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (patient_id)
        REFERENCES patients(id),

    FOREIGN KEY (doctor_id)
        REFERENCES doctors(id)
);

-- Auto-update updated_at (SQLite has no ON UPDATE)
CREATE TRIGGER IF NOT EXISTS trg_consultations_updated
AFTER UPDATE ON consultations
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE consultations
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.id;
END;

-- ==========================================
-- 5. CONSULTATION DIAGNOSES
-- ==========================================

CREATE TABLE IF NOT EXISTS consultation_diagnoses (
    id TEXT PRIMARY KEY,
    consultation_id TEXT NOT NULL,
    diagnosis_code TEXT NOT NULL,

    is_primary INTEGER NOT NULL DEFAULT 0
        CHECK (is_primary IN (0, 1)),

    UNIQUE (consultation_id, diagnosis_code),

    FOREIGN KEY (consultation_id)
        REFERENCES consultations(id)
        ON DELETE CASCADE,

    FOREIGN KEY (diagnosis_code)
        REFERENCES diagnosis_codes(code)
);

-- At most one primary diagnosis per consultation
CREATE UNIQUE INDEX IF NOT EXISTS idx_one_primary_per_consultation
ON consultation_diagnoses(consultation_id)
WHERE is_primary = 1;

-- ==========================================
-- 6. INDEXES
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_patients_name
ON patients(full_name);

CREATE INDEX IF NOT EXISTS idx_consultations_patient
ON consultations(patient_id);

CREATE INDEX IF NOT EXISTS idx_consultations_doctor
ON consultations(doctor_id);

CREATE INDEX IF NOT EXISTS idx_consultations_date
ON consultations(consultation_date);

CREATE INDEX IF NOT EXISTS idx_consultations_patient_date
ON consultations(patient_id, consultation_date DESC);

CREATE INDEX IF NOT EXISTS idx_consultations_doctor_date
ON consultations(doctor_id, consultation_date DESC);

-- Search notes by diagnosis code
CREATE INDEX IF NOT EXISTS idx_cd_code
ON consultation_diagnoses(diagnosis_code);

CREATE INDEX IF NOT EXISTS idx_consultation_diagnoses_batch
ON consultation_diagnoses(consultation_id, diagnosis_code);

CREATE INDEX IF NOT EXISTS idx_doctors_refresh
ON doctors(refresh_token_hash);
