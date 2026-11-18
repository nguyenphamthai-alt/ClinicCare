<script setup lang="ts">
const route = useRoute()
</script>

<template>
  <div class="app-shell">
    <AppSidebar />

    <main class="main-panel">
      <AppHeader :title="String(route.meta.title ?? '')" :subtitle="String(route.meta.subtitle ?? '')" />
      <slot />
    </main>
  </div>
</template>
