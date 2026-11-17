<script setup lang="ts">
import type { DiagnosisItem } from '~/types'

const props = defineProps<{
  modelValue: string
  results: DiagnosisItem[]
  selectedCodes: string[]
  loading: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  select: [item: DiagnosisItem]
  remove: [code: string]
}>()

const searchText = computed({
  get: () => props.modelValue,
  set: (value: string) => emit('update:modelValue', value)
})
</script>

<template>
  <div class="field-group">
    <label for="diagnosis-search">Diagnosis search</label>
    <input
      id="diagnosis-search"
      v-model="searchText"
      class="form-control"
      type="text"
      placeholder="Search by code or description"
    />

    <div v-if="props.loading" class="helper-text">Looking up diagnosis codes…</div>

    <ul v-if="props.results.length && props.modelValue.trim()" class="search-results">
      <li
        v-for="item in props.results"
        :key="item.code"
        class="search-result"
        @click="$emit('select', item)"
      >
        <span class="diagnosis-code diagnosis-code--large">{{ item.code }}</span>
        <span>{{ item.description }}</span>
      </li>
    </ul>

    <div v-if="props.selectedCodes.length" class="tag-list">
      <button
        v-for="code in props.selectedCodes"
        :key="code"
        type="button"
        class="tag"
        @click="$emit('remove', code)"
      >
        {{ code }}
        <span>×</span>
      </button>
    </div>
  </div>
</template>
