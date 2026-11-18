import { defineNuxtRouteMiddleware, navigateTo } from '#imports'
import { useAuth } from '~/composables/useAuth'

export default defineNuxtRouteMiddleware(async (to) => {
  const { initialized, isAuthenticated, hydrateSession } = useAuth()

  if (import.meta.server) return

  if (!initialized.value && to.path !== '/login') {
    const hasSession = await hydrateSession()
    if (!hasSession) return navigateTo('/login')
  }

  if (to.path === '/') {
    return navigateTo(isAuthenticated.value ? '/consultations' : '/login')
  }

  if (isAuthenticated.value && to.path === '/login') {
    return navigateTo('/consultations')
  }
})
