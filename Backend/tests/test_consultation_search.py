import os
import sqlite3
import tempfile
import uuid
import unittest

from fastapi.testclient import TestClient

from app.core.db import get_db, init_db
from app.core.security import current_doctor
from app.main import app

TEST_DB_PATH = os.path.join(tempfile.gettempdir(), f"cliniccare_test_{uuid.uuid4()}.db")
os.environ["CLINICCARE_DB_PATH"] = TEST_DB_PATH


DOCTOR_1_ID = "6b7b736a-15d0-4ea4-a223-6d05d1a1a8ee"
DOCTOR_2_ID = "a6c0d9b1-3d9d-4b8a-b0a3-16f8d68d0b21"
PATIENT_1_ID = "271ae31d-1a31-4dfa-9d3a-8d3e2e46b101"
PATIENT_2_ID = "3a4d0f58-df0e-4c4e-8f4a-7f713b5a1a22"
PATIENT_3_ID = "7ef4f0b1-9a5c-4ece-8d9f-63fa9cce2cac"
CONSULT_1_ID = "f2d8a7e6-3b29-4be4-9d18-8d2c4fe6912c"
CONSULT_2_ID = "0cf5cebe-c1be-4f14-9c9f-93d7572bf328"
CONSULT_3_ID = "9bc0d67d-7d20-4424-b527-4ec0fa46d2c8"
CONSULT_4_ID = "d5c6dd0a-05bc-41dc-8d42-8e6d808f7d44"


class ConsultationSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

        def override_get_db():
            conn = sqlite3.connect(TEST_DB_PATH)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            try:
                yield conn
            finally:
                conn.close()

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[current_doctor] = lambda: {"id": DOCTOR_1_ID, "username": "doctor01"}

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()

    def setUp(self):
        init_db()
        self.conn = sqlite3.connect(TEST_DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("DELETE FROM consultation_diagnoses")
        self.conn.execute("DELETE FROM consultations")
        self.conn.execute("DELETE FROM diagnosis_codes")
        self.conn.execute("DELETE FROM patients")
        self.conn.execute("DELETE FROM doctors")

        self.conn.executemany(
            "INSERT INTO doctors (id, username, password_hash, full_name, email) VALUES (?, ?, ?, ?, ?)",
            [
                (DOCTOR_1_ID, "doctor01", "hash-value", "Dr. Nguyen Minh", "minh.nguyen@cliniccare.com"),
                (DOCTOR_2_ID, "doctor02", "hash-value", "Dr. Tran Hoa", "hoa.tran@cliniccare.com"),
            ],
        )

        self.conn.executemany(
            "INSERT INTO patients (id, full_name, date_of_birth, sex, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (PATIENT_1_ID, "Nguyen Van An", "1995-05-20", "Male", "0901234567", "an.nguyen@example.com"),
                (PATIENT_2_ID, "Tran Thi Binh", "1998-10-15", "Female", "0909876543", "binh.tran@example.com"),
                (PATIENT_3_ID, "Le Van Cuong", "1987-03-12", "Male", "0912345678", "cuong.le@example.com"),
            ],
        )

        self.conn.executemany(
            "INSERT INTO diagnosis_codes (code, description) VALUES (?, ?)",
            [
                ("A00.0", "Cholera due to Vibrio cholerae 01, biovar cholerae"),
                ("A00.1", "Cholera due to Vibrio cholerae 01, biovar eltor"),
                ("A00.9", "Cholera, unspecified"),
                ("A01.00", "Typhoid fever, unspecified"),
                ("J00", "Acute nasopharyngitis"),
            ],
        )

        self.conn.executemany(
            "INSERT INTO consultations (id, patient_id, doctor_id, consultation_date, treatment_notes, status) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (CONSULT_1_ID, PATIENT_1_ID, DOCTOR_1_ID, "2026-11-17 09:00:00", "Patient has cholera symptoms and dehydration.", "completed"),
                (CONSULT_2_ID, PATIENT_1_ID, DOCTOR_1_ID, "2026-11-16 08:00:00", "Routine follow-up after fever episode.", "completed"),
                (CONSULT_3_ID, PATIENT_2_ID, DOCTOR_2_ID, "2026-11-15 15:00:00", "Patient reports cholera-like illness and diarrhea.", "completed"),
                (CONSULT_4_ID, PATIENT_3_ID, DOCTOR_1_ID, "2026-11-14 12:00:00", "Respiratory symptoms and sore throat.", "draft"),
            ],
        )

        self.conn.executemany(
            "INSERT INTO consultation_diagnoses (id, consultation_id, diagnosis_code, is_primary) VALUES (?, ?, ?, ?)",
            [
                ("3004f1f3-4d48-4a65-b8c6-f1269dc2d223", CONSULT_1_ID, "A00.0", 1),
                ("d7d2a6ee-0c7e-4f5d-b612-39f6d7848e7a", CONSULT_1_ID, "A00.1", 0),
                ("9dbf1c4e-7951-4263-b0da-613c3758cae8", CONSULT_2_ID, "A01.00", 1),
                ("1d7eb2ac-6daf-42c8-9ad9-8b0c2cdfe4bf", CONSULT_3_ID, "A00.9", 1),
                ("4481f6d6-69bf-4d53-9f79-dc5eb8d3b1d3", CONSULT_4_ID, "J00", 1),
            ],
        )
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_uuid_fields_are_valid_v4(self):
        response = self.client.get("/consultation")
        self.assertEqual(response.status_code, 200)
        for item in response.json():
            self.assertEqual(uuid.UUID(item["id"]).version, 4)
            self.assertEqual(uuid.UUID(item["patient_id"]).version, 4)

    def test_list_all_consultations(self):
        response = self.client.get("/consultation")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_search_by_patient_id(self):
        response = self.client.get(f"/consultation?patient_id={PATIENT_1_ID}")
        self.assertEqual(response.status_code, 200)
        ids = [item["id"] for item in response.json()]
        self.assertEqual(ids, [CONSULT_1_ID, CONSULT_2_ID])

    def test_search_by_patient_name(self):
        response = self.client.get("/consultation?patient_name=nguyen")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_search_by_exact_diagnosis_code(self):
        response = self.client.get("/consultation?diagnosis_code=A00.0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()], [CONSULT_1_ID])

    def test_search_by_diagnosis_code_prefix(self):
        response = self.client.get("/consultation?diagnosis_code=A00")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()], [CONSULT_1_ID, CONSULT_3_ID])

    def test_search_combines_patient_id_and_diagnosis_code(self):
        response = self.client.get(f"/consultation?patient_id={PATIENT_1_ID}&diagnosis_code=A00.0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()], [CONSULT_1_ID])

    def test_general_search_across_relevant_fields(self):
        response = self.client.get("/consultation?search=cholera")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()], [CONSULT_1_ID, CONSULT_3_ID])

    def test_pagination(self):
        response = self.client.get("/consultation?limit=1&offset=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], CONSULT_2_ID)

    def test_init_db_creates_database_when_missing(self):
        path = os.path.join(tempfile.gettempdir(), f"cliniccare_init_test_{uuid.uuid4()}.db")
        original = os.environ.get("CLINICCARE_DB_PATH")
        os.environ["CLINICCARE_DB_PATH"] = path
        try:
            if os.path.exists(path):
                os.remove(path)
            init_db()
            self.assertTrue(os.path.exists(path))
            with sqlite3.connect(path) as conn:
                count = conn.execute("SELECT COUNT(*) FROM diagnosis_codes").fetchone()[0]
                self.assertGreater(count, 0)
        finally:
            if os.path.exists(path):
                os.remove(path)
            if original is None:
                os.environ.pop("CLINICCARE_DB_PATH", None)
            else:
                os.environ["CLINICCARE_DB_PATH"] = original

    def test_init_db_preserves_existing_records(self):
        path = os.path.join(tempfile.gettempdir(), f"cliniccare_persist_test_{uuid.uuid4()}.db")
        original = os.environ.get("CLINICCARE_DB_PATH")
        os.environ["CLINICCARE_DB_PATH"] = path
        try:
            init_db()
            with sqlite3.connect(path) as conn:
                conn.execute("INSERT INTO patients (id, full_name, sex) VALUES (?, ?, ?)", (str(uuid.uuid4()), "Persisted Patient", "Male"))
                conn.commit()
            init_db()
            with sqlite3.connect(path) as conn:
                count = conn.execute("SELECT COUNT(*) FROM patients WHERE full_name = ?", ("Persisted Patient",)).fetchone()[0]
                self.assertEqual(count, 1)
        finally:
            if os.path.exists(path):
                os.remove(path)
            if original is None:
                os.environ.pop("CLINICCARE_DB_PATH", None)
            else:
                os.environ["CLINICCARE_DB_PATH"] = original

    def test_invalid_patient_id(self):
        response = self.client.get("/consultation?patient_id=0")
        self.assertEqual(response.status_code, 422)

    def test_invalid_pagination_values(self):
        response = self.client.get("/consultation?limit=0")
        self.assertEqual(response.status_code, 422)

        response = self.client.get("/consultation?offset=-1")
        self.assertEqual(response.status_code, 422)

    def test_empty_search_input_is_ignored(self):
        response = self.client.get("/consultation?search=   ")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_multiple_diagnoses_do_not_duplicate_consultation_rows(self):
        response = self.client.get(f"/consultation?patient_id={PATIENT_1_ID}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], CONSULT_1_ID)
        self.assertEqual(len(response.json()[0]["diagnoses"]), 2)

    def test_filtered_results_keep_full_diagnosis_payload(self):
        response = self.client.get(f"/consultation?patient_id={PATIENT_1_ID}&diagnosis_code=A00")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()], [CONSULT_1_ID])
        self.assertEqual(len(response.json()[0]["diagnoses"]), 2)

    def test_diagnosis_filter_excludes_non_matching_consults(self):
        response = self.client.get("/consultation?diagnosis_code=A01.00")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()], [CONSULT_2_ID])

    def test_no_matching_results_returns_empty_list(self):
        response = self.client.get("/consultation?patient_name=NoMatch")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_sql_injection_attempt_is_treated_as_literal_input(self):
        response = self.client.get("/consultation?search=%' OR 1=1 --")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)


if __name__ == "__main__":
    unittest.main()
