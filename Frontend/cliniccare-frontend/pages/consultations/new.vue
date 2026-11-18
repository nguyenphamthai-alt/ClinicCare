<script setup lang="ts">
import type { ConsultationFormState, DiagnosisItem, Patient } from '~/types'

definePageMeta({
  middleware: 'auth',
  layout: 'app',
  title: 'New Consultation',
  subtitle: 'Document a clinic visit and diagnosis details.'
})

const api = useApi()
const MAX_DIAGNOSES = 10

const form = reactive<ConsultationFormState>({
  patientId: '',
  patientName: '',
  consultationDate: new Date().toISOString().slice(0, 10),
  diagnosisCodes: [],
  primaryCode: '',
  treatmentNotes: '',
  status: 'completed'
})

const patientQuery = ref('')
const patientResults = ref<Patient[]>([])
const diagnosisQuery = ref('')
const diagnosisResults = ref<DiagnosisItem[]>([])
const patientLoading = ref(false)
const patientSearchError = ref<string | null>(null)
const patientSearchComplete = ref(false)
const diagnosisLoading = ref(false)
const diagnosisSearchError = ref<string | null>(null)
const submitError = ref('')
const submitting = ref(false)
let patientTimer: ReturnType<typeof setTimeout> | undefined
let diagnosisTimer: ReturnType<typeof setTimeout> | undefined
let patientRequest = 0
let diagnosisRequest = 0

watch(patientQuery, (value) => {
  const request = ++patientRequest
  if (patientTimer) clearTimeout(patientTimer)
  const term = value.trim()
  if (form.patientId && value !== form.patientName) {
    form.patientId = ''
    form.patientName = ''
  }
  patientSearchComplete.value = false
  if (term.length > 100 || (form.patientId && value === form.patientName)) {
    patientResults.value = []
    patientLoading.value = false
    patientSearchError.value = null
    return
  }

  patientResults.value = []
  patientLoading.value = true
  patientSearchError.value = null
  patientTimer = setTimeout(async () => {
    try {
      const results = await api.get<Patient[]>('/patients', { search: term || undefined, limit: 8 })
      if (request === patientRequest) patientResults.value = results
    } catch (error) {
      if (request === patientRequest) {
        patientResults.value = []
        patientSearchError.value = error instanceof Error ? error.message : 'Unable to search patients.'
      }
    } finally {
      if (request === patientRequest) {
        patientLoading.value = false
        patientSearchComplete.value = !patientSearchError.value
      }
    }
  }, 250)
}, { flush: 'sync' })

watch(diagnosisQuery, (value) => {
  const request = ++diagnosisRequest
  if (diagnosisTimer) clearTimeout(diagnosisTimer)
  const term = value.trim()
  diagnosisSearchError.value = null
  if (term.length > 100) {
    diagnosisResults.value = []
    diagnosisLoading.value = false
    return
  }

  diagnosisResults.value = []
  diagnosisLoading.value = true
  diagnosisTimer = setTimeout(async () => {
    try {
      const results = await api.get<DiagnosisItem[]>('/diagnosis', { search: term || undefined, limit: 10 })
      if (request === diagnosisRequest) diagnosisResults.value = results
    } catch (error) {
      if (request === diagnosisRequest) {
        diagnosisResults.value = []
        diagnosisSearchError.value = error instanceof Error ? error.message : 'Unable to search diagnosis codes.'
      }
    } finally {
      if (request === diagnosisRequest) diagnosisLoading.value = false
    }
  }, 250)
}, { flush: 'sync' })

const selectPatient = (patient: Patient) => {
  patientRequest += 1
  if (patientTimer) clearTimeout(patientTimer)
  patientLoading.value = false
  patientSearchError.value = null
  patientSearchComplete.value = true
  form.patientId = patient.id
  form.patientName = patient.full_name
  patientQuery.value = patient.full_name
  patientResults.value = []
}

const selectDiagnosis = (item: DiagnosisItem) => {
  diagnosisRequest += 1
  if (diagnosisTimer) clearTimeout(diagnosisTimer)
  diagnosisLoading.value = false
  if (form.diagnosisCodes.includes(item.code)) return
  if (form.diagnosisCodes.length >= MAX_DIAGNOSES) {
    submitError.value = `A consultation can include at most ${MAX_DIAGNOSES} diagnoses.`
    return
  }

  form.diagnosisCodes.push(item.code)
  form.primaryCode = form.primaryCode || item.code
  diagnosisQuery.value = ''
  diagnosisResults.value = []
  submitError.value = ''
}

onBeforeUnmount(() => {
  patientRequest += 1
  diagnosisRequest += 1
  if (patientTimer) clearTimeout(patientTimer)
  if (diagnosisTimer) clearTimeout(diagnosisTimer)
})

const removeDiagnosis = (code: string) => {
  form.diagnosisCodes = form.diagnosisCodes.filter((item) => item !== code)

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
      primary_code: form.primaryCode || form.diagnosisCodes[0],
      status: form.status
    })

    await navigateTo('/consultations')
  } catch (error) {
    submitError.value = error instanceof Error ? error.message : 'Unable to save consultation.'
  } finally {
    submitting.value = false
  }
}

const loadPatientSuggestions = async () => {
  if (patientLoading.value || patientResults.value.length || (form.patientId && patientQuery.value === form.patientName)) return
  const request = ++patientRequest
  if (patientTimer) clearTimeout(patientTimer)
  patientLoading.value = true
  patientSearchError.value = null
  patientSearchComplete.value = false
  try {
    const results = await api.get<Patient[]>('/patients', { search: patientQuery.value.trim() || undefined, limit: 8 })
    if (request === patientRequest) patientResults.value = results
  } catch (error) {
    if (request === patientRequest) {
      patientResults.value = []
      patientSearchError.value = error instanceof Error ? error.message : 'Unable to load patients.'
    }
  } finally {
    if (request === patientRequest) {
      patientLoading.value = false
      patientSearchComplete.value = !patientSearchError.value
    }
  }
}

const loadDiagnosisSuggestions = async () => {
  if (diagnosisLoading.value || diagnosisResults.value.length) return
  const request = ++diagnosisRequest
  if (diagnosisTimer) clearTimeout(diagnosisTimer)
  diagnosisLoading.value = true
  diagnosisSearchError.value = null
  try {
    const results = await api.get<DiagnosisItem[]>('/diagnosis', { search: diagnosisQuery.value.trim() || undefined, limit: 10 })
    if (request === diagnosisRequest) diagnosisResults.value = results
  } catch (error) {
    if (request === diagnosisRequest) {
      diagnosisResults.value = []
      diagnosisSearchError.value = error instanceof Error ? error.message : 'Unable to load diagnosis codes.'
    }
  } finally {
    if (request === diagnosisRequest) diagnosisLoading.value = false
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
            <input id="consultation-date" v-model="form.consultationDate" class="form-control" type="date" />
          </div>
        </div>

        <div class="field-column">
          <div class="field-group">
            <label for="status">Status</label>
            <select id="status" v-model="form.status" class="form-control">
              <option value="completed">Completed</option>
              <option value="draft">Draft</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
        </div>

        <div class="field-column field-column--full">
          <DiagnosisSearch
            v-model="diagnosisQuery"
            :results="diagnosisResults"
            :selected-codes="form.diagnosisCodes"
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
                {{ code }}
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
