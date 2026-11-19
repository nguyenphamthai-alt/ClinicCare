export const useAutocompleteDropdown = <T>(options: {
  getItems: () => T[]
  isSelectable?: (item: T) => boolean
  onSelect: (item: T) => void
  onOpen?: () => void
  moveOnOpenArrow?: boolean
}) => {
  const isOpen = ref(false)
  const activeIndex = ref(-1)
  const root = ref<HTMLElement | null>(null)

  const open = (loadSuggestions = true) => {
    isOpen.value = true
    activeIndex.value = -1
    if (loadSuggestions) options.onOpen?.()
  }

  const close = () => {
    isOpen.value = false
    activeIndex.value = -1
  }

  const moveActiveIndex = (direction: 1 | -1) => {
    const items = options.getItems()
    if (!items.length) return

    const isSelectable = options.isSelectable ?? (() => true)
    let next = activeIndex.value

    for (let step = 0; step < items.length; step += 1) {
      next = next < 0
        ? direction === 1 ? 0 : items.length - 1
        : (next + direction + items.length) % items.length
      if (isSelectable(items[next])) {
        activeIndex.value = next
        return
      }
    }
  }

  const selectActiveItem = () => {
    if (!isOpen.value || activeIndex.value < 0) return
    const item = options.getItems()[activeIndex.value]
    if (!item) return
    if (options.isSelectable && !options.isSelectable(item)) return
    close()
    options.onSelect(item)
  }

  const onKeydown = (event: KeyboardEvent) => {
    if (event.key === 'Escape') {
      event.preventDefault()
      event.stopPropagation()
      close()
      return
    }

    if (!isOpen.value && ['ArrowDown', 'ArrowUp'].includes(event.key)) {
      open()
      if (options.moveOnOpenArrow) {
        moveActiveIndex(event.key === 'ArrowDown' ? 1 : -1)
      }
      return
    }

    if (event.key === 'ArrowDown' && options.getItems().length) {
      event.preventDefault()
      moveActiveIndex(1)
    } else if (event.key === 'ArrowUp' && options.getItems().length) {
      event.preventDefault()
      moveActiveIndex(-1)
    } else if (event.key === 'Enter' && isOpen.value && activeIndex.value >= 0) {
      event.preventDefault()
      selectActiveItem()
    }
  }

  const onDocumentPointerDown = (event: PointerEvent) => {
    if (!root.value?.contains(event.target as Node)) close()
  }

  const onFocusOut = (event: FocusEvent) => {
    if (!root.value?.contains(event.relatedTarget as Node)) close()
  }

  onMounted(() => document.addEventListener('pointerdown', onDocumentPointerDown))
  onBeforeUnmount(() => document.removeEventListener('pointerdown', onDocumentPointerDown))

  return { isOpen, activeIndex, root, open, close, onKeydown, onFocusOut }
}
