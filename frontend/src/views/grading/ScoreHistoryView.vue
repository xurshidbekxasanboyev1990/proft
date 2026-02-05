<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Ball tarixi</h1>
        <p class="mt-1 text-sm text-gray-500">
          Barcha baholash o'zgarishlari tarixi
        </p>
      </div>
      <button @click="exportHistory" class="btn-secondary" :disabled="isExporting">
        <ArrowDownTrayIcon class="w-5 h-5 mr-2" />
        Export
      </button>
    </div>

    <!-- Filters -->
    <div class="card mb-6">
      <div class="card-body">
        <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <!-- Search -->
          <div>
            <SearchInput
              v-model="filters.search"
              placeholder="Qidirish..."
              @search="fetchHistory"
            />
          </div>

          <!-- Date from -->
          <div>
            <label class="text-xs text-gray-500">Boshlanish sanasi</label>
            <input
              v-model="filters.date_from"
              type="date"
              class="form-input"
              @change="fetchHistory"
            />
          </div>

          <!-- Date to -->
          <div>
            <label class="text-xs text-gray-500">Tugash sanasi</label>
            <input
              v-model="filters.date_to"
              type="date"
              class="form-input"
              @change="fetchHistory"
            />
          </div>

          <!-- Change type -->
          <div>
            <label class="text-xs text-gray-500">O'zgarish turi</label>
            <select v-model="filters.change_type" class="form-input" @change="fetchHistory">
              <option value="">Barchasi</option>
              <option value="grade">Baholash</option>
              <option value="score_update">Ball yangilash</option>
              <option value="multiplier">Ko'paytiruvchi</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- History table -->
    <div class="card">
      <div class="card-body p-0">
        <div v-if="isLoading" class="p-6">
          <SkeletonLoader type="table" />
        </div>

        <div v-else-if="history.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sana</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Topshiriq</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">O'qituvchi</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">O'zgarish</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Eski qiymat</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Yangi qiymat</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Kim tomonidan</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr 
                v-for="item in history" 
                :key="item.id" 
                class="hover:bg-gray-50 cursor-pointer"
                @click="openDetail(item)"
              >
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(item.created_at) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <RouterLink 
                    :to="`${basePath}/${item.assignment?.id}`"
                    class="text-sm font-medium text-primary-600 hover:text-primary-700"
                  >
                    {{ item.assignment?.title || '-' }}
                  </RouterLink>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ item.teacher?.full_name || '-' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    class="px-2 py-1 text-xs font-medium rounded-full"
                    :class="getChangeTypeClass(item.change_type)"
                  >
                    {{ getChangeTypeLabel(item.change_type) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ item.old_value ?? '-' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="text-sm font-medium" :class="getValueChangeClass(item)">
                    {{ item.new_value ?? '-' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ item.changed_by?.full_name || 'Sistema' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <EmptyState
          v-else
          title="Tarix topilmadi"
          description="Ball o'zgarishlari tarixi bo'sh"
          type="folder"
        />
      </div>

      <!-- Pagination -->
      <div v-if="pagination.total_pages > 1" class="card-footer">
        <Pagination
          :current-page="pagination.page"
          :total-pages="pagination.total_pages"
          :total-count="pagination.total_count"
          @page-change="handlePageChange"
        />
      </div>
    </div>

    <!-- Detail Modal -->
    <ScoreHistoryDetailModal
      :is-open="showDetailModal"
      :item="selectedItem"
      :related-history="getRelatedHistory(selectedItem)"
      @close="showDetailModal = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowDownTrayIcon } from '@heroicons/vue/24/outline'
import { SearchInput, SkeletonLoader, EmptyState, Pagination } from '@/components/common'
import { ScoreHistoryDetailModal } from '@/components/grading'
import { assignmentService } from '@/services'
import dayjs from 'dayjs'

const route = useRoute()

// Dynamic base path based on current route
const basePath = computed(() => {
  const path = route.path
  if (path.startsWith('/teacher')) return '/teacher/tasks'
  if (path.startsWith('/admin-panel')) return '/admin-panel/tasks'
  if (path.startsWith('/super-admin')) return '/super-admin/tasks'
  return '/admin-panel/tasks'
})

const isLoading = ref(true)
const isExporting = ref(false)
const showDetailModal = ref(false)
const selectedItem = ref(null)
const history = ref([])

const filters = reactive({
  search: '',
  date_from: '',
  date_to: '',
  change_type: ''
})

const pagination = reactive({
  page: 1,
  total_pages: 1,
  total_count: 0
})

onMounted(() => {
  fetchHistory()
})

async function fetchHistory() {
  isLoading.value = true
  try {
    const params = {
      page: pagination.page,
      ...filters
    }
    
    // Remove empty values
    Object.keys(params).forEach(key => {
      if (!params[key]) delete params[key]
    })

    const response = await assignmentService.getAllScoreHistory(params)
    history.value = response.results || response || []
    
    if (response.count !== undefined) {
      pagination.total_count = response.count
      pagination.total_pages = Math.ceil(response.count / 20)
    }
  } catch (error) {
    console.error('Failed to fetch score history:', error)
  } finally {
    isLoading.value = false
  }
}

function handlePageChange(page) {
  pagination.page = page
  fetchHistory()
}

function formatDate(date) {
  return dayjs(date).format('D MMM YYYY, HH:mm')
}

function getChangeTypeLabel(type) {
  const labels = {
    grade: 'Baholash',
    score_update: 'Ball yangilash',
    multiplier: 'Ko\'paytiruvchi',
    reset: 'Qayta o\'rnatish'
  }
  return labels[type] || type
}

function getChangeTypeClass(type) {
  const classes = {
    grade: 'bg-success-100 text-success-700',
    score_update: 'bg-primary-100 text-primary-700',
    multiplier: 'bg-warning-100 text-warning-700',
    reset: 'bg-gray-100 text-gray-700'
  }
  return classes[type] || 'bg-gray-100 text-gray-700'
}

function getValueChangeClass(item) {
  if (item.new_value > item.old_value) return 'text-success-600'
  if (item.new_value < item.old_value) return 'text-danger-600'
  return 'text-gray-900'
}

function openDetail(item) {
  selectedItem.value = item
  showDetailModal.value = true
}

function getRelatedHistory(item) {
  if (!item?.assignment?.id) return []
  return history.value.filter(h => h.assignment?.id === item.assignment.id)
}

async function exportHistory() {
  isExporting.value = true
  try {
    // Backend API: POST /api/analytics/export/
    const exportData = {
      type: 'score_history',
      format: 'excel',
      date_from: filters.date_from || undefined,
      date_to: filters.date_to || undefined
    }
    
    // DEV_MODE da mock CSV yaratish
    if (import.meta.env.VITE_DEV_MODE === 'true') {
      const headers = ['Sana', 'Topshiriq', 'O\'qituvchi', 'O\'zgarish turi', 'Eski qiymat', 'Yangi qiymat', 'Kim tomonidan']
      const rows = history.value.map(item => [
        formatDate(item.created_at),
        item.assignment?.title || '-',
        item.teacher?.full_name || '-',
        getChangeTypeLabel(item.change_type),
        item.old_value ?? '-',
        item.new_value ?? '-',
        item.changed_by?.full_name || 'Sistema'
      ])
      
      const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n')
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `ball_tarixi_${dayjs().format('YYYY-MM-DD')}.csv`
      a.click()
      URL.revokeObjectURL(url)
    } else {
      const response = await fetch('/api/analytics/export/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(exportData)
      })
      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `ball_tarixi_${dayjs().format('YYYY-MM-DD')}.xlsx`
      a.click()
      URL.revokeObjectURL(url)
    }
  } catch (error) {
    console.error('Export failed:', error)
  } finally {
    isExporting.value = false
  }
}
</script>
