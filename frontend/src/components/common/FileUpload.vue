<template>
  <div
    class="relative border-2 border-dashed rounded-lg transition-colors"
    :class="[
      isDragging ? 'border-primary-500 bg-primary-50' : 'border-gray-300 bg-gray-50',
      disabled ? 'opacity-50 cursor-not-allowed' : 'hover:border-primary-400 cursor-pointer'
    ]"
    @dragenter.prevent="onDragEnter"
    @dragleave.prevent="onDragLeave"
    @dragover.prevent
    @drop.prevent="onDrop"
    @click="openFilePicker"
  >
    <input
      ref="fileInput"
      type="file"
      :multiple="multiple"
      :accept="acceptString"
      class="hidden"
      :disabled="disabled"
      @change="onFileSelect"
    />
    
    <div class="p-6 text-center">
      <!-- Upload icon -->
      <div class="mx-auto w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center mb-4">
        <CloudArrowUpIcon class="w-6 h-6 text-gray-400" />
      </div>
      
      <!-- Instructions -->
      <p class="text-sm text-gray-600 mb-1">
        <span class="font-medium text-primary-600">Faylni tanlang</span>
        yoki bu yerga tashlang
      </p>
      <p class="text-xs text-gray-500">
        {{ acceptHint }} (max {{ formatSize(maxSize) }})
      </p>
    </div>
    
    <!-- Selected files list -->
    <div v-if="modelValue.length > 0" class="border-t border-gray-200 p-4 space-y-2">
      <div
        v-for="(file, index) in modelValue"
        :key="index"
        class="flex items-center justify-between p-2 bg-white rounded-lg border border-gray-200"
      >
        <div class="flex items-center gap-3 min-w-0">
          <div class="w-8 h-8 rounded flex items-center justify-center flex-shrink-0" :class="getFileIconBg(file)">
            <component :is="getFileIcon(file)" class="w-4 h-4" :class="getFileIconColor(file)" />
          </div>
          <div class="min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">{{ file.name }}</p>
            <p class="text-xs text-gray-500">{{ formatSize(file.size) }}</p>
          </div>
        </div>
        <button
          type="button"
          @click.stop="removeFile(index)"
          class="p-1 text-gray-400 hover:text-danger-500 transition-colors"
        >
          <XMarkIcon class="w-5 h-5" />
        </button>
      </div>
    </div>
    
    <!-- Progress bar (if uploading) -->
    <div v-if="uploadProgress > 0 && uploadProgress < 100" class="px-4 pb-4">
      <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
        <div 
          class="h-full bg-primary-500 transition-all duration-300"
          :style="{ width: `${uploadProgress}%` }"
        ></div>
      </div>
      <p class="text-xs text-gray-500 text-center mt-1">{{ uploadProgress }}% yuklandi</p>
    </div>
  </div>
  
  <!-- Error message -->
  <p v-if="error" class="mt-2 text-sm text-danger-600">{{ error }}</p>
</template>

<script setup>
import { ref, computed } from 'vue'
import { 
  CloudArrowUpIcon, 
  XMarkIcon,
  DocumentIcon,
  PhotoIcon,
  DocumentTextIcon,
  PresentationChartBarIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  multiple: {
    type: Boolean,
    default: true
  },
  maxFiles: {
    type: Number,
    default: 10
  },
  maxSize: {
    type: Number,
    default: 10 * 1024 * 1024 // 10MB
  },
  accept: {
    type: Array,
    default: () => ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.ppt', '.pptx']
  },
  disabled: {
    type: Boolean,
    default: false
  },
  uploadProgress: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['update:modelValue', 'error'])

const fileInput = ref(null)
const isDragging = ref(false)
const error = ref('')

const acceptString = computed(() => props.accept.join(','))

const acceptHint = computed(() => {
  const types = props.accept.map(ext => ext.replace('.', '').toUpperCase())
  if (types.length > 4) {
    return types.slice(0, 4).join(', ') + '...'
  }
  return types.join(', ')
})

function formatSize(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

function openFilePicker() {
  if (!props.disabled) {
    fileInput.value?.click()
  }
}

function onDragEnter() {
  if (!props.disabled) isDragging.value = true
}

function onDragLeave() {
  isDragging.value = false
}

function onDrop(event) {
  isDragging.value = false
  if (props.disabled) return
  
  const files = Array.from(event.dataTransfer.files)
  processFiles(files)
}

function onFileSelect(event) {
  const files = Array.from(event.target.files)
  processFiles(files)
  event.target.value = '' // Reset input
}

function processFiles(files) {
  error.value = ''
  
  // Check max files
  const totalFiles = props.modelValue.length + files.length
  if (totalFiles > props.maxFiles) {
    error.value = `Maksimum ${props.maxFiles} ta fayl yuklash mumkin`
    emit('error', error.value)
    return
  }
  
  // Validate each file
  const validFiles = []
  for (const file of files) {
    // Check file size
    if (file.size > props.maxSize) {
      error.value = `"${file.name}" fayli juda katta (max ${formatSize(props.maxSize)})`
      emit('error', error.value)
      continue
    }
    
    // Check file type
    const ext = '.' + file.name.split('.').pop().toLowerCase()
    if (!props.accept.includes(ext) && !props.accept.includes(file.type)) {
      error.value = `"${file.name}" fayl turi qo'llab-quvvatlanmaydi`
      emit('error', error.value)
      continue
    }
    
    validFiles.push(file)
  }
  
  if (validFiles.length > 0) {
    emit('update:modelValue', [...props.modelValue, ...validFiles])
  }
}

function removeFile(index) {
  const newFiles = [...props.modelValue]
  newFiles.splice(index, 1)
  emit('update:modelValue', newFiles)
  error.value = ''
}

function getFileIcon(file) {
  const ext = file.name.split('.').pop().toLowerCase()
  if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext)) return PhotoIcon
  if (['pdf'].includes(ext)) return DocumentTextIcon
  if (['ppt', 'pptx'].includes(ext)) return PresentationChartBarIcon
  return DocumentIcon
}

function getFileIconBg(file) {
  const ext = file.name.split('.').pop().toLowerCase()
  if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext)) return 'bg-purple-100'
  if (['pdf'].includes(ext)) return 'bg-red-100'
  if (['ppt', 'pptx'].includes(ext)) return 'bg-orange-100'
  if (['doc', 'docx'].includes(ext)) return 'bg-blue-100'
  return 'bg-gray-100'
}

function getFileIconColor(file) {
  const ext = file.name.split('.').pop().toLowerCase()
  if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext)) return 'text-purple-600'
  if (['pdf'].includes(ext)) return 'text-red-600'
  if (['ppt', 'pptx'].includes(ext)) return 'text-orange-600'
  if (['doc', 'docx'].includes(ext)) return 'text-blue-600'
  return 'text-gray-600'
}
</script>
