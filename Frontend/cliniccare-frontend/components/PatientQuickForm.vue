<script setup lang="ts">
import type { Patient } from '~/types'

const props = defineProps<{ initialName: string }>()
const emit = defineEmits<{
  created: [patient: Patient]
  cancel: []
}>()

const api = useApi()
const nameInput = ref<HTMLInputElement | null>(null)
const form = reactive({ full_name: props.initialName, sex: '' as '' | 'Male' | 'Female', date_of_birth: '' })
const error = ref('')
const submitting = ref(false)
const today = new Date()
const maxDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
const errorId = 'patient-create-error'

onMounted(() => nameInput.value?.focus())

const save = async () => {
  if (submitting.value) return
  error.value = ''

  if (!form.full_name.trim()) error.value = 'Full name is required.'
  else if (!form.sex) error.value = 'Select a sex.'
  else if (form.date_of_birth && form.date_of_birth > maxDate) error.value = 'Date of birth cannot be in the future.'
  if (error.value) return

  submitting.value = true
  try {
    const patient = await api.post<Patient>('/patients', {
      full_name: form.full_name.trim(),
      sex: form.sex,
      date_of_birth: form.date_of_birth || null
    })
    emit('created', patient)
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : 'Unable to create patient.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section class="quick-patient-card" role="group" aria-labelledby="patient-create-heading" @keydown.esc.prevent="emit('cancel')">
    <header class="quick-patient-header">
      <strong id="patient-create-heading">New patient</strong>
      <button class="quick-patient-close" type="button" aria-label="Cancel" @click="emit('cancel')">✕</button>
    </header>

    <div class="quick-patient-fields" @keydown.enter.prevent="save">
      <div class="field-group">
        <label for="patient-create-name">Full name</label>
        <input
          id="patient-create-name"
          ref="nameInput"
          v-model="form.full_name"
          class="form-control"
          type="text"
          maxlength="100"
          required
          :aria-describedby="error ? errorId : undefined"
          :aria-invalid="Boolean(error)"
        />
      </div>

      <fieldset class="quick-patient-sex" :aria-describedby="error ? errorId : undefined" :aria-invalid="Boolean(error)">
        <legend>Sex</legend>
        <div class="quick-patient-segmented">
          <div class="quick-patient-option">
            <input id="patient-create-male" v-model="form.sex" type="radio" name="patient-sex" value="Male" required />
            <label for="patient-create-male">Male</label>
          </div>
          <div class="quick-patient-option">
            <input id="patient-create-female" v-model="form.sex" type="radio" name="patient-sex" value="Female" required />
            <label for="patient-create-female">Female</label>
          </div>
        </div>
      </fieldset>

      <div class="field-group">
        <label for="patient-create-dob">Date of birth <small>(optional)</small></label>
        <input
          id="patient-create-dob"
          v-model="form.date_of_birth"
          class="form-control"
          type="date"
          :max="maxDate"
          :aria-describedby="error ? errorId : undefined"
          :aria-invalid="Boolean(error)"
        />
      </div>
    </div>

    <div v-if="error" :id="errorId" class="form-message form-message--error quick-patient-error" role="alert">{{ error }}</div>

    <div class="form-actions quick-patient-actions">
      <button class="secondary-button" type="button" @click="emit('cancel')">Cancel</button>
      <button class="primary-button" type="button" :disabled="submitting" @click="save">
        {{ submitting ? 'Saving…' : 'Save patient' }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.quick-patient-card {
  --quick-patient-accent: #2f6b73;
  --quick-patient-border: #dbe7e8;
  --quick-patient-background: #f6fafa;
  padding: 16px 20px;
  border: 1px solid var(--quick-patient-border);
  border-left: 4px solid var(--quick-patient-accent);
  border-radius: 10px;
  background: var(--quick-patient-background);
}

.quick-patient-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.quick-patient-close {
  padding: 2px 6px;
  border: 0;
  background: transparent;
  color: var(--muted);
  font-size: 0.9rem;
}

.quick-patient-close:hover {
  color: var(--text);
}

.quick-patient-close:focus-visible,
.quick-patient-option input:focus-visible + label {
  outline: 2px solid var(--quick-patient-accent);
  outline-offset: 2px;
}

.quick-patient-fields {
  display: grid;
  grid-template-columns: 2fr 1.2fr 1fr;
  align-items: end;
  gap: 16px;
}

.quick-patient-fields .field-group {
  gap: 6px;
}

.quick-patient-card label,
.quick-patient-sex legend {
  font-size: 0.8rem;
  font-weight: 600;
}

.quick-patient-sex {
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;
}

.quick-patient-sex legend {
  margin-bottom: 6px;
  padding: 0;
}

.quick-patient-card label small {
  color: var(--muted);
  font-size: 0.75rem;
  font-weight: 400;
}

.quick-patient-segmented {
  display: flex;
  min-height: 44px;
}

.quick-patient-option {
  position: relative;
  flex: 1;
}

.quick-patient-option input {
  position: absolute;
  width: 1px;
  height: 1px;
  opacity: 0;
}

.quick-patient-option label {
  display: flex;
  height: 100%;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--quick-patient-border);
  background: #fff;
  color: var(--text);
  cursor: pointer;
}

.quick-patient-option:first-child label {
  border-radius: 8px 0 0 8px;
}

.quick-patient-option:last-child label {
  border-left: 0;
  border-radius: 0 8px 8px 0;
}

.quick-patient-option input:checked + label {
  border-color: var(--quick-patient-accent);
  background: var(--quick-patient-accent);
  color: #fff;
}

.quick-patient-actions {
  gap: 8px;
  margin-top: 16px;
}

.quick-patient-error {
  margin-top: 12px;
  color: #b42318;
  font-size: 0.85rem;
}

@media (max-width: 720px) {
  .quick-patient-fields {
    grid-template-columns: 1fr;
  }
}
</style>
