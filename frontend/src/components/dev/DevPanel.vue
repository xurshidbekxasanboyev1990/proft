<template>
  <div v-if="isDevMode" class="fixed bottom-4 right-4 z-50">
    <!-- Toggle Button -->
    <button
      @click="isOpen = !isOpen"
      class="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white p-3 sm:p-4 rounded-full shadow-lg shadow-purple-500/30 transition-all duration-300 hover:scale-110"
      title="Dev Panel"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    </button>

    <!-- Backdrop for mobile -->
    <div 
      v-if="isOpen" 
      class="fixed inset-0 bg-black/50 backdrop-blur-sm sm:hidden -z-10"
      @click="isOpen = false"
    ></div>

    <!-- Panel -->
    <div 
      v-if="isOpen"
      class="fixed sm:absolute bottom-0 sm:bottom-16 left-0 sm:left-auto right-0 sm:right-0 
             bg-white dark:bg-slate-900 
             rounded-t-2xl sm:rounded-xl 
             shadow-2xl shadow-black/20 dark:shadow-black/50
             border-t sm:border border-gray-200 dark:border-slate-700
             p-4 sm:p-5
             w-full sm:w-96
             max-h-[85vh] sm:max-h-[80vh]
             overflow-hidden"
    >
      <!-- Header -->
      <div class="flex justify-between items-center mb-4 pb-3 border-b border-gray-100 dark:border-slate-800">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-lg flex items-center justify-center">
            <span class="text-white text-sm">🛠️</span>
          </div>
          <h3 class="text-lg font-bold text-gray-900 dark:text-white">Dev Panel</h3>
        </div>
        <button 
          @click="isOpen = false" 
          class="p-2 rounded-lg text-gray-400 hover:text-gray-600 dark:text-slate-500 dark:hover:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Current Role Badge -->
      <div class="mb-4 p-3 rounded-xl" :class="roleBgColor">
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-600 dark:text-slate-400">Joriy rol:</span>
          <span class="px-3 py-1 rounded-full text-sm font-bold" :class="roleBadgeColor">
            {{ currentRole?.toUpperCase() }}
          </span>
        </div>
      </div>

      <!-- Role Switcher -->
      <div class="mb-4">
        <label class="block text-xs font-semibold text-gray-500 dark:text-slate-500 uppercase tracking-wider mb-2">
          Rolni almashtirish
        </label>
        <div class="grid grid-cols-3 gap-2">
          <button
            v-for="r in roles"
            :key="r.value"
            @click="switchRole(r.value)"
            :class="[
              'px-3 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200',
              currentRole === r.value 
                ? r.activeClass 
                : 'bg-gray-100 dark:bg-slate-800 text-gray-600 dark:text-slate-400 hover:bg-gray-200 dark:hover:bg-slate-700 hover:scale-105'
            ]"
          >
            {{ r.label }}
          </button>
        </div>
      </div>

      <!-- Quick Links -->
      <div class="border-t border-gray-100 dark:border-slate-800 pt-4">
        <label class="block text-xs font-semibold text-gray-500 dark:text-slate-500 uppercase tracking-wider mb-3">
          Tezkor havolalar
        </label>
        <div class="space-y-3 max-h-48 sm:max-h-60 overflow-y-auto pr-1 scrollbar-thin">
          <div v-for="group in quickLinks" :key="group.title" class="mb-2">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-1.5 h-1.5 rounded-full" :class="group.color"></div>
              <span class="text-xs font-bold text-gray-700 dark:text-slate-300 uppercase">
                {{ group.title }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-1.5">
              <router-link
                v-for="link in group.links"
                :key="link.to"
                :to="link.to"
                class="block px-2.5 py-1.5 text-xs font-medium rounded-lg transition-all duration-200
                       text-gray-700 dark:text-slate-300
                       bg-gray-50 dark:bg-slate-800/50
                       hover:bg-indigo-50 dark:hover:bg-indigo-900/30
                       hover:text-indigo-600 dark:hover:text-indigo-400
                       hover:translate-x-0.5"
                @click="isOpen = false"
              >
                {{ link.label }}
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Login Button -->
      <div class="border-t border-gray-100 dark:border-slate-800 pt-4 mt-4">
        <button
          @click="goToLogin"
          class="w-full px-4 py-3 bg-gradient-to-r from-red-500 to-rose-600 hover:from-red-600 hover:to-rose-700 text-white rounded-xl font-semibold shadow-lg shadow-red-500/20 transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
        >
          🔑 Login sahifasiga o'tish
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores'

const router = useRouter()
const userStore = useUserStore()

const isOpen = ref(false)
const isDevMode = import.meta.env.VITE_DEV_MODE === 'true'

const currentRole = computed(() => userStore.role)

const roles = [
  { value: 'teacher', label: 'Teacher', activeClass: 'bg-gradient-to-r from-emerald-500 to-green-600 text-white shadow-lg shadow-green-500/30' },
  { value: 'admin', label: 'Admin', activeClass: 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg shadow-blue-500/30' },
  { value: 'superadmin', label: 'Super', activeClass: 'bg-gradient-to-r from-purple-500 to-violet-600 text-white shadow-lg shadow-purple-500/30' }
]

const roleBgColor = computed(() => {
  switch (currentRole.value) {
    case 'superadmin': return 'bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800'
    case 'admin': return 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800'
    case 'teacher': return 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800'
    default: return 'bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700'
  }
})

const roleBadgeColor = computed(() => {
  switch (currentRole.value) {
    case 'superadmin': return 'bg-purple-500 text-white'
    case 'admin': return 'bg-blue-500 text-white'
    case 'teacher': return 'bg-green-500 text-white'
    default: return 'bg-gray-500 text-white'
  }
})

const quickLinks = [
  {
    title: 'Auth',
    color: 'bg-gray-500',
    links: [
      { to: '/login', label: '🔑 Login' },
    ]
  },
  {
    title: 'Teacher',
    color: 'bg-green-500',
    links: [
      { to: '/teacher', label: '📊 Dashboard' },
      { to: '/teacher/portfolios', label: '📁 Portfolio' },
      { to: '/teacher/portfolios/new', label: '➕ Yaratish' },
      { to: '/teacher/tasks', label: '📝 Topshiriqlar' },
      { to: '/teacher/responses', label: '📤 Javoblar' },
      { to: '/teacher/scores', label: '⭐ Ballar' },
      { to: '/teacher/notifications', label: '🔔 Xabarlar' },
      { to: '/teacher/profile', label: '👤 Profil' },
    ]
  },
  {
    title: 'Admin',
    color: 'bg-blue-500',
    links: [
      { to: '/admin-panel', label: '📊 Dashboard' },
      { to: '/admin-panel/approvals', label: '✅ Tasdiqlash' },
      { to: '/admin-panel/teachers', label: '👨‍🏫 O\'qituvchilar' },
      { to: '/admin-panel/categories', label: '📂 Kategoriyalar' },
      { to: '/admin-panel/tasks', label: '📝 Topshiriqlar' },
      { to: '/admin-panel/tasks/new', label: '➕ Yangi topshiriq' },
      { to: '/admin-panel/scoring', label: '📋 Baholash' },
      { to: '/admin-panel/score-history', label: '📜 Ball tarixi' },
    ]
  },
  {
    title: 'SuperAdmin',
    color: 'bg-purple-500',
    links: [
      { to: '/super-admin', label: '📊 Dashboard' },
      { to: '/super-admin/users', label: '👥 Foydalanuvchi' },
      { to: '/super-admin/users/new', label: '➕ Yaratish' },
      { to: '/super-admin/approvals', label: '✅ Tasdiqlash' },
      { to: '/super-admin/categories', label: '📂 Kategoriya' },
      { to: '/super-admin/tasks', label: '📝 Topshiriqlar' },
      { to: '/super-admin/analytics', label: '📈 Analitika' },
      { to: '/super-admin/reports', label: '📑 Hisobotlar' },
    ]
  }
]

function switchRole(newRole) {
  if (userStore.user) {
    userStore.user.role = newRole
    
    if (newRole === 'teacher') {
      router.push('/teacher')
    } else if (newRole === 'admin') {
      router.push('/admin-panel')
    } else if (newRole === 'superadmin') {
      router.push('/super-admin')
    }
  }
}

function goToLogin() {
  userStore.isAuthenticated = false
  router.push('/login')
  isOpen.value = false
}
</script>
