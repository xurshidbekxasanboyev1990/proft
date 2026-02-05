<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="mb-6">
      <RouterLink to="/assignments" class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-2">
        <ArrowLeftIcon class="w-4 h-4 mr-1" />
        Orqaga
      </RouterLink>
      <h1 class="text-2xl font-bold text-gray-900">Topshiriqni tahrirlash</h1>
    </div>

    <LoadingSpinner v-if="isLoading" fullscreen text="Yuklanmoqda..." />

    <!-- Form -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Main form -->
      <div class="lg:col-span-2">
        <div class="card">
          <form @submit.prevent="handleSubmit" class="card-body space-y-6">
            <!-- Title -->
            <div>
              <label for="title" class="form-label">Sarlavha <span class="text-danger-500">*</span></label>
              <input
                id="title"
                v-model="form.title"
                type="text"
                class="form-input"
                :class="{ 'border-danger-500': errors.title }"
                placeholder="Topshiriq sarlavhasi"
              />
              <p v-if="errors.title" class="form-error">{{ errors.title }}</p>
            </div>

            <!-- Category -->
            <div>
              <label for="category" class="form-label">Kategoriya <span class="text-danger-500">*</span></label>
              <select
                id="category"
                v-model="form.category"
                class="form-input"
                :class="{ 'border-danger-500': errors.category }"
              >
                <option value="">Kategoriyani tanlang</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
              <p v-if="errors.category" class="form-error">{{ errors.category }}</p>
            </div>

            <!-- Description -->
            <div>
              <label for="description" class="form-label">Tavsif <span class="text-danger-500">*</span></label>
              <textarea
                id="description"
                v-model="form.description"
                rows="6"
                class="form-input"
                :class="{ 'border-danger-500': errors.description }"
                placeholder="Topshiriq haqida batafsil ma'lumot..."
              ></textarea>
              <p v-if="errors.description" class="form-error">{{ errors.description }}</p>
            </div>

            <!-- Priority & Status -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="priority" class="form-label">Prioritet</label>
                <select id="priority" v-model="form.priority" class="form-input">
                  <option v-for="p in ASSIGNMENT_PRIORITIES" :key="p.value" :value="p.value">
                    {{ p.label }}
                  </option>
                </select>
              </div>
              <div>
                <label for="status" class="form-label">Status</label>
                <select id="status" v-model="form.status" class="form-input">
                  <option v-for="s in ASSIGNMENT_STATUSES" :key="s.value" :value="s.value">
                    {{ s.label }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Deadline -->
            <div>
              <label for="deadline" class="form-label">Muddat <span class="text-danger-500">*</span></label>
              <input
                id="deadline"
                v-model="form.deadline"
                type="datetime-local"
                class="form-input"
                :class="{ 'border-danger-500': errors.deadline }"
              />
              <p v-if="errors.deadline" class="form-error">{{ errors.deadline }}</p>
            </div>

            <!-- Actions -->
            <div class="flex items-center justify-end gap-4 pt-4 border-t border-gray-200">
              <RouterLink to="/assignments" class="btn-secondary">
                Bekor qilish
              </RouterLink>
              <button type="submit" class="btn-primary" :disabled="isSubmitting">
                <LoadingSpinner v-if="isSubmitting" size="xs" color="white" />
                <span v-else>Saqlash</span>
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Sidebar - Score settings -->
      <div class="space-y-6">
        <!-- Score settings card -->
        <div class="card">
          <div class="card-header flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">Ball sozlamalari</h2>
            <button @click="showScoreModal = true" class="text-primary-600 hover:text-primary-700 text-sm font-medium">
              Tahrirlash
            </button>
          </div>
          <div class="card-body space-y-3">
            <div class="flex justify-between">
              <span class="text-sm text-gray-500">Maxsus ball</span>
              <span class="text-sm font-medium" :class="form.use_custom_score ? 'text-success-600' : 'text-gray-400'">
                {{ form.use_custom_score ? 'Ha' : 'Yo\'q' }}
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-500">Maksimal ball</span>
              <span class="text-sm font-medium text-gray-900">{{ form.custom_max_score || form.max_score || 100 }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-500">Ball ko'paytiruvchi</span>
              <span class="text-sm font-medium text-gray-900">{{ form.score_multiplier || 1 }}x</span>
            </div>
          </div>
        </div>

        <!-- Assignment info -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900">Ma'lumotlar</h2>
          </div>
          <div class="card-body space-y-3">
            <div class="flex justify-between">
              <span class="text-sm text-gray-500">Yaratilgan</span>
              <span class="text-sm text-gray-900">{{ formatDate(assignment?.created_at) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-500">Yangilangan</span>
              <span class="text-sm text-gray-900">{{ formatDate(assignment?.updated_at) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-gray-500">Javoblar</span>
              <span class="text-sm text-gray-900">{{ assignment?.submissions_count || 0 }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Score settings modal -->
    <ScoreSettingsModal
      v-if="showScoreModal"
      :is-open="showScoreModal"
      :assignment="form"
      @close="showScoreModal = false"
      @save="handleScoreSave"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner } from '@/components/common'
import ScoreSettingsModal from '@/components/assignments/ScoreSettingsModal.vue'
import { useAssignmentStore } from '@/stores'
import { ASSIGNMENT_STATUSES, ASSIGNMENT_PRIORITIES } from '@/services'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const assignmentStore = useAssignmentStore()

// Determine base path based on current route
const basePath = computed(() => {
  const path = route.path
  if (path.startsWith('/teacher')) return '/teacher/tasks'
  if (path.startsWith('/admin-panel')) return '/admin-panel/tasks'
  if (path.startsWith('/super-admin')) return '/super-admin/tasks'
  return '/admin-panel/tasks'
})

const isLoading = ref(true)
const isSubmitting = ref(false)
const showScoreModal = ref(false)
const assignment = ref(null)

const categories = computed(() => assignmentStore.categories)

const form = reactive({
  title: '',
  category: '',
  description: '',
  priority: 'medium',
  status: 'pending',
  deadline: '',
  max_score: 100,
  use_custom_score: false,
  custom_max_score: null,
  custom_min_score: null,
  score_multiplier: 1,
  score_note: ''
})

const errors = reactive({
  title: '',
  category: '',
  description: '',
  deadline: ''
})

onMounted(async () => {
  try {
    await assignmentStore.fetchCategories()
    const data = await assignmentStore.fetchAssignment(route.params.id)
    assignment.value = data
    
    // Populate form
    form.title = data.title || ''
    form.category = data.category?.id || data.category || ''
    form.description = data.description || ''
    form.priority = data.priority || 'medium'
    form.status = data.status || 'pending'
    form.deadline = data.deadline ? dayjs(data.deadline).format('YYYY-MM-DDTHH:mm') : ''
    form.max_score = data.max_score || 100
    form.use_custom_score = data.use_custom_score || false
    form.custom_max_score = data.custom_max_score
    form.custom_min_score = data.custom_min_score
    form.score_multiplier = data.score_multiplier || 1
    form.score_note = data.score_note || ''
  } catch (error) {
    console.error('Failed to load assignment:', error)
  } finally {
    isLoading.value = false
  }
})

function formatDate(date) {
  if (!date) return '-'
  return dayjs(date).format('D MMM YYYY, HH:mm')
}

function validate() {
  let isValid = true
  Object.keys(errors).forEach(key => errors[key] = '')

  if (!form.title.trim()) {
    errors.title = 'Sarlavha kiritish majburiy'
    isValid = false
  }

  if (!form.category) {
    errors.category = 'Kategoriya tanlash majburiy'
    isValid = false
  }

  if (!form.description.trim()) {
    errors.description = 'Tavsif kiritish majburiy'
    isValid = false
  }

  if (!form.deadline) {
    errors.deadline = 'Muddat kiritish majburiy'
    isValid = false
  }

  return isValid
}

async function handleSubmit() {
  if (!validate()) return

  isSubmitting.value = true
  try {
    const data = {
      title: form.title.trim(),
      category: form.category,
      description: form.description.trim(),
      priority: form.priority,
      status: form.status,
      deadline: new Date(form.deadline).toISOString(),
      use_custom_score: form.use_custom_score,
      custom_max_score: form.custom_max_score,
      custom_min_score: form.custom_min_score,
      score_multiplier: form.score_multiplier,
      score_note: form.score_note
    }

    await assignmentStore.updateAssignment(route.params.id, data)
    router.push(`${basePath.value}/${route.params.id}`)
  } catch (error) {
    console.error('Failed to update assignment:', error)
  } finally {
    isSubmitting.value = false
  }
}

function handleScoreSave(scoreData) {
  form.use_custom_score = scoreData.use_custom_score
  form.custom_max_score = scoreData.custom_max_score
  form.custom_min_score = scoreData.custom_min_score
  form.score_multiplier = scoreData.score_multiplier
  form.score_note = scoreData.score_note
  showScoreModal.value = false
}
</script>
