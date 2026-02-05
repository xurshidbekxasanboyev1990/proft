<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Admin Panel</h1>
      <p class="mt-1 text-sm text-gray-500">
        Tizim boshqaruvi va statistika
      </p>
    </div>
    
    <!-- Stats overview -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatsCard
        title="Jami foydalanuvchilar"
        :value="stats.totalUsers"
        icon="users"
        color="blue"
      />
      <StatsCard
        title="Jami portfoliolar"
        :value="stats.totalPortfolios"
        icon="folder"
        color="green"
      />
      <StatsCard
        title="Kutilayotgan"
        :value="stats.pendingPortfolios"
        icon="clock"
        color="warning"
      />
      <StatsCard
        title="Bugun tasdiqlangan"
        :value="stats.approvedToday"
        icon="check"
        color="success"
      />
    </div>
    
    <!-- Quick actions -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <!-- Recent portfolios -->
      <div class="card">
        <div class="card-header flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">So'nggi portfoliolar</h2>
          <RouterLink to="/approval" class="text-sm text-primary-600 hover:text-primary-700">
            Barchasini ko'rish →
          </RouterLink>
        </div>
        <div class="card-body p-0">
          <div v-if="isLoading" class="p-4">
            <SkeletonLoader v-for="i in 5" :key="i" type="list-item" class="mb-2" />
          </div>
          <div v-else-if="recentPortfolios.length > 0" class="divide-y divide-gray-200">
            <div 
              v-for="portfolio in recentPortfolios" 
              :key="portfolio.id"
              class="p-4 hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-center justify-between">
                <div class="flex-1 min-w-0">
                  <RouterLink 
                    :to="`/approval/${portfolio.id}`"
                    class="font-medium text-gray-900 hover:text-primary-600 truncate block"
                  >
                    {{ portfolio.title }}
                  </RouterLink>
                  <p class="text-xs text-gray-500 mt-0.5">
                    {{ portfolio.teacher?.full_name }} • {{ formatDate(portfolio.created_at) }}
                  </p>
                </div>
                <StatusBadge :variant="portfolio.status" size="sm">
                  {{ portfolio.status_display }}
                </StatusBadge>
              </div>
            </div>
          </div>
          <EmptyState 
            v-else
            title="Portfolio yo'q"
            description="Hozircha portfolio mavjud emas"
            type="folder"
            class="py-8"
          />
        </div>
      </div>
      
      <!-- Quick links -->
      <div class="card">
        <div class="card-header">
          <h2 class="text-lg font-semibold text-gray-900">Tezkor havolalar</h2>
        </div>
        <div class="card-body">
          <div class="grid grid-cols-2 gap-4">
            <RouterLink 
              to="/approval?status=pending" 
              class="flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors"
            >
              <div class="w-10 h-10 rounded-lg bg-warning-100 flex items-center justify-center">
                <ClockIcon class="w-5 h-5 text-warning-600" />
              </div>
              <div>
                <p class="font-medium text-gray-900">Kutilayotgan</p>
                <p class="text-sm text-gray-500">{{ stats.pendingPortfolios }} ta</p>
              </div>
            </RouterLink>
            
            <RouterLink 
              v-if="userStore.isSuperAdmin"
              to="/admin/users" 
              class="flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors"
            >
              <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                <UsersIcon class="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p class="font-medium text-gray-900">Foydalanuvchilar</p>
                <p class="text-sm text-gray-500">{{ stats.totalUsers }} ta</p>
              </div>
            </RouterLink>
            
            <RouterLink 
              v-if="userStore.isSuperAdmin"
              to="/admin/reports" 
              class="flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors"
            >
              <div class="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
                <ChartBarIcon class="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <p class="font-medium text-gray-900">Hisobotlar</p>
                <p class="text-sm text-gray-500">Statistika</p>
              </div>
            </RouterLink>
            
            <RouterLink 
              to="/profile" 
              class="flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors"
            >
              <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center">
                <UserIcon class="w-5 h-5 text-gray-600" />
              </div>
              <div>
                <p class="font-medium text-gray-900">Profil</p>
                <p class="text-sm text-gray-500">Sozlamalar</p>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Recent activity -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-lg font-semibold text-gray-900">So'nggi faollik</h2>
      </div>
      <div class="card-body p-0 max-h-80 overflow-y-auto">
        <div v-if="recentActivities.length > 0" class="divide-y divide-gray-200">
          <div 
            v-for="activity in recentActivities" 
            :key="activity.id"
            class="p-4 flex items-start gap-3"
          >
            <div 
              class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0"
              :class="getActivityClass(activity.action)"
            >
              <component :is="getActivityIcon(activity.action)" class="w-4 h-4" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm text-gray-900">
                <span class="font-medium">{{ activity.user }}</span>
                {{ getActivityText(activity.action) }}
                <span class="font-medium">{{ activity.target }}</span>
              </p>
              <p class="text-xs text-gray-500 mt-0.5">{{ formatDate(activity.created_at) }}</p>
            </div>
          </div>
        </div>
        <EmptyState 
          v-else
          title="Faollik yo'q"
          description="Hozircha faollik mavjud emas"
          type="activity"
          class="py-8"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  ClockIcon, 
  UsersIcon, 
  ChartBarIcon, 
  UserIcon,
  CheckCircleIcon,
  XCircleIcon,
  PlusCircleIcon,
  PencilSquareIcon
} from '@heroicons/vue/24/outline'
import { StatsCard, StatusBadge, SkeletonLoader, EmptyState } from '@/components/common'
import { useUserStore, usePortfolioStore } from '@/stores'
import dayjs from 'dayjs'

