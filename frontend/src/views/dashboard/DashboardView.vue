<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">
        Xush kelibsiz, {{ userStore.fullName }}! 👋
      </h1>
      <p class="mt-1 text-sm text-gray-500">
        Portfolio tizimining umumiy ko'rinishi
      </p>
    </div>
    
    <!-- Stats cards -->
    <div v-if="isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <SkeletonLoader v-for="i in 4" :key="i" type="stats" />
    </div>
    
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatsCard
        title="Jami portfoliolar"
        :value="stats.total"
        :icon="FolderIcon"
        color="primary"
      />
      <StatsCard
        title="Kutilmoqda"
        :value="stats.pending"
        :icon="ClockIcon"
        color="warning"
      />
      <StatsCard
        title="Tasdiqlangan"
        :value="stats.approved"
        :icon="CheckCircleIcon"
        color="success"
      />
      <StatsCard
        title="Rad etilgan"
        :value="stats.rejected"
        :icon="XCircleIcon"
        color="danger"
      />
    </div>
    
    <!-- Quick actions -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <!-- Quick actions card -->
      <div class="card">
        <div class="card-header">
          <h2 class="text-lg font-semibold text-gray-900">Tezkor amallar</h2>
        </div>
        <div class="card-body">
          <div class="grid grid-cols-2 gap-4">
            <RouterLink 
              v-if="userStore.isTeacher || userStore.isSuperAdmin"
              to="/portfolios/create" 
              class="flex flex-col items-center justify-center p-4 bg-primary-50 rounded-xl hover:bg-primary-100 transition-colors group"
            >
              <PlusCircleIcon class="w-8 h-8 text-primary-600 mb-2 group-hover:scale-110 transition-transform" />
              <span class="text-sm font-medium text-primary-700">Yangi portfolio</span>
            </RouterLink>
            
            <RouterLink 
              v-if="userStore.isTeacher || userStore.isSuperAdmin"
              to="/portfolios" 
              class="flex flex-col items-center justify-center p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors group"
            >
              <FolderIcon class="w-8 h-8 text-gray-600 mb-2 group-hover:scale-110 transition-transform" />
              <span class="text-sm font-medium text-gray-700">Portfoliolarim</span>
            </RouterLink>
            
            <RouterLink 
              v-if="userStore.isAdminOrSuperAdmin"
              to="/approval" 
              class="flex flex-col items-center justify-center p-4 bg-warning-50 rounded-xl hover:bg-warning-100 transition-colors group relative"
            >
              <ClipboardDocumentCheckIcon class="w-8 h-8 text-warning-600 mb-2 group-hover:scale-110 transition-transform" />
              <span class="text-sm font-medium text-warning-700">Tasdiqlash</span>
              <span 
                v-if="stats.pending > 0" 
                class="absolute top-2 right-2 bg-danger-500 text-white text-xs font-medium px-2 py-0.5 rounded-full"
              >
                {{ stats.pending }}
              </span>
            </RouterLink>
            
            <RouterLink 
              to="/profile" 
              class="flex flex-col items-center justify-center p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors group"
            >
              <UserCircleIcon class="w-8 h-8 text-gray-600 mb-2 group-hover:scale-110 transition-transform" />
              <span class="text-sm font-medium text-gray-700">Profil</span>
            </RouterLink>
          </div>
        </div>
      </div>
      
      <!-- Recent activity -->
      <div class="card">
        <div class="card-header flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">So'nggi faoliyat</h2>
          <RouterLink to="/portfolios" class="text-sm text-primary-600 hover:text-primary-700 font-medium">
            Barchasini ko'rish →
          </RouterLink>
        </div>
        <div class="card-body p-0">
          <div v-if="stats.recent && stats.recent.length > 0" class="divide-y divide-gray-200">
            <RouterLink 
              v-for="item in stats.recent" 
              :key="item.id"
              :to="`/portfolios/${item.id}`"
              class="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
            >
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 truncate">{{ item.title }}</p>
                <p class="text-xs text-gray-500">{{ formatDate(item.updated_at) }}</p>
              </div>
              <StatusBadge :variant="item.status" size="sm">
                {{ getStatusLabel(item.status) }}
              </StatusBadge>
            </RouterLink>
          </div>
          <EmptyState 
            v-else 
            title="Hozircha faoliyat yo'q"
            description="Portfolio yaratishni boshlang"
            type="folder"
          />
        </div>
      </div>
    </div>
    
    <!-- Category chart (for admins) -->
    <div v-if="userStore.isAdminOrSuperAdmin" class="card">
      <div class="card-header">
        <h2 class="text-lg font-semibold text-gray-900">Kategoriyalar bo'yicha</h2>
      </div>
      <div class="card-body">
        <div v-if="Object.keys(stats.by_category || {}).length > 0" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          <div 
            v-for="(count, category) in stats.by_category" 
            :key="category"
            class="text-center p-4 bg-gray-50 rounded-xl"
          >
            <p class="text-2xl font-bold text-gray-900">{{ count }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ getCategoryLabel(category) }}</p>
          </div>
        </div>
        <EmptyState 
          v-else 
          title="Ma'lumot yo'q"
          description="Portfolio yaratilganda statistika ko'rinadi"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { 
  FolderIcon, 
  ClockIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  PlusCircleIcon,
  ClipboardDocumentCheckIcon,
  UserCircleIcon
} from '@heroicons/vue/24/outline'
import { StatsCard, SkeletonLoader, StatusBadge, EmptyState } from '@/components/common'
import { useUserStore, usePortfolioStore } from '@/stores'
import { PORTFOLIO_CATEGORIES } from '@/services'
import dayjs from 'dayjs'
import 'dayjs/locale/uz'

dayjs.locale('uz')

const userStore = useUserStore()
const portfolioStore = usePortfolioStore()

const isLoading = ref(true)

const stats = computed(() => portfolioStore.stats)

onMounted(async () => {
  try {
    await portfolioStore.fetchStats()
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  } finally {
    isLoading.value = false
  }
})

function formatDate(date) {
  return dayjs(date).format('D MMMM, HH:mm')
}

function getStatusLabel(status) {
  const labels = {
    pending: 'Kutilmoqda',
    approved: 'Tasdiqlangan',
    rejected: 'Rad etilgan'
  }
  return labels[status] || status
}

function getCategoryLabel(category) {
  const cat = PORTFOLIO_CATEGORIES.find(c => c.value === category)
  return cat?.label || category
}
</script>
