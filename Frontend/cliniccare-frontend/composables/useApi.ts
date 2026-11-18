import { useRuntimeConfig } from '#imports'
import type { AuthResponse } from '~/types'

const getErrorMessage = (payload: unknown, fallback: string) => {
  if (typeof payload === 'string' && payload) return payload
  if (typeof payload !== 'object' || payload === null || !('detail' in payload)) return fallback

  const detail = payload.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((item) => {
      if (typeof item === 'object' && item !== null && 'msg' in item) return String(item.msg)
      return String(item)
    }).join('; ')
  }
  return fallback
}

const getBaseURL = (configuredBaseURL: string | undefined) => {
  const baseURL = configuredBaseURL ?? 'http://localhost:8000'
  if (typeof window === 'undefined') return baseURL

  const url = new URL(baseURL)
  const loopbackHosts = new Set(['localhost', '127.0.0.1', '[::1]'])

  if (loopbackHosts.has(url.hostname) && loopbackHosts.has(window.location.hostname)) {
    url.hostname = window.location.hostname
  }

  return url.toString().replace(/\/$/, '')
}

export const useApi = () => {
  const runtimeConfig = useRuntimeConfig()
  const baseURL = getBaseURL(runtimeConfig.public.apiBase as string | undefined)

  const refreshSession = async () => {
    const response = await fetch(`${baseURL}/auth/refresh`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    const contentType = response.headers.get('content-type') || ''
    const payload = contentType.includes('application/json') ? await response.json() : await response.text()

    if (!response.ok) {
      throw new Error(getErrorMessage(payload, 'Session expired. Please log in again.'))
    }

    return payload as AuthResponse
  }

  const request = async <T>(path: string, options: RequestInit & { params?: Record<string, any> } = {}, retry = true): Promise<T> => {
    const headers = new Headers(options.headers || {})
    const url = new URL(`${baseURL}${path.startsWith('/') ? path : `/${path}`}`)

    Object.entries(options.params ?? {}).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.append(key, String(value))
      }
    })

    const response = await fetch(url.toString(), {
      ...options,
      headers,
      credentials: 'include'
    })

    if (response.status === 401 && retry && path !== '/auth/login' && path !== '/auth/refresh' && path !== '/auth/me') {
      await refreshSession()
      return request<T>(path, options, false)
    }

    const contentType = response.headers.get('content-type') || ''
    const payload = contentType.includes('application/json') ? await response.json() : await response.text()

    if (!response.ok) {
      throw new Error(getErrorMessage(payload, 'Request failed'))
    }

    return (payload ?? null) as T
  }

  return {
    baseURL,
    refreshSession,
    request,
    get: <T>(path: string, params?: Record<string, any>) => request<T>(path, { method: 'GET', params }),
    post: <T>(path: string, body?: Record<string, any> | FormData, headers?: HeadersInit) => {
      const requestHeaders = new Headers(headers || {})
      if (!(body instanceof FormData) && !requestHeaders.has('Content-Type')) {
        requestHeaders.set('Content-Type', 'application/json')
      }

      return request<T>(path, {
        method: 'POST',
        headers: requestHeaders,
        body: body instanceof FormData ? body : JSON.stringify(body ?? {})
      })
    }
  }
}
