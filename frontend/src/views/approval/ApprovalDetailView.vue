<template>
  <div class="animate-fade-in">
    <LoadingSpinner v-if="isLoading" fullscreen text="Yuklanmoqda..." />
    
    <template v-else-if="portfolio">
      <!-- Page header -->
      <div class="mb-6">
        <RouterLink to="/approval" class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-2">
          <ArrowLeftIcon class="w-4 h-4 mr-1" />
          Orqaga
        </RouterLink>
        <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ portfolio.title }}</h1>
            <div class="flex items-center gap-3 mt-2">
              <StatusBadge :variant="portfolio.status" dot>
                {{ portfolio.status_display }}
              </StatusBadge>
              <span class="text-sm text-gray-500">{{ portfolio.category_display }}</span>
            </div>
          </div>
          
          <!-- Quick approve/reject buttons -->
          <div v-if="portfolio.status === 'pending'" class="flex items-center gap-2">
            <button @click="showApproveModal = true" class="btn-success">
              <CheckIcon class="w-5 h-5 mr-2" />
              Tasdiqlash
            </button>
            <button @click="showRejectModal = true" class="btn-danger">
              <XMarkIcon class="w-5 h-5 mr-2" />
              Rad etish
            </button>
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
          
          <!-- Review comment form -->
          <div v-if="portfolio.status === 'pending'" class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Ko'rib chiqish</h2>
            </div>
            <div class="card-body">
              <div class="mb-4">
                <label class="form-label">Izoh</label>
                <textarea 
                  v-model="reviewComment" 
                  rows="4" 
                  class="form-input"
                  placeholder="Ko'rib chiqish bo'yicha izohlaringizni yozing..."
                ></textarea>
              </div>
              <div class="flex items-center justify-end gap-3">
                <button @click="handleReject" class="btn-danger">
                  <XMarkIcon class="w-4 h-4 mr-2" />
                  Rad etish
                </button>
                <button @click="handleApprove" class="btn-success">
                  <CheckIcon class="w-4 h-4 mr-2" />
                  Tasdiqlash
                </button>
              </div>
            </div>
          </div>
          
          <!-- Previous review info -->
          <div v-if="portfolio.review_comment" class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Oldingi ko'rib chiqish</h2>
            </div>
            <div class="card-body">
              <AlertBox 
                :type="portfolio.status === 'approved' ? 'success' : 'error'"
                :title="portfolio.status === 'approved' ? 'Tasdiqlangan' : 'Rad etilgan'"
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
        </div>
        
        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Teacher info -->
          <div class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">O'qituvchi</h2>
            </div>
            <div class="card-body">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                  <span class="text-lg font-medium text-primary-700">
                    {{ (portfolio.teacher.full_name || portfolio.teacher.username).substring(0, 2).toUpperCase() }}
                  </span>
                </div>
                <div>
                  <p class="font-medium text-gray-900">{{ portfolio.teacher.full_name || portfolio.teacher.username }}</p>
                  <p class="text-sm text-gray-500">{{ portfolio.teacher.position || "O'qituvchi" }}</p>
                </div>
              </div>
              
              <div class="space-y-3 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-500">Bo'lim</span>
                  <span class="font-medium text-gray-900">{{ portfolio.teacher.department || '-' }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Portfolio info -->
          <div class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Ma'lumotlar</h2>
            </div>
            <div class="card-body space-y-3">
              <div class="flex justify-between text-sm">
                <span class="text-gray-500">Kategoriya</span>
                <span class="font-medium text-gray-900">{{ portfolio.category_display }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-500">Yaratilgan</span>
                <span class="font-medium text-gray-900">{{ formatDate(portfolio.created_at) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-500">Yangilangan</span>
                <span class="font-medium text-gray-900">{{ formatDate(portfolio.updated_at) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-500">Ommaviy</span>
                <span class="font-medium text-gray-900">{{ portfolio.is_public ? 'Ha' : "Yo'q" }}</span>
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
    
    <EmptyState 
      v-else
      title="Portfolio topilmadi"
      action-text="Ortga qaytish"
      @action="$router.push('/approval')"
    />
    
    <!-- Approve modal with comment -->
    <BaseModal :is-open="showApproveModal" title="Tasdiqlash" @close="showApproveModal = false">
      <p class="text-sm text-gray-600 mb-4">
        Bu portfolioni tasdiqlashga ishonchingiz komilmi?
      </p>
      <div>
        <label class="form-label">Izoh (ixtiyoriy)</label>
        <textarea 
          v-model="approveComment" 
          rows="3" 
          class="form-input"
          placeholder="Tasdiqlash bo'yicha izoh..."
        ></textarea>
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
    <BaseModal :is-open="showRejectModal" title="Rad etish" @close="showRejectModal = false">
      <p class="text-sm text-gray-600 mb-4">
        Bu portfolioni rad etish sababini ko'rsating:
      </p>
      <div>
        <textarea 
          v-model="rejectComment" 
          rows="4" 
          class="form-input"
          :class="{ 'border-danger-500': rejectError }"
          placeholder="Rad etish sababini kiriting..."
        ></textarea>
        <p v-if="rejectError" class="form-error">{{ rejectError }}</p>
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
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeftIcon, CheckIcon, XMarkIcon, UserIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner, StatusBadge, AlertBox, EmptyState, BaseModal } from '@/components/common'
import { usePortfolioStore } from '@/stores'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const portfolioStore = usePortfolioStore()

const isLoading = ref(true)
const portfolio = computed(() => portfolioStore.currentPortfolio)

const reviewComment = ref('')
const showApproveModal = ref(false)
const showRejectModal = ref(false)
const approveComment = ref('')
const rejectComment = ref('')
const rejectError = ref('')
const isProcessing = ref(false)

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

function handleApprove() {
  approveComment.value = reviewComment.value
  showApproveModal.value = true
}

function handleReject() {
  rejectComment.value = reviewComment.value
  rejectError.value = ''
  showRejectModal.value = true
}

async function confirmApprove() {
  isProcessing.value = true
  try {
    // Backend API: POST /api/portfolios/{id}/approve/ with { comment: string }
    await portfolioStore.approvePortfolio(portfolio.value.id, approveComment.value || reviewComment.value)
    showApproveModal.value = false
    router.push('/approval')
  } catch (error) {
    console.error('Approve failed:', error)
  } finally {
    isProcessing.value = false
  }
}

async function confirmReject() {
  if (!rejectComment.value.trim()) {
    rejectError.value = 'Rad etish sababini kiritish majburiy'
    return
  }
  
  isProcessing.value = true
  try {
    await portfolioStore.rejectPortfolio(portfolio.value.id, rejectComment.value)
    showRejectModal.value = false
    router.push('/approval')
  } catch (error) {
    console.error('Reject failed:', error)
  } finally {
    isProcessing.value = false
  }
}
</script>
