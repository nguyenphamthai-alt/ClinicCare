<script setup lang="ts">
import type { DiagnosisItem } from '~/types'
import { useAutocompleteDropdown } from '~/composables/useAutocompleteDropdown'

const props = defineProps<{
  modelValue: string
  results: DiagnosisItem[]
  selectedCodes: string[]
  selectedDescriptions?: Record<string, string>
  loading: boolean
  searchError?: string | null
  maxSelections?: number
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
  select: [item: DiagnosisItem]
  remove: [code: string]
  focus: []
}>()

const selectionLimit = computed(() => props.maxSelections ?? 10)
const selectionLimitReached = computed(() => props.selectedCodes.length >= selectionLimit.value)
const isSelected = (code: string) => props.selectedCodes.includes(code)
const isSelectable = (item: DiagnosisItem) => !selectionLimitReached.value && !isSelected(item.code)

const dropdown = useAutocompleteDropdown<DiagnosisItem>({
  getItems: () => props.results,
  isSelectable,
  moveOnOpenArrow: true,
  onSelect: (item) => emit('select', item),
  onOpen: () => emit('focus')
})
const { isOpen, activeIndex, root, open, close, onKeydown, onFocusOut } = dropdown

const searchText = computed({
  get: () => props.modelValue,
  set: (value: string) => {
    open(false)
    emit('update:modelValue', value)
  }
})

const selectItem = (item: DiagnosisItem) => {
  if (!isSelectable(item)) return
  close()
  emit('select', item)
}

const openSuggestions = () => open()
</script>

<template>
  <div class="field-group">
    <label for="diagnosis-search">Diagnosis search</label>
    <div ref="root" class="diagnosis-input-wrap" @focusout="onFocusOut">
      <input
        id="diagnosis-search"
        v-model="searchText"
        class="form-control"
        type="text"
        autocomplete="off"
        maxlength="100"
        placeholder="Search by code or description"
        role="combobox"
        aria-autocomplete="list"
        :aria-expanded="isOpen"
        aria-controls="diagnosis-search-results"
        :aria-activedescendant="activeIndex >= 0 ? `diagnosis-option-${activeIndex}` : undefined"
        @focus="openSuggestions"
        @click="openSuggestions"
        @keydown="onKeydown"
      />

      <div v-if="isOpen" id="diagnosis-search-results" class="autocomplete-results" role="listbox">
        <div v-if="props.loading" class="autocomplete-state">Looking up diagnosis codes…</div>
        <div v-else-if="props.searchError" class="autocomplete-state autocomplete-state--error" role="alert">{{ props.searchError }}</div>
        <template v-else-if="props.results.length">
          <button
            v-for="(item, index) in props.results"
            :id="`diagnosis-option-${index}`"
            :key="item.code"
            class="autocomplete-option"
            :class="{
              'autocomplete-option--active': index === activeIndex,
              'autocomplete-option--added': isSelected(item.code)
            }"
            type="button"
            role="option"
            :aria-selected="index === activeIndex"
            :aria-disabled="!isSelectable(item)"
            :disabled="!isSelectable(item)"
            @mouseenter="isSelectable(item) && (activeIndex = index)"
            @click="selectItem(item)"
          >
            <span class="diagnosis-code diagnosis-code--large">{{ item.code }}</span>
            <span class="autocomplete-description">{{ item.description }}</span>
            <span v-if="isSelected(item.code)" class="diagnosis-added-badge">Added</span>
          </button>
          <div v-if="selectionLimitReached" class="autocomplete-state autocomplete-state--warning" role="status">
            Maximum of {{ selectionLimit }} diagnosis codes selected. Remove one to add another.
          </div>
        </template>
        <div v-else class="autocomplete-state">No diagnosis found.</div>
      </div>
    </div>

    <div v-if="selectionLimitReached" class="diagnosis-limit-message" role="status">
      {{ selectedCodes.length }}/{{ selectionLimit }} diagnoses selected. Remove one to add another.
    </div>

    <div v-if="props.selectedCodes.length" class="tag-list">
      <button
        v-for="code in props.selectedCodes"
        :key="code"
        type="button"
        class="tag"
        @click="$emit('remove', code)"
      >
        {{ code }}<template v-if="props.selectedDescriptions?.[code]"> - {{ props.selectedDescriptions[code] }}</template>
        <span>×</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.diagnosis-input-wrap {
  position: relative;
  z-index: 30;
}

.autocomplete-description {
  min-width: 0;
  flex: 1;
  text-align: left;
}

.autocomplete-option--added {
  background: var(--surface-alt);
  cursor: not-allowed;
  opacity: 0.82;
}

.diagnosis-added-badge {
  flex: 0 0 auto;
  padding: 0.2rem 0.5rem;
  border: 1px solid rgba(40, 124, 131, 0.2);
  border-radius: 999px;
  background: var(--secondary);
  color: var(--primary);
  font-size: 0.72rem;
  font-weight: 700;
}

.diagnosis-limit-message {
  color: var(--warning);
  font-size: 0.82rem;
}
</style>
