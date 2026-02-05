<template>
  <RouterView />
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores'

const userStore = useUserStore()

onMounted(async () => {
  // Check if user is authenticated on app load
  try {
    await userStore.checkAuth()
  } catch (error) {
    console.warn('Auth check failed (backend may be offline):', error.message)
  }
})
</script>
