<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 sm:mb-8">
      <div>
        <h1 class="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-900 dark:text-white">
          Topshiriqlar
        </h1>
        <p class="mt-1 sm:mt-2 text-sm text-gray-500 dark:text-slate-400">
          Barcha topshiriqlarni boshqaring
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-2 sm:gap-3">
        <!-- Bulk actions -->
        <button 
          v-if="selectedAssignments.length > 0"
          @click="showBulkScoreModal = true" 
          class="inline-flex items-center px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl 
                 bg-gradient-to-r from-amber-500 to-orange-500 text-white 
                 font-semibold text-sm shadow-lg shadow-amber-500/30
                 hover:from-amber-600 hover:to-orange-600 transition-all"
        >
          <SparklesIcon class="w-4 h-4 sm:w-5 sm:h-5 mr-1.5 sm:mr-2" />
          Bulk ball ({{ selectedAssignments.length }})
        </button>
        <RouterLink 
          v-if="userStore.isAdminOrSuperAdmin" 
          :to="createPath" 
          class="inline-flex items-center px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl 
                 bg-gradient-to-r from-indigo-600 to-purple-600 text-white 
                 font-semibold text-sm shadow-lg shadow-indigo-500/30
                 hover:from-indigo-700 hover:to-purple-700 transition-all
                 hover:scale-[1.02] active:scale-[0.98]"
        >
          <PlusIcon class="w-4 h-4 sm:w-5 sm:h-5 mr-1.5 sm:mr-2" />
          <span class="hidden sm:inline">Yangi topshiriq</span>
          <span class="sm:hidden">Yangi</span>
        </RouterLink>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6 sm:mb-8">
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-4 sm:p-5 border border-gray-100 dark:border-slate-700 hover:shadow-lg transition-shadow">
        <div class="flex items-center gap-3">
          <div class="p-2.5 sm:p-3 rounded-xl bg-gray-100 dark:bg-slate-700">
            <FolderIcon class="w-5 h-5 sm:w-6 sm:h-6 text-gray-600 dark:text-slate-300" />
          </div>
          <div>
            <p class="text-xs sm:text-sm font-medium text-gray-500 dark:text-slate-400">Jami</p>
            <p class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white">{{ statistics?.total || 0 }}</p>
          </div>
        </div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-4 sm:p-5 border border-gray-100 dark:border-slate-700 hover:shadow-lg transition-shadow">
        <div class="flex items-center gap-3">
          <div class="p-2.5 sm:p-3 rounded-xl bg-amber-100 dark:bg-amber-900/30">
            <ClockIcon class="w-5 h-5 sm:w-6 sm:h-6 text-amber-600 dark:text-amber-400" />
          </div>
          <div>
            <p class="text-xs sm:text-sm font-medium text-gray-500 dark:text-slate-400">Kutilmoqda</p>
            <p class="text-xl sm:text-2xl font-bold text-amber-600 dark:text-amber-400">{{ statistics?.pending || 0 }}</p>
          </div>
        </div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-4 sm:p-5 border border-gray-100 dark:border-slate-700 hover:shadow-lg transition-shadow">
        <div class="flex items-center gap-3">
          <div class="p-2.5 sm:p-3 rounded-xl bg-emerald-100 dark:bg-emerald-900/30">
            <CheckCircleIcon class="w-5 h-5 sm:w-6 sm:h-6 text-emerald-600 dark:text-emerald-400" />
          </div>
          <div>
            <p class="text-xs sm:text-sm font-medium text-gray-500 dark:text-slate-400">Bajarildi</p>
            <p class="text-xl sm:text-2xl font-bold text-emerald-600 dark:text-emerald-400">{{ statistics?.completed || 0 }}</p>
          </div>
        </div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-4 sm:p-5 border border-gray-100 dark:border-slate-700 hover:shadow-lg transition-shadow">
        <div class="flex items-center gap-3">
          <div class="p-2.5 sm:p-3 rounded-xl bg-red-100 dark:bg-red-900/30">
            <ExclamationCircleIcon class="w-5 h-5 sm:w-6 sm:h-6 text-red-600 dark:text-red-400" />
          </div>
          <div>
            <p class="text-xs sm:text-sm font-medium text-gray-500 dark:text-slate-400">Muddati o'tgan</p>
            <p class="text-xl sm:text-2xl font-bold text-red-600 dark:text-red-400">{{ statistics?.overdue || 0 }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 p-4 sm:p-5 mb-6 sm:mb-8">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 sm:gap-4">
        <!-- Search -->
        <div class="sm:col-span-2">
          <div class="relative">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              v-model="filters.search"
              type="text"
              placeholder="Topshiriq qidirish..."
              class="w-full pl-10 pr-4 py-2.5 sm:py-3 rounded-xl border border-gray-200 dark:border-slate-600 
                     bg-gray-50 dark:bg-slate-700 text-gray-900 dark:text-white
                     placeholder-gray-400 dark:placeholder-slate-400
                     focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                     transition-all text-sm"
              @input="applyFilters"
            />
          </div>
        </div>

        <!-- Status filter -->
        <select 
          v-model="filters.status" 
          @change="applyFilters" 
          class="w-full px-4 py-2.5 sm:py-3 rounded-xl border border-gray-200 dark:border-slate-600 
                 bg-gray-50 dark:bg-slate-700 text-gray-900 dark:text-white
                 focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                 transition-all text-sm appearance-none cursor-pointer"
        >
          <option value="">Barcha statuslar</option>
          <option v-for="s in ASSIGNMENT_STATUSES" :key="s.value" :value="s.value">
            {{ s.label }}
          </option>
        </select>

        <!-- Priority filter -->
        <select 
          v-model="filters.priority" 
          @change="applyFilters" 
          class="w-full px-4 py-2.5 sm:py-3 rounded-xl border border-gray-200 dark:border-slate-600 
                 bg-gray-50 dark:bg-slate-700 text-gray-900 dark:text-white
                 focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                 transition-all text-sm appearance-none cursor-pointer"
        >
          <option value="">Barcha prioritetlar</option>
          <option v-for="p in ASSIGNMENT_PRIORITIES" :key="p.value" :value="p.value">
            {{ p.label }}
          </option>
        </select>

        <!-- Category filter -->
        <select 
          v-model="filters.category" 
          @change="applyFilters" 
          class="w-full px-4 py-2.5 sm:py-3 rounded-xl border border-gray-200 dark:border-slate-600 
                 bg-gray-50 dark:bg-slate-700 text-gray-900 dark:text-white
                 focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                 transition-all text-sm appearance-none cursor-pointer"
        >
          <option value="">Barcha kategoriyalar</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
      <div v-for="i in 6" :key="i" class="bg-white dark:bg-slate-800 rounded-2xl p-5 animate-pulse">
        <div class="h-4 bg-gray-200 dark:bg-slate-700 rounded w-3/4 mb-4"></div>
        <div class="h-3 bg-gray-200 dark:bg-slate-700 rounded w-1/2 mb-6"></div>
        <div class="grid grid-cols-2 gap-3 mb-4">
          <div class="h-16 bg-gray-200 dark:bg-slate-700 rounded-xl"></div>
          <div class="h-16 bg-gray-200 dark:bg-slate-700 rounded-xl"></div>
        </div>
        <div class="h-12 bg-gray-200 dark:bg-slate-700 rounded-xl"></div>
      </div>
    </div>

    <!-- Assignments grid -->
    <div v-else-if="assignments.length > 0">
      <!-- Select all checkbox -->
      <div v-if="userStore.isAdminOrSuperAdmin" class="mb-4 sm:mb-6 flex flex-wrap items-center gap-3 p-3 sm:p-4 bg-gray-50 dark:bg-slate-800/50 rounded-xl">
        <label class="flex items-center gap-2.5 cursor-pointer">
          <input 
            type="checkbox" 
            :checked="isAllSelected"
            @change="toggleSelectAll"
            class="w-5 h-5 text-indigo-600 rounded-lg border-gray-300 dark:border-slate-600 
                   focus:ring-indigo-500 dark:bg-slate-700 cursor-pointer"
          />
          <span class="text-sm font-medium text-gray-700 dark:text-slate-300">
            Barchasini tanlash 
            <span class="text-gray-500 dark:text-slate-400">
              ({{ selectedAssignments.length }}/{{ assignments.length }})
            </span>
          </span>
        </label>
        <button 
          v-if="selectedAssignments.length > 0"
          @click="clearSelection"
          class="text-sm text-red-500 hover:text-red-600 dark:text-red-400 font-medium"
        >
          Tozalash
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
        <div v-for="assignment in assignments" :key="assignment.id" class="relative">
          <!-- Selection checkbox -->
          <div 
            v-if="userStore.isAdminOrSuperAdmin"
            class="absolute top-4 left-4 z-10"
          >
            <input 
              type="checkbox" 
              :checked="isSelected(assignment)"
              @change="toggleSelection(assignment)"
              class="w-5 h-5 text-indigo-600 rounded-lg border-2 border-white dark:border-slate-700
                     shadow-lg focus:ring-indigo-500 cursor-pointer bg-white dark:bg-slate-700"
              @click.stop
            />
          </div>
          <AssignmentCard
            :assignment="assignment"
            :can-edit="userStore.isAdminOrSuperAdmin"
            :can-delete="userStore.isAdminOrSuperAdmin"
            :class="{ 'ring-2 ring-indigo-500 ring-offset-2 dark:ring-offset-slate-900': isSelected(assignment) }"
            @edit="handleEdit"
            @delete="handleDelete"
          />
        </div>
      </div>

      <!-- Pagination -->
      <div class="mt-6 sm:mt-8">
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
    <div 
      v-else
      class="flex flex-col items-center justify-center py-12 sm:py-16 px-4"
    >
      <div class="w-20 h-20 sm:w-24 sm:h-24 mb-6 rounded-2xl bg-gray-100 dark:bg-slate-800 flex items-center justify-center">
        <FolderIcon class="w-10 h-10 sm:w-12 sm:h-12 text-gray-400 dark:text-slate-500" />
      </div>
      <h3 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 text-center">
        Topshiriq topilmadi
      </h3>
      <p class="text-sm text-gray-500 dark:text-slate-400 text-center max-w-sm mb-6">
        Hozircha hech qanday topshiriq yo'q
      </p>
      <RouterLink 
        v-if="userStore.isAdminOrSuperAdmin"
        :to="createPath" 
        class="inline-flex items-center px-5 py-3 rounded-xl 
               bg-gradient-to-r from-indigo-600 to-purple-600 text-white 
               font-semibold shadow-lg shadow-indigo-500/30
               hover:from-indigo-700 hover:to-purple-700 transition-all"
      >
        <PlusIcon class="w-5 h-5 mr-2" />
        Yangi topshiriq
      </RouterLink>
    </div>

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

    <!-- Bulk Score Modal -->
    <BulkScoreModal
      :is-open="showBulkScoreModal"
      :selected-assignments="selectedAssignments"
      @close="showBulkScoreModal = false"
      @updated="handleBulkUpdated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  PlusIcon, 
  SparklesIcon, 
  FolderIcon, 
  ClockIcon, 
  CheckCircleIcon, 
  ExclamationCircleIcon,
  MagnifyingGlassIcon
} from '@heroicons/vue/24/outline'
import { Pagination, ConfirmModal } from '@/components/common'
import { AssignmentCard, BulkScoreModal } from '@/components/assignments'
import { useAssignmentStore, useUserStore } from '@/stores'
import { ASSIGNMENT_STATUSES, ASSIGNMENT_PRIORITIES } from '@/services'

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

