<script setup lang="ts">
import type { Patient } from '~/types'
import { formatDate } from '~/utils/date'
import { useAutocompleteDropdown } from '~/composables/useAutocompleteDropdown'

const props = defineProps<{
  modelValue: string
  results: Patient[]
  selectedPatientName?: string | null
  loading: boolean
  searchError?: string | null
  searchComplete?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  select: [patient: Patient]
  focus: []
}>()

const showQuickForm = ref(false)
const dropdown = useAutocompleteDropdown<Patient>({
  getItems: () => props.results,
  onSelect: (patient) => emit('select', patient),
  onOpen: () => emit('focus')
})
const { isOpen, activeIndex, root, open, close, onKeydown, onFocusOut } = dropdown

const searchText = computed({
  get: () => props.modelValue,
  set: (value: string) => {
    showQuickForm.value = false
    open(false)
    emit('update:modelValue', value)
  }
})

const noResults = computed(() =>
  props.searchComplete && !props.loading && !props.searchError && !props.selectedPatientName && props.modelValue.trim() && !props.results.length
)

watch(() => props.selectedPatientName, (selectedName) => {
  if (selectedName) close()
})

const selectCreatedPatient = (patient: Patient) => {
  showQuickForm.value = false
  close()
  emit('select', patient)
}

const selectPatient = (patient: Patient) => {
  close()
  emit('select', patient)
}

const openSuggestions = () => {
  if (props.selectedPatientName) {
    close()
    return
  }
  open()
}

</script>

<template>
  <div class="field-group">
    <label for="patient-search">Patient</label>
    <div class="patient-search-row">
      <div ref="root" class="patient-input-wrap" @focusout="onFocusOut">
        <input
          id="patient-search"
          v-model="searchText"
          class="form-control"
          type="text"
          autocomplete="off"
          maxlength="100"
          placeholder="Search patient by name"
          role="combobox"
          aria-autocomplete="list"
          :aria-expanded="isOpen"
          aria-controls="patient-search-results"
          :aria-activedescendant="activeIndex >= 0 ? `patient-option-${activeIndex}` : undefined"
          @focus="openSuggestions"
          @click="openSuggestions"
          @keydown="onKeydown"
        />

        <div v-if="isOpen" id="patient-search-results" class="autocomplete-results" role="listbox">
          <div v-if="props.loading" class="autocomplete-state">Searching patients…</div>
          <div v-else-if="props.searchError" class="autocomplete-state autocomplete-state--error" role="alert">{{ props.searchError }}</div>
          <template v-else-if="props.results.length">
            <button
              v-for="(patient, index) in props.results"
              :id="`patient-option-${index}`"
              :key="patient.id"
              class="autocomplete-option"
              :class="{ 'autocomplete-option--active': index === activeIndex }"
              type="button"
              role="option"
              :aria-selected="index === activeIndex"
              @mouseenter="activeIndex = index"
              @click="selectPatient(patient)"
            >
              <span>
                <strong>{{ patient.full_name }}</strong>
                <small>{{ patient.sex }}</small>
              </span>
              <small v-if="patient.date_of_birth">{{ formatDate(patient.date_of_birth) }}</small>
            </button>
          </template>
          <div v-else-if="props.searchComplete" class="autocomplete-state">No patient found.</div>
        </div>
      </div>
      <button class="secondary-button patient-add-new-button" type="button" @click="showQuickForm = true">
        <span aria-hidden="true">＋</span>
        Add new patient
      </button>
    </div>

    <div v-if="props.selectedPatientName" class="selected-patient">Selected patient: <strong>{{ props.selectedPatientName }}</strong></div>
    <div v-else-if="noResults" class="patient-no-results-group">
      <div v-if="!showQuickForm" class="patient-no-results">
        <span>No patient found.</span>
      </div>
    </div>

    <PatientQuickForm
      v-if="showQuickForm"
      :initial-name="props.modelValue.trim()"
      @created="selectCreatedPatient"
      @cancel="showQuickForm = false"
    />
  </div>
</template>

<style scoped>
.patient-input-wrap {
  position: relative;
  min-width: 0;
  flex: 1;
}

.patient-search-row {
  display: flex;
  align-items: stretch;
  gap: 10px;
}

.patient-search-row .form-control {
  min-width: 0;
  width: 100%;
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
</style>
