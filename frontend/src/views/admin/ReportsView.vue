<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Hisobotlar</h1>
      <p class="mt-1 text-sm text-gray-500">
        Portfolio va foydalanuvchilar bo'yicha statistika
      </p>
    </div>
    
    <!-- Date range filter -->
    <div class="card mb-6">
      <div class="card-body">
        <div class="flex flex-col sm:flex-row sm:items-center gap-4">
          <div class="flex items-center gap-2">
            <label class="text-sm font-medium text-gray-700">Davr:</label>
            <select v-model="dateRange" @change="fetchReports" class="form-input w-auto">
              <option value="7">Oxirgi 7 kun</option>
              <option value="30">Oxirgi 30 kun</option>
              <option value="90">Oxirgi 90 kun</option>
              <option value="365">Oxirgi 1 yil</option>
              <option value="all">Barchasi</option>
            </select>
          </div>
          <button @click="exportReport" class="btn-secondary sm:ml-auto">
            <ArrowDownTrayIcon class="w-5 h-5 mr-2" />
            Export (CSV)
          </button>
        </div>
      </div>
    </div>
    
    <LoadingSpinner v-if="isLoading" fullscreen text="Hisobotlar yuklanmoqda..." />
    
    <template v-else>
      <!-- Summary stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <StatsCard
          title="Jami portfoliolar"
          :value="reports.total_portfolios"
          icon="folder"
          color="blue"
        />
        <StatsCard
          title="Tasdiqlangan"
          :value="reports.approved_portfolios"
          icon="check"
          color="green"
          :trend="reports.approved_trend"
        />
        <StatsCard
          title="Kutilayotgan"
          :value="reports.pending_portfolios"
          icon="clock"
          color="warning"
        />
        <StatsCard
          title="Rad etilgan"
          :value="reports.rejected_portfolios"
          icon="x"
          color="red"
        />
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Portfolio status chart -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900">Status bo'yicha taqsimot</h2>
          </div>
          <div class="card-body">
            <div class="aspect-square max-w-xs mx-auto">
              <canvas ref="statusChartRef"></canvas>
            </div>
          </div>
        </div>
        
        <!-- Category chart -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900">Kategoriya bo'yicha</h2>
          </div>
          <div class="card-body">
            <div class="h-72">
              <canvas ref="categoryChartRef"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Activity chart -->
      <div class="card mb-6">
        <div class="card-header">
          <h2 class="text-lg font-semibold text-gray-900">Faollik</h2>
        </div>
        <div class="card-body">
          <div class="h-80">
            <canvas ref="activityChartRef"></canvas>
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Top teachers -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900">Eng faol o'qituvchilar</h2>
          </div>
          <div class="card-body p-0">
            <div class="divide-y divide-gray-200">
              <div 
                v-for="(teacher, index) in reports.top_teachers" 
                :key="teacher.id"
                class="flex items-center justify-between p-4"
              >
                <div class="flex items-center gap-3">
                  <span 
                    class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
                    :class="[
                      index === 0 ? 'bg-yellow-100 text-yellow-800' :
                      index === 1 ? 'bg-gray-100 text-gray-800' :
                      index === 2 ? 'bg-amber-100 text-amber-800' :
                      'bg-gray-50 text-gray-600'
                    ]"
                  >
                    {{ index + 1 }}
                  </span>
                  <div>
                    <p class="font-medium text-gray-900">{{ teacher.full_name || teacher.username }}</p>
                    <p class="text-xs text-gray-500">{{ teacher.department || "Noma'lum" }}</p>
                  </div>
                </div>
                <span class="text-sm font-medium text-gray-600">
                  {{ teacher.portfolio_count }} ta portfolio
                </span>
              </div>
              <div v-if="reports.top_teachers?.length === 0" class="p-4 text-center text-sm text-gray-500">
                Ma'lumot topilmadi
              </div>
            </div>
          </div>
        </div>
        
        <!-- Recent activity -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900">Oxirgi faollik</h2>
          </div>
          <div class="card-body p-0 max-h-96 overflow-y-auto">
            <div class="divide-y divide-gray-200">
              <div 
                v-for="activity in reports.recent_activities" 
                :key="activity.id"
                class="p-4"
              >
                <div class="flex items-start gap-3">
                  <div 
                    class="w-8 h-8 rounded-full flex items-center justify-center"
                    :class="getActivityIconClass(activity.action)"
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
              <div v-if="reports.recent_activities?.length === 0" class="p-4 text-center text-sm text-gray-500">
                Faollik topilmadi
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, shallowRef } from 'vue'
import { 
  ArrowDownTrayIcon, 
  PlusCircleIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  PencilSquareIcon
} from '@heroicons/vue/24/outline'
import { LoadingSpinner, StatsCard } from '@/components/common'
import { Chart, registerables } from 'chart.js'
import dayjs from 'dayjs'
import api from '@/services/api'

Chart.register(...registerables)

const isLoading = ref(true)
const dateRange = ref('30')

const reports = ref({
  total_portfolios: 0,
  approved_portfolios: 0,
  pending_portfolios: 0,
  rejected_portfolios: 0,
  approved_trend: 0,
  status_distribution: [],
  category_distribution: [],
  activity_data: [],
  top_teachers: [],
  recent_activities: []
})

const statusChartRef = ref(null)
const categoryChartRef = ref(null)
const activityChartRef = ref(null)

