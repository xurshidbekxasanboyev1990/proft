<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Sidebar -->
    <TheSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />
    
    <!-- Main content area -->
    <div class="lg:pl-72">
      <!-- Navbar -->
      <TheNavbar @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      
      <!-- Page content -->
      <main class="py-6 px-4 sm:px-6 lg:px-8">
        <RouterView v-slot="{ Component }">
          <transition
            enter-active-class="transition-opacity duration-200"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition-opacity duration-150"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
            mode="out-in"
          >
            <component :is="Component" />
          </transition>
        </RouterView>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { TheNavbar, TheSidebar } from '@/components/layout'
import { usePortfolioStore } from '@/stores'

const sidebarOpen = ref(false)
const portfolioStore = usePortfolioStore()

// Fetch initial stats for sidebar badge
onMounted(async () => {
  try {
    await portfolioStore.fetchStats()
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
})
</script>
