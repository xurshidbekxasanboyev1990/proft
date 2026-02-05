<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Tasdiqlash</h1>
        <p class="mt-1 text-sm text-gray-500">
          O'qituvchilar portfoliolarini ko'rib chiqing va tasdiqlang
        </p>
      </div>
      
      <!-- Stats -->
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2 px-3 py-1.5 bg-warning-50 rounded-lg">
          <ClockIcon class="w-5 h-5 text-warning-600" />
          <span class="text-sm font-medium text-warning-700">{{ stats.pending }} ta kutilmoqda</span>
        </div>
      </div>
    </div>
    
    <!-- Filters -->
    <div class="card mb-6">
      <div class="card-body">
        <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <!-- Search -->
          <div class="sm:col-span-2">
            <div class="relative">
              <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="filters.search"
                type="text"
                placeholder="Qidirish..."
                class="form-input pl-10"
                @input="debouncedSearch"
              />
            </div>
          </div>
          
          <!-- Status filter -->
          <select v-model="filters.status" @change="applyFilters" class="form-input">
            <option value="">Barcha statuslar</option>
            <option value="pending">Kutilmoqda</option>
            <option value="approved">Tasdiqlangan</option>
            <option value="rejected">Rad etilgan</option>
          </select>
          
          <!-- Category filter -->
          <select v-model="filters.category" @change="applyFilters" class="form-input">
            <option value="">Barcha kategoriyalar</option>
            <option v-for="cat in PORTFOLIO_CATEGORIES" :key="cat.value" :value="cat.value">
              {{ cat.label }}
            </option>
          </select>
        </div>
      </div>
    </div>
    
    <!-- Loading state -->
    <div v-if="isLoading" class="space-y-4">
      <SkeletonLoader v-for="i in 5" :key="i" type="table-row" />
    </div>
    
    <!-- Portfolios table -->
    <div v-else-if="portfolios.length > 0" class="card">
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>Portfolio</th>
              <th>O'qituvchi</th>
              <th>Kategoriya</th>
              <th>Status</th>
              <th>Sana</th>
              <th class="text-right">Amallar</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 bg-white">
            <tr v-for="portfolio in portfolios" :key="portfolio.id">
              <td>
                <RouterLink :to="`/approval/${portfolio.id}`" class="font-medium text-gray-900 hover:text-primary-600">
                  {{ portfolio.title }}
                </RouterLink>
                <p class="text-xs text-gray-500 mt-0.5 line-clamp-1">{{ portfolio.description }}</p>
              </td>
              <td>
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                    <span class="text-xs font-medium text-gray-600">
                      {{ portfolio.teacher.username.substring(0, 2).toUpperCase() }}
                    </span>
                  </div>
                  <div>
                    <p class="text-sm font-medium text-gray-900">{{ portfolio.teacher.full_name || portfolio.teacher.username }}</p>
                  </div>
                </div>
              </td>
              <td>
                <span class="text-sm text-gray-600">{{ portfolio.category_display }}</span>
              </td>
              <td>
                <StatusBadge :variant="portfolio.status" dot>
                  {{ portfolio.status_display }}
                </StatusBadge>
              </td>
              <td>
                <span class="text-sm text-gray-500">{{ formatDate(portfolio.created_at) }}</span>
              </td>
              <td class="text-right">
                <div class="flex items-center justify-end gap-2">
                  <RouterLink :to="`/approval/${portfolio.id}`" class="btn-secondary btn-sm">
                    Ko'rish
                  </RouterLink>
                  <template v-if="portfolio.status === 'pending'">
                    <button @click="handleApprove(portfolio)" class="btn-success btn-sm">
                      <CheckIcon class="w-4 h-4" />
                    </button>
                    <button @click="handleReject(portfolio)" class="btn-danger btn-sm">
                      <XMarkIcon class="w-4 h-4" />
                    </button>
                  </template>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <Pagination
        :current-page="pagination.page"
        :total-pages="pagination.total_pages"
        :total-count="pagination.total_count"
        :page-size="pagination.page_size"
        :has-next="pagination.has_next"
        :has-previous="pagination.has_previous"
        @page-change="handlePageChange"
      />
    </div>
    
    <!-- Empty state -->
    <EmptyState 
      v-else
      title="Portfolio topilmadi"
      :description="filters.status === 'pending' ? 'Kutilayotgan portfoliolar yo\'q' : 'Hech qanday portfolio topilmadi'"
      type="folder"
    />
    
    <!-- Approve modal -->
    <BaseModal :is-open="showApproveModal" title="Portfolioni tasdiqlash" @close="showApproveModal = false">
      <p class="text-sm text-gray-600 mb-4">
        <strong>{{ selectedPortfolio?.title }}</strong> portfoliosini tasdiqlashga ishonchingiz komilmi?
      </p>
      <div>
        <label class="form-label">Izoh (ixtiyoriy)</label>
        <textarea v-model="approvalComment" rows="3" class="form-input" placeholder="Tasdiqlash izohi..."></textarea>
      </div>
      <template #footer>
        <button @click="showApproveModal = false" class="btn-secondary">Bekor qilish</button>
        <button @click="confirmApprove" class="btn-success" :disabled="isProcessing">
          <LoadingSpinner v-if="isProcessing" size="xs" color="white" />
          <span v-else>Tasdiqlash</span>
        </button>
      </template>
    </BaseModal>
    
    <!-- Reject modal -->
    <BaseModal :is-open="showRejectModal" title="Portfolioni rad etish" @close="showRejectModal = false">
      <p class="text-sm text-gray-600 mb-4">
        <strong>{{ selectedPortfolio?.title }}</strong> portfoliosini rad etishga ishonchingiz komilmi?
      </p>
      <div>
        <label class="form-label">Sabab <span class="text-danger-500">*</span></label>
        <textarea 
          v-model="rejectionComment" 
          rows="3" 
          class="form-input" 
          :class="{ 'border-danger-500': rejectionError }"
          placeholder="Rad etish sababini kiriting..."
        ></textarea>
        <p v-if="rejectionError" class="form-error">{{ rejectionError }}</p>
      </div>
      <template #footer>
        <button @click="showRejectModal = false" class="btn-secondary">Bekor qilish</button>
        <button @click="confirmReject" class="btn-danger" :disabled="isProcessing">
          <LoadingSpinner v-if="isProcessing" size="xs" color="white" />
          <span v-else>Rad etish</span>
        </button>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  ClockIcon, 
  MagnifyingGlassIcon,
  CheckIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import { SkeletonLoader, StatusBadge, Pagination, EmptyState, BaseModal, LoadingSpinner } from '@/components/common'
