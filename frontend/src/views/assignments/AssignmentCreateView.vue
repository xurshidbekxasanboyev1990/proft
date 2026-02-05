<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="mb-6">
      <RouterLink to="/assignments" class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-2">
        <ArrowLeftIcon class="w-4 h-4 mr-1" />
        Orqaga
      </RouterLink>
      <h1 class="text-2xl font-bold text-gray-900">Yangi topshiriq</h1>
      <p class="mt-1 text-sm text-gray-500">
        O'qituvchilarga yangi topshiriq yarating
      </p>
    </div>

    <!-- Form -->
    <div class="card max-w-3xl">
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

        <!-- Priority -->
        <div>
          <label for="priority" class="form-label">Prioritet</label>
          <select id="priority" v-model="form.priority" class="form-input">
            <option v-for="p in ASSIGNMENT_PRIORITIES" :key="p.value" :value="p.value">
              {{ p.label }}
            </option>
          </select>
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

        <!-- Assigned to -->
        <div>
          <label for="assigned_to" class="form-label">Tayinlash</label>
          <select id="assigned_to" v-model="form.assigned_to" class="form-input">
            <option value="">Barcha o'qituvchilarga</option>
            <option v-for="user in teachers" :key="user.id" :value="user.id">
              {{ user.full_name || user.username }}
            </option>
          </select>
          <p class="text-xs text-gray-400 mt-1">Bo'sh qoldirilsa barcha o'qituvchilarga tayinlanadi</p>
        </div>

        <!-- Max score -->
        <div>
          <label for="max_score" class="form-label">Maksimal ball</label>
          <input
            id="max_score"
            v-model.number="form.max_score"
            type="number"
            min="1"
            max="1000"
            class="form-input"
            placeholder="100"
          />
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-end gap-4 pt-4 border-t border-gray-200">
          <RouterLink to="/assignments" class="btn-secondary">
            Bekor qilish
          </RouterLink>
          <button type="submit" class="btn-primary" :disabled="isSubmitting">
            <LoadingSpinner v-if="isSubmitting" size="xs" color="white" />
            <span v-else>Yaratish</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner } from '@/components/common'
import { useAssignmentStore, useUserStore } from '@/stores'
import { ASSIGNMENT_PRIORITIES, userService } from '@/services'

const router = useRouter()
const route = useRoute()
const assignmentStore = useAssignmentStore()
const userStore = useUserStore()

// Determine base path based on current route
const basePath = computed(() => {
  const path = route.path
  if (path.startsWith('/teacher')) return '/teacher/tasks'
  if (path.startsWith('/admin-panel')) return '/admin-panel/tasks'
  if (path.startsWith('/super-admin')) return '/super-admin/tasks'
  return '/admin-panel/tasks'
})

const categories = computed(() => assignmentStore.categories)
const teachers = ref([])

const form = reactive({
  title: '',
  category: '',
  description: '',
  priority: 'medium',
  deadline: '',
  assigned_to: '',
  max_score: 100
})

const errors = reactive({
  title: '',
  category: '',
  description: '',
  deadline: ''
})

const isSubmitting = ref(false)

onMounted(async () => {
  await assignmentStore.fetchCategories()
  try {
    const data = await userService.getUsers({ role: 'teacher' })
    teachers.value = data.users || data.results || []
  } catch (error) {
    console.error('Failed to fetch teachers:', error)
  }
})

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
      deadline: new Date(form.deadline).toISOString(),
      max_score: form.max_score
    }

    if (form.assigned_to) {
      data.assigned_to = form.assigned_to
    }

    const result = await assignmentStore.createAssignment(data)
    router.push(`${basePath.value}/${result.id}`)
  } catch (error) {
    console.error('Failed to create assignment:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>
