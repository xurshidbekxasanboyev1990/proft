<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="mb-6">
      <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
        <RouterLink to="/reports" class="hover:text-primary-600">Hisobotlar</RouterLink>
        <ChevronRightIcon class="w-4 h-4" />
        <span class="text-gray-900">Yangi hisobot</span>
      </div>
      <h1 class="text-2xl font-bold text-gray-900">Hisobot yaratish</h1>
      <p class="mt-1 text-sm text-gray-500">
        Parametrlarni tanlab hisobot yarating
      </p>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Configuration -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Report Type -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <DocumentChartBarIcon class="w-5 h-5 text-gray-400" />
              Hisobot turi
            </h2>
          </div>
          <div class="card-body">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <label 
                v-for="type in reportTypes" 
                :key="type.value"
                :class="[
                  'flex items-center gap-3 p-4 border-2 rounded-xl cursor-pointer transition-all',
                  form.type === type.value 
                    ? 'border-primary-500 bg-primary-50' 
                    : 'border-gray-200 hover:border-gray-300'
                ]"
              >
                <input 
                  type="radio" 
                  :value="type.value" 
                  v-model="form.type" 
                  class="sr-only"
                />
                <div 
                  :class="[
                    'w-10 h-10 rounded-lg flex items-center justify-center',
                    form.type === type.value ? type.activeClass : 'bg-gray-100'
                  ]"
                >
                  <component :is="type.icon" class="w-5 h-5" :class="form.type === type.value ? 'text-white' : 'text-gray-500'" />
                </div>
                <div>
                  <p class="font-medium text-gray-900">{{ type.label }}</p>
                  <p class="text-xs text-gray-500">{{ type.description }}</p>
                </div>
              </label>
            </div>
          </div>
        </div>
        
        <!-- Date Range -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <CalendarIcon class="w-5 h-5 text-gray-400" />
              Sana oralig'i
            </h2>
          </div>
          <div class="card-body">
            <!-- Preset ranges -->
            <div class="flex flex-wrap gap-2 mb-4">
              <button 
                v-for="preset in datePresets" 
                :key="preset.value"
                @click="applyDatePreset(preset.value)"
                :class="[
                  'px-3 py-1.5 text-sm rounded-lg transition-colors',
                  activePreset === preset.value 
                    ? 'bg-primary-600 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                {{ preset.label }}
              </button>
            </div>
            
            <!-- Custom range -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="form-label">Boshlanish sanasi</label>
                <input 
                  type="date" 
                  v-model="form.date_from" 
                  class="form-input"
                  @change="activePreset = null"
                />
              </div>
              <div>
                <label class="form-label">Tugash sanasi</label>
                <input 
                  type="date" 
                  v-model="form.date_to" 
                  class="form-input"
                  @change="activePreset = null"
                />
              </div>
            </div>
          </div>
        </div>
        
        <!-- Filters -->
        <div class="card">
          <div class="card-header flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <FunnelIcon class="w-5 h-5 text-gray-400" />
              Qo'shimcha filtrlar
            </h2>
            <button 
              @click="showFilters = !showFilters" 
              class="btn-ghost btn-sm"
            >
              {{ showFilters ? 'Yashirish' : "Ko'rsatish" }}
              <ChevronDownIcon 
                class="w-4 h-4 ml-1 transition-transform" 
                :class="showFilters ? 'rotate-180' : ''"
              />
            </button>
          </div>
          <div v-if="showFilters" class="card-body space-y-4 border-t border-gray-100">
            <!-- Department -->
            <div>
              <label class="form-label">Bo'lim</label>
              <select v-model="form.department" class="form-input">
                <option value="">Barcha bo'limlar</option>
                <option value="it">IT</option>
                <option value="pedagogika">Pedagogika</option>
                <option value="tarix">Tarix</option>
                <option value="matematika">Matematika</option>
                <option value="filologiya">Filologiya</option>
              </select>
            </div>
            
            <!-- Status (for portfolios) -->
            <div v-if="form.type === 'portfolios'">
              <label class="form-label">Status</label>
              <select v-model="form.status" class="form-input">
                <option value="">Barcha statuslar</option>
                <option value="draft">Qoralama</option>
                <option value="pending">Kutilmoqda</option>
                <option value="approved">Tasdiqlangan</option>
                <option value="rejected">Rad etilgan</option>
              </select>
            </div>
            
            <!-- Category (for assignments) -->
            <div v-if="form.type === 'assignments'">
              <label class="form-label">Kategoriya</label>
              <select v-model="form.category" class="form-input">
                <option value="">Barcha kategoriyalar</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
            </div>
            
            <!-- Include inactive users -->
            <div class="flex items-center gap-2">
              <input 
                type="checkbox" 
                id="include_inactive" 
                v-model="form.include_inactive"
                class="form-checkbox"
              />
              <label for="include_inactive" class="text-sm text-gray-700">
                Faol bo'lmagan foydalanuvchilarni ham qo'shish
              </label>
            </div>
          </div>
        </div>
        
        <!-- Report Name -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <TagIcon class="w-5 h-5 text-gray-400" />
              Hisobot nomi
            </h2>
          </div>
          <div class="card-body">
            <input 
              type="text" 
              v-model="form.title"
              class="form-input"
              placeholder="Masalan: Yanvar oyi portfolio hisoboti"
            />
            <p class="text-xs text-gray-400 mt-1">
              Bo'sh qoldirilsa avtomatik nom beriladi
            </p>
          </div>
        </div>
      </div>
      
      <!-- Preview & Actions -->
      <div class="space-y-6">
        <!-- Format selection -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900">Format</h2>
          </div>
          <div class="card-body space-y-2">
            <label 
              v-for="fmt in formats" 
              :key="fmt.value"
              :class="[
                'flex items-center gap-3 p-3 border-2 rounded-lg cursor-pointer transition-all',
                form.format === fmt.value 
                  ? 'border-primary-500 bg-primary-50' 
                  : 'border-gray-200 hover:border-gray-300'
              ]"
            >
              <input 
                type="radio" 
                :value="fmt.value" 
                v-model="form.format" 
                class="sr-only"
              />
              <div :class="['w-8 h-8 rounded-lg flex items-center justify-center', fmt.bgClass]">
                <component :is="fmt.icon" class="w-4 h-4" :class="fmt.iconClass" />
              </div>
              <div class="flex-1">
                <p class="font-medium text-gray-900">{{ fmt.label }}</p>
                <p class="text-xs text-gray-500">{{ fmt.ext }}</p>
              </div>
              <CheckCircleIcon 
                v-if="form.format === fmt.value" 
                class="w-5 h-5 text-primary-600" 
              />
            </label>
          </div>
        </div>
        
        <!-- Summary -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900">Xulosa</h2>
          </div>
          <div class="card-body space-y-3">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Turi:</span>
              <span class="font-medium">{{ getTypeLabel(form.type) }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Sana:</span>
              <span class="font-medium">{{ formatDateRange }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Format:</span>
              <span class="font-medium uppercase">{{ form.format }}</span>
            </div>
            <div v-if="form.department" class="flex justify-between text-sm">
              <span class="text-gray-500">Bo'lim:</span>
              <span class="font-medium">{{ form.department }}</span>
            </div>
          </div>
        </div>
        
        <!-- Actions -->
        <div class="space-y-3">
          <button 
            @click="generateReport" 
            class="btn-primary w-full"
            :disabled="isGenerating"
          >
            <LoadingSpinner v-if="isGenerating" size="xs" color="white" class="mr-2" />
            <DocumentArrowDownIcon v-else class="w-5 h-5 mr-2" />
            {{ isGenerating ? 'Yaratilmoqda...' : 'Hisobot yaratish' }}
          </button>
          
          <button 
            @click="previewReport" 
            class="btn-secondary w-full"
            :disabled="isPreviewing"
          >
            <EyeIcon class="w-5 h-5 mr-2" />
            Oldindan ko'rish
          </button>
          
          <RouterLink to="/reports" class="btn-ghost w-full text-center block">
            Bekor qilish
          </RouterLink>
        </div>
        
        <!-- Recent reports -->
        <div class="card" v-if="recentReports.length > 0">
          <div class="card-header">
            <h3 class="text-sm font-medium text-gray-700">So'nggi hisobotlar</h3>
          </div>
          <div class="card-body p-0">
            <div 
              v-for="report in recentReports" 
              :key="report.id"
              class="flex items-center justify-between px-4 py-3 border-b border-gray-100 last:border-0"
            >
              <div class="flex items-center gap-2">
                <DocumentTextIcon class="w-4 h-4 text-gray-400" />
                <span class="text-sm text-gray-700 truncate max-w-[150px]">{{ report.title }}</span>
              </div>
              <button @click="downloadReport(report)" class="text-primary-600 hover:text-primary-700">
                <ArrowDownTrayIcon class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import dayjs from 'dayjs'
import { 
  ChevronRightIcon,
  ChevronDownIcon,
  DocumentChartBarIcon,
  CalendarIcon,
  FunnelIcon,
  TagIcon,
  CheckCircleIcon,
  DocumentArrowDownIcon,
  EyeIcon,
  DocumentTextIcon,
  ArrowDownTrayIcon,
  FolderIcon,
  ClipboardDocumentListIcon,
  UsersIcon,
  ChartBarIcon,
  TableCellsIcon,
  DocumentIcon
} from '@heroicons/vue/24/outline'
import { LoadingSpinner } from '@/components/common'
import { analyticsService } from '@/services'
import { useUserStore } from '@/stores'

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const isGenerating = ref(false)
const isPreviewing = ref(false)
const showFilters = ref(false)
const activePreset = ref('month')
const recentReports = ref([])
const categories = ref([])

const form = reactive({
  type: 'overview',
  format: 'excel',
  date_from: dayjs().subtract(1, 'month').format('YYYY-MM-DD'),
  date_to: dayjs().format('YYYY-MM-DD'),
  department: '',
  status: '',
  category: '',
  include_inactive: false,
  title: ''
})

const reportTypes = [
  { 
    value: 'overview', 
    label: 'Umumiy statistika', 
    description: 'Tizim umumiy ko\'rsatkichlari',
    icon: ChartBarIcon,
    activeClass: 'bg-blue-600'
  },
  { 
    value: 'portfolios', 
    label: 'Portfoliolar', 
    description: 'Portfolio hisoboti',
    icon: FolderIcon,
    activeClass: 'bg-green-600'
  },
  { 
    value: 'assignments', 
    label: 'Topshiriqlar', 
    description: 'Topshiriqlar hisoboti',
    icon: ClipboardDocumentListIcon,
    activeClass: 'bg-purple-600'
  },
  { 
    value: 'teachers', 
    label: "O'qituvchilar", 
    description: "O'qituvchilar reytingi",
    icon: UsersIcon,
    activeClass: 'bg-orange-600'
  }
]

const formats = [
  { 
    value: 'excel', 
    label: 'Excel', 
    ext: '.xlsx',
    icon: TableCellsIcon,
    bgClass: 'bg-green-100',
    iconClass: 'text-green-600'
  },
  { 
    value: 'pdf', 
    label: 'PDF', 
    ext: '.pdf',
    icon: DocumentIcon,
    bgClass: 'bg-red-100',
    iconClass: 'text-red-600'
  },
  { 
    value: 'csv', 
    label: 'CSV', 
    ext: '.csv',
    icon: TableCellsIcon,
    bgClass: 'bg-blue-100',
    iconClass: 'text-blue-600'
  }
]

const datePresets = [
  { value: 'week', label: 'Bu hafta' },
  { value: 'month', label: 'Bu oy' },
  { value: 'quarter', label: 'Bu chorak' },
  { value: 'year', label: 'Bu yil' }
]

const formatDateRange = computed(() => {
  if (!form.date_from || !form.date_to) return '-'
  return `${dayjs(form.date_from).format('DD.MM.YYYY')} - ${dayjs(form.date_to).format('DD.MM.YYYY')}`
})

function getTypeLabel(type) {
  return reportTypes.find(t => t.value === type)?.label || type
}

function applyDatePreset(preset) {
  activePreset.value = preset
  const today = dayjs()
  
  switch (preset) {
    case 'week':
      form.date_from = today.startOf('week').format('YYYY-MM-DD')
      form.date_to = today.format('YYYY-MM-DD')
      break
    case 'month':
      form.date_from = today.startOf('month').format('YYYY-MM-DD')
      form.date_to = today.format('YYYY-MM-DD')
      break
    case 'quarter':
      form.date_from = today.startOf('quarter').format('YYYY-MM-DD')
      form.date_to = today.format('YYYY-MM-DD')
      break
    case 'year':
      form.date_from = today.startOf('year').format('YYYY-MM-DD')
      form.date_to = today.format('YYYY-MM-DD')
      break
  }
}

async function generateReport() {
  isGenerating.value = true
  
  try {
    const params = {
      type: form.type,
      format: form.format,
      date_from: form.date_from,
      date_to: form.date_to,
      title: form.title || `${getTypeLabel(form.type)} - ${formatDateRange.value}`
    }
    
    if (form.department) params.department = form.department
    if (form.status) params.status = form.status
    if (form.category) params.category = form.category
    if (form.include_inactive) params.include_inactive = true
    
    const response = await analyticsService.createReport(params)
    
    toast.success('Hisobot muvaffaqiyatli yaratildi')
    
    // Download the report
    if (response.download_url) {
      window.open(response.download_url, '_blank')
    }
    
    router.push('/reports')
  } catch (error) {
    console.error('Failed to generate report:', error)
    toast.error('Hisobot yaratishda xatolik')
  } finally {
    isGenerating.value = false
  }
}

async function previewReport() {
  isPreviewing.value = true
  
  try {
    const params = {
      type: form.type,
      format: 'json',
      date_from: form.date_from,
      date_to: form.date_to
    }
    
    const response = await analyticsService.quickExport(params)
    
    // Show preview in modal or new tab
    console.log('Preview data:', response)
    toast.info('Preview funksiyasi tez orada qo\'shiladi')
  } catch (error) {
    console.error('Failed to preview:', error)
    toast.error('Preview xatosi')
  } finally {
    isPreviewing.value = false
  }
}

async function downloadReport(report) {
  try {
    const response = await analyticsService.downloadReport(report.id)
    if (response.url) {
      window.open(response.url, '_blank')
    }
  } catch (error) {
    toast.error('Yuklab olishda xatolik')
  }
}

async function fetchRecentReports() {
  try {
    const response = await analyticsService.getReports({ limit: 3 })
    recentReports.value = response.results || []
  } catch (error) {
    console.error('Failed to fetch recent reports:', error)
  }
}

onMounted(() => {
  applyDatePreset('month')
  fetchRecentReports()
})
</script>
