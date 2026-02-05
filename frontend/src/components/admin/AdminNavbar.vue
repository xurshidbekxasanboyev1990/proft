<template>
  <header class="sticky top-0 z-30 bg-white/80 backdrop-blur-lg border-b border-gray-200 dark:bg-gray-800/80 dark:border-gray-700">
    <div class="flex h-16 items-center gap-x-4 px-4 sm:px-6 lg:px-8">
      <!-- Mobile menu button -->
      <button
        type="button"
        class="lg:hidden -m-2.5 p-2.5 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
        @click="$emit('toggleSidebar')"
      >
        <Bars3Icon class="h-6 w-6" />
      </button>
      
      <!-- Separator -->
      <div class="h-6 w-px bg-gray-200 dark:bg-gray-700 lg:hidden"></div>
      
      <!-- Search -->
      <div class="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <div class="relative flex flex-1 items-center">
          <MagnifyingGlassIcon class="pointer-events-none absolute left-3 h-5 w-5 text-gray-400" />
          <input
            type="search"
            placeholder="Qidirish..."
            class="h-10 w-full max-w-md rounded-xl border-0 bg-gray-100 dark:bg-gray-700 pl-10 pr-4 text-sm text-gray-900 dark:text-white placeholder:text-gray-400 focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div class="flex items-center gap-x-2 sm:gap-x-4">
          <!-- Theme Toggle -->
          <ThemeToggle />
          
          <!-- Pending approvals -->
          <RouterLink
            to="/admin-panel/approvals"
            class="relative p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            title="Kutayotgan tasdiqlashlar"
          >
            <ClipboardDocumentCheckIcon class="h-6 w-6" />
            <span
              v-if="pendingCount > 0"
              class="absolute -top-1 -right-1 h-5 w-5 rounded-full bg-yellow-500 flex items-center justify-center text-xs font-bold text-white"
            >
              {{ pendingCount > 9 ? '9+' : pendingCount }}
            </span>
          </RouterLink>
          
          <!-- User dropdown -->
          <Menu as="div" class="relative">
            <MenuButton class="flex items-center gap-3 p-1.5 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-semibold text-sm">
                {{ userInitials }}
              </div>
              <div class="hidden sm:block text-left">
                <p class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ user?.full_name || 'Foydalanuvchi' }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">Administrator</p>
              </div>
              <ChevronDownIcon class="hidden sm:block w-4 h-4 text-gray-400" />
            </MenuButton>
            
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <MenuItems class="absolute right-0 mt-2 w-56 origin-top-right rounded-xl bg-white dark:bg-gray-800 shadow-lg ring-1 ring-black/5 dark:ring-white/10 focus:outline-none py-1">
                <MenuItem v-slot="{ active }">
                  <RouterLink
                    to="/admin-panel/profile"
                    class="flex items-center gap-3 px-4 py-2 text-sm"
                    :class="active ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white' : 'text-gray-700 dark:text-gray-300'"
                  >
                    <UserCircleIcon class="w-5 h-5" />
                    Profilim
                  </RouterLink>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <RouterLink
                    to="/admin-panel/profile/edit"
                    class="flex items-center gap-3 px-4 py-2 text-sm"
                    :class="active ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white' : 'text-gray-700 dark:text-gray-300'"
                  >
                    <Cog6ToothIcon class="w-5 h-5" />
                    Sozlamalar
                  </RouterLink>
                </MenuItem>
                <div class="border-t border-gray-200 dark:border-gray-700 my-1"></div>
                <MenuItem v-slot="{ active }">
                  <button
                    @click="handleLogout"
                    class="flex w-full items-center gap-3 px-4 py-2 text-sm"
                    :class="active ? 'bg-red-50 dark:bg-red-900/50 text-red-700 dark:text-red-300' : 'text-gray-700 dark:text-gray-300'"
                  >
                    <ArrowRightOnRectangleIcon class="w-5 h-5" />
                    Chiqish
                  </button>
                </MenuItem>
              </MenuItems>
            </transition>
          </Menu>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { useUserStore, usePortfolioStore } from '@/stores'
import { ThemeToggle } from '@/components/common'
import {
  Bars3Icon,
  MagnifyingGlassIcon,
  ClipboardDocumentCheckIcon,
  UserCircleIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  ChevronDownIcon
} from '@heroicons/vue/24/outline'

defineEmits(['toggleSidebar'])

const router = useRouter()
const authStore = useUserStore()
const portfolioStore = usePortfolioStore()

const user = computed(() => authStore.user)
const pendingCount = computed(() => portfolioStore.stats?.pending_count || 0)

const userInitials = computed(() => {
  const name = user.value?.full_name || ''
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase() || 'U'
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>