const createPath = computed(() => `${basePath.value}/new`)

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
const showBulkScoreModal = ref(false)
const isDeleting = ref(false)
const assignmentToDelete = ref(null)
const selectedAssignments = ref([])

const isAllSelected = computed(() => {
  return assignments.value.length > 0 && selectedAssignments.value.length === assignments.value.length
})

onMounted(async () => {
  await Promise.all([
    assignmentStore.fetchAssignments(),
    assignmentStore.fetchCategories(),
    assignmentStore.fetchStatistics()
  ])
})

function applyFilters() {
  assignmentStore.setFilters(filters.value)
  clearSelection()
}

function handlePageChange(page) {
  assignmentStore.goToPage(page)
  clearSelection()
}

function isSelected(assignment) {
  return selectedAssignments.value.some(a => a.id === assignment.id)
}

function toggleSelection(assignment) {
  if (isSelected(assignment)) {
    selectedAssignments.value = selectedAssignments.value.filter(a => a.id !== assignment.id)
  } else {
    selectedAssignments.value.push(assignment)
  }
}

function toggleSelectAll() {
  if (isAllSelected.value) {
    clearSelection()
  } else {
    selectedAssignments.value = [...assignments.value]
  }
}

function clearSelection() {
  selectedAssignments.value = []
}

function handleBulkUpdated() {
  clearSelection()
  assignmentStore.fetchAssignments()
}

function handleEdit(assignment) {
  router.push(`${basePath.value}/${assignment.id}/edit`)
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
