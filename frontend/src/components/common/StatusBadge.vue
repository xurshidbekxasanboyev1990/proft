<template>
  <span :class="badgeClass">
    <span v-if="dot" class="w-1.5 h-1.5 rounded-full mr-1.5" :class="dotClass"></span>
    <slot>{{ label }}</slot>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => [
      'default', 'primary', 'success', 'warning', 'danger',
      'pending', 'approved', 'rejected',
      'superadmin', 'admin', 'teacher'
    ].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  dot: {
    type: Boolean,
    default: false
  }
})

const badgeClass = computed(() => {
  const base = 'inline-flex items-center font-medium rounded-full'
  
  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-0.5 text-xs',
    lg: 'px-3 py-1 text-sm'
  }
  
  const variants = {
    default: 'bg-gray-100 text-gray-700',
    primary: 'bg-primary-100 text-primary-700',
    success: 'bg-success-50 text-success-600',
    warning: 'bg-warning-50 text-warning-600',
    danger: 'bg-danger-50 text-danger-600',
    // Status badges
    pending: 'bg-warning-50 text-warning-600',
    approved: 'bg-success-50 text-success-600',
    rejected: 'bg-danger-50 text-danger-600',
    // Role badges
    superadmin: 'bg-purple-100 text-purple-700',
    admin: 'bg-blue-100 text-blue-700',
    teacher: 'bg-green-100 text-green-700'
  }
  
  return `${base} ${sizes[props.size]} ${variants[props.variant]}`
})

const dotClass = computed(() => {
  const variants = {
    default: 'bg-gray-500',
    primary: 'bg-primary-500',
    success: 'bg-success-500',
    warning: 'bg-warning-500',
    danger: 'bg-danger-500',
    pending: 'bg-warning-500',
    approved: 'bg-success-500',
    rejected: 'bg-danger-500',
    superadmin: 'bg-purple-500',
    admin: 'bg-blue-500',
    teacher: 'bg-green-500'
  }
  return variants[props.variant]
})
</script>
