<script setup lang="ts">
import type { Patient } from '~/types'

const props = defineProps<{
  modelValue: string
  results: Patient[]
  selectedPatientName?: string | null
  loading: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  select: [patient: Patient]
}>()

const searchText = computed({
  get: () => props.modelValue,
  set: (value: string) => emit('update:modelValue', value)
})

const formatDob = (value?: string | null) => {
  if (!value) return 'DOB not provided'
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleDateString('en-GB', { dateStyle: 'medium' })
}
</script>

<template>
  <div class="field-group">
    <label for="patient-search">Patient</label>
    <input
      id="patient-search"
      v-model="searchText"
      class="form-control"
      type="text"
      maxlength="100"
      placeholder="Search patient by name"
    />

    <div v-if="props.selectedPatientName" class="selected-patient">Selected patient: <strong>{{ props.selectedPatientName }}</strong></div>
    <div v-else-if="props.loading" class="helper-text">Searching patients…</div>

    <ul v-if="props.results.length && props.modelValue.trim()" class="search-results">
      <li
        v-for="patient in props.results"
        :key="patient.id"
        class="search-result"
        @click="$emit('select', patient)"
      >
        <div>
          <strong>{{ patient.full_name }}</strong>
          <small>{{ patient.sex }} • {{ formatDob(patient.date_of_birth) }}</small>
        </div>
      </li>
    </ul>
  </div>
</template>
