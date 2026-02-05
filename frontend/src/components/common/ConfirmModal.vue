<template>
  <BaseModal 
    :is-open="isOpen" 
    :title="title"
    size="sm"
    @close="cancel"
  >
    <div class="text-center sm:text-left">
      <div class="flex items-center gap-4">
        <!-- Icon -->
        <div 
          class="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-full"
          :class="iconBgClass"
        >
          <component :is="iconComponent" class="w-6 h-6" :class="iconClass" />
        </div>
        
        <!-- Message -->
        <div class="flex-1">
          <p class="text-sm text-gray-600">{{ message }}</p>
        </div>
      </div>
    </div>

    <template #footer>
      <button 
        @click="cancel" 
        class="btn-secondary"
        :disabled="isLoading"
      >
        {{ cancelText }}
      </button>
      <button 
        @click="confirm" 
        :class="confirmButtonClass"
        :disabled="isLoading"
      >
        <LoadingSpinner v-if="isLoading" size="xs" color="white" />
        <span v-else>{{ confirmText }}</span>
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed } from 'vue'
import BaseModal from './BaseModal.vue'
import LoadingSpinner from './LoadingSpinner.vue'
import { 
  ExclamationTriangleIcon, 
  TrashIcon, 
  CheckCircleIcon,
  InformationCircleIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: 'Tasdiqlash'
  },
  message: {
    type: String,
    default: 'Bu amalni bajarishga ishonchingiz komilmi?'
  },
  confirmText: {
    type: String,
    default: 'Tasdiqlash'
  },
  cancelText: {
    type: String,
    default: 'Bekor qilish'
  },
  type: {
    type: String,
    default: 'warning',
    validator: (value) => ['warning', 'danger', 'success', 'info'].includes(value)
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['confirm', 'cancel'])

const iconComponent = computed(() => {
  const icons = {
    warning: ExclamationTriangleIcon,
    danger: TrashIcon,
    success: CheckCircleIcon,
    info: InformationCircleIcon
  }
  return icons[props.type]
})

const iconBgClass = computed(() => {
  const classes = {
    warning: 'bg-warning-50',
    danger: 'bg-danger-50',
    success: 'bg-success-50',
    info: 'bg-primary-50'
  }
  return classes[props.type]
})

const iconClass = computed(() => {
  const classes = {
    warning: 'text-warning-600',
    danger: 'text-danger-600',
    success: 'text-success-600',
    info: 'text-primary-600'
  }
  return classes[props.type]
})

const confirmButtonClass = computed(() => {
  const classes = {
    warning: 'btn-warning',
    danger: 'btn-danger',
    success: 'btn-success',
    info: 'btn-primary'
  }
  return classes[props.type]
})

function confirm() {
  emit('confirm')
}

function cancel() {
  emit('cancel')
}
</script>
