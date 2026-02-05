<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 flex items-center justify-center p-4">
    <div class="w-full max-w-sm">
      <!-- Card -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
        <!-- Logo -->
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-12 h-12 bg-primary-600 rounded-xl mb-3 shadow-lg shadow-primary-200 dark:shadow-primary-900/30">
            <span class="text-xl font-bold text-white">P</span>
          </div>
          <h1 class="text-xl font-bold text-gray-900 dark:text-white">Proft</h1>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Portfolio tizimi</p>
        </div>

        <!-- Error -->
        <div v-if="error" class="mb-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
          <p class="text-sm text-red-600 dark:text-red-400 text-center">{{ error }}</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <input
            v-model="form.username"
            type="text"
            placeholder="Foydalanuvchi nomi"
            class="w-full h-11 px-4 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            :disabled="isLoading"
          />

          <div class="relative">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Parol"
              class="w-full h-11 px-4 pr-11 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              :disabled="isLoading"
            />
            <button 
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"
            >
              <EyeIcon v-if="!showPassword" class="w-5 h-5" />
              <EyeSlashIcon v-else class="w-5 h-5" />
            </button>
          </div>

          <button
            type="submit"
            :disabled="isLoading || !form.username || !form.password"
            class="w-full h-11 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary-200 dark:shadow-primary-900/30 hover:shadow-xl hover:shadow-primary-300 dark:hover:shadow-primary-900/40"
          >
            <span v-if="isLoading" class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Kuting...
            </span>
            <span v-else>Kirish</span>
          </button>
        </form>

        <!-- Hemis -->
        <div class="mt-6 pt-6 border-t border-gray-100 dark:border-gray-700">
          <p class="text-xs text-center text-gray-400 dark:text-gray-500 mb-3">yoki</p>
          <button
            @click="handleHemisLogin"
            class="w-full h-11 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-medium rounded-lg transition-all flex items-center justify-center gap-2 shadow-lg shadow-blue-200 dark:shadow-blue-900/30 hover:shadow-xl"
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
            </svg>
            Hemis orqali kirish
          </button>
        </div>

        <!-- DEV -->
        <div v-if="isDev" class="mt-4 pt-4 border-t border-dashed border-gray-200 dark:border-gray-700">
          <p class="text-xs text-center text-gray-400 dark:text-gray-500 mb-2">🛠️ DEV rejimi</p>
          <div class="flex justify-center gap-2">
            <button 
              v-for="role in ['teacher', 'admin', 'superadmin']"
              :key="role"
              @click="quickLogin(role)"
              class="px-3 py-1.5 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-md hover:bg-primary-100 hover:text-primary-600 dark:hover:bg-primary-900/30 dark:hover:text-primary-400 transition-colors"
            >
              {{ role }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline'
import { useUserStore } from '@/stores'
import { authService } from '@/services'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const isDev = computed(() => import.meta.env.VITE_DEV_MODE === 'true')
const isLoading = ref(false)
const showPassword = ref(false)
const error = ref('')
const form = reactive({ username: '', password: '' })

onMounted(() => {
  const saved = localStorage.getItem('proft_user')
  if (saved) form.username = saved
})

function quickLogin(role) {
  form.username = role
  form.password = `${role}123`
  handleLogin()
}

async function handleHemisLogin() {
  // DEV_MODE'da mock user bilan kirish
  if (isDev.value) {
    isLoading.value = true
    try {
      // Mock Hemis user
      userStore.user = {
        id: 1,
        username: 'hemis_user',
        email: 'user@hemis.uz',
        full_name: 'Hemis Foydalanuvchi',
        role: 'teacher',
        hemis_id: 'H123456',
        department: 'Pedagogika',
        position: "O'qituvchi"
      }
      userStore.isAuthenticated = true
      toast.success('Hemis orqali muvaffaqiyatli kirdingiz!')
      router.push(route.query.redirect || '/teacher')
    } finally {
      isLoading.value = false
    }
    return
  }
  
  // Production: Hemis OAuth ga redirect
  userStore.login(route.query.redirect || '/')
}

async function handleLogin() {
  if (!form.username || !form.password) return
  
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await authService.devLogin(form.username, form.password)
    localStorage.setItem('proft_user', form.username)
    userStore.user = response.user
    userStore.isAuthenticated = true
    toast.success(`Xush kelibsiz!`)
    router.push(route.query.redirect || response.redirect || '/')
  } catch (err) {
    error.value = "Login yoki parol noto'g'ri"
  } finally {
    isLoading.value = false
  }
}
</script>
