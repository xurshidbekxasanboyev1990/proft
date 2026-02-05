<template>
  <div class="flex flex-col h-full">
    <!-- Logo (mobile) -->
    <div class="flex items-center justify-between h-16 lg:hidden border-b border-gray-200 px-4 -mx-6">
      <RouterLink to="/dashboard" class="flex items-center gap-2">
        <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-lg">P</span>
        </div>
        <span class="text-xl font-bold text-gray-900">Proft</span>
      </RouterLink>
      <button @click="$emit('close')" class="p-2 rounded-lg text-gray-500 hover:bg-gray-100">
        <XMarkIcon class="w-6 h-6" />
      </button>
    </div>
    
    <!-- Navigation -->
    <nav class="flex-1 pt-6 space-y-1">
      <!-- Main Navigation -->
      <div class="space-y-1">
        <p class="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
          Asosiy
        </p>
        
        <RouterLink 
          v-for="item in mainNavigation" 
          :key="item.name"
          :to="item.to"
          :class="[
            'sidebar-link',
            isActive(item.to) ? 'active' : ''
          ]"
          @click="$emit('close')"
        >
          <component :is="item.icon" />
          {{ item.name }}
        </RouterLink>
      </div>
      
      <!-- Teacher Navigation -->
      <div v-if="userStore.isTeacher || userStore.isSuperAdmin" class="pt-6 space-y-1">
        <p class="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
          Portfolio
        </p>
        
        <RouterLink 
          v-for="item in teacherNavigation" 
          :key="item.name"
          :to="item.to"
          :class="[
            'sidebar-link',
            isActive(item.to) ? 'active' : ''
          ]"
          @click="$emit('close')"
        >
          <component :is="item.icon" />
          {{ item.name }}
        </RouterLink>
      </div>
      
      <!-- Admin Navigation -->
      <div v-if="userStore.isAdminOrSuperAdmin" class="pt-6 space-y-1">
        <p class="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
          Tasdiqlash
        </p>
        
        <RouterLink 
          v-for="item in adminNavigation" 
          :key="item.name"
          :to="item.to"
          :class="[
            'sidebar-link',
            isActive(item.to) ? 'active' : ''
          ]"
          @click="$emit('close')"
        >
          <component :is="item.icon" />
          {{ item.name }}
          <span 
            v-if="item.badge && portfolioStore.stats.pending > 0" 
            class="ml-auto bg-danger-100 text-danger-600 text-xs font-medium px-2 py-0.5 rounded-full"
          >
            {{ portfolioStore.stats.pending }}
          </span>
        </RouterLink>
      </div>
      
      <!-- Super Admin Navigation -->
      <div v-if="userStore.isSuperAdmin" class="pt-6 space-y-1">
        <p class="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
          Boshqaruv
        </p>
        
        <RouterLink 
          v-for="item in superAdminNavigation" 
          :key="item.name"
          :to="item.to"
          :class="[
            'sidebar-link',
            isActive(item.to) ? 'active' : ''
          ]"
          @click="$emit('close')"
        >
          <component :is="item.icon" />
          {{ item.name }}
        </RouterLink>
      </div>
    </nav>
    
    <!-- Footer -->
    <div class="border-t border-gray-200 pt-4 pb-2">
      <div class="px-4 py-2 text-xs text-gray-400">
        &copy; 2026 Proft v1.0
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, useRoute } from 'vue-router'
import { 
  XMarkIcon,
  HomeIcon,
  FolderIcon,
  PlusCircleIcon,
  ClipboardDocumentCheckIcon,
  UsersIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  UserCircleIcon,
  ClipboardDocumentListIcon,
  TagIcon,
  DocumentChartBarIcon,
  ArrowDownTrayIcon,
  AcademicCapIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'
import { useUserStore, usePortfolioStore } from '@/stores'

defineEmits(['close'])

const route = useRoute()
const userStore = useUserStore()
const portfolioStore = usePortfolioStore()

// Main navigation (all users)
const mainNavigation = [
  { name: 'Bosh sahifa', to: '/dashboard', icon: HomeIcon },
  { name: 'Profil', to: '/profile', icon: UserCircleIcon }
]

// Teacher navigation
const teacherNavigation = [
  { name: 'Portfoliolarim', to: '/portfolios', icon: FolderIcon },
  { name: 'Yangi portfolio', to: '/portfolios/create', icon: PlusCircleIcon },
  { name: 'Mening topshiriqlarim', to: '/my-assignments', icon: ClipboardDocumentListIcon }
]

// Admin navigation
const adminNavigation = [
  { name: 'Tasdiqlash', to: '/approval', icon: ClipboardDocumentCheckIcon, badge: true },
  { name: 'Topshiriqlar', to: '/assignments', icon: ClipboardDocumentListIcon },
  { name: 'Kategoriyalar', to: '/categories', icon: TagIcon },
  { name: 'Javoblar', to: '/submissions', icon: AcademicCapIcon },
  { name: 'Ball tarixi', to: '/score-history', icon: ClockIcon },
  { name: 'Analitika', to: '/analytics', icon: DocumentChartBarIcon },
  { name: 'Hisobotlar', to: '/reports', icon: ArrowDownTrayIcon }
]

// Super Admin navigation
const superAdminNavigation = [
  { name: 'Admin panel', to: '/admin', icon: Cog6ToothIcon },
  { name: 'Foydalanuvchilar', to: '/admin/users', icon: UsersIcon }
]

function isActive(path) {
  if (path === '/dashboard') {
    return route.path === '/dashboard'
  }
  return route.path.startsWith(path)
}
</script>
