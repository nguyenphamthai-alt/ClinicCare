<script setup lang="ts">
import type { Consultation, DiagnosisItem } from '~/types'
import { formatDateTime } from '~/utils/date'

definePageMeta({
  middleware: 'auth',
  layout: 'app',
  title: 'Search',
  subtitle: 'Locate diagnoses and consultation history quickly.'
})

const api = useApi()

const diagnosisQuery = ref('')
const diagnosisResults = ref<DiagnosisItem[]>([])
const diagnosisLoading = ref(false)
const diagnosisError = ref<string | null>(null)
const diagnosisPage = ref(1)
const diagnosisPageSize = 10
const diagnosisHasMore = ref(true)
const diagnosisReady = ref(false)
const initialDiagnosisResults = ref<DiagnosisItem[]>([])
const initialDiagnosisHasMore = ref(false)
const initialDiagnosisReady = ref(false)
let diagnosisTimer: ReturnType<typeof setTimeout> | undefined
let diagnosisRequest = 0

const consultationQuery = ref('')
const consultationResults = ref<Consultation[]>([])
const consultationLoading = ref(false)
const consultationError = ref<string | null>(null)
const consultationPage = ref(1)
const consultationPageSize = 10
const consultationHasMore = ref(true)
const consultationReady = ref(false)
const initialConsultationResults = ref<Consultation[]>([])
const initialConsultationHasMore = ref(false)
const initialConsultationReady = ref(false)
let consultationTimer: ReturnType<typeof setTimeout> | undefined
let consultationRequest = 0

const fetchDiagnosisResults = async (search: string, page: number, request: number) => {
  const term = search.trim()
  diagnosisLoading.value = true
  diagnosisError.value = null
  diagnosisReady.value = false

  try {
    const rows = await api.get<DiagnosisItem[]>('/diagnosis', {
      search: term,
      limit: diagnosisPageSize + 1,
      offset: (page - 1) * diagnosisPageSize
    })

    if (request !== diagnosisRequest) return
    const hasMore = rows.length > diagnosisPageSize
    diagnosisResults.value = hasMore ? rows.slice(0, diagnosisPageSize) : rows
    diagnosisHasMore.value = hasMore
    if (!term && page === 1) {
      initialDiagnosisResults.value = diagnosisResults.value
      initialDiagnosisHasMore.value = hasMore
      initialDiagnosisReady.value = true
    }

    if (!diagnosisResults.value.length && page > 1) {
      diagnosisPage.value = Math.max(1, page - 1)
      return
    }

    diagnosisPage.value = page
    diagnosisReady.value = true
  } catch (error) {
    if (request !== diagnosisRequest) return
    diagnosisError.value = error instanceof Error ? error.message : 'Diagnosis search failed.'
    diagnosisResults.value = []
    diagnosisHasMore.value = false
    diagnosisReady.value = true
  } finally {
    if (request === diagnosisRequest) diagnosisLoading.value = false
  }
}

const fetchConsultationResults = async (search: string, page: number, request: number) => {
  const term = search.trim()
  consultationLoading.value = true
  consultationError.value = null
  consultationReady.value = false

  try {
    const rows = await api.get<Consultation[]>('/consultation', {
      search: term || undefined,
      limit: consultationPageSize + 1,
      offset: (page - 1) * consultationPageSize
    })

    if (request !== consultationRequest) return
    const hasMore = rows.length > consultationPageSize
    consultationResults.value = hasMore ? rows.slice(0, consultationPageSize) : rows
    consultationHasMore.value = hasMore
    if (!term && page === 1) {
      initialConsultationResults.value = consultationResults.value
      initialConsultationHasMore.value = hasMore
      initialConsultationReady.value = true
    }

    if (!consultationResults.value.length && page > 1) {
      consultationPage.value = Math.max(1, page - 1)
      return
    }

    consultationPage.value = page
    consultationReady.value = true
  } catch (error) {
    if (request !== consultationRequest) return
    consultationError.value = error instanceof Error ? error.message : 'Consultation search failed.'
    consultationResults.value = []
    consultationHasMore.value = false
    consultationReady.value = true
  } finally {
    if (request === consultationRequest) consultationLoading.value = false
  }
}

