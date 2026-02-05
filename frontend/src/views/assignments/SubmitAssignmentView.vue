<template>
  <div class="animate-fade-in">
    <!-- Back button -->
    <div class="mb-6">
      <button
        @click="router.back()"
        class="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
      >
        <ArrowLeftIcon class="w-5 h-5" />
        <span>Orqaga</span>
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="space-y-6">
      <SkeletonLoader type="card" />
      <SkeletonLoader type="card" />
    </div>

    <!-- Content -->
    <div v-else-if="assignment" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left: Assignment info -->
      <div class="lg:col-span-1 space-y-6">
        <!-- Assignment card -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-start gap-4">
            <div 
              class="w-12 h-12 rounded-xl flex items-center justify-center"
              :style="{ backgroundColor: assignment.category?.color + '20' }"
            >
              <ClipboardDocumentListIcon 
                class="w-6 h-6" 
                :style="{ color: assignment.category?.color }"
              />
            </div>
            <div class="flex-1">
              <h1 class="text-xl font-bold text-gray-900">{{ assignment.title }}</h1>
              <p class="text-sm text-gray-500 mt-1">{{ assignment.category?.name }}</p>
            </div>
          </div>

          <p class="text-gray-600 mt-4">{{ assignment.description }}</p>

          <!-- Deadline -->
          <div class="mt-6 p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Muddat:</span>
              <span class="text-sm font-medium" :class="deadlineClass">
                {{ formatDate(assignment.deadline) }}
              </span>
            </div>
            <div class="mt-2">
              <DeadlineCountdown :deadline="assignment.deadline" />
            </div>
          </div>

          <!-- Score info -->
          <div class="mt-4 p-4 bg-blue-50 rounded-lg">
            <div class="flex items-center justify-between">
              <span class="text-sm text-blue-700">Maksimal ball:</span>
              <span class="text-lg font-bold text-blue-700">
                {{ assignment.use_custom_score ? assignment.custom_max_score : assignment.category?.default_score || 10 }}
              </span>
            </div>
            <div v-if="assignment.score_multiplier > 1" class="mt-2 flex items-center justify-between">
              <span class="text-sm text-blue-700">Bonus:</span>
              <span class="text-sm font-medium text-blue-700">
                {{ assignment.score_multiplier }}x
              </span>
            </div>
          </div>

          <!-- Priority -->
          <div class="mt-4 flex items-center gap-2">
            <span class="text-sm text-gray-600">Muhimlik:</span>
            <StatusBadge :status="assignment.priority" type="priority" />
          </div>
        </div>

        <!-- Previous submissions -->
        <div v-if="previousSubmissions.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 class="font-semibold text-gray-900 mb-4">Oldingi javoblar</h3>
          <div class="space-y-3">
            <div 
              v-for="sub in previousSubmissions" 
              :key="sub.id"
              class="p-3 bg-gray-50 rounded-lg"
            >
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">{{ formatDate(sub.submitted_at) }}</span>
                <StatusBadge :status="sub.status" />
              </div>
              <div v-if="sub.grade !== null" class="mt-2 flex items-center gap-2">
                <span class="text-sm text-gray-600">Ball:</span>
                <span class="font-medium text-primary-600">{{ sub.grade }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Submit form -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-6">Javob yuborish</h2>

          <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Content -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Javob matni <span class="text-danger-500">*</span>
              </label>
              <textarea
                v-model="form.content"
                rows="8"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
                placeholder="Javobingizni yozing..."
                required
              ></textarea>
              <p class="mt-1 text-xs text-gray-500">
                Kamida 50 ta belgi kiritish kerak
              </p>
            </div>

            <!-- Links -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Havolalar (ixtiyoriy)
              </label>
              <div class="space-y-2">
                <div 
                  v-for="(link, index) in form.links" 
                  :key="index"
                  class="flex items-center gap-2"
                >
                  <input
                    v-model="form.links[index]"
                    type="url"
                    class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="https://..."
                  />
                  <button
                    type="button"
                    @click="removeLink(index)"
                    class="p-2 text-gray-400 hover:text-danger-500 transition-colors"
                  >
                    <XMarkIcon class="w-5 h-5" />
                  </button>
                </div>
              </div>
              <button
                type="button"
                @click="addLink"
                class="mt-2 flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700"
              >
                <PlusIcon class="w-4 h-4" />
                Havola qo'shish
              </button>
            </div>

            <!-- File upload -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Fayllar (ixtiyoriy)
              </label>
              <FileUpload
                v-model="form.files"
                :multiple="true"
                :max-size="10"
                accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.zip,.rar,.jpg,.jpeg,.png"
              />
              <p class="mt-1 text-xs text-gray-500">
                PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, ZIP, RAR, JPG, PNG. Maksimum 10MB.
              </p>
            </div>

            <!-- Notes -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Qo'shimcha izoh (ixtiyoriy)
              </label>
              <textarea
                v-model="form.notes"
                rows="3"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
                placeholder="Baholovchi uchun qo'shimcha ma'lumot..."
              ></textarea>
            </div>

            <!-- Agreement -->
            <div class="flex items-start gap-3">
              <input
                v-model="form.agreed"
                type="checkbox"
                id="agreement"
                class="mt-1 w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                required
              />
              <label for="agreement" class="text-sm text-gray-600">
                Men bu ishni mustaqil bajarganman va barcha manbalar ko'rsatilgan. 
                Plagiat uchun javobgarlikni o'z zimmamga olaman.
              </label>
            </div>

            <!-- Submit button -->
            <div class="flex items-center justify-end gap-4 pt-4 border-t">
              <button
                type="button"
                @click="saveDraft"
                class="px-6 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                :disabled="isSubmitting"
              >
                Qoralama saqlash
              </button>
              <button
                type="submit"
                class="px-6 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                :disabled="isSubmitting || !isFormValid"
              >
                <LoadingSpinner v-if="isSubmitting" size="sm" />
                <PaperAirplaneIcon v-else class="w-5 h-5" />
                <span>Yuborish</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Not found -->
    <EmptyState
      v-else
      title="Topshiriq topilmadi"
      description="Bu topshiriq mavjud emas yoki sizga tayinlanmagan"
      type="folder"
    >
      <template #action>
        <RouterLink
          to="/my-assignments"
          class="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          <ArrowLeftIcon class="w-5 h-5" />
          Topshiriqlarimga qaytish
        </RouterLink>
      </template>
    </EmptyState>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { 
  ArrowLeftIcon, 
  ClipboardDocumentListIcon,
  PlusIcon,
  XMarkIcon,
  PaperAirplaneIcon
} from '@heroicons/vue/24/outline'
import { SkeletonLoader, EmptyState, StatusBadge, FileUpload, LoadingSpinner } from '@/components/common'
import { DeadlineCountdown } from '@/components/assignments'
import { useAssignmentStore } from '@/stores'
import { formatDate } from '@/utils/date'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const assignmentStore = useAssignmentStore()

const isLoading = ref(true)
const isSubmitting = ref(false)
const assignment = ref(null)
const previousSubmissions = ref([])

const form = ref({
  content: '',
  links: [''],
  files: [],
  notes: '',
  agreed: false
})

const isFormValid = computed(() => {
  return form.value.content.length >= 50 && form.value.agreed
})

const deadlineClass = computed(() => {
  if (!assignment.value?.deadline) return 'text-gray-900'
  const deadline = new Date(assignment.value.deadline)
  const now = new Date()
  const diff = deadline - now
  const days = diff / (1000 * 60 * 60 * 24)
  
  if (days < 0) return 'text-danger-600'
  if (days < 1) return 'text-warning-600'
  if (days < 3) return 'text-orange-600'
  return 'text-gray-900'
})

function addLink() {
  form.value.links.push('')
}

function removeLink(index) {
  form.value.links.splice(index, 1)
  if (form.value.links.length === 0) {
    form.value.links.push('')
  }
}

async function handleSubmit() {
  if (!isFormValid.value) return
  
  isSubmitting.value = true
  try {
    const data = {
      content: form.value.content,
      links: form.value.links.filter(l => l.trim()),
      notes: form.value.notes
    }
    
    await assignmentStore.submitAssignment(route.params.id, data)
    toast.success('Javob muvaffaqiyatli yuborildi!')
    router.push('/my-submissions')
  } catch (error) {
    console.error('Submit failed:', error)
    toast.error('Javob yuborishda xatolik yuz berdi')
  } finally {
    isSubmitting.value = false
  }
}

async function saveDraft() {
  toast.info('Qoralama saqlandi')
  // Save to localStorage
  localStorage.setItem(`draft_${route.params.id}`, JSON.stringify(form.value))
}

async function loadData() {
  isLoading.value = true
  try {
    const data = await assignmentStore.fetchAssignment(route.params.id)
    assignment.value = data
    
    // Load previous submissions (mock)
    previousSubmissions.value = [
      { id: 1, submitted_at: new Date().toISOString(), status: 'graded', grade: 85 },
    ]
    
    // Load draft if exists
    const draft = localStorage.getItem(`draft_${route.params.id}`)
    if (draft) {
      const parsed = JSON.parse(draft)
      form.value = { ...form.value, ...parsed, agreed: false }
    }
  } catch (error) {
    console.error('Failed to load assignment:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(loadData)
</script>
