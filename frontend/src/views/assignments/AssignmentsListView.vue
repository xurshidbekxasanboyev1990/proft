<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Topshiriqlar</h1>
        <p class="mt-1 text-sm text-gray-500">
          Barcha topshiriqlarni boshqaring
        </p>
      </div>
      <RouterLink v-if="userStore.isAdminOrSuperAdmin" to="/assignments/create" class="btn-primary">
        <PlusIcon class="w-5 h-5 mr-2" />
        Yangi topshiriq
      </RouterLink>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <StatsCard title="Jami" :value="statistics?.total || 0" icon="folder" color="gray" />
      <StatsCard title="Kutilmoqda" :value="statistics?.pending || 0" icon="clock" color="warning" />
      <StatsCard title="Bajarildi" :value="statistics?.completed || 0" icon="check" color="success" />
      <StatsCard title="Muddati o'tgan" :value="statistics?.overdue || 0" icon="exclamation" color="danger" />
    </div>

    <!-- Filters -->
    <div class="card mb-6">
      <div class="card-body">
        <div class="grid grid-cols-1 sm:grid-cols-5 gap-4">
          <!-- Search -->
          <div class="sm:col-span-2">
            <SearchInput
              v-model="filters.search"
              placeholder="Topshiriq qidirish..."
              @search="applyFilters"
            />
          </div>

          <!-- Status filter -->
          <select v-model="filters.status" @change="applyFilters" class="form-input">
            <option value="">Barcha statuslar</option>
            <option v-for="s in ASSIGNMENT_STATUSES" :key="s.value" :value="s.value">
              {{ s.label }}
            </option>
          </select>

          <!-- Priority filter -->
          <select v-model="filters.priority" @change="applyFilters" class="form-input">
            <option value="">Barcha prioritetlar</option>
            <option v-for="p in ASSIGNMENT_PRIORITIES" :key="p.value" :value="p.value">
              {{ p.label }}
            </option>
          </select>

          <!-- Category filter -->
          <select v-model="filters.category" @change="applyFilters" class="form-input">
            <option value="">Barcha kategoriyalar</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <SkeletonLoader v-for="i in 6" :key="i" type="card" />
    </div>

    <!-- Assignments grid -->
    <div v-else-if="assignments.length > 0">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <AssignmentCard
          v-for="assignment in assignments"
          :key="assignment.id"
          :assignment="assignment"
          :can-edit="userStore.isAdminOrSuperAdmin"
          :can-delete="userStore.isAdminOrSuperAdmin"
          @edit="handleEdit"
          @delete="handleDelete"
        />
      </div>

      <!-- Pagination -->
      <div class="mt-6">
        <Pagination
          :current-page="pagination.page"
          :total-pages="pagination.total_pages"
          :total-count="pagination.total_count"
          :has-next="pagination.has_next"
          :has-previous="pagination.has_previous"
          @page-change="handlePageChange"
        />
      </div>
    </div>

    <!-- Empty state -->
    <EmptyState
      v-else
      title="Topshiriq topilmadi"
      description="Hozircha hech qanday topshiriq yo'q"
      :action-text="userStore.isAdminOrSuperAdmin ? 'Yangi topshiriq' : ''"
      type="folder"
      @action="$router.push('/assignments/create')"
    />

    <!-- Delete modal -->
    <ConfirmModal
      :is-open="showDeleteModal"
      title="Topshiriqni o'chirish"
      message="Bu topshiriqni o'chirishga ishonchingiz komilmi?"
      type="danger"
      :is-loading="isDeleting"
      @confirm="confirmDelete"
      @cancel="showDeleteModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { PlusIcon } from '@heroicons/vue/24/outline'
import { StatsCard, SkeletonLoader, Pagination, EmptyState, ConfirmModal, SearchInput } from '@/components/common'
import { AssignmentCard } from '@/components/assignments'
import { useAssignmentStore, useUserStore } from '@/stores'
import { ASSIGNMENT_STATUSES, ASSIGNMENT_PRIORITIES } from '@/services'

const router = useRouter()
const assignmentStore = useAssignmentStore()
const userStore = useUserStore()

const isLoading = computed(() => assignmentStore.isLoading)
const assignments = computed(() => assignmentStore.assignments)
const categories = computed(() => assignmentStore.categories)
const pagination = computed(() => assignmentStore.pagination)
const statistics = computed(() => assignmentStore.statistics)

const filters = ref({
  search: '',
  status: '',
  priority: '',
  category: ''
})

const showDeleteModal = ref(false)
const isDeleting = ref(false)
const assignmentToDelete = ref(null)

onMounted(async () => {
  await Promise.all([
    assignmentStore.fetchAssignments(),
    assignmentStore.fetchCategories(),
    assignmentStore.fetchStatistics()
  ])
})

function applyFilters() {
  assignmentStore.setFilters(filters.value)
}

function handlePageChange(page) {
  assignmentStore.goToPage(page)
}

function handleEdit(assignment) {
  router.push(`/assignments/${assignment.id}/edit`)
}

function handleDelete(assignment) {
  assignmentToDelete.value = assignment
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!assignmentToDelete.value) return

  isDeleting.value = true
  try {
    await assignmentStore.deleteAssignment(assignmentToDelete.value.id)
    showDeleteModal.value = false
    assignmentToDelete.value = null
  } catch (error) {
    console.error('Delete failed:', error)
  } finally {
    isDeleting.value = false
  }
}
</script>
