/**
 * Theme Store
 * Manages light/dark theme with localStorage persistence
 */

import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // Get initial theme from localStorage or default to 'light'
  const savedTheme = localStorage.getItem('theme') || 'light'
  const theme = ref(savedTheme)

  // Apply theme to document
  function applyTheme(newTheme) {
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Set theme
  function setTheme(newTheme) {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    applyTheme(newTheme)
  }

  // Toggle between light and dark
  function toggleTheme() {
    setTheme(theme.value === 'light' ? 'dark' : 'light')
  }

  // Initialize theme on load
  function init() {
    applyTheme(theme.value)
  }

  // Watch for changes
  watch(theme, (newTheme) => {
    applyTheme(newTheme)
  })

  // Initialize
  init()

  return {
    theme,
    setTheme,
    toggleTheme,
    init
  }
})
