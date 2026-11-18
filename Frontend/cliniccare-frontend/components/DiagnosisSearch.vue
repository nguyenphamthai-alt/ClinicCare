<script setup lang="ts">
import type { DiagnosisItem } from '~/types'

const props = defineProps<{
  modelValue: string
  results: DiagnosisItem[]
  selectedCodes: string[]
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

const isOpen = ref(false)
const activeIndex = ref(-1)
const root = ref<HTMLElement | null>(null)
const searchText = computed({
  get: () => props.modelValue,
  set: (value: string) => {
    isOpen.value = true
    activeIndex.value = -1
    emit('update:modelValue', value)
  }
})

const selectionLimit = computed(() => props.maxSelections ?? 10)
const selectionLimitReached = computed(() => props.selectedCodes.length >= selectionLimit.value)
const isSelected = (code: string) => props.selectedCodes.includes(code)
const isSelectable = (item: DiagnosisItem) => !selectionLimitReached.value && !isSelected(item.code)

const selectItem = (item: DiagnosisItem) => {
  if (!isSelectable(item)) return
  isOpen.value = false
  activeIndex.value = -1
  emit('select', item)
}

const moveActiveIndex = (direction: 1 | -1) => {
  const count = props.results.length
  if (!count) return

  let next = activeIndex.value
  for (let step = 0; step < count; step += 1) {
    next = next < 0
      ? direction === 1 ? 0 : count - 1
      : (next + direction + count) % count
    if (isSelectable(props.results[next])) {
      activeIndex.value = next
      return
    }
  }
}

const openSuggestions = () => {
  isOpen.value = true
  activeIndex.value = -1
  emit('focus')
}

const onKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    event.preventDefault()
    event.stopPropagation()
    isOpen.value = false
    activeIndex.value = -1
    return
  }
  if (!isOpen.value && ['ArrowDown', 'ArrowUp'].includes(event.key)) {
    openSuggestions()
  }
  if (event.key === 'ArrowDown' && props.results.length) {
    event.preventDefault()
    moveActiveIndex(1)
  } else if (event.key === 'ArrowUp' && props.results.length) {
    event.preventDefault()
    moveActiveIndex(-1)
  } else if (event.key === 'Enter' && isOpen.value && activeIndex.value >= 0) {
    event.preventDefault()
    selectItem(props.results[activeIndex.value])
  }
}

const onDocumentPointerDown = (event: PointerEvent) => {
  if (!root.value?.contains(event.target as Node)) isOpen.value = false
}

const onFocusOut = (event: FocusEvent) => {
  if (!root.value?.contains(event.relatedTarget as Node)) isOpen.value = false
}

onMounted(() => document.addEventListener('pointerdown', onDocumentPointerDown))
onBeforeUnmount(() => document.removeEventListener('pointerdown', onDocumentPointerDown))
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
        {{ code }}
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
