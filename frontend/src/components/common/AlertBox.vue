<template>
  <div 
    v-if="visible" 
    class="rounded-lg p-4"
    :class="alertClass"
    role="alert"
  >
    <div class="flex items-start gap-3">
      <component 
        :is="iconComponent" 
        class="w-5 h-5 flex-shrink-0 mt-0.5" 
        :class="iconClass" 
      />
      
      <div class="flex-1">
        <h4 v-if="title" class="font-medium mb-1" :class="titleClass">
          {{ title }}
        </h4>
        <p class="text-sm" :class="textClass">
          <slot>{{ message }}</slot>
        </p>
      </div>
      
      <button 
        v-if="dismissible"
        @click="dismiss" 
        class="flex-shrink-0 p-1 rounded hover:bg-black/5 transition-colors"
        :class="closeClass"
      >
        <XMarkIcon class="w-4 h-4" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { 
  XMarkIcon,
  CheckCircleIcon, 
  ExclamationTriangleIcon, 
  XCircleIcon,
  InformationCircleIcon 
} from '@heroicons/vue/24/outline'

const props = defineProps({
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['info', 'success', 'warning', 'error'].includes(value)
  },
  title: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    default: ''
  },
  dismissible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['dismiss'])

const visible = ref(true)

const iconComponent = computed(() => {
  const icons = {
    info: InformationCircleIcon,
    success: CheckCircleIcon,
    warning: ExclamationTriangleIcon,
    error: XCircleIcon
  }
  return icons[props.type]
})

const alertClass = computed(() => {
  const classes = {
    info: 'bg-primary-50 border border-primary-200',
    success: 'bg-success-50 border border-green-200',
    warning: 'bg-warning-50 border border-yellow-200',
    error: 'bg-danger-50 border border-red-200'
  }
  return classes[props.type]
})

const iconClass = computed(() => {
  const classes = {
    info: 'text-primary-600',
    success: 'text-success-600',
    warning: 'text-warning-600',
    error: 'text-danger-600'
  }
  return classes[props.type]
})

const titleClass = computed(() => {
  const classes = {
    info: 'text-primary-800',
    success: 'text-green-800',
    warning: 'text-yellow-800',
    error: 'text-red-800'
  }
  return classes[props.type]
})

const textClass = computed(() => {
  const classes = {
    info: 'text-primary-700',
    success: 'text-green-700',
    warning: 'text-yellow-700',
    error: 'text-red-700'
  }
  return classes[props.type]
})

const closeClass = computed(() => {
  const classes = {
    info: 'text-primary-600',
    success: 'text-green-600',
    warning: 'text-yellow-600',
    error: 'text-red-600'
  }
  return classes[props.type]
})

function dismiss() {
  visible.value = false
  emit('dismiss')
}
</script>
