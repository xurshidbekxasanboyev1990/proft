<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Card -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r from-primary-600 to-primary-700 px-6 py-8 text-center">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-white/20 rounded-2xl mb-4">
            <UserCircleIcon class="w-10 h-10 text-white" />
          </div>
          <h1 class="text-xl font-bold text-white">
            {{ isAuthenticated ? 'Tizimga kirgansiz' : 'Tizimga kirilmagan' }}
          </h1>
        </div>

        <!-- Content -->
        <div class="p-6">
          <!-- Loading -->
          <div v-if="isLoading" class="text-center py-8">
            <LoadingSpinner size="lg" text="Tekshirilmoqda..." />
          </div>

          <!-- Authenticated -->
          <div v-else-if="isAuthenticated && user" class="space-y-4">
            <!-- User Info -->
            <div class="flex items-center gap-4 p-4 bg-gray-50 dark:bg-gray-900 rounded-xl">
              <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center">
                <span class="text-lg font-bold text-primary-600 dark:text-primary-400">
                  {{ user.full_name?.charAt(0) || user.username?.charAt(0) || '?' }}
                </span>
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-900 dark:text-white truncate">
                  {{ user.full_name || user.username }}
                </p>
                <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
                  {{ user.email }}
                </p>
              </div>
            </div>

            <!-- Details -->
            <div class="space-y-3">
              <div class="flex justify-between items-center py-2 border-b border-gray-100 dark:border-gray-700">
                <span class="text-sm text-gray-500 dark:text-gray-400">Rol</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white capitalize">
                  {{ roleLabel }}
                </span>
              </div>
              <div v-if="user.department" class="flex justify-between items-center py-2 border-b border-gray-100 dark:border-gray-700">
                <span class="text-sm text-gray-500 dark:text-gray-400">Bo'lim</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ user.department }}
                </span>
              </div>
              <div v-if="user.position" class="flex justify-between items-center py-2 border-b border-gray-100 dark:border-gray-700">
                <span class="text-sm text-gray-500 dark:text-gray-400">Lavozim</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ user.position }}
                </span>
              </div>
              <div v-if="user.hemis_id" class="flex justify-between items-center py-2">
                <span class="text-sm text-gray-500 dark:text-gray-400">Hemis ID</span>
                <code class="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-gray-700 dark:text-gray-300">
                  {{ user.hemis_id }}
                </code>
              </div>
            </div>

            <!-- Actions -->
            <div class="pt-4 space-y-3">
              <RouterLink 
                :to="dashboardRoute"
                class="w-full h-11 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-all flex items-center justify-center gap-2"
              >
                <HomeIcon class="w-5 h-5" />
                Bosh sahifaga o'tish
              </RouterLink>
              
              <button 
                @click="handleLogout"
                class="w-full h-10 border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 font-medium rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-all flex items-center justify-center gap-2"
              >
                <ArrowRightOnRectangleIcon class="w-5 h-5" />
                Chiqish
              </button>
            </div>
          </div>

          <!-- Not Authenticated -->
          <div v-else class="text-center py-8">
            <div class="w-16 h-16 mx-auto bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mb-4">
              <LockClosedIcon class="w-8 h-8 text-gray-400" />
            </div>
            <p class="text-gray-500 dark:text-gray-400 mb-6">
              Tizimga kirish uchun autentifikatsiya talab qilinadi.
            </p>
            <RouterLink 
              to="/login"
              class="inline-flex items-center gap-2 px-6 h-11 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-all"
            >
              <ArrowLeftOnRectangleIcon class="w-5 h-5" />
              Kirish
            </RouterLink>
          </div>

          <!-- Error -->
          <div v-if="error" class="mt-4 p-3 bg-danger-50 dark:bg-danger-900/20 rounded-lg">
            <p class="text-sm text-danger-600 dark:text-danger-400 text-center">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-6 text-center">
        <button 
          @click="checkStatus"
          class="text-sm text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
        >
          <ArrowPathIcon class="w-4 h-4 inline mr-1" />
          Qayta tekshirish
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  UserCircleIcon, 
  HomeIcon, 
  LockClosedIcon,
  ArrowLeftOnRectangleIcon,
  ArrowRightOnRectangleIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'
import { LoadingSpinner } from '@/components/common'
import { useUserStore } from '@/stores'
import { authService } from '@/services'
import { getDashboardRoute } from '@/router'

const router = useRouter()
const userStore = useUserStore()

const isLoading = ref(true)
const error = ref('')

const isAuthenticated = computed(() => userStore.isAuthenticated)
const user = computed(() => userStore.user)

const roleLabel = computed(() => {
  const labels = {
    teacher: "O'qituvchi",
    admin: 'Administrator',
    superadmin: 'Super Admin'
  }
  return labels[user.value?.role] || user.value?.role
})

const dashboardRoute = computed(() => {
  return getDashboardRoute(user.value?.role || 'teacher')
})

async function checkStatus() {
  isLoading.value = true
  error.value = ''
  
  try {
    const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true'
    
    if (DEV_MODE) {
      await new Promise(resolve => setTimeout(resolve, 500))
      // In DEV mode, just use current store state
    } else {
      const response = await authService.checkStatus()
      
      if (response.authenticated && response.user) {
        userStore.user = response.user
        userStore.isAuthenticated = true
      } else {
        userStore.user = null
        userStore.isAuthenticated = false
      }
    }
  } catch (err) {
    console.error('Status check error:', err)
    error.value = err.message || 'Holatni tekshirishda xatolik'
  } finally {
    isLoading.value = false
  }
}

function handleLogout() {
  router.push('/logout')
}

onMounted(() => {
  checkStatus()
})
</script>
