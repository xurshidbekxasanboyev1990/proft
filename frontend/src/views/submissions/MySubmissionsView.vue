<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Mening javoblarim</h1>
        <p class="mt-1 text-sm text-gray-500">
          Siz yuborgan barcha javoblar va ularning holati
        </p>
      </div>
    </div>

    <!-- Stats cards -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <StatsCard 
        title="Jami javoblar" 
        :value="stats.total" 
        icon="folder" 
        color="gray" 
      />
      <StatsCard 
        title="Tekshirilmoqda" 
        :value="stats.pending" 
        icon="clock" 
        color="warning" 
      />
      <StatsCard 
        title="Baholangan" 
        :value="stats.graded" 
        icon="check" 
        color="success" 
      />
      <StatsCard 
        title="O'rtacha ball" 
        :value="stats.averageGrade + '%'" 
        icon="chart" 
        color="primary" 
      />
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
      <div class="flex flex-col sm:flex-row gap-4">
        <!-- Search -->
        <div class="flex-1">
          <SearchInput
            v-model="filters.search"
            placeholder="Topshiriq nomi bo'yicha qidirish..."
          />
        </div>

        <!-- Status filter -->
        <select
          v-model="filters.status"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        >
          <option value="">Barcha holatlar</option>
          <option value="pending">Tekshirilmoqda</option>
          <option value="graded">Baholangan</option>
          <option value="returned">Qaytarilgan</option>
        </select>

        <!-- Date filter -->
        <input
          v-model="filters.date"
          type="date"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="space-y-4">
      <SkeletonLoader v-for="i in 5" :key="i" type="card" />
    </div>

    <!-- Submissions list -->
    <div v-else-if="filteredSubmissions.length > 0" class="space-y-4">
      <div
        v-for="submission in filteredSubmissions"
        :key="submission.id"
        class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
      >
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <!-- Left: Info -->
          <div class="flex items-start gap-4">
            <div 
              class="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
              :style="{ backgroundColor: submission.assignment?.category?.color + '20' || '#E5E7EB' }"
            >
              <DocumentTextIcon 
                class="w-6 h-6" 
                :style="{ color: submission.assignment?.category?.color || '#6B7280' }"
              />
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">
                {{ submission.assignment?.title || 'Topshiriq' }}
              </h3>
              <p class="text-sm text-gray-500 mt-1">
                {{ submission.assignment?.category?.name }}
              </p>
              <div class="flex items-center gap-4 mt-2 text-sm text-gray-500">
                <span class="flex items-center gap-1">
                  <CalendarIcon class="w-4 h-4" />
                  {{ formatDate(submission.submitted_at) }}
                </span>
                <span v-if="submission.files_count > 0" class="flex items-center gap-1">
                  <PaperClipIcon class="w-4 h-4" />
                  {{ submission.files_count }} fayl
                </span>
              </div>
            </div>
          </div>

          <!-- Right: Status & Score -->
          <div class="flex items-center gap-6">
            <!-- Status -->
            <div class="text-center">
              <StatusBadge :status="submission.status" />
            </div>

            <!-- Score -->
            <div v-if="submission.status === 'graded'" class="text-center">
              <div class="text-2xl font-bold" :class="getScoreColor(submission.grade, submission.max_score)">
                {{ submission.grade }}
              </div>
              <div class="text-xs text-gray-500">
                / {{ submission.max_score }}
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-2">
              <button
                @click="viewSubmission(submission)"
                class="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                title="Ko'rish"
              >
                <EyeIcon class="w-5 h-5" />
              </button>
              <button
                v-if="submission.status === 'returned'"
                @click="resubmit(submission)"
                class="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                title="Qayta yuborish"
              >
                <ArrowPathIcon class="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        <!-- Feedback -->
        <div 
          v-if="submission.feedback" 
          class="mt-4 p-4 bg-gray-50 rounded-lg border-l-4"
          :class="submission.status === 'graded' ? 'border-success-500' : 'border-warning-500'"
        >
          <p class="text-sm font-medium text-gray-700 mb-1">Baholovchi izohi:</p>
          <p class="text-sm text-gray-600">{{ submission.feedback }}</p>
          <p class="text-xs text-gray-400 mt-2">
            {{ submission.graded_by }} - {{ formatDate(submission.graded_at) }}
          </p>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <EmptyState
      v-else
      title="Javoblar topilmadi"
      description="Siz hali birorta javob yubormadingiz"
      type="folder"
    >
      <template #action>
        <RouterLink
          to="/my-assignments"
          class="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          <ClipboardDocumentListIcon class="w-5 h-5" />
          Topshiriqlarni ko'rish
        </RouterLink>
      </template>
    </EmptyState>

    <!-- Pagination -->
    <Pagination
      v-if="filteredSubmissions.length > 0"
      :current-page="pagination.page"
      :total-pages="pagination.totalPages"
      :total-items="pagination.total"
      @page-change="handlePageChange"
      class="mt-6"
    />

    <!-- View Modal -->
    <BaseModal
      :show="showViewModal"
      @close="showViewModal = false"
      title="Javob tafsilotlari"
      size="lg"
    >
      <div v-if="selectedSubmission" class="space-y-4">
        <!-- Assignment info -->
        <div class="p-4 bg-gray-50 rounded-lg">
          <h4 class="font-medium text-gray-900">{{ selectedSubmission.assignment?.title }}</h4>
          <p class="text-sm text-gray-500 mt-1">{{ selectedSubmission.assignment?.category?.name }}</p>
        </div>

        <!-- Content -->
        <div>
          <h5 class="text-sm font-medium text-gray-700 mb-2">Javob matni:</h5>
          <div class="p-4 bg-white border border-gray-200 rounded-lg text-gray-700 whitespace-pre-wrap">
            {{ selectedSubmission.content }}
          </div>
        </div>

        <!-- Links -->
        <div v-if="selectedSubmission.links?.length > 0">
          <h5 class="text-sm font-medium text-gray-700 mb-2">Havolalar:</h5>
          <ul class="space-y-1">
            <li v-for="(link, i) in selectedSubmission.links" :key="i">
              <a 
                :href="link" 
                target="_blank" 
                class="text-primary-600 hover:underline text-sm"
              >
                {{ link }}
              </a>
            </li>
          </ul>
        </div>

        <!-- Files -->
        <div v-if="selectedSubmission.files?.length > 0">
          <h5 class="text-sm font-medium text-gray-700 mb-2">Fayllar:</h5>
          <div class="flex flex-wrap gap-2">
            <a
              v-for="file in selectedSubmission.files"
              :key="file.id"
              :href="file.url"
              target="_blank"
              class="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg text-sm hover:bg-gray-200 transition-colors"
            >
              <PaperClipIcon class="w-4 h-4 text-gray-500" />
              {{ file.name }}
            </a>
          </div>
        </div>

        <!-- Grade info -->
        <div v-if="selectedSubmission.status === 'graded'" class="p-4 bg-success-50 rounded-lg">
          <div class="flex items-center justify-between">
            <span class="text-success-700 font-medium">Ball:</span>
            <span class="text-2xl font-bold text-success-700">
              {{ selectedSubmission.grade }} / {{ selectedSubmission.max_score }}
            </span>
          </div>
          <div v-if="selectedSubmission.feedback" class="mt-3 pt-3 border-t border-success-200">
            <p class="text-sm text-success-700">{{ selectedSubmission.feedback }}</p>
          </div>
        </div>
      </div>

      <template #footer>
        <button
          @click="showViewModal = false"
          class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
        >
          Yopish
        </button>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import {
  DocumentTextIcon,
  CalendarIcon,
  PaperClipIcon,
  EyeIcon,
  ArrowPathIcon,
  ClipboardDocumentListIcon
} from '@heroicons/vue/24/outline'
import { StatsCard, SearchInput, SkeletonLoader, EmptyState, StatusBadge, Pagination, BaseModal } from '@/components/common'
import { formatDate } from '@/utils/date'

