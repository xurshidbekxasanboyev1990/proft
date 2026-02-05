<template>
  <div 
    class="group relative bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 
           hover:shadow-xl hover:shadow-gray-200/50 dark:hover:shadow-slate-900/50 
           hover:border-gray-200 dark:hover:border-slate-600
           transition-all duration-300 overflow-hidden"
  >
    <!-- Priority indicator bar -->
    <div 
      class="absolute top-0 left-0 right-0 h-1.5"
      :class="priorityBarColor"
    ></div>

    <div class="p-4 sm:p-5 pt-5 sm:pt-6">
      <!-- Header -->
      <div class="flex items-start justify-between gap-3 mb-3">
        <div class="flex-1 min-w-0">
          <RouterLink 
            :to="detailPath"
            class="block text-base sm:text-lg font-bold text-gray-900 dark:text-white 
                   hover:text-indigo-600 dark:hover:text-indigo-400 
                   line-clamp-2 transition-colors"
          >
            {{ assignment.title }}
          </RouterLink>
        </div>
        <span 
          class="inline-flex items-center px-2 sm:px-2.5 py-1 rounded-lg text-xs font-semibold shrink-0"
          :class="statusClass"
        >
          <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="statusDotClass"></span>
          {{ statusLabel }}
        </span>
      </div>

      <!-- Category badge -->
      <div class="mb-3">
        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium 
                     bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-slate-300">
          <FolderIcon class="w-3.5 h-3.5 mr-1.5" />
          {{ assignment.category?.name || 'Kategoriyasiz' }}
        </span>
      </div>

      <!-- Description -->
      <p class="text-sm text-gray-600 dark:text-slate-400 line-clamp-2 mb-4 leading-relaxed">
        {{ assignment.description || 'Tavsif mavjud emas' }}
      </p>

      <!-- Meta Grid -->
      <div class="grid grid-cols-2 gap-2 sm:gap-3 mb-4">
        <!-- Priority -->
        <div class="flex items-center gap-2 p-2 sm:p-2.5 rounded-xl bg-gray-50 dark:bg-slate-700/50">
          <div class="p-1 sm:p-1.5 rounded-lg" :class="priorityBgColor">
            <FlagIcon class="w-3.5 sm:w-4 h-3.5 sm:h-4" :class="priorityIconColor" />
          </div>
          <div class="min-w-0">
            <p class="text-[9px] sm:text-[10px] font-medium text-gray-400 dark:text-slate-500 uppercase tracking-wider">Prioritet</p>
            <p class="text-xs sm:text-sm font-semibold truncate" :class="priorityTextColor">{{ priorityLabel }}</p>
          </div>
        </div>

        <!-- Deadline -->
        <div class="flex items-center gap-2 p-2 sm:p-2.5 rounded-xl" :class="deadlineBgColor">
          <div class="p-1 sm:p-1.5 rounded-lg" :class="deadlineIconBg">
            <CalendarIcon class="w-3.5 sm:w-4 h-3.5 sm:h-4" :class="deadlineIconColor" />
          </div>
          <div class="min-w-0">
            <p class="text-[9px] sm:text-[10px] font-medium text-gray-400 dark:text-slate-500 uppercase tracking-wider">Muddat</p>
            <p class="text-xs sm:text-sm font-semibold truncate" :class="deadlineTextColor">{{ formatDeadline }}</p>
          </div>
        </div>
      </div>

      <!-- Assigned to -->
      <div v-if="assignment.assigned_to" class="flex items-center gap-2 mb-4 p-2 sm:p-2.5 rounded-xl bg-indigo-50 dark:bg-indigo-900/20">
        <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center shrink-0">
          <span class="text-white text-xs font-bold">
            {{ (assignment.assigned_to.full_name || assignment.assigned_to.username || '?').charAt(0).toUpperCase() }}
          </span>
        </div>
        <div class="min-w-0">
          <p class="text-[9px] sm:text-[10px] font-medium text-indigo-400 dark:text-indigo-500 uppercase tracking-wider">Tayinlangan</p>
          <p class="text-xs sm:text-sm font-semibold text-indigo-700 dark:text-indigo-300 truncate">
            {{ assignment.assigned_to.full_name || assignment.assigned_to.username }}
          </p>
        </div>
      </div>

      <!-- Countdown -->
      <div 
        v-if="assignment.status !== 'completed' && assignment.status !== 'cancelled'"
        class="mb-4 p-2.5 sm:p-3 rounded-xl"
        :class="countdownBgColor"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <ClockIcon class="w-4 sm:w-5 h-4 sm:h-5" :class="countdownIconColor" />
            <span class="text-xs sm:text-sm font-medium" :class="countdownTextColor">
              {{ isOverdue ? 'Muddati o\'tgan' : 'Qolgan vaqt' }}
            </span>
          </div>
          <span class="text-xs sm:text-sm font-bold" :class="countdownValueColor">
            {{ timeRemaining }}
          </span>
        </div>
        <!-- Progress bar -->
        <div class="mt-2 h-1 sm:h-1.5 bg-gray-200 dark:bg-slate-600 rounded-full overflow-hidden">
          <div 
            class="h-full rounded-full transition-all duration-300"
            :class="progressBarColor"
            :style="{ width: `${progressPercent}%` }"
          ></div>
        </div>
      </div>

      <!-- Max score badge -->
      <div v-if="assignment.max_score" class="mb-4">
        <div class="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400">
          <SparklesIcon class="w-4 h-4" />
          <span class="text-xs sm:text-sm font-semibold">Maks. {{ assignment.max_score }} ball</span>
        </div>
      </div>

      <!-- Actions -->
      <div v-if="showActions" class="flex items-center gap-2 pt-3 sm:pt-4 border-t border-gray-100 dark:border-slate-700">
        <RouterLink 
          :to="detailPath" 
          class="flex-1 inline-flex items-center justify-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-2 sm:py-2.5 
                 bg-indigo-600 hover:bg-indigo-700 text-white 
                 rounded-xl font-semibold text-xs sm:text-sm 
                 transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
        >
          <EyeIcon class="w-4 h-4" />
          Batafsil
        </RouterLink>
        <button 
          v-if="canEdit" 
          @click="$emit('edit', assignment)" 
          class="p-2 sm:p-2.5 rounded-xl bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-slate-300
                 hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors"
          title="Tahrirlash"
        >
          <PencilIcon class="w-4 sm:w-5 h-4 sm:h-5" />
        </button>
        <button 
          v-if="canDelete" 
          @click="$emit('delete', assignment)" 
          class="p-2 sm:p-2.5 rounded-xl bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400
                 hover:bg-red-100 dark:hover:bg-red-900/40 transition-colors"
          title="O'chirish"
        >
          <TrashIcon class="w-4 sm:w-5 h-4 sm:h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { 
  FlagIcon, 
  CalendarIcon, 
  ClockIcon, 
  EyeIcon, 
  PencilIcon, 
  TrashIcon,
  FolderIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'
