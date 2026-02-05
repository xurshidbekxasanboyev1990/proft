<template>
  <div class="text-center animate-fade-in">
    <LoadingSpinner size="lg" text="Qayta yo'naltirilmoqda..." />
    <p class="mt-4 text-sm text-gray-500">
      Hemis tizimidan ma'lumotlar olinmoqda...
    </p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { LoadingSpinner } from '@/components/common'
import { useUserStore } from '@/stores'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

onMounted(async () => {
  // Wait a moment for session to be established
  await new Promise(resolve => setTimeout(resolve, 500))
  
  // Check authentication status
  const isAuth = await userStore.checkAuth()
  
  if (isAuth) {
    // Redirect to intended destination or dashboard
    const redirectUrl = route.query.next || '/dashboard'
    router.replace(redirectUrl)
  } else {
    // Authentication failed, redirect to login
    router.replace('/login')
  }
})
</script>
