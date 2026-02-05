<template>
  <div class="flex h-full flex-col">
    <!-- Logo -->
    <div class="flex h-16 shrink-0 items-center border-b border-gray-200 dark:border-gray-700 px-2">
      <RouterLink to="/teacher" class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg">
          <AcademicCapIcon class="w-6 h-6 text-white" />
        </div>
        <div>
          <span class="text-lg font-bold text-gray-900 dark:text-white">Portfolio</span>
          <span class="block text-xs text-primary-600 dark:text-primary-400 font-medium">O'qituvchi paneli</span>
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
                ? 'bg-primary-50 text-primary-700 dark:bg-primary-900/50 dark:text-primary-300'
                : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700/50'
            ]"
            @click="$emit('close')"
          >
            <component
              :is="item.icon"
              class="w-5 h-5 shrink-0 transition-colors"
              :class="[
                isActive(item.to)
                  ? 'text-primary-600 dark:text-primary-400'
                  : 'text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300'
              ]"
            />
            <span>{{ item.name }}</span>
            
            <!-- Badge -->
            <span
              v-if="item.badge"
              class="ml-auto inline-flex items-center justify-center px-2 py-0.5 text-xs font-bold rounded-full"
              :class="item.badgeClass || 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300'"
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
        to="/teacher/profile"
        class="flex items-center gap-3 p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors"
        @click="$emit('close')"
      >
        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white font-semibold text-sm">
          {{ userInitials }}
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
            {{ user?.full_name || 'Foydalanuvchi' }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-400 truncate">
            O'qituvchi
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
import { useUserStore, useNotificationStore } from '@/stores'
import {
  HomeIcon,
  FolderIcon,
  PlusCircleIcon,
  ClipboardDocumentListIcon,
  ChatBubbleLeftRightIcon,
  ChartBarIcon,
  BellIcon,
  UserCircleIcon,
  AcademicCapIcon,
  XMarkIcon,
  ChevronRightIcon
} from '@heroicons/vue/24/outline'

defineEmits(['close'])

const route = useRoute()
const authStore = useUserStore()
const notificationStore = useNotificationStore()

const user = computed(() => authStore.user)

const userInitials = computed(() => {
  const name = user.value?.full_name || ''
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase() || 'U'
})

const unreadCount = computed(() => notificationStore.unreadCount || 0)

const menuItems = computed(() => [
  {
    name: 'Dashboard',
    to: '/teacher',
    icon: HomeIcon
  },
  {
    name: 'Portfoliolarim',
    to: '/teacher/portfolios',
    icon: FolderIcon
  },
  {
    name: 'Yangi portfolio',
    to: '/teacher/portfolios/new',
    icon: PlusCircleIcon
  },
  {
    name: 'Topshiriqlarim',
    to: '/teacher/tasks',
    icon: ClipboardDocumentListIcon
  },
  {
    name: 'Javoblarim',
    to: '/teacher/responses',
    icon: ChatBubbleLeftRightIcon
  },
  {
    name: 'Ballarim',
    to: '/teacher/scores',
    icon: ChartBarIcon
  },
  {
    name: 'Bildirishnomalar',
    to: '/teacher/notifications',
    icon: BellIcon,
    badge: unreadCount.value > 0 ? unreadCount.value : null,
    badgeClass: 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300'
  },
  {
    name: 'Profil',
    to: '/teacher/profile',
    icon: UserCircleIcon
  }
])

const isActive = (path) => {
  if (path === '/teacher') {
    return route.path === '/teacher' || route.path === '/teacher/'
  }
  return route.path.startsWith(path)
}
</script>
