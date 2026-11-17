-- ==========================================
-- CLINICCARE MINI EMR
-- SAMPLE DATA (UUID v4 primary keys)
-- ==========================================

PRAGMA foreign_keys = ON;

-- ==========================================
-- 1. PATIENTS
-- ==========================================

INSERT INTO patients (
    id,
    full_name,
    date_of_birth,
    sex,
    phone,
    email
)
VALUES
(
    '271ae31d-1a31-4dfa-9d3a-8d3e2e46b101',
    'Nguyen Van An',
    '1995-05-20',
    'Male',
    '0901234567',
    'an.nguyen@example.com'
),
(
    '3a4d0f58-df0e-4c4e-8f4a-7f713b5a1a22',
    'Tran Thi Binh',
    '1998-10-15',
    'Female',
    '0909876543',
    'binh.tran@example.com'
),
(
    '7ef4f0b1-9a5c-4ece-8d9f-63fa9cce2cac',
    'Le Van Cuong',
    '1987-03-12',
    'Male',
    '0912345678',
    'cuong.le@example.com'
),
(
    'a04d8e73-3d1d-4f9d-9a3f-601b7ec7d4e1',
    'Pham Thi Dung',
    '2000-08-25',
    'Female',
    '0923456789',
    'dung.pham@example.com'
),
(
    'de5297e5-0d57-49b2-8c1e-8d0c7f6adfa8',
    'Hoang Van Nam',
    '1975-12-10',
    'Male',
    '0934567890',
    'nam.hoang@example.com'
)
ON CONFLICT(id) DO NOTHING;

-- ==========================================
-- 2. DOCTORS
-- ==========================================

INSERT INTO doctors (
    id,
    username,
    password_hash,
    full_name,
    email
)
VALUES
(
    '6b7b736a-15d0-4ea4-a223-6d05d1a1a8ee',
    'doctor01',
    '$2a$12$6u4fFRNqfttMpb5XclX2JOUTrssDeJq.3C8AtHebGQ63.HTyhgf/a',
    'Dr. Nguyen Minh',
    'minh.nguyen@cliniccare.com'
),
(
    'a6c0d9b1-3d9d-4b8a-b0a3-16f8d68d0b21',
    'doctor02',
    '$2a$12$6u4fFRNqfttMpb5XclX2JOUTrssDeJq.3C8AtHebGQ63.HTyhgf/a',
    'Dr. Tran Hoa',
    'hoa.tran@cliniccare.com'
),
(
    'f2823f2b-d94c-4fd8-9c92-f70f16e1a2dd',
    'doctor03',
    '$2a$12$6u4fFRNqfttMpb5XclX2JOUTrssDeJq.3C8AtHebGQ63.HTyhgf/a',
    'Dr. Le Thanh Thien Tung',
    'thanh.le@cliniccare.com'
)
ON CONFLICT(id) DO NOTHING;

-- ==========================================
-- 3. CONSULTATIONS
-- ==========================================

INSERT INTO consultations (
    id,
    patient_id,
    doctor_id,
    consultation_date,
    treatment_notes,
    status
)
VALUES
(
    'f2d8a7e6-3b29-4be4-9d18-8d2c4fe6912c',
    '271ae31d-1a31-4dfa-9d3a-8d3e2e46b101',
    '6b7b736a-15d0-4ea4-a223-6d05d1a1a8ee',
    '2026-11-17 09:00:00',
    'Patient has fever, cough and sore throat.',
    'completed'
),
(
    '0cf5cebe-c1be-4f14-9c9f-93d7572bf328',
    '271ae31d-1a31-4dfa-9d3a-8d3e2e46b101',
    '6b7b736a-15d0-4ea4-a223-6d05d1a1a8ee',
    '2026-11-17 10:30:00',
    'Patient reports headache and dizziness.',
    'completed'
),
(
    '9bc0d67d-7d20-4424-b527-4ec0fa46d2c8',
    '3a4d0f58-df0e-4c4e-8f4a-7f713b5a1a22',
    'a6c0d9b1-3d9d-4b8a-b0a3-16f8d68d0b21',
    '2026-11-17 11:00:00',
    'Follow-up examination for hypertension.',
    'draft'
),
(
    'd5c6dd0a-05bc-41dc-8d42-8e6d808f7d44',
    '7ef4f0b1-9a5c-4ece-8d9f-63fa9cce2cac',
    'f2823f2b-d94c-4fd8-9c92-f70f16e1a2dd',
    '2026-11-17 13:00:00',
    'Patient reports symptoms of acid reflux.',
    'completed'
),
(
    'c9a2d7eb-c4d9-4c91-b9dc-d57dcdb17640',
    'de5297e5-0d57-49b2-8c1e-8d0c7f6adfa8',
    'a6c0d9b1-3d9d-4b8a-b0a3-16f8d68d0b21',
    '2026-11-17 14:30:00',
    'Patient reports lower back pain.',
    'draft'
)
ON CONFLICT(id) DO NOTHING;

-- ==========================================
-- 4. CONSULTATION DIAGNOSES
-- ==========================================

INSERT INTO consultation_diagnoses (
    id,
    consultation_id,
    diagnosis_code,
    is_primary
)
VALUES
-- Consultation 1
('3004f1f3-4d48-4a65-b8c6-f1269dc2d223', 'f2d8a7e6-3b29-4be4-9d18-8d2c4fe6912c', 'A00.0', 1),
('d7d2a6ee-0c7e-4f5d-b612-39f6d7848e7a', 'f2d8a7e6-3b29-4be4-9d18-8d2c4fe6912c', 'A00.1', 0),

-- Consultation 2
('9dbf1c4e-7951-4263-b0da-613c3758cae8', '0cf5cebe-c1be-4f14-9c9f-93d7572bf328', 'A01.00', 1),

-- Consultation 3
('1d7eb2ac-6daf-42c8-9ad9-8b0c2cdfe4bf', '9bc0d67d-7d20-4424-b527-4ec0fa46d2c8', 'A02.0', 1),
('cf8ea444-f9cb-4a60-9f7a-99d80f6822dd', '9bc0d67d-7d20-4424-b527-4ec0fa46d2c8', 'A02.1', 0),

-- Consultation 4
('4481f6d6-69bf-4d53-9f79-dc5eb8d3b1d3', 'd5c6dd0a-05bc-41dc-8d42-8e6d808f7d44', 'A03.0', 1),

-- Consultation 5
('f4af4d59-73da-4a3d-b6ef-abf36d7b7367', 'c9a2d7eb-c4d9-4c91-b9dc-d57dcdb17640', 'A04.5', 1)
ON CONFLICT(id) DO NOTHING;
