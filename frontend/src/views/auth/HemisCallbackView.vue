<template>
  <div class="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-primary-50 via-white to-blue-50 px-4">
    <div class="text-center">
      <!-- Loading spinner -->
      <div class="mb-6">
        <div class="w-16 h-16 mx-auto bg-primary-600 rounded-2xl flex items-center justify-center shadow-lg shadow-primary-200 animate-pulse">
          <span class="text-2xl font-bold text-white">P</span>
        </div>
      </div>
      
      <h1 class="text-2xl font-bold text-gray-900 mb-2">
        {{ status === 'loading' ? 'Autentifikatsiya...' : status === 'success' ? 'Muvaffaqiyatli!' : 'Xatolik' }}
      </h1>
      
      <p class="text-gray-500 mb-6">
        {{ statusMessage }}
      </p>
      
      <!-- Loading indicator -->
      <div v-if="status === 'loading'" class="flex justify-center">
        <LoadingSpinner size="lg" />
      </div>
      
      <!-- Success -->
      <div v-else-if="status === 'success'" class="text-center">
        <div class="w-16 h-16 mx-auto bg-success-50 rounded-full flex items-center justify-center mb-4">
          <CheckCircleIcon class="w-10 h-10 text-success-500" />
        </div>
        <p class="text-sm text-gray-500">Yo'naltirilmoqda...</p>
      </div>
      
      <!-- Error -->
      <div v-else-if="status === 'error'" class="text-center">
        <div class="w-16 h-16 mx-auto bg-danger-50 rounded-full flex items-center justify-center mb-4">
          <XCircleIcon class="w-10 h-10 text-danger-500" />
        </div>
        <p class="text-sm text-danger-600 mb-6">{{ errorMessage }}</p>
        <RouterLink to="/login" class="btn-primary inline-flex">
          Qayta kirish
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { CheckCircleIcon, XCircleIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner } from '@/components/common'
import { useUserStore } from '@/stores'
import { authService } from '@/services'
import { getDashboardRoute } from '@/router'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const status = ref('loading')
const statusMessage = ref('Hemis tizimidan ma\'lumotlar olinmoqda...')
const errorMessage = ref('')

async function handleCallback() {
  try {
    // Get code and state from query params
    const code = route.query.code
    const state = route.query.state
    const error = route.query.error
    
    // Check for OAuth errors
    if (error) {
      throw new Error(route.query.error_description || 'OAuth autentifikatsiya xatosi')
    }
    
    if (!code) {
      throw new Error('Autentifikatsiya kodi topilmadi')
    }
    
    statusMessage.value = 'Sessiya yaratilmoqda...'
    
    // In DEV_MODE, simulate successful login
    const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true'
    
    if (DEV_MODE) {
      // Mock successful callback
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      userStore.user = {
        id: 1,
        username: 'hemis_user',
        email: 'user@hemis.uz',
        full_name: 'Hemis User',
        role: 'teacher',
        hemis_id: code,
        department: 'Pedagogika',
        position: "O'qituvchi"
      }
      userStore.isAuthenticated = true
      
      status.value = 'success'
      statusMessage.value = 'Tizimga muvaffaqiyatli kirdingiz!'
      
      toast.success('Xush kelibsiz!')
      
      setTimeout(() => {
        // Redirect to role-based dashboard
        const dashboardRoute = getDashboardRoute(userStore.user?.role || 'teacher')
        router.push(dashboardRoute)
      }, 1500)
      
      return
    }
    
    // Real OAuth callback processing
    const response = await authService.checkStatus()
    
    if (response.authenticated && response.user) {
      userStore.user = response.user
      userStore.isAuthenticated = true
      
      status.value = 'success'
      statusMessage.value = 'Tizimga muvaffaqiyatli kirdingiz!'
      
      toast.success(`Xush kelibsiz, ${response.user.full_name}!`)
      
      setTimeout(() => {
        // Redirect to role-based dashboard
        const dashboardRoute = getDashboardRoute(response.user.role || 'teacher')
        router.push(dashboardRoute)
      }, 1500)
    } else {
      throw new Error('Autentifikatsiya muvaffaqiyatsiz')
    }
  } catch (err) {
    console.error('Callback error:', err)
    status.value = 'error'
    errorMessage.value = err.message || 'Noma\'lum xatolik yuz berdi'
    statusMessage.value = 'Autentifikatsiya amalga oshmadi'
  }
}

onMounted(() => {
  handleCallback()
})
</script>
