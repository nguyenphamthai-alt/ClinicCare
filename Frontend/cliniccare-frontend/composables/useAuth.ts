import { computed, navigateTo } from '#imports'
import type { AuthResponse } from '~/types'
import { useApi } from '~/composables/useApi'

export const useAuth = () => {
  const api = useApi()
  const session = useState<{ isAuthenticated: boolean; fullName: string | null }>('cliniccare-session', () => ({
    isAuthenticated: false,
    fullName: null
  }))

  const isAuthenticated = computed(() => session.value.isAuthenticated)
  const fullName = computed(() => session.value.fullName)

  const clearSession = () => {
    session.value = { isAuthenticated: false, fullName: null }
  }

  const storeSession = (payload: AuthResponse, doctorUsername?: string, doctorFullName?: string | null) => {
    session.value = {
      isAuthenticated: true,
      fullName: doctorFullName ?? payload.full_name ?? doctorUsername ?? 'Doctor'
    }
  }

  const hydrateSession = async () => {
    try {
      const profile = await api.get<{ id: string; username: string; full_name?: string | null }>('/auth/me')
      session.value = {
        isAuthenticated: true,
        fullName: profile.full_name ?? profile.username ?? 'Doctor'
      }
      return true
    } catch (error) {
      clearSession()
      return false
    }
  }

  const refreshSession = async () => {
    const payload = await api.refreshSession()
    storeSession(payload, undefined, payload.full_name ?? session.value.fullName ?? undefined)
    return payload
  }

  const login = async (credentials: { username: string; password: string }) => {
    const payload = await api.post<AuthResponse>('/auth/login', credentials)
    storeSession(payload, credentials.username, payload.full_name ?? undefined)
    return payload
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout')
    } catch (error) {
      console.warn('Logout request failed:', error)
    } finally {
      clearSession()
      await navigateTo('/login')
    }
  }

  return {
    fullName,
    isAuthenticated,
    hydrateSession,
    login,
    logout,
    clearSession,
    storeSession,
    refreshSession
  }
}
