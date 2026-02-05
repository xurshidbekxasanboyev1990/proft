<template>
  <div class="animate-fade-in">
    <LoadingSpinner v-if="isLoading" fullscreen text="Yuklanmoqda..." />

    <template v-else-if="assignment">
      <!-- Page header -->
      <div class="mb-6">
        <RouterLink :to="backPath" class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-2">
          <ArrowLeftIcon class="w-4 h-4 mr-1" />
          Orqaga
        </RouterLink>
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ assignment.title }}</h1>
            <div class="flex items-center gap-3 mt-2">
              <StatusBadge :variant="assignment.status" dot>
                {{ statusLabel }}
              </StatusBadge>
              <span class="text-sm text-gray-500">{{ assignment.category?.name }}</span>
            </div>
          </div>

          <div v-if="userStore.isAdminOrSuperAdmin" class="flex items-center gap-2">
            <RouterLink :to="editPath" class="btn-secondary">
              <PencilIcon class="w-4 h-4 mr-2" />
              Tahrirlash
            </RouterLink>
            <button @click="showDeleteModal = true" class="btn-danger">
              <TrashIcon class="w-4 h-4 mr-2" />
              O'chirish
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
              <p class="whitespace-pre-wrap">{{ assignment.description }}</p>
            </div>
          </div>

          <!-- Deadline countdown -->
          <DeadlineCountdown 
            v-if="assignment.status !== 'completed' && assignment.status !== 'cancelled'"
            :deadline="assignment.deadline" 
          />

          <!-- Submit section (for teachers) -->
          <div v-if="userStore.isTeacher && assignment.status !== 'completed'" class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Javob yuborish</h2>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleSubmit">
                <div class="mb-4">
                  <label class="form-label">Izoh</label>
                  <textarea
                    v-model="submission.content"
                    rows="4"
                    class="form-input"
                    placeholder="Javobingizni yozing..."
                  ></textarea>
                </div>
                <div class="mb-4">
                  <label class="form-label">Fayl biriktirish (ixtiyoriy)</label>
                  <FileUpload v-model="submission.files" :max-files="5" />
                </div>
                <div class="flex justify-end">
                  <button type="submit" class="btn-primary" :disabled="isSubmitting || !submission.content.trim()">
                    <LoadingSpinner v-if="isSubmitting" size="xs" color="white" />
                    <span v-else>Yuborish</span>
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Submissions list (for admins) -->
          <div v-if="userStore.isAdminOrSuperAdmin && assignment.submissions?.length > 0" class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">
                Javoblar ({{ assignment.submissions.length }})
              </h2>
            </div>
            <div class="card-body p-0 divide-y divide-gray-200">
              <div v-for="sub in assignment.submissions" :key="sub.id" class="p-4">
                <div class="flex items-start justify-between gap-4">
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="font-medium text-gray-900">{{ sub.submitted_by?.full_name }}</span>
                      <span class="text-xs text-gray-500">{{ formatDate(sub.submitted_at) }}</span>
                    </div>
                    <p class="text-sm text-gray-600">{{ sub.content }}</p>
                    <div v-if="sub.score !== null" class="mt-2">
                      <span class="text-sm font-medium text-primary-600">Ball: {{ sub.score }}</span>
                    </div>
                  </div>
                  <button
                    v-if="sub.score === null"
                    @click="openGradeModal(sub)"
                    class="btn-primary btn-sm"
                  >
                    Baholash
                  </button>
                </div>
              </div>
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
                <span class="text-sm text-gray-500">Prioritet</span>
                <span class="text-sm font-medium" :class="priorityColor">{{ priorityLabel }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">Kategoriya</span>
                <span class="text-sm font-medium text-gray-900">{{ assignment.category?.name || '-' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">Muddat</span>
                <span class="text-sm font-medium text-gray-900">{{ formatDate(assignment.deadline) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">Tayinlangan</span>
                <span class="text-sm font-medium text-gray-900">
                  {{ assignment.assigned_to?.full_name || 'Barchaga' }}
                </span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">Yaratilgan</span>
                <span class="text-sm font-medium text-gray-900">{{ formatDate(assignment.created_at) }}</span>
              </div>
              <div v-if="assignment.max_score" class="flex justify-between">
                <span class="text-sm text-gray-500">Maksimal ball</span>
                <span class="text-sm font-medium text-gray-900">{{ assignment.max_score }}</span>
              </div>
            </div>
          </div>

          <!-- Created by -->
          <div class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Yaratuvchi</h2>
            </div>
            <div class="card-body">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                  <span class="text-sm font-medium text-primary-600">
                    {{ assignment.created_by?.username?.substring(0, 2).toUpperCase() }}
                  </span>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900">
                    {{ assignment.created_by?.full_name || assignment.created_by?.username }}
                  </p>
                  <p class="text-xs text-gray-500">{{ formatDate(assignment.created_at) }}</p>
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
      title="Topshiriq topilmadi"
      description="Bu topshiriq mavjud emas yoki o'chirilgan"
      action-text="Ortga qaytish"
      @action="$router.push(backPath)"
    />

    <!-- Delete modal -->
    <ConfirmModal
      :is-open="showDeleteModal"
      title="Topshiriqni o'chirish"
      message="Bu topshiriqni o'chirishga ishonchingiz komilmi?"
      type="danger"
      :is-loading="isDeleting"
      @confirm="handleDelete"
      @cancel="showDeleteModal = false"
    />

    <!-- Grade modal -->
    <BaseModal :is-open="showGradeModal" title="Javobni baholash" @close="showGradeModal = false">
      <div class="space-y-4">
        <div>
          <label class="form-label">Ball</label>
          <input
            v-model.number="gradeData.score"
            type="number"
            min="0"
            :max="assignment?.max_score || 100"
            class="form-input"
          />
        </div>
        <div>
          <label class="form-label">Izoh (ixtiyoriy)</label>
          <textarea v-model="gradeData.feedback" rows="3" class="form-input"></textarea>
        </div>
      </div>
      <template #footer>
        <button @click="showGradeModal = false" class="btn-secondary">Bekor qilish</button>
        <button @click="confirmGrade" class="btn-primary" :disabled="isGrading">
          <LoadingSpinner v-if="isGrading" size="xs" color="white" />
          <span v-else>Saqlash</span>
        </button>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeftIcon, PencilIcon, TrashIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner, StatusBadge, EmptyState, ConfirmModal, BaseModal, FileUpload } from '@/components/common'
import { DeadlineCountdown } from '@/components/assignments'
import { useAssignmentStore, useUserStore } from '@/stores'
import { ASSIGNMENT_STATUSES, ASSIGNMENT_PRIORITIES } from '@/services'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const assignmentStore = useAssignmentStore()
const userStore = useUserStore()

// Determine base path based on current route
const basePath = computed(() => {
  const path = route.path
  if (path.startsWith('/teacher')) return '/teacher/tasks'
  if (path.startsWith('/admin-panel')) return '/admin-panel/tasks'
  if (path.startsWith('/super-admin')) return '/super-admin/tasks'
  return '/teacher/tasks'
})

const backPath = computed(() => basePath.value)
const editPath = computed(() => `${basePath.value}/${route.params.id}/edit`)

const isLoading = ref(true)
const showDeleteModal = ref(false)
const isDeleting = ref(false)
const showGradeModal = ref(false)
const isGrading = ref(false)
const isSubmitting = ref(false)
const selectedSubmission = ref(null)

const assignment = computed(() => assignmentStore.currentAssignment)

const submission = reactive({
  content: '',
  files: []
})

const gradeData = reactive({
  score: 0,
  feedback: ''
})

const statusLabel = computed(() => {
  const status = ASSIGNMENT_STATUSES.find(s => s.value === assignment.value?.status)
  return status?.label || assignment.value?.status
})

const priorityLabel = computed(() => {
  const priority = ASSIGNMENT_PRIORITIES.find(p => p.value === assignment.value?.priority)
  return priority?.label || assignment.value?.priority
})

const priorityColor = computed(() => {
  const colors = {
    low: 'text-gray-600',
    medium: 'text-warning-600',
    high: 'text-danger-600'
  }
  return colors[assignment.value?.priority] || 'text-gray-600'
})

onMounted(async () => {
  try {
    await assignmentStore.fetchAssignment(route.params.id)
  } catch (error) {
    console.error('Failed to fetch assignment:', error)
  } finally {
    isLoading.value = false
  }
})

function formatDate(date) {
  return dayjs(date).format('D MMM YYYY, HH:mm')
}

async function handleSubmit() {
  if (!submission.content.trim()) return

  isSubmitting.value = true
  try {
    await assignmentStore.submitAssignment(assignment.value.id, {
      content: submission.content,
      files: submission.files
    })
    submission.content = ''
    submission.files = []
    await assignmentStore.fetchAssignment(route.params.id)
  } catch (error) {
    console.error('Submit failed:', error)
  } finally {
    isSubmitting.value = false
  }
}

async function handleDelete() {
  isDeleting.value = true
  try {
    await assignmentStore.deleteAssignment(assignment.value.id)
    router.push(basePath.value)
  } catch (error) {
    console.error('Delete failed:', error)
  } finally {
    isDeleting.value = false
  }
}

function openGradeModal(sub) {
  selectedSubmission.value = sub
  gradeData.score = 0
  gradeData.feedback = ''
  showGradeModal.value = true
}

async function confirmGrade() {
  if (!selectedSubmission.value) return

  isGrading.value = true
  try {
    await assignmentStore.gradeSubmission(selectedSubmission.value.id, gradeData)
    showGradeModal.value = false
    await assignmentStore.fetchAssignment(route.params.id)
  } catch (error) {
    console.error('Grade failed:', error)
  } finally {
    isGrading.value = false
  }
}
</script>
