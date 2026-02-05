<template>
  <header class="bg-white border-b border-gray-200 sticky top-0 z-40 dark:bg-gray-800 dark:border-gray-700">
    <div class="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
      <!-- Left: Menu button (mobile) + Logo -->
      <div class="flex items-center gap-4">
        <button 
          @click="$emit('toggle-sidebar')"
          class="lg:hidden p-2 rounded-lg text-gray-500 hover:bg-gray-100 transition-colors dark:text-gray-400 dark:hover:bg-gray-700"
        >
          <Bars3Icon class="w-6 h-6" />
        </button>
        
        <RouterLink to="/dashboard" class="flex items-center gap-2">
          <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-lg">P</span>
          </div>
          <span class="text-xl font-bold text-gray-900 hidden sm:block dark:text-white">Proft</span>
        </RouterLink>
      </div>
      
      <!-- Right: Theme toggle + Notifications + User menu -->
      <div class="flex items-center gap-2 sm:gap-4">
        <!-- Theme toggle -->
        <ThemeToggle />
        
        <!-- Notifications dropdown -->
        <Menu as="div" class="relative">
          <MenuButton class="p-2 rounded-lg text-gray-500 hover:bg-gray-100 transition-colors relative dark:text-gray-400 dark:hover:bg-gray-700">
            <BellIcon class="w-6 h-6" />
            <span v-if="notificationCount > 0" class="absolute top-1 right-1 w-2 h-2 bg-danger-500 rounded-full"></span>
          </MenuButton>
          
          <transition
            enter-active-class="transition duration-100 ease-out"
            enter-from-class="transform scale-95 opacity-0"
            enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0"
          >
            <MenuItems class="absolute right-0 mt-2 w-80 origin-top-right bg-white rounded-xl shadow-lg ring-1 ring-black/5 focus:outline-none dark:bg-gray-800 dark:ring-gray-700">
              <!-- Header -->
              <div class="px-4 py-3 border-b border-gray-100 flex items-center justify-between dark:border-gray-700">
                <h3 class="font-medium text-gray-900 dark:text-white">Bildirishnomalar</h3>
                <span v-if="notificationCount > 0" class="text-xs bg-primary-100 text-primary-700 px-2 py-0.5 rounded-full">
                  {{ notificationCount }} yangi
                </span>
              </div>
              
              <!-- Notifications list -->
              <div class="max-h-80 overflow-y-auto">
                <MenuItem v-for="notification in notifications" :key="notification.id" v-slot="{ active, close }">
                  <div 
                    @click="handleNotificationClick(notification, close)"
                    :class="[
                      active ? 'bg-gray-50 dark:bg-gray-700' : '',
                      'px-4 py-3 cursor-pointer border-b border-gray-50 last:border-0 dark:border-gray-700'
                    ]"
                  >
                    <div class="flex items-start gap-3">
                      <div :class="[
                        'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
                        notification.type === 'assignment' ? 'bg-blue-100 text-blue-600' :
                        notification.type === 'portfolio' ? 'bg-green-100 text-green-600' :
                        'bg-gray-100 text-gray-600'
                      ]">
                        <component :is="getNotificationIcon(notification.type)" class="w-4 h-4" />
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm text-gray-900 dark:text-gray-100">{{ notification.title }}</p>
                        <p class="text-xs text-gray-500 mt-0.5 dark:text-gray-400">{{ notification.time }}</p>
                      </div>
                    </div>
                  </div>
                </MenuItem>
                
                <!-- Empty state -->
                <div v-if="notifications.length === 0" class="px-4 py-8 text-center">
                  <BellIcon class="w-8 h-8 text-gray-300 mx-auto mb-2 dark:text-gray-600" />
                  <p class="text-sm text-gray-500 dark:text-gray-400">Bildirishnomalar yo'q</p>
                </div>
              </div>
              
              <!-- Footer -->
              <div class="px-4 py-2 border-t border-gray-100 dark:border-gray-700">
                <RouterLink 
                  to="/my-assignments" 
                  class="text-sm text-primary-600 hover:text-primary-700 font-medium dark:text-primary-400"
                >
                  Barchasini ko'rish
                </RouterLink>
              </div>
            </MenuItems>
          </transition>
        </Menu>
        
        <!-- User dropdown -->
        <Menu as="div" class="relative">
          <MenuButton class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-100 transition-colors dark:hover:bg-gray-700">
            <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center dark:bg-primary-900">
              <span class="text-primary-700 font-medium text-sm dark:text-primary-300">
                {{ userInitials }}
              </span>
            </div>
            <div class="hidden sm:block text-left">
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ userStore.fullName }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ roleDisplay }}</p>
            </div>
            <ChevronDownIcon class="w-4 h-4 text-gray-400 hidden sm:block" />
          </MenuButton>
          
          <transition
            enter-active-class="transition duration-100 ease-out"
            enter-from-class="transform scale-95 opacity-0"
            enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0"
          >
            <MenuItems class="absolute right-0 mt-2 w-56 origin-top-right bg-white rounded-xl shadow-lg ring-1 ring-black/5 focus:outline-none py-1 dark:bg-gray-800 dark:ring-gray-700">
              <!-- User info -->
              <div class="px-4 py-3 border-b border-gray-100 dark:border-gray-700">
                <p class="text-sm font-medium text-gray-900 dark:text-white">{{ userStore.fullName }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ userStore.user?.email }}</p>
              </div>
              
              <div class="py-1">
                <MenuItem v-slot="{ active }">
                  <RouterLink 
                    to="/profile"
                    :class="[
                      active ? 'bg-gray-50 dark:bg-gray-700' : '',
                      'flex items-center gap-3 px-4 py-2 text-sm text-gray-700 dark:text-gray-200'
                    ]"
                  >
                    <UserCircleIcon class="w-5 h-5 text-gray-400" />
                    Profil
                  </RouterLink>
                </MenuItem>
                
                <MenuItem v-slot="{ active }">
                  <RouterLink 
                    to="/dashboard"
                    :class="[
                      active ? 'bg-gray-50 dark:bg-gray-700' : '',
                      'flex items-center gap-3 px-4 py-2 text-sm text-gray-700 dark:text-gray-200'
                    ]"
                  >
                    <Cog6ToothIcon class="w-5 h-5 text-gray-400" />
                    Sozlamalar
                  </RouterLink>
                </MenuItem>
              </div>
              
              <div class="py-1 border-t border-gray-100 dark:border-gray-700">
                <MenuItem v-slot="{ active }">
                  <button 
                    @click="handleLogout"
                    :class="[
                      active ? 'bg-gray-50 dark:bg-gray-700' : '',
                      'flex items-center gap-3 w-full px-4 py-2 text-sm text-danger-600'
                    ]"
                  >
                    <ArrowRightOnRectangleIcon class="w-5 h-5" />
                    Chiqish
                  </button>
                </MenuItem>
              </div>
            </MenuItems>
          </transition>
        </Menu>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import { 
  Bars3Icon, 
  BellIcon, 
  ChevronDownIcon,
  UserCircleIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  DocumentTextIcon,
  ClipboardDocumentListIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'
import { useUserStore } from '@/stores'
import { ThemeToggle } from '@/components/common'

defineEmits(['toggle-sidebar'])

const router = useRouter()
const userStore = useUserStore()

// Mock notifications
const notifications = ref([
  { id: 1, type: 'assignment', title: 'Yangi topshiriq: Ilmiy maqola yozish', time: '5 daqiqa oldin', link: '/my-assignments' },
  { id: 2, type: 'portfolio', title: 'Portfolio tasdiqlandi', time: '1 soat oldin', link: '/portfolios' },
  { id: 3, type: 'assignment', title: 'Topshiriq muddati yaqinlashmoqda', time: '3 soat oldin', link: '/my-assignments' },
])

const notificationCount = computed(() => notifications.value.length)

function getNotificationIcon(type) {
  switch (type) {
    case 'assignment': return ClipboardDocumentListIcon
    case 'portfolio': return DocumentTextIcon
    default: return CheckCircleIcon
  }
}

function handleNotificationClick(notification, close) {
  // Close the dropdown
  close()
  // Navigate to the notification link
  router.push(notification.link || '/dashboard')
}

const userInitials = computed(() => {
  const name = userStore.fullName
  if (!name) return '?'
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
})

const roleDisplay = computed(() => {
  const roles = {
    superadmin: 'Super Admin',
    admin: 'Admin',
    teacher: "O'qituvchi"
  }
  return roles[userStore.role] || userStore.role
})

async function handleLogout() {
  await userStore.logout()
  router.push('/login')
}
</script>
