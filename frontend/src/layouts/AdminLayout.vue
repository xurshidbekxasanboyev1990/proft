<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Mobile sidebar backdrop -->
    <TransitionRoot :show="sidebarOpen" as="template">
      <div class="lg:hidden">
        <TransitionChild
          as="template"
          enter="transition-opacity ease-linear duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="transition-opacity ease-linear duration-300"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-gray-900/80 z-40" @click="sidebarOpen = false"></div>
        </TransitionChild>
        
        <TransitionChild
          as="template"
          enter="transition ease-in-out duration-300 transform"
          enter-from="-translate-x-full"
          enter-to="translate-x-0"
          leave="transition ease-in-out duration-300 transform"
          leave-from="translate-x-0"
          leave-to="-translate-x-full"
        >
          <div class="fixed inset-y-0 left-0 z-50 w-72 bg-white shadow-xl dark:bg-gray-800">
            <AdminSidebarContent @close="sidebarOpen = false" />
          </div>
        </TransitionChild>
      </div>
    </TransitionRoot>
    
    <!-- Desktop sidebar -->
    <div class="hidden lg:fixed lg:inset-y-0 lg:z-40 lg:flex lg:w-72 lg:flex-col">
      <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-white border-r border-gray-200 px-6 pb-4 dark:bg-gray-800 dark:border-gray-700">
        <AdminSidebarContent />
      </div>
    </div>
    
    <!-- Main content area -->
    <div class="lg:pl-72">
      <!-- Navbar -->
      <AdminNavbar @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      
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
import { TransitionRoot, TransitionChild } from '@headlessui/vue'
import AdminNavbar from '@/components/admin/AdminNavbar.vue'
import AdminSidebarContent from '@/components/admin/AdminSidebarContent.vue'
import { usePortfolioStore } from '@/stores'

const sidebarOpen = ref(false)
const portfolioStore = usePortfolioStore()

onMounted(async () => {
  try {
    await portfolioStore.fetchStats()
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
})
</script>
