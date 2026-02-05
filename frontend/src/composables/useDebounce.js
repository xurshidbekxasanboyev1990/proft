import { ref, onMounted, onUnmounted } from 'vue'

/**
 * Debounce composable
 */
export function useDebounce(value, delay = 300) {
  const debouncedValue = ref(value.value)
  let timeout = null
  
  const updateValue = () => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      debouncedValue.value = value.value
    }, delay)
  }
  
  onMounted(() => {
    // Watch for changes
    updateValue()
  })
  
  onUnmounted(() => {
    clearTimeout(timeout)
  })
  
  return debouncedValue
}

/**
 * Create a debounced function
 */
export function useDebounceFn(fn, delay = 300) {
  let timeout = null
  
  const debouncedFn = (...args) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      fn(...args)
    }, delay)
  }
  
  const cancel = () => {
    clearTimeout(timeout)
  }
  
  onUnmounted(() => {
    cancel()
  })
  
  return { debouncedFn, cancel }
}