const userStore = useUserStore()
const portfolioStore = usePortfolioStore()

const isLoading = ref(true)
const recentPortfolios = ref([])
const recentActivities = ref([])

const stats = computed(() => ({
  totalUsers: portfolioStore.stats?.total_users || 0,
  totalPortfolios: portfolioStore.stats?.total || 0,
  pendingPortfolios: portfolioStore.stats?.pending || 0,
  approvedToday: portfolioStore.stats?.approved_today || 0
}))

onMounted(async () => {
  try {
    await portfolioStore.fetchStats()
    
    // Fetch recent portfolios
    await portfolioStore.fetchPortfolios({ page_size: 5 })
    recentPortfolios.value = portfolioStore.portfolios.slice(0, 5)
    
    // Mock recent activities (in real app, fetch from API)
    recentActivities.value = [
      { id: 1, user: 'Admin', action: 'approved', target: 'Ilmiy maqola', created_at: new Date() },
      { id: 2, user: "O'qituvchi", action: 'created', target: 'Dars ishlanma', created_at: new Date(Date.now() - 3600000) },
      { id: 3, user: 'Admin', action: 'rejected', target: 'Konferensiya', created_at: new Date(Date.now() - 7200000) }
    ]
  } catch (error) {
    console.error('Failed to load dashboard:', error)
  } finally {
    isLoading.value = false
  }
})

function formatDate(date) {
  return dayjs(date).format('D MMM, HH:mm')
}

function getActivityIcon(action) {
  const icons = {
    created: PlusCircleIcon,
    approved: CheckCircleIcon,
    rejected: XCircleIcon,
    updated: PencilSquareIcon
  }
  return icons[action] || PlusCircleIcon
}

function getActivityClass(action) {
  const classes = {
    created: 'bg-blue-100 text-blue-600',
    approved: 'bg-green-100 text-green-600',
    rejected: 'bg-red-100 text-red-600',
    updated: 'bg-yellow-100 text-yellow-600'
  }
  return classes[action] || 'bg-gray-100 text-gray-600'
}

function getActivityText(action) {
  const texts = {
    created: 'yangi portfolio yaratdi:',
    approved: 'portfolioni tasdiqladi:',
    rejected: 'portfolioni rad etdi:',
    updated: 'portfolioni yangiladi:'
  }
  return texts[action] || action
}
</script>