const loadDiagnosisPage = (page: number) => {
  if (diagnosisTimer) clearTimeout(diagnosisTimer)
  const request = ++diagnosisRequest
  return fetchDiagnosisResults(diagnosisQuery.value, page, request)
}

const loadConsultationPage = (page: number) => {
  if (consultationTimer) clearTimeout(consultationTimer)
  const request = ++consultationRequest
  return fetchConsultationResults(consultationQuery.value, page, request)
}

watch(diagnosisQuery, (value) => {
  const request = ++diagnosisRequest
  if (diagnosisTimer) clearTimeout(diagnosisTimer)
  diagnosisPage.value = 1
  diagnosisError.value = null
  const term = value.trim()
  if (!term) {
    if (initialDiagnosisReady.value) {
      diagnosisResults.value = initialDiagnosisResults.value
      diagnosisHasMore.value = initialDiagnosisHasMore.value
      diagnosisReady.value = true
      diagnosisLoading.value = false
    } else {
      diagnosisTimer = setTimeout(() => fetchDiagnosisResults('', 1, request), 300)
    }
    return
  }
  if (term.length > 100) {
    diagnosisResults.value = []
    diagnosisLoading.value = false
    diagnosisReady.value = true
    diagnosisError.value = 'Search must be 100 characters or fewer.'
    return
  }
  diagnosisResults.value = []
  diagnosisLoading.value = true
  diagnosisReady.value = false
  diagnosisTimer = setTimeout(() => fetchDiagnosisResults(value, 1, request), 300)
}, { flush: 'sync' })

watch(consultationQuery, (value) => {
  const request = ++consultationRequest
  if (consultationTimer) clearTimeout(consultationTimer)
  consultationPage.value = 1
  consultationError.value = null
  const term = value.trim()
  if (!term) {
    if (initialConsultationReady.value) {
      consultationResults.value = initialConsultationResults.value
      consultationHasMore.value = initialConsultationHasMore.value
      consultationReady.value = true
      consultationLoading.value = false
    } else {
      consultationTimer = setTimeout(() => fetchConsultationResults('', 1, request), 300)
    }
    return
  }
  if (term.length > 200) {
    consultationResults.value = []
    consultationLoading.value = false
    consultationReady.value = true
    consultationError.value = 'Search must be 200 characters or fewer.'
    return
  }
  consultationResults.value = []
  consultationLoading.value = true
  consultationReady.value = false
  consultationTimer = setTimeout(() => fetchConsultationResults(value, 1, request), 300)
}, { flush: 'sync' })

onMounted(async () => {
  await loadDiagnosisPage(1)
  await loadConsultationPage(1)
})

onBeforeUnmount(() => {
  diagnosisRequest += 1
  consultationRequest += 1
  if (diagnosisTimer) clearTimeout(diagnosisTimer)
  if (consultationTimer) clearTimeout(consultationTimer)
})

const diagnosisPageLabel = computed(() => {
  if (!diagnosisResults.value.length) return 'No records'
  return `Showing ${diagnosisResults.value.length} items`
})

const consultationPageLabel = computed(() => {
  if (!consultationResults.value.length) return 'No records'
  return `Showing ${consultationResults.value.length} items`
})
</script>

