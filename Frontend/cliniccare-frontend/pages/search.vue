<script setup lang="ts">
import type { DiagnosisItem } from '~/types'

definePageMeta({
  middleware: 'auth',
  layout: 'app',
  title: 'Diagnosis Search',
  subtitle: 'Look up ICD-10 diagnosis codes and descriptions.'
})

const api = useApi()
const PAGE_SIZE = 10
const DEBOUNCE_MS = 300

const createPagedSearch = <T>(path: string, maxLength: number, failureMessage: string) => {
  const query = ref('')
  const results = ref<T[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const page = ref(1)
  const hasMore = ref(true)
  const ready = ref(false)
  let timer: ReturnType<typeof setTimeout> | undefined
  let request = 0

  const loadPage = async (requestedPage: number) => {
    if (timer) clearTimeout(timer)
    const currentRequest = ++request
    const term = query.value.trim()
    loading.value = true
    error.value = null
    ready.value = false

    try {
      let rows = await api.get<T[]>(path, {
        search: term || undefined,
        limit: PAGE_SIZE + 1,
        offset: (requestedPage - 1) * PAGE_SIZE
      })

      if (currentRequest !== request) return
      let resolvedPage = requestedPage
      let fellBack = false
      if (!rows.length && requestedPage > 1) {
        fellBack = true
        resolvedPage -= 1
        rows = await api.get<T[]>(path, {
          search: term || undefined,
          limit: PAGE_SIZE + 1,
          offset: (resolvedPage - 1) * PAGE_SIZE
        })
        if (currentRequest !== request) return
      }

      hasMore.value = !fellBack && rows.length > PAGE_SIZE
      results.value = rows.slice(0, PAGE_SIZE)
      page.value = resolvedPage
      ready.value = true
    } catch (cause) {
      if (currentRequest !== request) return
      error.value = cause instanceof Error ? cause.message : failureMessage
      results.value = []
      hasMore.value = false
      ready.value = true
    } finally {
      if (currentRequest === request) loading.value = false
    }
  }

  watch(query, (value) => {
    ++request
    if (timer) clearTimeout(timer)
    page.value = 1
    error.value = null
    const term = value.trim()

    if (term.length > maxLength) {
      results.value = []
      loading.value = false
      ready.value = true
      hasMore.value = false
      error.value = `Search must be ${maxLength} characters or fewer.`
      return
    }

    results.value = []
    loading.value = true
    ready.value = false
    timer = setTimeout(() => loadPage(1), DEBOUNCE_MS)
  }, { flush: 'sync' })

  const stop = () => {
    request += 1
    if (timer) clearTimeout(timer)
  }

  return { query, results, loading, error, page, hasMore, ready, loadPage, stop }
}

const diagnosis = createPagedSearch<DiagnosisItem>('/diagnosis', 100, 'Diagnosis search failed.')
const {
  query: diagnosisQuery,
  results: diagnosisResults,
  loading: diagnosisLoading,
  error: diagnosisError,
  page: diagnosisPage,
  hasMore: diagnosisHasMore,
  ready: diagnosisReady,
  loadPage: loadDiagnosisPage
} = diagnosis

onMounted(() => {
  loadDiagnosisPage(1)
})

onBeforeUnmount(() => {
  diagnosis.stop()
})

const pageLabel = (count: number) => count ? `Showing ${count} items` : 'No records'
const diagnosisPageLabel = computed(() => pageLabel(diagnosisResults.value.length))
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
  </div>
</template>
