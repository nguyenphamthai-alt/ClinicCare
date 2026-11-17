<script setup lang="ts">
import type { Consultation, DiagnosisItem } from '~/types'

definePageMeta({ middleware: 'auth' })

const api = useApi()

const diagnosisQuery = ref('')
const diagnosisResults = ref<DiagnosisItem[]>([])
const diagnosisLoading = ref(false)
const diagnosisError = ref<string | null>(null)
const diagnosisPage = ref(1)
const diagnosisPageSize = 10
const diagnosisHasMore = ref(true)
const diagnosisReady = ref(false)

const consultationQuery = ref('')
const consultationResults = ref<Consultation[]>([])
const consultationLoading = ref(false)
const consultationError = ref<string | null>(null)
const consultationPage = ref(1)
const consultationPageSize = 10
const consultationHasMore = ref(true)
const consultationReady = ref(false)

const formatDate = (value: string) => new Date(value).toLocaleString('en-GB', {
  dateStyle: 'medium',
  timeStyle: 'short'
})

const fetchDiagnosisResults = async (search = diagnosisQuery.value, page = diagnosisPage.value) => {
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

    const hasMore = rows.length > diagnosisPageSize
    diagnosisResults.value = hasMore ? rows.slice(0, diagnosisPageSize) : rows
    diagnosisHasMore.value = hasMore

    if (!diagnosisResults.value.length && page > 1) {
      diagnosisPage.value = Math.max(1, page - 1)
      return
    }

    diagnosisPage.value = page
    diagnosisReady.value = true
  } catch (error) {
    diagnosisError.value = error instanceof Error ? error.message : 'Diagnosis search failed.'
    diagnosisResults.value = []
    diagnosisHasMore.value = false
    diagnosisReady.value = true
  } finally {
    diagnosisLoading.value = false
  }
}

const fetchConsultationResults = async (search = consultationQuery.value, page = consultationPage.value) => {
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

    const hasMore = rows.length > consultationPageSize
    consultationResults.value = hasMore ? rows.slice(0, consultationPageSize) : rows
    consultationHasMore.value = hasMore

    if (!consultationResults.value.length && page > 1) {
      consultationPage.value = Math.max(1, page - 1)
      return
    }

    consultationPage.value = page
    consultationReady.value = true
  } catch (error) {
    consultationError.value = error instanceof Error ? error.message : 'Consultation search failed.'
    consultationResults.value = []
    consultationHasMore.value = false
    consultationReady.value = true
  } finally {
    consultationLoading.value = false
  }
}

watch(diagnosisQuery, async (value) => {
  diagnosisPage.value = 1
  await fetchDiagnosisResults(value, 1)
})

watch(consultationQuery, async (value) => {
  consultationPage.value = 1
  await fetchConsultationResults(value, 1)
})

onMounted(async () => {
  await fetchDiagnosisResults('', 1)
  await fetchConsultationResults('', 1)
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
  <div class="app-shell">
    <AppSidebar />

    <main class="main-panel">
      <AppHeader title="Search" subtitle="Locate diagnoses and consultation history quickly." />

      <div class="page-content search-page">
        <section class="card search-card">
          <div class="section-header">
            <h2>Diagnosis Search</h2>
          </div>

          <div class="field-group">
            <label for="diagnosis-search-page">ICD-10 or description</label>
            <input id="diagnosis-search-page" v-model="diagnosisQuery" class="form-control" type="search" placeholder="Search diagnosis code or description" />
          </div>

          <div class="results-toolbar" v-if="diagnosisResults.length || diagnosisQuery.trim()">
            <span>{{ diagnosisPageLabel }}</span>
            <div class="page-actions">
              <button class="page-button" type="button" :disabled="diagnosisPage === 1" @click="fetchDiagnosisResults(diagnosisQuery, Math.max(1, diagnosisPage - 1))">Prev</button>
              <span class="page-number">Page {{ diagnosisPage }}</span>
              <button class="page-button" type="button" :disabled="!diagnosisHasMore" @click="fetchDiagnosisResults(diagnosisQuery, diagnosisPage + 1)">Next</button>
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
            <input id="consultation-search-page" v-model="consultationQuery" class="form-control" type="search" placeholder="Search patient name or diagnosis code" />
          </div>

          <div class="results-toolbar" v-if="consultationResults.length || consultationQuery.trim()">
            <span>{{ consultationPageLabel }}</span>
            <div class="page-actions">
              <button class="page-button" type="button" :disabled="consultationPage === 1" @click="fetchConsultationResults(consultationQuery, Math.max(1, consultationPage - 1))">Prev</button>
              <span class="page-number">Page {{ consultationPage }}</span>
              <button class="page-button" type="button" :disabled="!consultationHasMore" @click="fetchConsultationResults(consultationQuery, consultationPage + 1)">Next</button>
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
                  <td>{{ formatDate(consultation.consultation_date) }}</td>
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
    </main>
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
