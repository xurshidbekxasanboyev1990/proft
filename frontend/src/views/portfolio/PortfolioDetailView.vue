<template>
  <div class="animate-fade-in">
    <LoadingSpinner v-if="isLoading" fullscreen text="Yuklanmoqda..." />
    
    <template v-else-if="portfolio">
      <!-- Page header -->
      <div class="mb-6">
        <RouterLink to="/portfolios" class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-2">
          <ArrowLeftIcon class="w-4 h-4 mr-1" />
          Orqaga
        </RouterLink>
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ portfolio.title }}</h1>
            <div class="flex items-center gap-3 mt-2">
              <StatusBadge :variant="portfolio.status" dot>
                {{ portfolio.status_display }}
              </StatusBadge>
              <span class="text-sm text-gray-500">{{ portfolio.category_display }}</span>
            </div>
          </div>
          
          <div class="flex items-center gap-2">
            <!-- PDF Export button -->
            <button @click="exportPdf" class="btn-secondary" :disabled="isExporting">
              <LoadingSpinner v-if="isExporting" size="xs" />
              <template v-else>
                <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
                PDF
              </template>
            </button>
            
            <template v-if="portfolio.permissions?.can_edit">
              <RouterLink :to="`/portfolios/${portfolio.id}/edit`" class="btn-secondary">
                <PencilIcon class="w-4 h-4 mr-2" />
                Tahrirlash
              </RouterLink>
              <button @click="showDeleteModal = true" class="btn-danger">
                <TrashIcon class="w-4 h-4 mr-2" />
                O'chirish
              </button>
            </template>
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Description -->
          <div class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Tavsif</h2>
            </div>
            <div class="card-body prose prose-sm max-w-none">
              <p class="whitespace-pre-wrap">{{ portfolio.description }}</p>
            </div>
          </div>
          
          <!-- Review info -->
          <div v-if="portfolio.review_comment" class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Ko'rib chiqish natijalari</h2>
            </div>
            <div class="card-body">
              <AlertBox 
                :type="portfolio.status === 'approved' ? 'success' : portfolio.status === 'rejected' ? 'error' : 'info'"
                :title="portfolio.status === 'approved' ? 'Tasdiqlangan' : portfolio.status === 'rejected' ? 'Rad etilgan' : 'Kutilmoqda'"
              >
                {{ portfolio.review_comment }}
              </AlertBox>
              <div v-if="portfolio.reviewed_by" class="mt-4 flex items-center gap-2 text-sm text-gray-500">
                <UserIcon class="w-4 h-4" />
                <span>{{ portfolio.reviewed_by.full_name }}</span>
                <span>•</span>
                <span>{{ formatDate(portfolio.reviewed_at) }}</span>
              </div>
            </div>
          </div>
          
          <!-- Attachments -->
          <div class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">
                Fayllar ({{ portfolio.attachments?.length || 0 }})
              </h2>
            </div>
            <div class="card-body">
              <div v-if="portfolio.attachments?.length > 0" class="space-y-2">
                <a
                  v-for="file in portfolio.attachments"
                  :key="file.id"
                  :href="file.file"
                  target="_blank"
                  class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div class="w-10 h-10 rounded-lg bg-primary-100 flex items-center justify-center">
                    <DocumentIcon class="w-5 h-5 text-primary-600" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900 truncate">{{ file.title || 'Fayl' }}</p>
                    <p class="text-xs text-gray-500">{{ formatFileSize(file.file_size) }} • {{ file.file_type }}</p>
                  </div>
                  <ArrowDownTrayIcon class="w-5 h-5 text-gray-400" />
                </a>
              </div>
              <EmptyState v-else title="Fayllar yo'q" description="Bu portfolioga hech qanday fayl biriktirilmagan" type="document" />
            </div>
          </div>

          <!-- Comments -->
          <div class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">
                Izohlar ({{ portfolio.comments?.length || 0 }})
              </h2>
            </div>
            <div class="card-body">
              <!-- Comment form -->
              <form @submit.prevent="addComment" class="mb-6">
                <textarea
                  v-model="newComment"
                  rows="3"
                  class="form-input"
                  placeholder="Izoh qo'shish..."
                ></textarea>
                <div class="mt-2 flex justify-end">
                  <button type="submit" class="btn-primary btn-sm" :disabled="!newComment.trim() || isAddingComment">
                    <LoadingSpinner v-if="isAddingComment" size="xs" color="white" />
                    <span v-else>Yuborish</span>
                  </button>
                </div>
              </form>
              
              <!-- Comments list -->
              <div v-if="portfolio.comments?.length > 0" class="space-y-4">
                <div v-for="comment in portfolio.comments" :key="comment.id" class="flex gap-3">
                  <div class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span class="text-xs font-medium text-gray-600">
                      {{ comment.author.username.substring(0, 2).toUpperCase() }}
                    </span>
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-1">
                      <span class="text-sm font-medium text-gray-900">{{ comment.author.full_name || comment.author.username }}</span>
                      <span class="text-xs text-gray-400">{{ formatDate(comment.created_at) }}</span>
                    </div>
                    <p class="text-sm text-gray-600">{{ comment.content }}</p>
                  </div>
                </div>
              </div>
              <EmptyState v-else title="Izohlar yo'q" description="Birinchi izohni qoldiring" type="document" />
            </div>
          </div>
        </div>
        
        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Info card -->
          <div class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Ma'lumotlar</h2>
            </div>
            <div class="card-body space-y-4">
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">Muallif</span>
                <span class="text-sm font-medium text-gray-900">{{ portfolio.teacher?.full_name }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">Bo'lim</span>
                <span class="text-sm font-medium text-gray-900">{{ portfolio.teacher?.department || '-' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">Yaratilgan</span>
                <span class="text-sm font-medium text-gray-900">{{ formatDate(portfolio.created_at) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">Yangilangan</span>
                <span class="text-sm font-medium text-gray-900">{{ formatDate(portfolio.updated_at) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">Ommaviy</span>
                <span class="text-sm font-medium text-gray-900">{{ portfolio.is_public ? 'Ha' : "Yo'q" }}</span>
              </div>
            </div>
          </div>
          
          <!-- History -->
          <div v-if="portfolio.history?.length > 0" class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Tarix</h2>
            </div>
            <div class="card-body p-0">
              <div class="divide-y divide-gray-200">
                <div v-for="entry in portfolio.history" :key="entry.id" class="p-4 text-sm">
                  <div class="flex items-center gap-2 mb-1">
                    <StatusBadge v-if="entry.old_status" :variant="entry.old_status" size="sm">
                      {{ entry.old_status }}
                    </StatusBadge>
                    <span v-if="entry.old_status">→</span>
                    <StatusBadge :variant="entry.new_status" size="sm">
                      {{ entry.new_status }}
                    </StatusBadge>
                  </div>
                  <p class="text-xs text-gray-400">
                    {{ entry.changed_by }} • {{ formatDate(entry.created_at) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <!-- Not found -->
    <EmptyState 
      v-else
      title="Portfolio topilmadi"
      description="Bu portfolio mavjud emas yoki o'chirilgan"
      action-text="Ortga qaytish"
      @action="$router.push('/portfolios')"
    />
    
    <!-- Delete modal -->
    <ConfirmModal
      :is-open="showDeleteModal"
      title="Portfolioni o'chirish"
      message="Bu portfolioni o'chirishga ishonchingiz komilmi?"
      type="danger"
      :is-loading="isDeleting"
      @confirm="handleDelete"
      @cancel="showDeleteModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeftIcon, PencilIcon, TrashIcon, UserIcon, DocumentIcon, ArrowDownTrayIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner, StatusBadge, AlertBox, EmptyState, ConfirmModal } from '@/components/common'
import { usePortfolioStore } from '@/stores'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const portfolioStore = usePortfolioStore()

const isLoading = ref(true)
const showDeleteModal = ref(false)
const isDeleting = ref(false)
const isExporting = ref(false)
const newComment = ref('')
const isAddingComment = ref(false)

const portfolio = computed(() => portfolioStore.currentPortfolio)

onMounted(async () => {
  try {
    await portfolioStore.fetchPortfolio(route.params.id)
  } catch (error) {
    console.error('Failed to fetch portfolio:', error)
  } finally {
    isLoading.value = false
  }
})

function formatDate(date) {
  return dayjs(date).format('D MMM YYYY, HH:mm')
}

function formatFileSize(bytes) {
  if (!bytes) return '-'
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
}

async function addComment() {
  if (!newComment.value.trim()) return
  
  isAddingComment.value = true
  try {
    await portfolioStore.addComment(portfolio.value.id, newComment.value.trim())
    newComment.value = ''
    // Refresh portfolio to get new comment
    await portfolioStore.fetchPortfolio(route.params.id)
  } catch (error) {
    console.error('Failed to add comment:', error)
  } finally {
    isAddingComment.value = false
  }
}

async function handleDelete() {
  isDeleting.value = true
  try {
    await portfolioStore.deletePortfolio(portfolio.value.id)
    router.push('/portfolios')
  } catch (error) {
    console.error('Failed to delete:', error)
  } finally {
    isDeleting.value = false
  }
}

async function exportPdf() {
  isExporting.value = true
  try {
    // Backend API: POST /api/analytics/export/
    const response = await fetch('/api/analytics/export/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: 'portfolios',
        format: 'pdf',
        portfolio_id: portfolio.value.id
      })
    })
    
    // DEV_MODE da mock PDF yaratish
    if (import.meta.env.VITE_DEV_MODE === 'true') {
      // Create simple text blob as mock PDF
      const content = `Portfolio: ${portfolio.value.title}\n\nTavsif: ${portfolio.value.description}\n\nMuallif: ${portfolio.value.teacher?.full_name}\nSana: ${new Date().toLocaleDateString()}`
      const blob = new Blob([content], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `portfolio_${portfolio.value.id}.txt`
      a.click()
      URL.revokeObjectURL(url)
    } else {
      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `portfolio_${portfolio.value.id}.pdf`
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
