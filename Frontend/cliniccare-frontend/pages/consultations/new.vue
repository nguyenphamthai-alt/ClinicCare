<script setup lang="ts">
import type { ConsultationFormState, DiagnosisItem, Patient } from '~/types'

definePageMeta({ middleware: 'auth' })

const api = useApi()

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
const diagnosisLoading = ref(false)
const submitError = ref('')
const submitting = ref(false)

watch(patientQuery, async (value) => {
  if (!value.trim()) {
    patientResults.value = []
    return
  }

  patientLoading.value = true

  try {
    patientResults.value = await api.get<Patient[]>('/patients', { search: value.trim(), limit: 8 })
  } catch (error) {
    patientResults.value = []
    console.error(error)
  } finally {
    patientLoading.value = false
  }
})

watch(diagnosisQuery, async (value) => {
  if (!value.trim()) {
    diagnosisResults.value = []
    return
  }

  diagnosisLoading.value = true

  try {
    diagnosisResults.value = await api.get<DiagnosisItem[]>('/diagnosis', {
      search: value.trim(),
      limit: 10
    })
  } catch (error) {
    diagnosisResults.value = []
    console.error(error)
  } finally {
    diagnosisLoading.value = false
  }
})

const selectPatient = (patient: Patient) => {
  form.patientId = patient.id
  form.patientName = patient.full_name
  patientQuery.value = patient.full_name
  patientResults.value = []
}

const selectDiagnosis = (item: DiagnosisItem) => {
  if (!form.diagnosisCodes.includes(item.code)) {
    form.diagnosisCodes.push(item.code)
  }

  form.primaryCode = form.primaryCode || item.code
  diagnosisQuery.value = ''
  diagnosisResults.value = []
}

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
</script>

<template>
  <div class="app-shell">
    <AppSidebar />

    <main class="main-panel">
      <AppHeader title="New Consultation" subtitle="Document a clinic visit and diagnosis details." />

      <div class="page-content">
        <form class="card form-card" @submit.prevent="submitConsultation">
          <div class="form-grid">
            <div class="field-column field-column--full">
              <PatientSearch
                v-model="patientQuery"
                :results="patientResults"
                :selected-patient-name="form.patientName || null"
                :loading="patientLoading"
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
    </main>
  </div>
</template>
