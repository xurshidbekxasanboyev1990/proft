<template>
  <div class="card hover:shadow-md transition-shadow">
    <div class="card-body">
      <!-- Header -->
      <div class="flex items-start justify-between gap-4 mb-3">
        <div class="flex-1 min-w-0">
          <RouterLink 
            :to="`/assignments/${assignment.id}`"
            class="text-lg font-semibold text-gray-900 hover:text-primary-600 line-clamp-1"
          >
            {{ assignment.title }}
          </RouterLink>
          <p class="text-sm text-gray-500 mt-0.5">
            {{ assignment.category?.name || 'Kategoriyasiz' }}
          </p>
        </div>
        <StatusBadge :variant="assignment.status" size="sm" dot>
          {{ statusLabel }}
        </StatusBadge>
      </div>

      <!-- Description -->
      <p class="text-sm text-gray-600 line-clamp-2 mb-4">
        {{ assignment.description }}
      </p>

      <!-- Meta info -->
      <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500">
        <!-- Priority -->
        <div class="flex items-center gap-1.5">
          <FlagIcon class="w-4 h-4" :class="priorityColor" />
          <span>{{ priorityLabel }}</span>
        </div>

        <!-- Deadline -->
        <div class="flex items-center gap-1.5">
          <CalendarIcon class="w-4 h-4" />
          <span :class="isOverdue ? 'text-danger-600 font-medium' : ''">
            {{ formatDate(assignment.deadline) }}
          </span>
        </div>

        <!-- Assigned to -->
        <div v-if="assignment.assigned_to" class="flex items-center gap-1.5">
          <UserIcon class="w-4 h-4" />
          <span>{{ assignment.assigned_to.full_name || assignment.assigned_to.username }}</span>
        </div>
      </div>

      <!-- Countdown -->
      <DeadlineCountdown 
        v-if="assignment.status !== 'completed' && assignment.status !== 'cancelled'"
        :deadline="assignment.deadline" 
        class="mt-4"
      />

      <!-- Actions -->
      <div v-if="showActions" class="flex items-center justify-end gap-2 mt-4 pt-4 border-t border-gray-100">
        <RouterLink :to="`/assignments/${assignment.id}`" class="btn-secondary btn-sm">
          Ko'rish
        </RouterLink>
        <button 
          v-if="canEdit" 
          @click="$emit('edit', assignment)" 
          class="btn-secondary btn-sm"
        >
          <PencilIcon class="w-4 h-4" />
        </button>
        <button 
          v-if="canDelete" 
          @click="$emit('delete', assignment)" 
          class="btn-danger btn-sm"
        >
          <TrashIcon class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { FlagIcon, CalendarIcon, UserIcon, PencilIcon, TrashIcon } from '@heroicons/vue/24/outline'
import { StatusBadge } from '@/components/common'
import DeadlineCountdown from './DeadlineCountdown.vue'
import { ASSIGNMENT_STATUSES, ASSIGNMENT_PRIORITIES } from '@/services'
import dayjs from 'dayjs'

const props = defineProps({
  assignment: {
    type: Object,
    required: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  canEdit: {
    type: Boolean,
    default: false
  },
  canDelete: {
    type: Boolean,
    default: false
  }
})

defineEmits(['edit', 'delete'])

const statusLabel = computed(() => {
  const status = ASSIGNMENT_STATUSES.find(s => s.value === props.assignment.status)
  return status?.label || props.assignment.status
})

const priorityLabel = computed(() => {
  const priority = ASSIGNMENT_PRIORITIES.find(p => p.value === props.assignment.priority)
  return priority?.label || props.assignment.priority
})

const priorityColor = computed(() => {
  const colors = {
    low: 'text-gray-400',
    medium: 'text-warning-500',
    high: 'text-danger-500'
  }
  return colors[props.assignment.priority] || 'text-gray-400'
})

const isOverdue = computed(() => {
  return dayjs(props.assignment.deadline).isBefore(dayjs())
})

function formatDate(date) {
  return dayjs(date).format('D MMM YYYY, HH:mm')
}
</script>
