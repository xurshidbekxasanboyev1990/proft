<template>
  <TransitionGroup
    name="toast"
    tag="div"
    class="fixed bottom-4 right-4 z-50 flex flex-col gap-2"
  >
    <div
      v-for="toast in toasts"
      :key="toast.id"
      :class="[
        'flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg min-w-[280px] max-w-md',
        typeClasses[toast.type]
      ]"
      role="alert"
    >
      <component :is="icons[toast.type]" class="w-5 h-5 flex-shrink-0" />
      <p class="flex-1 text-sm font-medium">{{ toast.message }}</p>
      <button
        @click="$emit('remove', toast.id)"
        class="p-1 rounded hover:bg-black/10 focus:outline-none"
      >
        <XMarkIcon class="w-4 h-4" />
      </button>
    </div>
  </TransitionGroup>
</template>

<script setup>
import { 
  CheckCircleIcon, 
  ExclamationCircleIcon, 
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

defineProps({
  toasts: {
    type: Array,
    default: () => []
  }
})

defineEmits(['remove'])

const typeClasses = {
  success: 'bg-success-500 text-white',
  error: 'bg-danger-500 text-white',
  warning: 'bg-warning-500 text-white',
  info: 'bg-primary-500 text-white'
}

const icons = {
  success: CheckCircleIcon,
  error: ExclamationCircleIcon,
  warning: ExclamationTriangleIcon,
  info: InformationCircleIcon
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
