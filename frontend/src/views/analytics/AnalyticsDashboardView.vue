<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Analitika</h1>
        <p class="mt-1 text-sm text-gray-500">
          Portfolio va topshiriqlar statistikasi
        </p>
      </div>

      <div class="flex items-center gap-3">
        <!-- Period filter -->
        <select v-model="period" @change="fetchData" class="form-input">
          <option v-for="p in CHART_PERIODS" :key="p.value" :value="p.value">
            {{ p.label }}
          </option>
        </select>

        <!-- Export button -->
        <button @click="showExportModal = true" class="btn-secondary">
          <ArrowDownTrayIcon class="w-5 h-5 mr-2" />
          Export
        </button>
      </div>
    </div>

    <!-- Overview stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <StatsCard
        title="Jami o'qituvchilar"
        :value="overview?.total_teachers || 0"
        icon="users"
        color="primary"
      />
      <StatsCard
        title="Jami portfoliolar"
        :value="overview?.total_portfolios || 0"
        icon="folder"
        color="success"
      />
      <StatsCard
        title="Jami topshiriqlar"
        :value="overview?.total_assignments || 0"
        icon="document"
        color="warning"
      />
      <StatsCard
        title="O'rtacha ball"
        :value="overview?.average_score?.toFixed(1) || 0"
        icon="star"
        color="info"
      />
    </div>

    <!-- Charts row 1 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Portfolio trend -->
      <div class="card">
        <div class="card-header">
          <h2 class="text-lg font-semibold text-gray-900">Portfolio tendensiyasi</h2>
        </div>
        <div class="card-body">
          <div v-if="isLoading" class="h-64 flex items-center justify-center">
            <LoadingSpinner />
          </div>
          <div v-else class="h-64">
            <LineChart :data="portfolioTrendData" />
          </div>
        </div>
      </div>

      <!-- Assignment status distribution -->
      <div class="card">
        <div class="card-header">
          <h2 class="text-lg font-semibold text-gray-900">Topshiriq statuslari</h2>
        </div>
        <div class="card-body">
          <div v-if="isLoading" class="h-64 flex items-center justify-center">
            <LoadingSpinner />
          </div>
          <div v-else class="h-64">
            <DoughnutChart :data="assignmentStatusData" />
          </div>
        </div>
      </div>
    </div>

    <!-- Charts row 2 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Category distribution -->
      <div class="card">
        <div class="card-header">
          <h2 class="text-lg font-semibold text-gray-900">Kategoriya taqsimoti</h2>
        </div>
        <div class="card-body">
          <div v-if="isLoading" class="h-64 flex items-center justify-center">
            <LoadingSpinner />
          </div>
          <div v-else class="h-64">
            <PieChart :data="categoryDistributionData" />
          </div>
        </div>
      </div>

      <!-- Score distribution -->
      <div class="card">
        <div class="card-header">
          <h2 class="text-lg font-semibold text-gray-900">Ball taqsimoti</h2>
        </div>
        <div class="card-body">
          <div v-if="isLoading" class="h-64 flex items-center justify-center">
            <LoadingSpinner />
          </div>
          <div v-else class="h-64">
            <BarChart :data="scoreDistributionData" />
          </div>
        </div>
      </div>
    </div>

    <!-- Teachers performance table -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-lg font-semibold text-gray-900">O'qituvchilar reytingi</h2>
      </div>
      <div class="card-body p-0">
        <div v-if="isLoading" class="p-6">
          <SkeletonLoader type="table" />
        </div>
        <div v-else-if="teachersPerformance.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">#</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">O'qituvchi</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Portfoliolar</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Bajarilgan</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">O'rtacha ball</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Progress</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(teacher, index) in teachersPerformance" :key="teacher.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ index + 1 }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center mr-3">
                      <span class="text-xs font-medium text-primary-600">
                        {{ getInitials(teacher.full_name) }}
                      </span>
                    </div>
                    <div>
                      <div class="text-sm font-medium text-gray-900">{{ teacher.full_name }}</div>
                      <div class="text-sm text-gray-500">{{ teacher.department || '-' }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ teacher.portfolio_count }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ teacher.completed_assignments }} / {{ teacher.total_assignments }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="text-sm font-medium" :class="getScoreColor(teacher.average_score)">
                    {{ teacher.average_score?.toFixed(1) || 0 }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div
                      class="h-2 rounded-full"
                      :class="getProgressColor(teacher.progress)"
                      :style="{ width: `${teacher.progress || 0}%` }"
                    ></div>
                  </div>
                  <span class="text-xs text-gray-500 mt-1">{{ teacher.progress || 0 }}%</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <EmptyState v-else title="Ma'lumot yo'q" description="O'qituvchilar statistikasi topilmadi" />
      </div>
    </div>

    <!-- Export modal -->
    <ExportModal
      :is-open="showExportModal"
      @close="showExportModal = false"
      @export="handleExport"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ArrowDownTrayIcon } from '@heroicons/vue/24/outline'
import { StatsCard, LoadingSpinner, SkeletonLoader, EmptyState } from '@/components/common'
import { LineChart, PieChart, BarChart, DoughnutChart } from '@/components/analytics'
import ExportModal from './ExportModal.vue'
import { useAnalyticsStore } from '@/stores'
import { CHART_PERIODS } from '@/services'

const analyticsStore = useAnalyticsStore()

const isLoading = computed(() => analyticsStore.isLoading)
const overview = computed(() => analyticsStore.dashboardOverview)
const teachersPerformance = computed(() => analyticsStore.teachersPerformance)

const period = ref('month')
const showExportModal = ref(false)

// Chart data computed properties
const portfolioTrendData = computed(() => {
  const data = analyticsStore.portfolioTrend
  return {
    labels: data?.labels || [],
    datasets: [
      {
        label: 'Portfoliolar',
        data: data?.values || []
      }
    ]
  }
})

const assignmentStatusData = computed(() => {
  const data = analyticsStore.assignmentStatus
  return {
    labels: data?.labels || ['Kutilmoqda', 'Bajarildi', 'Muddati o\'tgan'],
    values: data?.values || [0, 0, 0],
    colors: ['#F59E0B', '#22C55E', '#EF4444']
  }
})

const categoryDistributionData = computed(() => {
  const data = analyticsStore.categoryDistribution
  return {
    labels: data?.labels || [],
    values: data?.values || []
  }
})

const scoreDistributionData = computed(() => {
  const data = analyticsStore.scoreDistribution || {
    labels: ['0-20', '21-40', '41-60', '61-80', '81-100'],
    values: [0, 0, 0, 0, 0]
  }
  return {
    labels: data.labels,
    datasets: [
      {
        label: "O'qituvchilar soni",
        data: data.values
      }
    ]
  }
})

onMounted(() => {
  fetchData()
})

async function fetchData() {
  await Promise.all([
    analyticsStore.fetchDashboardOverview(period.value),
    analyticsStore.fetchAllCharts(period.value),
    analyticsStore.fetchTeachersPerformance()
  ])
}

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

function getScoreColor(score) {
  if (score >= 80) return 'text-success-600'
  if (score >= 60) return 'text-warning-600'
  return 'text-danger-600'
}

function getProgressColor(progress) {
  if (progress >= 80) return 'bg-success-500'
  if (progress >= 60) return 'bg-warning-500'
  return 'bg-danger-500'
}

async function handleExport(options) {
  await analyticsStore.quickExport(options.format, options.data_type)
  showExportModal.value = false
}
</script>
