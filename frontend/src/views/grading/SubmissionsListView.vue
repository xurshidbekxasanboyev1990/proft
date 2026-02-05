<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Javoblar</h1>
        <p class="mt-1 text-sm text-gray-500">
          Barcha topshiriq javoblarini ko'ring va baholang
        </p>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <StatsCard title="Jami javoblar" :value="stats.total" icon="folder" color="gray" />
      <StatsCard title="Baholanmagan" :value="stats.ungraded" icon="clock" color="warning" />
      <StatsCard title="Baholangan" :value="stats.graded" icon="check" color="success" />
      <StatsCard title="O'rtacha ball" :value="stats.average_score?.toFixed(1) || 0" icon="star" color="primary" />
    </div>

    <!-- Filters -->
    <div class="card mb-6">
      <div class="card-body">
        <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <!-- Search -->
          <div class="sm:col-span-2">
            <SearchInput
              v-model="filters.search"
              placeholder="O'qituvchi yoki topshiriq qidirish..."
              @search="fetchSubmissions"
            />
          </div>

          <!-- Status filter -->
          <select v-model="filters.graded" @change="fetchSubmissions" class="form-input">
            <option value="">Barchasi</option>
            <option value="false">Baholanmagan</option>
            <option value="true">Baholangan</option>
          </select>

          <!-- Category filter -->
          <select v-model="filters.category" @change="fetchSubmissions" class="form-input">
            <option value="">Barcha kategoriyalar</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Submissions list -->
    <div class="card">
      <div class="card-body p-0">
        <div v-if="isLoading" class="p-6">
          <SkeletonLoader type="table" />
        </div>

        <div v-else-if="submissions.length > 0" class="divide-y divide-gray-200">
          <div
            v-for="submission in submissions"
            :key="submission.id"
            class="p-6 hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-start justify-between gap-4">
              <!-- Left side - submission info -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-3 mb-2">
                  <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                    <span class="text-sm font-medium text-primary-600">
                      {{ getInitials(submission.submitted_by?.full_name) }}
                    </span>
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">{{ submission.submitted_by?.full_name }}</p>
                    <p class="text-sm text-gray-500">{{ formatDate(submission.submitted_at) }}</p>
                  </div>
                </div>

                <RouterLink 
                  :to="`/assignments/${submission.assignment?.id}`"
                  class="text-primary-600 hover:text-primary-700 font-medium"
                >
                  {{ submission.assignment?.title }}
                </RouterLink>

                <p class="text-sm text-gray-600 mt-2 line-clamp-2">{{ submission.content }}</p>

                <!-- Attachments -->
                <div v-if="submission.attachments?.length > 0" class="flex items-center gap-2 mt-3">
                  <PaperClipIcon class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-500">{{ submission.attachments.length }} ta fayl</span>
                </div>
              </div>

              <!-- Right side - grading -->
              <div class="flex-shrink-0 w-64">
                <div v-if="submission.score !== null" class="text-center">
                  <div class="text-3xl font-bold" :class="getScoreColor(submission.score, submission.max_score)">
                    {{ submission.score }}
                  </div>
                  <p class="text-sm text-gray-500">{{ submission.max_score }} dan</p>
                  <p v-if="submission.grade_note" class="text-xs text-gray-400 mt-1">{{ submission.grade_note }}</p>
                  <p class="text-xs text-gray-400 mt-1">
                    Baholagan: {{ submission.graded_by?.full_name }}
                  </p>
                </div>

                <div v-else class="space-y-3">
                  <div>
                    <label class="text-xs text-gray-500">Ball</label>
                    <input
                      v-model.number="gradeForm[submission.id]"
                      type="number"
                      min="0"
                      :max="submission.max_score || 100"
                      class="form-input"
                      :placeholder="`0-${submission.max_score || 100}`"
                    />
                  </div>
                  <button
                    @click="gradeSubmission(submission)"
                    class="btn-primary w-full"
                    :disabled="gradeForm[submission.id] === undefined || isGrading === submission.id"
                  >
                    <LoadingSpinner v-if="isGrading === submission.id" size="xs" color="white" />
                    <span v-else>Baholash</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <EmptyState
          v-else
          title="Javob topilmadi"
          description="Hozircha javoblar yo'q"
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
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { PaperClipIcon } from '@heroicons/vue/24/outline'
import { StatsCard, SearchInput, SkeletonLoader, EmptyState, Pagination, LoadingSpinner } from '@/components/common'
import { useAssignmentStore } from '@/stores'
import { assignmentService } from '@/services'
import dayjs from 'dayjs'

const assignmentStore = useAssignmentStore()

const isLoading = ref(true)
const isGrading = ref(null)
const submissions = ref([])
const gradeForm = reactive({})

const categories = computed(() => assignmentStore.categories)

const stats = reactive({
  total: 0,
  graded: 0,
  ungraded: 0,
  average_score: 0
})

const filters = reactive({
  search: '',
  graded: '',
  category: ''
})

const pagination = reactive({
  page: 1,
  total_pages: 1,
  total_count: 0
})

onMounted(async () => {
  await assignmentStore.fetchCategories()
  await fetchSubmissions()
})

async function fetchSubmissions() {
  isLoading.value = true
  try {
    const params = {
      page: pagination.page,
      search: filters.search || undefined,
      graded: filters.graded || undefined,
      category: filters.category || undefined
    }

    const response = await assignmentService.getSubmissions(params)
    submissions.value = response.results || response || []

    if (response.count !== undefined) {
      pagination.total_count = response.count
      pagination.total_pages = Math.ceil(response.count / 20)
    }

    // Calculate stats
    stats.total = submissions.value.length
    stats.graded = submissions.value.filter(s => s.score !== null).length
    stats.ungraded = stats.total - stats.graded
    
    const gradedSubmissions = submissions.value.filter(s => s.score !== null)
    if (gradedSubmissions.length > 0) {
      stats.average_score = gradedSubmissions.reduce((sum, s) => sum + s.score, 0) / gradedSubmissions.length
    }
  } catch (error) {
    console.error('Failed to fetch submissions:', error)
  } finally {
    isLoading.value = false
  }
}

function handlePageChange(page) {
  pagination.page = page
  fetchSubmissions()
}

function formatDate(date) {
  return dayjs(date).format('D MMM YYYY, HH:mm')
}

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

function getScoreColor(score, maxScore) {
  const percent = (score / (maxScore || 100)) * 100
  if (percent >= 80) return 'text-success-600'
  if (percent >= 60) return 'text-warning-600'
  return 'text-danger-600'
}

async function gradeSubmission(submission) {
  const score = gradeForm[submission.id]
  if (score === undefined || score === null) return

  isGrading.value = submission.id
  try {
    await assignmentService.gradeSubmission(submission.id, {
      score: score,
      feedback: ''
    })
    
    // Update local state
    submission.score = score
    delete gradeForm[submission.id]
    
    // Refresh stats
    stats.graded++
    stats.ungraded--
  } catch (error) {
    console.error('Failed to grade submission:', error)
  } finally {
    isGrading.value = null
  }
}
</script>