<template>
  <div class="page-content search-page">
    <section class="card search-card">
      <div class="section-header">
        <h2>Diagnosis Search</h2>
      </div>

      <div class="field-group">
        <label for="diagnosis-search-page">ICD-10 or description</label>
        <input id="diagnosis-search-page" v-model="diagnosisQuery" class="form-control" type="search" maxlength="100" placeholder="Search diagnosis code or description" />
      </div>

      <div class="results-toolbar" v-if="diagnosisResults.length || diagnosisQuery.trim()">
        <span>{{ diagnosisPageLabel }}</span>
        <div class="page-actions">
          <button class="page-button" type="button" :disabled="diagnosisPage === 1 || diagnosisLoading" @click="loadDiagnosisPage(Math.max(1, diagnosisPage - 1))">Prev</button>
          <span class="page-number">Page {{ diagnosisPage }}</span>
          <button class="page-button" type="button" :disabled="!diagnosisHasMore || diagnosisLoading" @click="loadDiagnosisPage(diagnosisPage + 1)">Next</button>
        </div>
      </div>

      <div v-if="diagnosisLoading" class="state-panel state-panel--compact">Loading all diagnosis records…</div>
      <div v-else-if="diagnosisError" class="state-panel state-panel--compact state-panel--error">{{ diagnosisError }}</div>

      <div v-else-if="diagnosisResults.length" class="table-wrap">
        <table class="data-table data-table--compact">
          <thead>
            <tr>
              <th>Code</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="diagnosis in diagnosisResults" :key="diagnosis.code">
              <td><span class="diagnosis-code diagnosis-code--large">{{ diagnosis.code }}</span></td>
              <td>{{ diagnosis.description }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else-if="diagnosisReady && !diagnosisResults.length" class="state-panel state-panel--compact">No diagnosis results found.</div>
    </section>

    <section class="card search-card">
      <div class="section-header">
        <h2>Consultation Search</h2>
      </div>

      <div class="field-group">
        <label for="consultation-search-page">Patient or diagnosis</label>
        <input id="consultation-search-page" v-model="consultationQuery" class="form-control" type="search" maxlength="200" placeholder="Search patient name or diagnosis code" />
      </div>

      <div class="results-toolbar" v-if="consultationResults.length || consultationQuery.trim()">
        <span>{{ consultationPageLabel }}</span>
        <div class="page-actions">
          <button class="page-button" type="button" :disabled="consultationPage === 1 || consultationLoading" @click="loadConsultationPage(Math.max(1, consultationPage - 1))">Prev</button>
          <span class="page-number">Page {{ consultationPage }}</span>
          <button class="page-button" type="button" :disabled="!consultationHasMore || consultationLoading" @click="loadConsultationPage(consultationPage + 1)">Next</button>
        </div>
      </div>

      <div v-if="consultationLoading" class="state-panel state-panel--compact">Loading all consultation records…</div>
      <div v-else-if="consultationError" class="state-panel state-panel--compact state-panel--error">{{ consultationError }}</div>

      <div v-else-if="consultationResults.length" class="table-wrap">
        <table class="data-table data-table--compact">
          <thead>
            <tr>
              <th>Patient</th>
              <th>Date</th>
              <th>Diagnosis</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="consultation in consultationResults" :key="consultation.id">
              <td>{{ consultation.patient_name }}</td>
              <td>{{ formatDateTime(consultation.consultation_date) }}</td>
              <td>
                <div class="code-stack">
                  <span v-for="diagnosis in consultation.diagnoses.slice(0, 2)" :key="`${consultation.id}-${diagnosis.code}`" class="diagnosis-code">
                    {{ diagnosis.code }}
                  </span>
                </div>
              </td>
              <td class="notes-cell">{{ consultation.treatment_notes }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else-if="consultationReady && !consultationResults.length" class="state-panel state-panel--compact">No consultation results found.</div>
    </section>
  </div>
</template>

<style scoped>
.results-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin: 12px 0 16px;
  color: #4b5563;
  font-size: 0.9rem;
}

.page-actions {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.page-button {
  border: 1px solid #cfd8dc;
  background: #fff;
  color: #1f2937;
  border-radius: 8px;
  padding: 6px 10px;
  cursor: pointer;
}

.page-button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.page-number {
  font-weight: 600;
  color: #1f2937;
}
</style>
