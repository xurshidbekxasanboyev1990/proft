<template>
  <button
    @click="toggleTheme"
    class="p-2 rounded-lg text-gray-500 hover:bg-gray-100 transition-colors dark:text-gray-400 dark:hover:bg-gray-700"
    :title="themeStore.theme === 'light' ? 'Qorong\'u rejim' : 'Yorug\' rejim'"
  >
    <SunIcon v-if="themeStore.theme === 'dark'" class="w-5 h-5" />
    <MoonIcon v-else class="w-5 h-5" />
  </button>
</template>

<script setup>
import { SunIcon, MoonIcon } from '@heroicons/vue/24/outline'
import { useThemeStore } from '@/stores'

const themeStore = useThemeStore()

function toggleTheme() {
  themeStore.toggleTheme()
}
</script>
