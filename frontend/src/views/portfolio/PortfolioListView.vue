<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Portfoliolarim</h1>
        <p class="mt-1 text-sm text-gray-500">
          Barcha portfoliolaringizni boshqaring
        </p>
      </div>
      <RouterLink to="/portfolios/create" class="btn-primary">
        <PlusIcon class="w-5 h-5 mr-2" />
        Yangi portfolio
      </RouterLink>
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
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <SkeletonLoader v-for="i in 6" :key="i" type="card" />
    </div>
    
    <!-- Portfolio list -->
    <div v-else-if="portfolios.length > 0">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <PortfolioCard 
          v-for="portfolio in portfolios" 
          :key="portfolio.id" 
          :portfolio="portfolio"
          @delete="handleDelete"
        />
      </div>
      
      <!-- Pagination -->
      <div class="mt-6">
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
    </div>
    
    <!-- Empty state -->
    <EmptyState 
      v-else
      title="Portfolio topilmadi"
      description="Hozircha hech qanday portfolio yo'q. Yangi portfolio yaratishni boshlang!"
      action-text="Yangi portfolio"
      type="folder"
      @action="$router.push('/portfolios/create')"
    />
    
    <!-- Delete confirmation modal -->
    <ConfirmModal
      :is-open="showDeleteModal"
      title="Portfolioni o'chirish"
      message="Bu portfolioni o'chirishga ishonchingiz komilmi? Bu amalni qaytarib bo'lmaydi."
      confirm-text="O'chirish"
      type="danger"
      :is-loading="isDeleting"
      @confirm="confirmDelete"
      @cancel="showDeleteModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { PlusIcon, MagnifyingGlassIcon } from '@heroicons/vue/24/outline'
import { SkeletonLoader, Pagination, EmptyState, ConfirmModal } from '@/components/common'
import PortfolioCard from '@/components/portfolio/PortfolioCard.vue'
import { usePortfolioStore } from '@/stores'
import { PORTFOLIO_CATEGORIES } from '@/services'

const portfolioStore = usePortfolioStore()

const isLoading = computed(() => portfolioStore.isLoading)
const portfolios = computed(() => portfolioStore.portfolios)
const pagination = computed(() => portfolioStore.pagination)

const filters = ref({
  search: '',
  status: '',
  category: ''
})

const showDeleteModal = ref(false)
const isDeleting = ref(false)
const portfolioToDelete = ref(null)

let searchTimeout = null

onMounted(() => {
  portfolioStore.fetchPortfolios()
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

function handleDelete(portfolio) {
  portfolioToDelete.value = portfolio
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!portfolioToDelete.value) return
  
  isDeleting.value = true
  try {
    await portfolioStore.deletePortfolio(portfolioToDelete.value.id)
    showDeleteModal.value = false
    portfolioToDelete.value = null
  } catch (error) {
    console.error('Delete failed:', error)
  } finally {
    isDeleting.value = false
  }
}
</script>
