<script setup lang="ts">
import type { Consultation } from '~/types'

definePageMeta({ middleware: 'auth' })

const api = useApi()
const consultations = ref<Consultation[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const searchTerm = ref('')

const filteredConsultations = computed(() => {
  const term = searchTerm.value.trim().toLowerCase()

  if (!term) return consultations.value

  return consultations.value.filter((consultation) => {
    const patientMatch = consultation.patient_name.toLowerCase().includes(term)
    const treatmentMatch = consultation.treatment_notes.toLowerCase().includes(term)
    const diagnosisMatch = consultation.diagnoses.some((diagnosis) =>
      diagnosis.code.toLowerCase().includes(term) || diagnosis.description.toLowerCase().includes(term)
    )

    return patientMatch || treatmentMatch || diagnosisMatch
  })
})

const loadConsultations = async () => {
  loading.value = true
  error.value = null

  try {
    consultations.value = await api.get<Consultation[]>('/consultation', {
      limit: 50,
      offset: 0
    })
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unable to load consultation records.'
    consultations.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadConsultations()
})
</script>

<template>
  <div class="app-shell">
    <AppSidebar />

    <main class="main-panel">
      <AppHeader title="Consultations" subtitle="Review completed and pending patient visits." />

      <div class="page-content">
        <div class="toolbar">
          <div class="search-box">
            <input v-model="searchTerm" type="search" placeholder="Search patient or diagnosis" />
          </div>

          <NuxtLink to="/consultations/new" class="primary-button primary-button--inline">New Consultation</NuxtLink>
        </div>

        <ConsultationTable :consultations="filteredConsultations" :loading="loading" :error="error" />
      </div>
    </main>
  </div>
</template>
