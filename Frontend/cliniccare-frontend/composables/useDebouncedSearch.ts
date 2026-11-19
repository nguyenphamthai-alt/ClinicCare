export const useDebouncedSearch = <T>(options: {
  path: string
  limit: number
  debounceMs?: number
  maxLength?: number
  failureMessage: string
  onQueryChange?: (value: string) => void
}) => {
  const api = useApi()
  const query = ref('')
  const results = ref<T[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const searchComplete = ref(false)

  const debounceMs = options.debounceMs ?? 250
  const maxLength = options.maxLength ?? 100
  let timer: ReturnType<typeof setTimeout> | undefined
  let request = 0
  let suppressQueryWatch = false

  const cancel = (clearResults = true) => {
    request += 1
    if (timer) clearTimeout(timer)
    timer = undefined
    loading.value = false
    error.value = null
    if (clearResults) results.value = []
  }

  const reset = (value = '', complete = false) => {
    suppressQueryWatch = true
    query.value = value
    suppressQueryWatch = false
    cancel()
    searchComplete.value = complete
  }

  const runSearch = async (term: string) => {
    const currentRequest = ++request
    if (timer) clearTimeout(timer)
    timer = undefined
    loading.value = true
    error.value = null
    searchComplete.value = false

    try {
      const rows = await api.get<T[]>(options.path, {
        search: term || undefined,
        limit: options.limit
      })
      if (currentRequest !== request) return
      results.value = rows
    } catch (cause) {
      if (currentRequest !== request) return
      results.value = []
      error.value = cause instanceof Error ? cause.message : options.failureMessage
    } finally {
      if (currentRequest === request) {
        loading.value = false
        searchComplete.value = !error.value
      }
    }
  }

  watch(query, (value) => {
    if (suppressQueryWatch) return

    request += 1
    if (timer) clearTimeout(timer)
    timer = undefined
    options.onQueryChange?.(value)

    const term = value.trim()
    searchComplete.value = false

    if (term.length > maxLength) {
      results.value = []
      loading.value = false
      error.value = null
      return
    }

    results.value = []
    loading.value = true
    error.value = null
    timer = setTimeout(() => runSearch(term), debounceMs)
  }, { flush: 'sync' })

  const loadSuggestions = async () => {
    if (loading.value || results.value.length) return
    const term = query.value.trim()
    if (term.length > maxLength) return
    await runSearch(term)
  }

  onBeforeUnmount(() => cancel())

  return {
    query,
    results,
    loading,
    error,
    searchComplete,
    loadSuggestions,
    reset
  }
}