let statusChart = shallowRef(null)
let categoryChart = shallowRef(null)
let activityChart = shallowRef(null)

onMounted(async () => {
  await fetchReports()
})

async function fetchReports() {
  isLoading.value = true
  try {
    // In a real app, this would call the API
    // const response = await api.get('/api/reports/', { params: { days: dateRange.value } })
    // reports.value = response.data
    
    // Mock data for demonstration
    reports.value = {
      total_portfolios: 156,
      approved_portfolios: 89,
      pending_portfolios: 42,
      rejected_portfolios: 25,
      approved_trend: 12.5,
      status_distribution: [
        { label: 'Tasdiqlangan', value: 89, color: '#10b981' },
        { label: 'Kutilayotgan', value: 42, color: '#f59e0b' },
        { label: 'Rad etilgan', value: 25, color: '#ef4444' }
      ],
      category_distribution: [
        { label: "Ta'lim", value: 45 },
        { label: 'Ilmiy', value: 38 },
        { label: "Tashkiliy", value: 28 },
        { label: "Boshqa", value: 45 }
      ],
      activity_data: {
        labels: getLast7Days(),
        created: [5, 8, 12, 7, 10, 6, 9],
        approved: [3, 6, 8, 5, 7, 4, 6],
        rejected: [1, 2, 1, 2, 1, 1, 2]
      },
      top_teachers: [
        { id: 1, full_name: 'Aliyev Jasur', username: 'jasur', department: 'Informatika', portfolio_count: 12 },
        { id: 2, full_name: "Karimova Dilnoza", username: 'dilnoza', department: 'Matematika', portfolio_count: 10 },
        { id: 3, full_name: 'Rahimov Bobur', username: 'bobur', department: 'Fizika', portfolio_count: 8 },
        { id: 4, full_name: "Yusupova Madina", username: 'madina', department: "Ingliz tili", portfolio_count: 7 },
        { id: 5, full_name: "Normatov Sardor", username: 'sardor', department: 'Kimyo', portfolio_count: 6 }
      ],
      recent_activities: [
        { id: 1, user: 'Aliyev Jasur', action: 'created', target: 'Ilmiy maqola', created_at: new Date() },
        { id: 2, user: 'Admin', action: 'approved', target: 'Dars ishlanma', created_at: new Date(Date.now() - 3600000) },
        { id: 3, user: 'Karimova Dilnoza', action: 'updated', target: 'Metodik qo\'llanma', created_at: new Date(Date.now() - 7200000) },
        { id: 4, user: 'Admin', action: 'rejected', target: 'Konferensiya', created_at: new Date(Date.now() - 10800000) }
      ]
    }
    
    await nextTick()
    initCharts()
  } catch (error) {
    console.error('Failed to fetch reports:', error)
  } finally {
    isLoading.value = false
  }
}

function getLast7Days() {
  const days = []
  for (let i = 6; i >= 0; i--) {
    days.push(dayjs().subtract(i, 'day').format('DD MMM'))
  }
  return days
}

function initCharts() {
  // Destroy existing charts
  if (statusChart.value) statusChart.value.destroy()
  if (categoryChart.value) categoryChart.value.destroy()
  if (activityChart.value) activityChart.value.destroy()
  
  // Status doughnut chart
  if (statusChartRef.value) {
    const ctx = statusChartRef.value.getContext('2d')
    statusChart.value = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: reports.value.status_distribution.map(s => s.label),
        datasets: [{
          data: reports.value.status_distribution.map(s => s.value),
          backgroundColor: reports.value.status_distribution.map(s => s.color),
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    })
  }
  
  // Category bar chart
  if (categoryChartRef.value) {
    const ctx = categoryChartRef.value.getContext('2d')
    categoryChart.value = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: reports.value.category_distribution.map(c => c.label),
        datasets: [{
          label: 'Portfoliolar soni',
          data: reports.value.category_distribution.map(c => c.value),
          backgroundColor: '#3b82f6',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })
  }
  
  // Activity line chart
  if (activityChartRef.value) {
    const ctx = activityChartRef.value.getContext('2d')
    activityChart.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: reports.value.activity_data.labels,
        datasets: [
          {
            label: 'Yaratilgan',
            data: reports.value.activity_data.created,
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            fill: true,
            tension: 0.3
          },
          {
            label: 'Tasdiqlangan',
            data: reports.value.activity_data.approved,
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            fill: true,
            tension: 0.3
          },
          {
            label: 'Rad etilgan',
            data: reports.value.activity_data.rejected,
            borderColor: '#ef4444',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            fill: true,
            tension: 0.3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom'
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })
  }
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

function getActivityIconClass(action) {
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

function formatDate(date) {
  return dayjs(date).format('D MMM, HH:mm')
}

function exportReport() {
  // Generate CSV export
  const headers = ['Ko\'rsatkich', 'Qiymat']
  const rows = [
    ['Jami portfoliolar', reports.value.total_portfolios],
    ['Tasdiqlangan', reports.value.approved_portfolios],
    ['Kutilayotgan', reports.value.pending_portfolios],
    ['Rad etilgan', reports.value.rejected_portfolios]
  ]
  
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.join(','))
  ].join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `hisobot_${dayjs().format('YYYY-MM-DD')}.csv`
  link.click()
}
</script>
