export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  full_name?: string | null
}

export interface DiagnosisItem {
  code: string
  description: string
  is_primary?: boolean
}

export interface Patient {
  id: string
  full_name: string
  date_of_birth?: string | null
  sex: string
  phone?: string | null
  email?: string | null
}

export interface Consultation {
  id: string
  consultation_date: string
  treatment_notes: string
  status: string
  patient_id: string
  patient_name: string
  doctor_name: string
  diagnoses: DiagnosisItem[]
}

export interface ConsultationFormState {
  patientId: string
  patientName: string
  consultationDate: string
  diagnosisCodes: string[]
  primaryCode: string
  treatmentNotes: string
  status: 'draft' | 'completed' | 'cancelled'
}
