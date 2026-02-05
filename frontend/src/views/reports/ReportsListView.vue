<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Hisobotlar</h1>
        <p class="mt-1 text-sm text-gray-500">
          Tizim hisobotlarini yarating va yuklab oling
        </p>
      </div>
      <button @click="showCreateModal = true" class="btn-primary">
        <PlusIcon class="w-5 h-5 mr-2" />
        Yangi hisobot
      </button>
    </div>

    <!-- Quick export cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <button
        v-for="format in quickExportFormats"
        :key="format.value"
        @click="handleQuickExport(format.value)"
        class="card hover:shadow-lg transition-all text-left group"
        :disabled="exportingFormat === format.value"
      >
        <div class="card-body">
          <div class="flex items-center gap-4">
            <div
              class="w-12 h-12 rounded-xl flex items-center justify-center transition-colors"
              :class="format.bgClass"
            >
              <component :is="format.icon" class="w-6 h-6" :class="format.iconClass" />
            </div>
            <div>
              <p class="font-medium text-gray-900 group-hover:text-primary-600">{{ format.label }}</p>
              <p class="text-xs text-gray-500">{{ format.description }}</p>
            </div>
          </div>
          <LoadingSpinner v-if="exportingFormat === format.value" size="sm" class="absolute top-2 right-2" />
        </div>
      </button>
    </div>

    <!-- Reports table -->
    <div class="card">
      <div class="card-header flex items-center justify-between">
        <h2 class="text-lg font-semibold text-gray-900">Yaratilgan hisobotlar</h2>
        <button @click="fetchReports" class="btn-ghost btn-sm">
          <ArrowPathIcon class="w-4 h-4 mr-1" />
          Yangilash
        </button>
      </div>
      <div class="card-body p-0">
        <div v-if="isLoading" class="p-6">
          <SkeletonLoader type="table" />
        </div>
        <div v-else-if="reports.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nomi</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Turi</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Format</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Yaratilgan</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amallar</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="report in reports" :key="report.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center">
                      <DocumentTextIcon class="w-4 h-4 text-gray-500" />
                    </div>
                    <span class="text-sm font-medium text-gray-900">{{ report.title }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="text-sm text-gray-600">{{ getReportTypeLabel(report.report_type) }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="px-2 py-1 text-xs font-medium rounded-md uppercase"
                    :class="getFormatClass(report.format)"
                  >
                    {{ report.format }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <StatusBadge :variant="report.status" dot>
                    {{ getStatusLabel(report.status) }}
                  </StatusBadge>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(report.created_at) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button
                      v-if="report.status === 'completed'"
                      @click="handleDownload(report)"
                      class="p-1.5 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                      title="Yuklab olish"
                    >
                      <ArrowDownTrayIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleDelete(report)"
                      class="p-1.5 text-danger-600 hover:bg-danger-50 rounded-lg transition-colors"
                      title="O'chirish"
                    >
                      <TrashIcon class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <EmptyState
          v-else
          title="Hisobot topilmadi"
          description="Yangi hisobot yarating"
          action-text="Yangi hisobot"
          @action="showCreateModal = true"
        />
      </div>
    </div>

    <!-- Create report modal -->
    <BaseModal
      :is-open="showCreateModal"
      title="Yangi hisobot"
      @close="showCreateModal = false"
    >
      <form @submit.prevent="handleCreate" class="space-y-4">
        <div>
          <label for="title" class="form-label">Nomi <span class="text-danger-500">*</span></label>
          <input
            id="title"
            v-model="createForm.title"
            type="text"
            class="form-input"
            placeholder="Hisobot nomi"
          />
        </div>

        <div>
          <label class="form-label">Hisobot turi</label>
          <select v-model="createForm.report_type" class="form-input">
            <option v-for="type in REPORT_TYPES" :key="type.value" :value="type.value">
              {{ type.label }}
            </option>
          </select>
        </div>

        <div>
          <label class="form-label">Format</label>
          <div class="grid grid-cols-4 gap-2">
            <button
              v-for="format in EXPORT_FORMATS"
              :key="format.value"
              type="button"
              @click="createForm.format = format.value"
              class="p-3 border rounded-lg text-center transition-all"
              :class="createForm.format === format.value 
                ? 'border-primary-500 bg-primary-50' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <span class="text-sm font-medium">{{ format.label }}</span>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="form-label">Boshlanish sanasi</label>
            <input v-model="createForm.start_date" type="date" class="form-input" />
          </div>
          <div>
            <label class="form-label">Tugash sanasi</label>
            <input v-model="createForm.end_date" type="date" class="form-input" />
          </div>
        </div>
      </form>

      <template #footer>
        <button @click="showCreateModal = false" class="btn-secondary">Bekor qilish</button>
        <button @click="handleCreate" class="btn-primary" :disabled="isCreating">
          <LoadingSpinner v-if="isCreating" size="xs" color="white" />
          <span v-else>Yaratish</span>
        </button>
      </template>
    </BaseModal>

    <!-- Delete modal -->
    <ConfirmModal
      :is-open="showDeleteModal"
      title="Hisobotni o'chirish"
      message="Bu hisobotni o'chirishga ishonchingiz komilmi?"
      type="danger"
      :is-loading="isDeleting"
      @confirm="confirmDelete"
      @cancel="showDeleteModal = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { 
  PlusIcon, 
  ArrowPathIcon, 
  ArrowDownTrayIcon, 
  TrashIcon, 
  DocumentTextIcon,
  TableCellsIcon,
  DocumentIcon,
  CodeBracketIcon
} from '@heroicons/vue/24/outline'
import { StatsCard, SkeletonLoader, EmptyState, BaseModal, ConfirmModal, LoadingSpinner, StatusBadge } from '@/components/common'
import { useAnalyticsStore } from '@/stores'
import { REPORT_TYPES, EXPORT_FORMATS } from '@/services'
import dayjs from 'dayjs'

const analyticsStore = useAnalyticsStore()

const isLoading = computed(() => analyticsStore.isLoading)
const reports = computed(() => analyticsStore.reports)

const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const isCreating = ref(false)
const isDeleting = ref(false)
const exportingFormat = ref(null)
const reportToDelete = ref(null)

const createForm = reactive({
  title: '',
  report_type: 'general',
  format: 'xlsx',
  start_date: '',
  end_date: ''
})

const quickExportFormats = [
  { 
    value: 'xlsx', 
    label: 'Excel', 
    description: 'XLSX formatida', 
    icon: TableCellsIcon,
    bgClass: 'bg-success-100',
    iconClass: 'text-success-600'
  },
  { 
    value: 'pdf', 
    label: 'PDF', 
    description: 'PDF formatida',
    icon: DocumentTextIcon,
    bgClass: 'bg-danger-100',
    iconClass: 'text-danger-600'
  },
  { 
    value: 'csv', 
    label: 'CSV', 
    description: 'CSV formatida',
    icon: DocumentIcon,
    bgClass: 'bg-warning-100',
    iconClass: 'text-warning-600'
  },
  { 
    value: 'json', 
    label: 'JSON', 
    description: 'JSON formatida',
    icon: CodeBracketIcon,
    bgClass: 'bg-primary-100',
    iconClass: 'text-primary-600'
  }
]

onMounted(() => {
  fetchReports()
})

async function fetchReports() {
  await analyticsStore.fetchReports()
}

function formatDate(date) {
  return dayjs(date).format('D MMM YYYY, HH:mm')
}

function getReportTypeLabel(type) {
  const found = REPORT_TYPES.find(t => t.value === type)
  return found?.label || type
}

function getStatusLabel(status) {
  const labels = {
    pending: 'Kutilmoqda',
    processing: 'Jarayonda',
    completed: 'Tayyor',
    failed: 'Xato'
  }
  return labels[status] || status
}

function getFormatClass(format) {
  const classes = {
    xlsx: 'bg-success-100 text-success-700',
    pdf: 'bg-danger-100 text-danger-700',
    csv: 'bg-warning-100 text-warning-700',
    json: 'bg-primary-100 text-primary-700'
  }
  return classes[format] || 'bg-gray-100 text-gray-700'
}

async function handleQuickExport(format) {
  exportingFormat.value = format
  try {
    await analyticsStore.quickExport(format, 'portfolios')
  } catch (error) {
    console.error('Quick export failed:', error)
  } finally {
    exportingFormat.value = null
  }
}

async function handleCreate() {
  if (!createForm.title.trim()) return

  isCreating.value = true
  try {
    await analyticsStore.createReport(createForm)
    showCreateModal.value = false
    Object.assign(createForm, {
      title: '',
      report_type: 'general',
      format: 'xlsx',
      start_date: '',
      end_date: ''
    })
  } catch (error) {
    console.error('Create report failed:', error)
  } finally {
    isCreating.value = false
  }
}

async function handleDownload(report) {
  await analyticsStore.downloadReport(report.id)
}

function handleDelete(report) {
  reportToDelete.value = report
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!reportToDelete.value) return

  isDeleting.value = true
  try {
    await analyticsStore.deleteReport(reportToDelete.value.id)
    showDeleteModal.value = false
    reportToDelete.value = null
  } catch (error) {
    console.error('Delete failed:', error)
  } finally {
    isDeleting.value = false
  }
}
</script>
