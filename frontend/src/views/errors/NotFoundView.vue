<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4">
    <div class="text-center animate-fade-in">
      <!-- 404 Icon -->
      <div class="w-24 h-24 mx-auto bg-gray-100 rounded-full flex items-center justify-center mb-6">
        <MagnifyingGlassIcon class="w-12 h-12 text-gray-400" />
      </div>
      
      <!-- Title -->
      <h1 class="text-4xl font-bold text-gray-900 mb-2">404</h1>
      <h2 class="text-xl font-semibold text-gray-700 mb-4">Sahifa topilmadi</h2>
      
      <!-- Description -->
      <p class="text-gray-500 max-w-md mb-8">
        Siz izlayotgan sahifa mavjud emas yoki ko'chirilgan bo'lishi mumkin.
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
  MagnifyingGlassIcon, 
  HomeIcon, 
  ArrowLeftIcon 
} from '@heroicons/vue/24/outline'

const router = useRouter()

function goBack() {
  router.go(-1)
}
</script>
