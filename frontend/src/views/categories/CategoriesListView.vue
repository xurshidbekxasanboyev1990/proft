<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Kategoriyalar</h1>
        <p class="mt-1 text-sm text-gray-500">
          Topshiriq va portfolio kategoriyalarini boshqaring
        </p>
      </div>
      <button @click="openCreateModal" class="btn-primary">
        <PlusIcon class="w-5 h-5 mr-2" />
        Yangi kategoriya
      </button>
    </div>

    <!-- Categories grid -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <SkeletonLoader v-for="i in 6" :key="i" type="card" />
    </div>

    <div v-else-if="categories.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="category in categories"
        :key="category.id"
        class="card hover:shadow-lg transition-shadow"
      >
        <div class="card-body">
          <div class="flex items-start justify-between gap-4">
            <div class="flex-1">
              <div class="flex items-center gap-2">
                <div
                  class="w-3 h-3 rounded-full"
                  :style="{ backgroundColor: category.color || '#6366F1' }"
                ></div>
                <h3 class="font-semibold text-gray-900">{{ category.name }}</h3>
              </div>
              <p v-if="category.description" class="text-sm text-gray-500 mt-2 line-clamp-2">
                {{ category.description }}
              </p>
            </div>
            <div class="flex items-center gap-1">
              <button
                @click="openScoreModal(category)"
                class="p-1.5 text-gray-400 hover:text-warning-600 hover:bg-gray-100 rounded-lg transition-colors"
                title="Ball sozlamalari"
              >
                <AdjustmentsHorizontalIcon class="w-4 h-4" />
              </button>
              <button
                @click="openEditModal(category)"
                class="p-1.5 text-gray-400 hover:text-primary-600 hover:bg-gray-100 rounded-lg transition-colors"
                title="Tahrirlash"
              >
                <PencilIcon class="w-4 h-4" />
              </button>
              <button
                @click="openDeleteModal(category)"
                class="p-1.5 text-gray-400 hover:text-danger-600 hover:bg-gray-100 rounded-lg transition-colors"
                title="O'chirish"
              >
                <TrashIcon class="w-4 h-4" />
              </button>
            </div>
          </div>

          <div class="flex items-center gap-4 mt-4 pt-4 border-t border-gray-100">
            <div class="flex items-center gap-1.5 text-sm text-gray-500">
              <FolderIcon class="w-4 h-4" />
              <span>{{ category.assignment_count || 0 }} topshiriq</span>
            </div>
            <div class="flex items-center gap-1.5 text-sm text-gray-500">
              <StarIcon class="w-4 h-4" />
              <span>{{ category.default_score || category.max_score || 100 }} ball</span>
            </div>
            <div v-if="category.score_weight && category.score_weight !== 1" class="flex items-center gap-1.5 text-sm text-warning-600">
              <span>{{ category.score_weight }}x vazn</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <EmptyState
      v-else
      title="Kategoriya topilmadi"
      description="Yangi kategoriya qo'shing"
      action-text="Yangi kategoriya"
      type="folder"
      @action="openCreateModal"
    />

    <!-- Create/Edit modal -->
    <BaseModal
      :is-open="showFormModal"
      :title="isEditing ? 'Kategoriyani tahrirlash' : 'Yangi kategoriya'"
      @close="closeFormModal"
    >
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label for="name" class="form-label">Nomi <span class="text-danger-500">*</span></label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            class="form-input"
            :class="{ 'border-danger-500': errors.name }"
            placeholder="Kategoriya nomi"
          />
          <p v-if="errors.name" class="form-error">{{ errors.name }}</p>
        </div>

        <div>
          <label for="description" class="form-label">Tavsif</label>
          <textarea
            id="description"
            v-model="form.description"
            rows="3"
            class="form-input"
            placeholder="Qisqacha tavsif..."
          ></textarea>
        </div>

        <div>
          <label for="color" class="form-label">Rang</label>
          <div class="flex items-center gap-3">
            <input
              id="color"
              v-model="form.color"
              type="color"
              class="w-10 h-10 p-1 border border-gray-300 rounded-lg cursor-pointer"
            />
            <input
              v-model="form.color"
              type="text"
              class="form-input flex-1"
              placeholder="#6366F1"
            />
          </div>
        </div>

        <div>
          <label for="max_score" class="form-label">Maksimal ball</label>
          <input
            id="max_score"
            v-model.number="form.max_score"
            type="number"
            min="0"
            max="1000"
            class="form-input"
            placeholder="100"
          />
        </div>

        <div>
          <label for="weight" class="form-label">Vazn (foiz)</label>
          <input
            id="weight"
            v-model.number="form.weight"
            type="number"
            min="0"
            max="100"
            class="form-input"
            placeholder="10"
          />
          <p class="text-xs text-gray-400 mt-1">Umumiy ballni hisoblashda ishlatiladi</p>
        </div>
      </form>

      <template #footer>
        <button @click="closeFormModal" class="btn-secondary">Bekor qilish</button>
        <button @click="handleSubmit" class="btn-primary" :disabled="isSubmitting">
          <LoadingSpinner v-if="isSubmitting" size="xs" color="white" />
          <span v-else>{{ isEditing ? 'Saqlash' : 'Yaratish' }}</span>
        </button>
      </template>
    </BaseModal>

    <!-- Delete modal -->
    <ConfirmModal
      :is-open="showDeleteModal"
      title="Kategoriyani o'chirish"
      :message="`'${categoryToDelete?.name}' kategoriyasini o'chirishga ishonchingiz komilmi?`"
      type="danger"
      :is-loading="isDeleting"
      @confirm="confirmDelete"
      @cancel="showDeleteModal = false"
    />

    <!-- Score settings modal -->
    <CategoryScoreModal
      v-if="showScoreModal"
      :is-open="showScoreModal"
      :category="categoryForScore"
      @close="showScoreModal = false"
      @saved="handleScoreSaved"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { PlusIcon, PencilIcon, TrashIcon, FolderIcon, StarIcon, AdjustmentsHorizontalIcon } from '@heroicons/vue/24/outline'
