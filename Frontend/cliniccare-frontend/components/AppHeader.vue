<script setup lang="ts">
defineProps<{ title: string; subtitle?: string }>()
</script>

<template>
  <header class="topbar">
    <div>
      <p class="eyebrow">ClinicCare</p>
      <h1>{{ title }}</h1>
      <p v-if="subtitle" class="subheading">{{ subtitle }}</p>
    </div>
  </header>
</template>
