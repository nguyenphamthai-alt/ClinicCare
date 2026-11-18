<script setup lang="ts">
import type { Consultation } from '~/types'
import { formatDate } from '~/utils/date'

const props = defineProps<{
  consultations: Consultation[]
  loading: boolean
  error: string | null
}>()

</script>

<template>
  <section class="card table-card">
    <div v-if="props.loading" class="state-panel">Loading consultation records…</div>
    <div v-else-if="props.error" class="state-panel state-panel--error">{{ props.error }}</div>
    <div v-else-if="!props.consultations.length" class="state-panel">No consultations found for this selection.</div>

    <div v-else class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>Patient</th>
            <th>Date</th>
            <th>Diagnosis</th>
            <th>Treatment notes</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="consultation in props.consultations" :key="consultation.id">
            <td>
              <div class="patient-cell">
                <strong>{{ consultation.patient_name }}</strong>
                <small>{{ consultation.doctor_name }}</small>
              </div>
            </td>
            <td>{{ formatDate(consultation.consultation_date) }}</td>
            <td>
              <div class="code-stack">
                <span v-for="diagnosis in consultation.diagnoses" :key="`${consultation.id}-${diagnosis.code}`" class="diagnosis-code">
                  {{ diagnosis.code }}
                </span>
              </div>
            </td>
            <td class="notes-cell">{{ consultation.treatment_notes }}</td>
            <td>
              <span :class="['status-badge', `status-badge--${consultation.status}`]">{{ consultation.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
