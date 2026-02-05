<template>
  <div class="flex flex-col items-center justify-center py-12 text-center">
    <div 
      class="flex items-center justify-center w-16 h-16 rounded-full mb-4"
      :class="iconBgClass"
    >
      <component :is="icon" class="w-8 h-8" :class="iconColorClass" />
    </div>
    
    <h3 class="text-lg font-medium text-gray-900 mb-2">{{ title }}</h3>
    <p class="text-sm text-gray-500 max-w-md mb-6">{{ description }}</p>
    
    <slot name="action">
      <button v-if="actionText" @click="$emit('action')" class="btn-primary">
        {{ actionText }}
      </button>
    </slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { 
  FolderOpenIcon, 
  DocumentIcon,
  UsersIcon,
  MagnifyingGlassIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  title: {
    type: String,
    default: "Ma'lumot topilmadi"
  },
  description: {
    type: String,
    default: "Hozircha hech qanday ma'lumot yo'q"
  },
  actionText: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'folder', 'document', 'users', 'search'].includes(value)
  },
  color: {
    type: String,
    default: 'gray'
  }
})

defineEmits(['action'])

const icon = computed(() => {
  const icons = {
    default: FolderOpenIcon,
    folder: FolderOpenIcon,
    document: DocumentIcon,
    users: UsersIcon,
    search: MagnifyingGlassIcon
  }
  return icons[props.type]
})

const iconBgClass = computed(() => {
  return `bg-${props.color}-100`
})

const iconColorClass = computed(() => {
  return `text-${props.color}-400`
})
</script>
