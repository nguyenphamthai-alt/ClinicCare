<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { isAuthenticated } = useAuth()

onMounted(() => {
  navigateTo(isAuthenticated.value ? '/consultations' : '/login')
})
</script>

<template>
  <div class="page-loading">Redirecting…</div>
</template>