const router = useRouter()

const isLoading = ref(true)
const showViewModal = ref(false)
const selectedSubmission = ref(null)

const filters = ref({
  search: '',
  status: '',
  date: ''
})

const pagination = ref({
  page: 1,
  totalPages: 1,
  total: 0
})

const stats = ref({
  total: 0,
  pending: 0,
  graded: 0,
  averageGrade: 0
})

// Mock submissions data
const submissions = ref([
  {
    id: 1,
    assignment: { id: 1, title: 'Ilmiy maqola yozish', category: { name: 'Ilmiy maqola', color: '#3B82F6' } },
    content: 'Bu mening ilmiy maqolam. Pedagogika sohasida zamonaviy usullar haqida...',
    submitted_at: new Date().toISOString(),
    status: 'graded',
    grade: 85,
    max_score: 100,
    files_count: 2,
    feedback: 'Juda yaxshi ish! Maqola mazmunli va strukturali yozilgan.',
    graded_by: 'Admin User',
    graded_at: new Date().toISOString(),
    links: ['https://example.com/article'],
    files: [{ id: 1, name: 'maqola.pdf', url: '#' }]
  },
  {
    id: 2,
    assignment: { id: 2, title: 'Esse tayyorlash', category: { name: 'Esse', color: '#10B981' } },
    content: 'Zamonaviy ta\'lim metodlari haqida esse...',
    submitted_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'pending',
    grade: null,
    max_score: 50,
    files_count: 1,
    feedback: null,
    graded_by: null,
    graded_at: null,
    links: [],
    files: [{ id: 2, name: 'esse.docx', url: '#' }]
  },
  {
    id: 3,
    assignment: { id: 3, title: 'Loyiha hisoboti', category: { name: 'Hisobot', color: '#F59E0B' } },
    content: 'Loyiha hisoboti...',
    submitted_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'returned',
    grade: null,
    max_score: 100,
    files_count: 0,
    feedback: 'Hisobot to\'liq emas. Iltimos, natijalar bo\'limini qo\'shing.',
    graded_by: 'Admin User',
    graded_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    links: [],
    files: []
  }
])

