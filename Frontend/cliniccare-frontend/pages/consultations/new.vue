<script setup lang="ts">
import type { ConsultationFormState, DiagnosisItem, Patient } from '~/types'
import { todayLocal } from '~/utils/date'

definePageMeta({
  middleware: 'auth',
  layout: 'app',
  title: 'New Consultation',
  subtitle: 'Document a clinic visit and diagnosis details.'
})

const api = useApi()
const MAX_DIAGNOSES = 10
const initialConsultationDate = todayLocal()
const maxConsultationDate = todayLocal()

const form = reactive<ConsultationFormState>({
  patientId: '',
  patientName: '',
  consultationDate: initialConsultationDate,
  diagnosisCodes: [],
  primaryCode: '',
  treatmentNotes: ''
})

const patientSearch = useDebouncedSearch<Patient>({
  path: '/patients',
  limit: 8,
  failureMessage: 'Unable to search patients.',
  onQueryChange: (value) => {
    if (form.patientId && value !== form.patientName) {
      form.patientId = ''
      form.patientName = ''
    }
  }
})

const diagnosisSearch = useDebouncedSearch<DiagnosisItem>({
  path: '/diagnosis',
  limit: 10,
  failureMessage: 'Unable to search diagnosis codes.'
})

const {
  query: patientQuery,
  results: patientResults,
  loading: patientLoading,
  error: patientSearchError,
  searchComplete: patientSearchComplete,
  loadSuggestions: loadPatientSuggestions,
  reset: resetPatientSearch
} = patientSearch

const {
  query: diagnosisQuery,
  results: diagnosisResults,
  loading: diagnosisLoading,
  error: diagnosisSearchError,
  loadSuggestions: loadDiagnosisSuggestions,
  reset: resetDiagnosisSearch
} = diagnosisSearch

const diagnosisDescriptions = ref<Record<string, string>>({})
const submitError = ref('')
const submitting = ref(false)

const selectPatient = (patient: Patient) => {
  resetPatientSearch(patient.full_name, true)
  form.patientId = patient.id
  form.patientName = patient.full_name
}

const selectDiagnosis = (item: DiagnosisItem) => {
  if (form.diagnosisCodes.includes(item.code)) return
  if (form.diagnosisCodes.length >= MAX_DIAGNOSES) {
    submitError.value = `A consultation can include at most ${MAX_DIAGNOSES} diagnoses.`
    return
  }

  form.diagnosisCodes.push(item.code)
  diagnosisDescriptions.value[item.code] = item.description
  form.primaryCode = form.primaryCode || item.code
  resetDiagnosisSearch()
  submitError.value = ''
}

const removeDiagnosis = (code: string) => {
  form.diagnosisCodes = form.diagnosisCodes.filter((item) => item !== code)
  delete diagnosisDescriptions.value[code]

  if (form.primaryCode === code) {
    form.primaryCode = form.diagnosisCodes[0] ?? ''
  }
}

const submitConsultation = async () => {
  submitError.value = ''

  if (!form.patientId) {
    submitError.value = 'Please select a patient.'
    return
  }

  if (!form.diagnosisCodes.length) {
    submitError.value = 'Please add at least one diagnosis.'
    return
  }

  if (!form.consultationDate) {
    submitError.value = 'Consultation date is required.'
    return
  }

  if (form.consultationDate > maxConsultationDate) {
    submitError.value = 'Consultation date cannot be in the future.'
    return
  }

  if (!form.treatmentNotes.trim()) {
    submitError.value = 'Treatment notes are required.'
    return
  }

  submitting.value = true

  try {
    await api.post('/consultation', {
      patient_id: form.patientId,
      consultation_date: form.consultationDate,
      treatment_notes: form.treatmentNotes.trim(),
      diagnosis_codes: form.diagnosisCodes,
      primary_code: form.primaryCode || form.diagnosisCodes[0]
    })

    await navigateTo('/consultations')
  } catch (error) {
    submitError.value = error instanceof Error ? error.message : 'Unable to save consultation.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="page-content">
    <form class="card form-card" @submit.prevent="submitConsultation">
      <div class="form-grid">
        <div class="field-column field-column--full">
          <PatientSearch
            v-model="patientQuery"
            :results="patientResults"
            :selected-patient-name="form.patientName || null"
            :loading="patientLoading"
            :search-error="patientSearchError"
            :search-complete="patientSearchComplete"
            @focus="loadPatientSuggestions"
            @select="selectPatient"
          />
        </div>

        <div class="field-column">
          <div class="field-group">
            <label for="consultation-date">Consultation date</label>
            <input
              id="consultation-date"
              v-model="form.consultationDate"
              class="form-control"
              type="date"
              :max="maxConsultationDate"
              required
            />
          </div>
        </div>

        <div class="field-column field-column--full">
          <DiagnosisSearch
            v-model="diagnosisQuery"
            :results="diagnosisResults"
            :selected-codes="form.diagnosisCodes"
            :selected-descriptions="diagnosisDescriptions"
            :loading="diagnosisLoading"
            :search-error="diagnosisSearchError"
            :max-selections="MAX_DIAGNOSES"
            @focus="loadDiagnosisSuggestions"
            @select="selectDiagnosis"
            @remove="removeDiagnosis"
          />
        </div>

        <div class="field-column field-column--full">
          <div class="field-group">
            <label for="primary-code">Primary diagnosis</label>
            <select id="primary-code" v-model="form.primaryCode" class="form-control" :disabled="!form.diagnosisCodes.length">
              <option v-for="code in form.diagnosisCodes" :key="code" :value="code">
                {{ code }}<template v-if="diagnosisDescriptions[code]"> - {{ diagnosisDescriptions[code] }}</template>
              </option>
            </select>
          </div>
        </div>

        <div class="field-column field-column--full">
          <div class="field-group">
            <label for="treatment-notes">Treatment notes</label>
            <textarea id="treatment-notes" v-model="form.treatmentNotes" class="form-control form-control--textarea" rows="7" placeholder="Enter assessment, treatment plan, medications and follow-up guidance." />
          </div>
        </div>
      </div>

      <div v-if="submitError" class="form-message form-message--error">{{ submitError }}</div>

      <div class="form-actions">
        <NuxtLink to="/consultations" class="secondary-button">Cancel</NuxtLink>
        <button class="primary-button" type="submit" :disabled="submitting">
          {{ submitting ? 'Saving…' : 'Save consultation' }}
        </button>
      </div>
    </form>
  </div>
</template>
