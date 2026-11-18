<script setup lang="ts">
import type { Consultation } from '~/types'

definePageMeta({
  middleware: 'auth',
  layout: 'app',
  title: 'Consultations',
  subtitle: 'Review completed and pending patient visits.'
})

const api = useApi()
const consultations = ref<Consultation[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const searchTerm = ref('')

const page = ref(1)
const pageSize = 10
const hasMore = ref(false)
let searchTimer: ReturnType<typeof setTimeout> | undefined
let requestSequence = 0

const loadConsultations = async (requestedPage = page.value) => {
  const sequence = ++requestSequence
  loading.value = true
  error.value = null

  try {
    const term = searchTerm.value.trim()
    const rows = await api.get<Consultation[]>('/consultation', {
      search: term || undefined,
      limit: pageSize + 1,
      offset: (requestedPage - 1) * pageSize
    })

    if (sequence !== requestSequence) return
    hasMore.value = rows.length > pageSize
    consultations.value = rows.slice(0, pageSize)
    page.value = requestedPage
  } catch (err) {
    if (sequence !== requestSequence) return
    error.value = err instanceof Error ? err.message : 'Unable to load consultation records.'
    consultations.value = []
    hasMore.value = false
  } finally {
    if (sequence === requestSequence) loading.value = false
  }
}

watch(searchTerm, () => {
  requestSequence += 1
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    page.value = 1
    loadConsultations(1)
  }, 300)
})

onMounted(() => {
  loadConsultations()
})

onBeforeUnmount(() => {
  requestSequence += 1
  if (searchTimer) clearTimeout(searchTimer)
})
</script>

<template>
  <div class="page-content">
    <div class="toolbar">
      <div class="search-box">
        <input v-model="searchTerm" type="search" maxlength="200" placeholder="Search patient or diagnosis" />
      </div>

      <NuxtLink to="/consultations/new" class="primary-button primary-button--inline">New Consultation</NuxtLink>
    </div>

    <ConsultationTable :consultations="consultations" :loading="loading" :error="error" />

    <div v-if="consultations.length || page > 1" class="consultation-pagination">
      <div class="page-actions">
        <button class="page-button" type="button" :disabled="page === 1 || loading" @click="loadConsultations(page - 1)">Prev</button>
        <span class="page-number">Page {{ page }}</span>
        <button class="page-button" type="button" :disabled="!hasMore || loading" @click="loadConsultations(page + 1)">Next</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.consultation-pagination {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin: 12px 0 16px;
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
