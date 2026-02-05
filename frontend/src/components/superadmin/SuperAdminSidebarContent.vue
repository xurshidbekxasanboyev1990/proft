<template>
  <div class="flex h-full flex-col">
    <!-- Logo -->
    <div class="flex h-16 shrink-0 items-center border-b border-gray-200 dark:border-gray-700 px-2">
      <RouterLink to="/super-admin" class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
          <CogIcon class="w-6 h-6 text-white" />
        </div>
        <div>
          <span class="text-lg font-bold text-gray-900 dark:text-white">Portfolio</span>
          <span class="block text-xs text-purple-600 dark:text-purple-400 font-medium">Super Admin</span>
        </div>
      </RouterLink>
      
      <!-- Mobile close button -->
      <button
        @click="$emit('close')"
        class="lg:hidden ml-auto p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
      >
        <XMarkIcon class="w-5 h-5 text-gray-500 dark:text-gray-400" />
      </button>
    </div>
    
    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto py-4">
      <ul class="space-y-1 px-2">
        <li v-for="item in menuItems" :key="item.name">
          <RouterLink
            :to="item.to"
            class="group flex items-center gap-x-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-200"
            :class="[
              isActive(item.to)
                ? 'bg-purple-50 text-purple-700 dark:bg-purple-900/50 dark:text-purple-300'
                : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700/50'
            ]"
            @click="$emit('close')"
          >
            <component
              :is="item.icon"
              class="w-5 h-5 shrink-0 transition-colors"
              :class="[
                isActive(item.to)
                  ? 'text-purple-600 dark:text-purple-400'
                  : 'text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300'
              ]"
            />
            <span>{{ item.name }}</span>
            
            <!-- Badge -->
            <span
              v-if="item.badge"
              class="ml-auto inline-flex items-center justify-center px-2 py-0.5 text-xs font-bold rounded-full"
              :class="item.badgeClass || 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300'"
            >
              {{ item.badge }}
            </span>
          </RouterLink>
        </li>
      </ul>
    </nav>
    
    <!-- User info -->
    <div class="border-t border-gray-200 dark:border-gray-700 p-4">
      <RouterLink
        to="/super-admin/profile"
        class="flex items-center gap-3 p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors"
        @click="$emit('close')"
      >
        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-white font-semibold text-sm">
          {{ userInitials }}
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
            {{ user?.full_name || 'Foydalanuvchi' }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-400 truncate">
            Super Administrator
          </p>
        </div>
        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore, usePortfolioStore } from '@/stores'
import {
  HomeIcon,
  UsersIcon,
  TagIcon,
  ClipboardDocumentListIcon,
  ClipboardDocumentCheckIcon,
  ChartBarIcon,
  DocumentChartBarIcon,
  Cog6ToothIcon,
  CogIcon,
  XMarkIcon,
  ChevronRightIcon
} from '@heroicons/vue/24/outline'

defineEmits(['close'])

const route = useRoute()
const authStore = useUserStore()
const portfolioStore = usePortfolioStore()

const user = computed(() => authStore.user)

const userInitials = computed(() => {
  const name = user.value?.full_name || ''
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase() || 'U'
})

const pendingCount = computed(() => portfolioStore.stats?.pending_count || 0)

const menuItems = computed(() => [
  {
    name: 'Dashboard',
    to: '/super-admin',
    icon: HomeIcon
  },
  {
    name: 'Foydalanuvchilar',
    to: '/super-admin/users',
    icon: UsersIcon
  },
  {
    name: 'Kategoriyalar',
    to: '/super-admin/categories',
    icon: TagIcon
  },
  {
    name: 'Topshiriqlar',
    to: '/super-admin/tasks',
    icon: ClipboardDocumentListIcon
  },
  {
    name: 'Tasdiqlash',
    to: '/super-admin/approvals',
    icon: ClipboardDocumentCheckIcon,
    badge: pendingCount.value > 0 ? pendingCount.value : null,
    badgeClass: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300'
  },
  {
    name: 'Analitika',
    to: '/super-admin/analytics',
    icon: ChartBarIcon
  },
  {
    name: 'Hisobotlar',
    to: '/super-admin/reports',
    icon: DocumentChartBarIcon
  },
  {
    name: 'Sozlamalar',
    to: '/super-admin/settings',
    icon: Cog6ToothIcon
  }
])

const isActive = (path) => {
  if (path === '/super-admin') {
    return route.path === '/super-admin' || route.path === '/super-admin/'
  }
  return route.path.startsWith(path)
}
</script>
