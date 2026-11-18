<script setup lang="ts">
import type { Patient } from '~/types'
import { formatDate } from '~/utils/date'

const props = defineProps<{
  modelValue: string
  results: Patient[]
  selectedPatientName?: string | null
  loading: boolean
  searchError?: string | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  select: [patient: Patient]
}>()

const showQuickForm = ref(false)
const searchText = computed({
  get: () => props.modelValue,
  set: (value: string) => {
    showQuickForm.value = false
    emit('update:modelValue', value)
  }
})

const noResults = computed(() =>
  !props.loading && !props.searchError && !props.selectedPatientName && props.modelValue.trim() && !props.results.length
)

const selectCreatedPatient = (patient: Patient) => {
  showQuickForm.value = false
  emit('select', patient)
}
</script>

<template>
  <div class="field-group">
    <label for="patient-search">Patient</label>
    <div class="patient-search-row">
      <input
        id="patient-search"
        v-model="searchText"
        class="form-control"
        type="text"
        autocomplete="off"
        maxlength="100"
        placeholder="Search patient by name"
      />
      <button class="secondary-button patient-add-new-button" type="button" @click="showQuickForm = true">
        <span aria-hidden="true">＋</span>
        Add new patient
      </button>
    </div>

    <div v-if="props.selectedPatientName" class="selected-patient">Selected patient: <strong>{{ props.selectedPatientName }}</strong></div>
    <div v-else-if="props.loading" class="helper-text">Searching patients…</div>
    <div v-else-if="props.searchError" class="state-panel state-panel--compact state-panel--error" role="alert">{{ props.searchError }}</div>
    <div v-else-if="noResults" class="patient-no-results-group">
      <div v-if="!showQuickForm" class="patient-no-results">
        <span>No patient found.</span>
      </div>

      <PatientQuickForm
        v-if="showQuickForm"
        :initial-name="props.modelValue.trim()"
        @created="selectCreatedPatient"
        @cancel="showQuickForm = false"
      />
    </div>

    <PatientQuickForm
      v-if="showQuickForm && !noResults"
      :initial-name="props.modelValue.trim()"
      @created="selectCreatedPatient"
      @cancel="showQuickForm = false"
    />

    <ul v-if="props.results.length && props.modelValue.trim()" class="search-results">
      <li
        v-for="patient in props.results"
        :key="patient.id"
        class="search-result"
        @click="$emit('select', patient)"
      >
        <div>
          <strong>{{ patient.full_name }}<template v-if="patient.date_of_birth"> · {{ formatDate(patient.date_of_birth) }}</template></strong>
          <small>{{ patient.sex }}</small>
        </div>
      </li>
    </ul>

  </div>
</template>

<style scoped>
.patient-search-row {
  display: flex;
  align-items: stretch;
  gap: 10px;
}

.patient-search-row .form-control {
  min-width: 0;
  flex: 1;
}

.patient-add-new-button {
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 0.65rem 0.9rem;
  white-space: nowrap;
  font-size: 0.86rem;
}

.patient-no-results {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--muted);
  font-size: 0.82rem;
  text-align: left;
}

.patient-no-results-group {
  display: grid;
  gap: 12px;
}

@media (max-width: 640px) {
  .patient-search-row {
    align-items: stretch;
    flex-direction: column;
  }

  .patient-add-new-button {
    width: 100%;
  }
}
</style>
