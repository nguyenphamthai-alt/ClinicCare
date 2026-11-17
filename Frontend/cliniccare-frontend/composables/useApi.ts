import { useRuntimeConfig } from '#imports'

export const useApi = () => {
  const runtimeConfig = useRuntimeConfig()
  const baseURL = (runtimeConfig.public.apiBase as string | undefined) ?? 'http://localhost:8000'

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
      const message =
        typeof payload === 'object' && payload !== null && 'detail' in payload
          ? String(payload.detail)
          : typeof payload === 'string' && payload
            ? payload
            : 'Session expired. Please log in again.'
      throw new Error(message)
    }

    return payload as { access_token: string; refresh_token: string; token_type?: string; full_name?: string | null }
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
      try {
        await refreshSession()
        return request<T>(path, options, false)
      } catch (error) {
        throw error
      }
    }

    const contentType = response.headers.get('content-type') || ''
    const payload = contentType.includes('application/json') ? await response.json() : await response.text()

    if (!response.ok) {
      const message =
        typeof payload === 'object' && payload !== null && 'detail' in payload
          ? String(payload.detail)
          : typeof payload === 'string' && payload
            ? payload
            : 'Request failed'
      throw new Error(message)
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