import { SkeletonLoader, EmptyState, BaseModal, ConfirmModal, LoadingSpinner } from '@/components/common'
import { CategoryScoreModal } from '@/components/categories'
import { useAssignmentStore } from '@/stores'

const assignmentStore = useAssignmentStore()

const isLoading = computed(() => assignmentStore.isLoading)
const categories = computed(() => assignmentStore.categories)

const showFormModal = ref(false)
const showDeleteModal = ref(false)
const showScoreModal = ref(false)
const isEditing = ref(false)
const isSubmitting = ref(false)
const isDeleting = ref(false)
const categoryToDelete = ref(null)
const categoryForScore = ref(null)

const form = reactive({
  id: null,
  name: '',
  description: '',
  color: '#6366F1',
  max_score: 100,
  weight: 10
})

const errors = reactive({
  name: ''
})

onMounted(() => {
  assignmentStore.fetchCategories()
})

function resetForm() {
  form.id = null
  form.name = ''
  form.description = ''
  form.color = '#6366F1'
  form.max_score = 100
  form.weight = 10
  errors.name = ''
}

function openCreateModal() {
  resetForm()
  isEditing.value = false
  showFormModal.value = true
}

function openEditModal(category) {
  form.id = category.id
  form.name = category.name
  form.description = category.description || ''
  form.color = category.color || '#6366F1'
  form.max_score = category.max_score || 100
  form.weight = category.weight || 10
  isEditing.value = true
  showFormModal.value = true
}

function closeFormModal() {
  showFormModal.value = false
  resetForm()
}

function openDeleteModal(category) {
  categoryToDelete.value = category
  showDeleteModal.value = true
}

function validate() {
  errors.name = ''
  if (!form.name.trim()) {
    errors.name = 'Kategoriya nomi kiritish majburiy'
    return false
  }
  return true
}

async function handleSubmit() {
  if (!validate()) return

  isSubmitting.value = true
  try {
    const data = {
      name: form.name.trim(),
      description: form.description.trim(),
      color: form.color,
      max_score: form.max_score,
      weight: form.weight
    }

    if (isEditing.value) {
      await assignmentStore.updateCategory(form.id, data)
    } else {
      await assignmentStore.createCategory(data)
    }

    closeFormModal()
  } catch (error) {
    console.error('Failed to save category:', error)
  } finally {
    isSubmitting.value = false
  }
}

async function confirmDelete() {
  if (!categoryToDelete.value) return

  isDeleting.value = true
  try {
    await assignmentStore.deleteCategory(categoryToDelete.value.id)
    showDeleteModal.value = false
    categoryToDelete.value = null
  } catch (error) {
    console.error('Delete failed:', error)
  } finally {
    isDeleting.value = false
  }
}

function openScoreModal(category) {
  categoryForScore.value = category
  showScoreModal.value = true
}

function handleScoreSaved() {
  // Refresh categories to show updated score settings
  assignmentStore.fetchCategories()
}
</script>
