<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4">
    <div class="text-center animate-fade-in">
      <!-- 403 Icon -->
      <div class="w-24 h-24 mx-auto bg-danger-100 rounded-full flex items-center justify-center mb-6">
        <ShieldExclamationIcon class="w-12 h-12 text-danger-600" />
      </div>
      
      <!-- Title -->
      <h1 class="text-4xl font-bold text-gray-900 mb-2">403</h1>
      <h2 class="text-xl font-semibold text-gray-700 mb-4">Ruxsat berilmagan</h2>
      
      <!-- Description -->
      <p class="text-gray-500 max-w-md mb-8">
        Sizda bu sahifaga kirish uchun ruxsat yo'q. 
        Agar bu xato deb hisoblasangiz, administratorga murojaat qiling.
      </p>
      
      <!-- Actions -->
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <RouterLink to="/dashboard" class="btn-primary">
          <HomeIcon class="w-5 h-5 mr-2" />
          Bosh sahifaga
        </RouterLink>
        <button @click="goBack" class="btn-secondary">
          <ArrowLeftIcon class="w-5 h-5 mr-2" />
          Orqaga qaytish
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { 
  ShieldExclamationIcon, 
  HomeIcon, 
  ArrowLeftIcon 
} from '@heroicons/vue/24/outline'

const router = useRouter()

function goBack() {
  router.go(-1)
}
</script>
