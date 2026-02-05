<template>
  <div class="card">
    <div class="flex items-center justify-between p-6">
      <div class="flex items-center gap-4">
        <div 
          class="flex items-center justify-center w-12 h-12 rounded-lg"
          :class="iconBgClass"
        >
          <component :is="icon" class="w-6 h-6" :class="iconClass" />
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500">{{ title }}</p>
          <p class="text-2xl font-bold text-gray-900">{{ formattedValue }}</p>
        </div>
      </div>
      
      <div v-if="change !== null" class="flex items-center gap-1">
        <ArrowUpIcon v-if="change > 0" class="w-4 h-4 text-success-500" />
        <ArrowDownIcon v-else-if="change < 0" class="w-4 h-4 text-danger-500" />
        <span 
          class="text-sm font-medium"
          :class="change > 0 ? 'text-success-500' : change < 0 ? 'text-danger-500' : 'text-gray-500'"
        >
          {{ Math.abs(change) }}%
        </span>
      </div>
    </div>
    
    <div v-if="$slots.footer" class="px-6 py-3 bg-gray-50 border-t border-gray-200">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/vue/24/solid'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    required: true
  },
  icon: {
    type: [Object, Function],
    required: true
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'success', 'warning', 'danger', 'purple'].includes(value)
  },
  change: {
    type: Number,
    default: null
  }
})

const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    return props.value.toLocaleString('uz-UZ')
  }
  return props.value
})

const iconBgClass = computed(() => {
  const classes = {
    primary: 'bg-primary-100',
    success: 'bg-success-50',
    warning: 'bg-warning-50',
    danger: 'bg-danger-50',
    purple: 'bg-purple-100'
  }
  return classes[props.color]
})

const iconClass = computed(() => {
  const classes = {
    primary: 'text-primary-600',
    success: 'text-success-600',
    warning: 'text-warning-600',
    danger: 'text-danger-600',
    purple: 'text-purple-600'
  }
  return classes[props.color]
})
</script>
