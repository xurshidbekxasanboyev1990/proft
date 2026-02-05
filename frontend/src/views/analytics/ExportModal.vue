<template>
  <BaseModal :is-open="isOpen" title="Ma'lumotlarni eksport qilish" @close="$emit('close')">
    <div class="space-y-6">
      <!-- Format selection -->
      <div>
        <label class="form-label">Format</label>
        <div class="grid grid-cols-2 gap-3">
          <button
            v-for="format in EXPORT_FORMATS"
            :key="format.value"
            @click="selectedFormat = format.value"
            class="p-4 border rounded-lg text-left transition-all"
            :class="selectedFormat === format.value 
              ? 'border-primary-500 bg-primary-50 ring-2 ring-primary-500' 
              : 'border-gray-200 hover:border-gray-300'"
          >
            <div class="flex items-center gap-3">
              <component :is="getFormatIcon(format.value)" class="w-8 h-8 text-gray-400" />
              <div>
                <p class="font-medium text-gray-900">{{ format.label }}</p>
                <p class="text-xs text-gray-500">{{ getFormatDescription(format.value) }}</p>
              </div>
            </div>
          </button>
        </div>
      </div>

      <!-- Data type selection -->
      <div>
        <label class="form-label">Ma'lumot turi</label>
        <div class="space-y-2">
          <label
            v-for="type in dataTypes"
            :key="type.value"
            class="flex items-center gap-3 p-3 border rounded-lg cursor-pointer transition-all"
            :class="selectedDataType === type.value 
              ? 'border-primary-500 bg-primary-50' 
              : 'border-gray-200 hover:border-gray-300'"
          >
            <input
              type="radio"
              :value="type.value"
              v-model="selectedDataType"
              class="text-primary-600 focus:ring-primary-500"
            />
            <div>
              <p class="font-medium text-gray-900">{{ type.label }}</p>
              <p class="text-xs text-gray-500">{{ type.description }}</p>
            </div>
          </label>
        </div>
      </div>

      <!-- Date range (optional) -->
      <div>
        <label class="form-label">Vaqt oralig'i (ixtiyoriy)</label>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-xs text-gray-500">Boshlanish</label>
            <input v-model="dateRange.start" type="date" class="form-input" />
          </div>
          <div>
            <label class="text-xs text-gray-500">Tugash</label>
            <input v-model="dateRange.end" type="date" class="form-input" />
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <button @click="$emit('close')" class="btn-secondary">
        Bekor qilish
      </button>
      <button @click="handleExport" class="btn-primary" :disabled="isExporting">
        <LoadingSpinner v-if="isExporting" size="xs" color="white" />
        <template v-else>
          <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
          Yuklab olish
        </template>
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ArrowDownTrayIcon, DocumentIcon, TableCellsIcon, DocumentTextIcon, CodeBracketIcon } from '@heroicons/vue/24/outline'
import { BaseModal, LoadingSpinner } from '@/components/common'
import { EXPORT_FORMATS } from '@/services'

defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close', 'export'])

const selectedFormat = ref('xlsx')
const selectedDataType = ref('portfolios')
const isExporting = ref(false)

const dateRange = reactive({
  start: '',
  end: ''
})

const dataTypes = [
  { value: 'portfolios', label: 'Portfoliolar', description: 'Barcha portfoliolar va ularning ma\'lumotlari' },
  { value: 'assignments', label: 'Topshiriqlar', description: 'Topshiriqlar va bajarilish holati' },
  { value: 'teachers', label: 'O\'qituvchilar', description: 'O\'qituvchilar reytingi va statistikasi' },
  { value: 'analytics', label: 'Analitika', description: 'Umumiy statistik ma\'lumotlar' }
]

function getFormatIcon(format) {
  const icons = {
    xlsx: TableCellsIcon,
    pdf: DocumentTextIcon,
    csv: DocumentIcon,
    json: CodeBracketIcon
  }
  return icons[format] || DocumentIcon
}

function getFormatDescription(format) {
  const descriptions = {
    xlsx: 'Microsoft Excel formati',
    pdf: 'Portable Document Format',
    csv: 'Comma Separated Values',
    json: 'JavaScript Object Notation'
  }
  return descriptions[format] || ''
}

async function handleExport() {
  isExporting.value = true
  try {
    emit('export', {
      format: selectedFormat.value,
      data_type: selectedDataType.value,
      start_date: dateRange.start || undefined,
      end_date: dateRange.end || undefined
    })
  } finally {
    isExporting.value = false
  }
}
</script>