import { usePortfolioStore } from '@/stores'
import { PORTFOLIO_CATEGORIES } from '@/services'
import dayjs from 'dayjs'

const portfolioStore = usePortfolioStore()

const isLoading = computed(() => portfolioStore.isLoading)
const portfolios = computed(() => portfolioStore.portfolios)
const pagination = computed(() => portfolioStore.pagination)
const stats = computed(() => portfolioStore.stats)

const filters = ref({
  search: '',
  status: 'pending',
  category: ''
})

// Modal states
const showApproveModal = ref(false)
const showRejectModal = ref(false)
const selectedPortfolio = ref(null)
const approvalComment = ref('')
const rejectionComment = ref('')
const rejectionError = ref('')
const isProcessing = ref(false)

let searchTimeout = null

onMounted(async () => {
  await Promise.all([
    portfolioStore.fetchPortfolios({ status: 'pending' }),
    portfolioStore.fetchStats()
  ])
})

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 300)
}

function applyFilters() {
  portfolioStore.setFilters({
    search: filters.value.search,
    status: filters.value.status,
    category: filters.value.category
  })
}

function handlePageChange(page) {
  portfolioStore.goToPage(page)
}

function formatDate(date) {
  return dayjs(date).format('D MMM, YYYY')
}

function handleApprove(portfolio) {
  selectedPortfolio.value = portfolio
  approvalComment.value = ''
  showApproveModal.value = true
}

function handleReject(portfolio) {
  selectedPortfolio.value = portfolio
  rejectionComment.value = ''
  rejectionError.value = ''
  showRejectModal.value = true
}

async function confirmApprove() {
  if (!selectedPortfolio.value) return
  
  isProcessing.value = true
  try {
    await portfolioStore.approvePortfolio(selectedPortfolio.value.id, approvalComment.value)
    showApproveModal.value = false
    selectedPortfolio.value = null
    // Refresh stats
    await portfolioStore.fetchStats()
  } catch (error) {
    console.error('Approve failed:', error)
  } finally {
    isProcessing.value = false
  }
}

async function confirmReject() {
  if (!selectedPortfolio.value) return
  
  if (!rejectionComment.value.trim()) {
    rejectionError.value = 'Rad etish sababini kiritish majburiy'
    return
  }
  
  isProcessing.value = true
  try {
    await portfolioStore.rejectPortfolio(selectedPortfolio.value.id, rejectionComment.value)
    showRejectModal.value = false
    selectedPortfolio.value = null
    // Refresh stats
    await portfolioStore.fetchStats()
  } catch (error) {
    console.error('Reject failed:', error)
  } finally {
    isProcessing.value = false
  }
}
</script>
