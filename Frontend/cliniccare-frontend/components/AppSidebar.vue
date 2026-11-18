<script setup lang="ts">
const route = useRoute()
const { logout, fullName } = useAuth()
const clientReady = ref(false)
onMounted(() => { clientReady.value = true })

const navigation = [
  { label: 'Consultations', to: '/consultations', icon: '🗂️' },
  { label: 'New Consultation', to: '/consultations/new', icon: '➕' },
  { label: 'Diagnosis Search', to: '/search', icon: '🔎' }
]

const isActive = (path: string) => route.path === path || (path !== '/consultations' && route.path.startsWith(path))
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-brand">
      <div class="brand-mark">CC</div>
      <div>
        <strong>ClinicCare</strong>
        <small>Mini EMR</small>
      </div>
    </div>

    <nav class="sidebar-nav" aria-label="Primary navigation">
      <NuxtLink
        v-for="item in navigation"
        :key="item.to"
        :to="item.to"
        :class="['nav-item', { 'nav-item--active': isActive(item.to) }]"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </NuxtLink>
    </nav>

    <div class="sidebar-footer">
      <div class="doctor-pill">
        <span class="doctor-pill__label">Doctor</span>
        <strong>{{ clientReady && fullName ? fullName : 'Doctor' }}</strong>
      </div>
      <button class="logout-button" type="button" @click="logout">Logout</button>
    </div>
  </aside>
</template>