import { ASSIGNMENT_STATUSES, ASSIGNMENT_PRIORITIES } from '@/services'
import { useUserStore } from '@/stores'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/uz'

dayjs.extend(relativeTime)
dayjs.locale('uz')

const route = useRoute()
const userStore = useUserStore()

// Determine base path based on current route or user role
const basePath = computed(() => {
  const path = route.path
  if (path.startsWith('/teacher')) return '/teacher/tasks'
  if (path.startsWith('/admin-panel')) return '/admin-panel/tasks'
  if (path.startsWith('/super-admin')) return '/super-admin/tasks'
  // Fallback based on role
  if (userStore.isTeacher) return '/teacher/tasks'
  if (userStore.isAdmin) return '/admin-panel/tasks'
  if (userStore.isSuperAdmin) return '/super-admin/tasks'
  return '/teacher/tasks'
})

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

// Detail path for assignment
const detailPath = computed(() => `${basePath.value}/${props.assignment.id}`)

// Status
const statusLabel = computed(() => {
  const status = ASSIGNMENT_STATUSES.find(s => s.value === props.assignment.status)
  return status?.label || props.assignment.status
})

const isOverdue = computed(() => {
  if (!props.assignment.deadline) return false
  return dayjs().isAfter(dayjs(props.assignment.deadline)) && props.assignment.status !== 'completed'
})

const statusClass = computed(() => {
  const status = props.assignment.status
  const classes = {
    'pending': 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400',
    'in_progress': 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400',
    'completed': 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400',
    'overdue': 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400',
    'cancelled': 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
  }
  return classes[status] || classes['pending']
})

