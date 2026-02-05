<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 flex items-center justify-center p-4">
    <div class="w-full max-w-sm">
      <!-- Card -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <!-- Icon -->
        <div class="mb-6">
          <div 
            class="inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-4 transition-all duration-500"
            :class="{
              'bg-primary-100 dark:bg-primary-900/30': status === 'loading',
              'bg-success-50 dark:bg-success-900/30': status === 'success',
              'bg-danger-50 dark:bg-danger-900/30': status === 'error'
            }"
          >
            <!-- Loading -->
            <svg 
              v-if="status === 'loading'"
              class="animate-spin w-8 h-8 text-primary-600 dark:text-primary-400" 
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24"
            >
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            
            <!-- Success -->
            <CheckCircleIcon v-else-if="status === 'success'" class="w-8 h-8 text-success-500" />
            
            <!-- Error -->
            <XCircleIcon v-else class="w-8 h-8 text-danger-500" />
          </div>
        </div>

        <!-- Title -->
        <h1 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
          {{ statusTitle }}
        </h1>

        <!-- Message -->
        <p class="text-gray-500 dark:text-gray-400 mb-6">
          {{ statusMessage }}
        </p>

        <!-- Actions -->
        <div v-if="status !== 'loading'" class="space-y-3">
          <RouterLink 
            to="/login" 
            class="w-full h-11 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-all flex items-center justify-center gap-2 shadow-lg shadow-primary-200 dark:shadow-primary-900/30"
          >
            <ArrowLeftOnRectangleIcon class="w-5 h-5" />
            Qayta kirish
          </RouterLink>
          
          <button 
            v-if="status === 'error'"
            @click="performLogout"
            class="w-full h-10 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 font-medium rounded-lg transition-colors"
          >
            Qayta urinish
          </button>
        </div>

        <!-- Countdown -->
        <div v-if="status === 'success' && countdown > 0" class="mt-4">
          <p class="text-sm text-gray-400 dark:text-gray-500">
            {{ countdown }} soniyadan so'ng yo'naltiriladi...
          </p>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-6 text-center">
        <p class="text-xs text-gray-400 dark:text-gray-500">
          © 2024 Proft. Barcha huquqlar himoyalangan.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { CheckCircleIcon, XCircleIcon, ArrowLeftOnRectangleIcon } from '@heroicons/vue/24/outline'
import { useUserStore } from '@/stores'
import { authService } from '@/services'

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const status = ref('loading') // 'loading' | 'success' | 'error'
const errorMessage = ref('')
const countdown = ref(3)
let countdownTimer = null

const statusTitle = computed(() => {
  switch (status.value) {
    case 'loading': return 'Chiqish...'
    case 'success': return 'Muvaffaqiyatli chiqildi'
    case 'error': return 'Xatolik yuz berdi'
    default: return ''
  }
})

const statusMessage = computed(() => {
  switch (status.value) {
    case 'loading': return 'Sessiya tugatilmoqda...'
    case 'success': return 'Tizimdan muvaffaqiyatli chiqdingiz.'
    case 'error': return errorMessage.value || 'Chiqishda xatolik yuz berdi'
    default: return ''
  }
})

async function performLogout() {
  status.value = 'loading'
  errorMessage.value = ''
  
  try {
    // DEV_MODE check
    const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true'
    
    if (DEV_MODE) {
      // Simulate logout
      await new Promise(resolve => setTimeout(resolve, 800))
    } else {
      // Real logout
      await authService.logout()
    }
    
    // Clear user store
    userStore.user = null
    userStore.isAuthenticated = false
    
    // Clear local storage
    localStorage.removeItem('proft_user')
    localStorage.removeItem('proft_token')
    
    status.value = 'success'
    toast.success('Tizimdan chiqdingiz')
    
    // Start countdown for redirect
    startCountdown()
    
  } catch (err) {
    console.error('Logout error:', err)
    status.value = 'error'
    errorMessage.value = err.message || 'Chiqishda xatolik yuz berdi'
  }
}

function startCountdown() {
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer)
      router.push('/login')
    }
  }, 1000)
}

onMounted(() => {
  performLogout()
})

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>