const filteredSubmissions = computed(() => {
  let result = [...submissions.value]

  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    result = result.filter(s => 
      s.assignment?.title?.toLowerCase().includes(search)
    )
  }

  if (filters.value.status) {
    result = result.filter(s => s.status === filters.value.status)
  }

  if (filters.value.date) {
    const filterDate = new Date(filters.value.date).toDateString()
    result = result.filter(s => 
      new Date(s.submitted_at).toDateString() === filterDate
    )
  }

  return result
})

function getScoreColor(grade, maxScore) {
  const percentage = (grade / maxScore) * 100
  if (percentage >= 80) return 'text-success-600'
  if (percentage >= 60) return 'text-warning-600'
  return 'text-danger-600'
}

function viewSubmission(submission) {
  selectedSubmission.value = submission
  showViewModal.value = true
}

function resubmit(submission) {
  router.push(`/assignments/${submission.assignment?.id}/submit`)
}

function handlePageChange(page) {
  pagination.value.page = page
  // Fetch new page
}

async function loadData() {
  isLoading.value = true
  try {
    // Calculate stats
    stats.value = {
      total: submissions.value.length,
      pending: submissions.value.filter(s => s.status === 'pending').length,
      graded: submissions.value.filter(s => s.status === 'graded').length,
      averageGrade: Math.round(
        submissions.value
          .filter(s => s.grade !== null)
          .reduce((acc, s) => acc + (s.grade / s.max_score) * 100, 0) / 
        (submissions.value.filter(s => s.grade !== null).length || 1)
      )
    }
    pagination.value.total = submissions.value.length
  } finally {
    isLoading.value = false
  }
}

onMounted(loadData)
</script>