const statusDotClass = computed(() => {
  const status = props.assignment.status
  const classes = {
    'pending': 'bg-amber-500',
    'in_progress': 'bg-blue-500',
    'completed': 'bg-emerald-500',
    'overdue': 'bg-red-500',
    'cancelled': 'bg-gray-500'
  }
  return classes[status] || classes['pending']
})

// Priority
const priorityLabel = computed(() => {
  const priority = ASSIGNMENT_PRIORITIES.find(p => p.value === props.assignment.priority)
  return priority?.label || props.assignment.priority || 'O\'rta'
})

const priorityBarColor = computed(() => {
  const priority = props.assignment.priority
  const colors = {
    'high': 'bg-gradient-to-r from-red-500 to-rose-500',
    'medium': 'bg-gradient-to-r from-amber-400 to-orange-400',
    'low': 'bg-gradient-to-r from-emerald-400 to-green-400'
  }
  return colors[priority] || colors['medium']
})

const priorityBgColor = computed(() => {
  const priority = props.assignment.priority
  const colors = {
    'high': 'bg-red-100 dark:bg-red-900/30',
    'medium': 'bg-amber-100 dark:bg-amber-900/30',
    'low': 'bg-emerald-100 dark:bg-emerald-900/30'
  }
  return colors[priority] || colors['medium']
})

const priorityIconColor = computed(() => {
  const priority = props.assignment.priority
  const colors = {
    'high': 'text-red-600 dark:text-red-400',
    'medium': 'text-amber-600 dark:text-amber-400',
    'low': 'text-emerald-600 dark:text-emerald-400'
  }
  return colors[priority] || colors['medium']
})

const priorityTextColor = computed(() => priorityIconColor.value)

// Deadline
const formatDeadline = computed(() => {
  if (!props.assignment.deadline) return 'Belgilanmagan'
  return dayjs(props.assignment.deadline).format('DD MMM, HH:mm')
})

const deadlineBgColor = computed(() => {
  if (isOverdue.value) return 'bg-red-50 dark:bg-red-900/20'
  return 'bg-gray-50 dark:bg-slate-700/50'
})

const deadlineIconBg = computed(() => {
  if (isOverdue.value) return 'bg-red-100 dark:bg-red-900/30'
  return 'bg-gray-200 dark:bg-slate-600'
})

const deadlineIconColor = computed(() => {
  if (isOverdue.value) return 'text-red-600 dark:text-red-400'
  return 'text-gray-600 dark:text-slate-400'
})

const deadlineTextColor = computed(() => {
  if (isOverdue.value) return 'text-red-600 dark:text-red-400'
  return 'text-gray-900 dark:text-white'
})

// Countdown
const timeRemaining = computed(() => {
  if (!props.assignment.deadline) return '-'
  const deadline = dayjs(props.assignment.deadline)
  const now = dayjs()
  
  if (now.isAfter(deadline)) {
    return deadline.fromNow()
  }
  
  const diff = deadline.diff(now, 'hour')
  if (diff < 24) {
    const hours = deadline.diff(now, 'hour')
    const mins = deadline.diff(now, 'minute') % 60
    return `${hours}s ${mins}d`
  } else {
    const days = deadline.diff(now, 'day')
    const hours = deadline.diff(now, 'hour') % 24
    return `${days}k ${hours}s`
  }
})

const progressPercent = computed(() => {
  if (!props.assignment.deadline || !props.assignment.created_at) return 50
  const start = dayjs(props.assignment.created_at)
  const end = dayjs(props.assignment.deadline)
  const now = dayjs()
  
  const total = end.diff(start)
  const elapsed = now.diff(start)
  
  return Math.min(100, Math.max(0, (elapsed / total) * 100))
})

const countdownBgColor = computed(() => {
  if (isOverdue.value) return 'bg-red-50 dark:bg-red-900/20'
  if (progressPercent.value > 80) return 'bg-amber-50 dark:bg-amber-900/20'
  return 'bg-emerald-50 dark:bg-emerald-900/20'
})

const countdownIconColor = computed(() => {
  if (isOverdue.value) return 'text-red-500'
  if (progressPercent.value > 80) return 'text-amber-500'
  return 'text-emerald-500'
})

const countdownTextColor = computed(() => countdownIconColor.value)
const countdownValueColor = computed(() => countdownIconColor.value)

const progressBarColor = computed(() => {
  if (isOverdue.value) return 'bg-red-500'
  if (progressPercent.value > 80) return 'bg-amber-500'
  return 'bg-emerald-500'
})
</script>
