<template>
  <div class="animate-fade-in">
    <div class="text-center">
      <h1 class="text-2xl font-bold text-gray-900 mb-2">
        Tizimga kirish
      </h1>
      <p class="text-sm text-gray-500 mb-8">
        Portfolio tizimiga kirish uchun Hemis orqali autentifikatsiya qiling
      </p>
    </div>
    
    <!-- Hemis Login Button -->
    <button
      @click="loginWithHemis"
      :disabled="isLoading"
      class="w-full flex items-center justify-center gap-3 py-3 px-4 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-50"
    >
      <svg v-if="!isLoading" class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
      </svg>
      <LoadingSpinner v-else size="xs" color="white" />
      <span>{{ isLoading ? 'Kirish...' : 'Hemis orqali kirish' }}</span>
    </button>
    
    <!-- Divider -->
    <div class="relative my-8">
      <div class="absolute inset-0 flex items-center">
        <div class="w-full border-t border-gray-200"></div>
      </div>
      <div class="relative flex justify-center text-sm">
        <span class="px-4 bg-white text-gray-500">yoki</span>
      </div>
    </div>
    
    <!-- Demo accounts info (Development only) -->
    <div class="bg-gray-50 rounded-xl p-4">
      <h3 class="text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
        <InformationCircleIcon class="w-4 h-4 text-gray-400" />
        Test hisoblar
      </h3>
      <div class="space-y-2 text-xs text-gray-600">
        <div class="flex justify-between items-center p-2 bg-white rounded-lg">
          <span class="font-medium">Super Admin</span>
          <StatusBadge variant="superadmin" size="sm">superadmin</StatusBadge>
        </div>
        <div class="flex justify-between items-center p-2 bg-white rounded-lg">
          <span class="font-medium">Admin</span>
          <StatusBadge variant="admin" size="sm">admin</StatusBadge>
        </div>
        <div class="flex justify-between items-center p-2 bg-white rounded-lg">
          <span class="font-medium">O'qituvchi</span>
          <StatusBadge variant="teacher" size="sm">teacher</StatusBadge>
        </div>
      </div>
    </div>
    
    <!-- Help text -->
    <p class="mt-6 text-center text-xs text-gray-500">
      Muammo bormi? 
      <a href="mailto:support@proft.uz" class="text-primary-600 hover:text-primary-700 font-medium">
        Yordam markazi
      </a>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { InformationCircleIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner, StatusBadge } from '@/components/common'
import { useUserStore } from '@/stores'

const route = useRoute()
const userStore = useUserStore()

const isLoading = ref(false)

function loginWithHemis() {
  isLoading.value = true
  const redirectUrl = route.query.redirect || '/dashboard'
  userStore.login(redirectUrl)
}
</script>
