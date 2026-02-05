import { ref, computed } from 'vue'

/**
 * Toast notification composable
 */
export function useToast() {
  const toasts = ref([])
  let toastId = 0
  
  function show(message, type = 'info', duration = 3000) {
    const id = ++toastId
    
    toasts.value.push({
      id,
      message,
      type, // 'success', 'error', 'warning', 'info'
      duration
    })
    
    if (duration > 0) {
      setTimeout(() => {
        remove(id)
      }, duration)
    }
    
    return id
  }
  
  function success(message, duration) {
    return show(message, 'success', duration)
  }
  
  function error(message, duration) {
    return show(message, 'error', duration)
  }
  
  function warning(message, duration) {
    return show(message, 'warning', duration)
  }
  
  function info(message, duration) {
    return show(message, 'info', duration)
  }
  
  function remove(id) {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }
  
  function clear() {
    toasts.value = []
  }
  
  return {
    toasts: computed(() => toasts.value),
    show,
    success,
    error,
    warning,
    info,
    remove,
    clear
  }
}

// Create a global toast instance
const globalToast = useToast()

export function useGlobalToast() {
  return globalToast
}
