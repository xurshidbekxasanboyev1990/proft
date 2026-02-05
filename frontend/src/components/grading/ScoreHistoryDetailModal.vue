<template>
  <BaseModal :is-open="isOpen" :title="modalTitle" size="lg" @close="$emit('close')">
    <div v-if="item" class="space-y-6">
      <!-- Header info -->
      <div class="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
        <div 
          class="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
          :class="getChangeTypeIconClass(item.change_type)"
        >
          <component :is="getChangeTypeIcon(item.change_type)" class="w-6 h-6" />
        </div>
        <div class="flex-1">
          <h3 class="font-semibold text-gray-900">{{ getChangeTypeLabel(item.change_type) }}</h3>
          <p class="text-sm text-gray-500">{{ formatDateTime(item.created_at) }}</p>
        </div>
        <span 
          class="px-3 py-1 text-sm font-medium rounded-full"
          :class="getChangeTypeClass(item.change_type)"
        >
          {{ getChangeTypeLabel(item.change_type) }}
        </span>
      </div>

      <!-- Assignment info -->
      <div>
        <h4 class="text-sm font-medium text-gray-500 mb-2">Topshiriq</h4>
        <div class="p-4 border border-gray-200 rounded-lg">
          <div class="flex items-start justify-between">
            <div>
              <p class="font-medium text-gray-900">{{ item.assignment?.title || 'Noma\'lum topshiriq' }}</p>
              <p class="text-sm text-gray-500 mt-1">{{ item.assignment?.category?.name || '-' }}</p>
            </div>
            <RouterLink 
              v-if="item.assignment?.id"
              :to="`${basePath}/${item.assignment.id}`"
              class="text-primary-600 hover:text-primary-700 text-sm font-medium"
            >
              Ko'rish →
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Teacher info -->
      <div>
        <h4 class="text-sm font-medium text-gray-500 mb-2">O'qituvchi</h4>
        <div class="flex items-center gap-3 p-4 border border-gray-200 rounded-lg">
          <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
            <span class="text-sm font-medium text-primary-600">
              {{ getInitials(item.teacher?.full_name) }}
            </span>
          </div>
          <div>
            <p class="font-medium text-gray-900">{{ item.teacher?.full_name || 'Noma\'lum' }}</p>
            <p class="text-sm text-gray-500">{{ item.teacher?.department || '-' }}</p>
          </div>
        </div>
      </div>

      <!-- Value change -->
      <div>
        <h4 class="text-sm font-medium text-gray-500 mb-2">Ball o'zgarishi</h4>
        <div class="p-4 border border-gray-200 rounded-lg">
          <div class="flex items-center justify-center gap-6">
            <!-- Old value -->
            <div class="text-center">
              <p class="text-xs text-gray-400 mb-1">Eski qiymat</p>
              <p class="text-3xl font-bold text-gray-400">{{ item.old_value ?? '-' }}</p>
            </div>

            <!-- Arrow -->
            <div class="flex items-center">
              <ArrowRightIcon class="w-8 h-8 text-gray-300" />
            </div>

            <!-- New value -->
            <div class="text-center">
              <p class="text-xs text-gray-400 mb-1">Yangi qiymat</p>
              <p class="text-3xl font-bold" :class="getValueChangeClass(item)">
                {{ item.new_value ?? '-' }}
              </p>
            </div>

            <!-- Change indicator -->
            <div v-if="item.old_value !== null && item.new_value !== null" class="ml-4">
              <div 
                class="flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium"
                :class="getDifferenceClass(item)"
              >
                <component :is="getDifferenceIcon(item)" class="w-4 h-4" />
                {{ getDifferenceText(item) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Changed by -->
      <div>
        <h4 class="text-sm font-medium text-gray-500 mb-2">Kim tomonidan</h4>
        <div class="flex items-center gap-3 p-4 border border-gray-200 rounded-lg">
          <div class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
            <UserIcon class="w-5 h-5 text-gray-500" />
          </div>
          <div>
            <p class="font-medium text-gray-900">{{ item.changed_by?.full_name || 'Sistema' }}</p>
            <p class="text-sm text-gray-500">{{ item.changed_by?.role || 'Avtomatik' }}</p>
          </div>
        </div>
      </div>

      <!-- Note -->
      <div v-if="item.note">
        <h4 class="text-sm font-medium text-gray-500 mb-2">Izoh</h4>
        <div class="p-4 bg-warning-50 border border-warning-200 rounded-lg">
          <p class="text-sm text-warning-800">{{ item.note }}</p>
        </div>
      </div>

      <!-- Timeline if multiple changes -->
      <div v-if="relatedHistory && relatedHistory.length > 1">
        <h4 class="text-sm font-medium text-gray-500 mb-2">Tarix</h4>
        <div class="border border-gray-200 rounded-lg overflow-hidden">
          <div 
            v-for="(h, index) in relatedHistory" 
            :key="h.id"
            :class="[
              'flex items-center justify-between p-3',
              h.id === item.id ? 'bg-primary-50' : 'hover:bg-gray-50',
              index !== relatedHistory.length - 1 ? 'border-b border-gray-200' : ''
            ]"
          >
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full" :class="h.id === item.id ? 'bg-primary-500' : 'bg-gray-300'"></div>
              <span class="text-sm" :class="h.id === item.id ? 'font-medium text-primary-900' : 'text-gray-600'">
                {{ getChangeTypeLabel(h.change_type) }}
              </span>
            </div>
            <div class="flex items-center gap-4">
              <span class="text-sm text-gray-500">
                {{ h.old_value ?? '-' }} → {{ h.new_value ?? '-' }}
              </span>
              <span class="text-xs text-gray-400">{{ formatDate(h.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <button @click="$emit('close')" class="btn-primary">
        Yopish
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { 
  ArrowRightIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  MinusIcon,
  UserIcon,
  AcademicCapIcon,
  ArrowPathIcon,
  SparklesIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'
import { BaseModal } from '@/components/common'
import dayjs from 'dayjs'

const route = useRoute()

// Dynamic base path based on current route
const basePath = computed(() => {
  const path = route.path
  if (path.startsWith('/teacher')) return '/teacher/tasks'
  if (path.startsWith('/admin-panel')) return '/admin-panel/tasks'
  if (path.startsWith('/super-admin')) return '/super-admin/tasks'
  return '/admin-panel/tasks'
})

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  item: {
    type: Object,
    default: null
  },
  relatedHistory: {
    type: Array,
    default: () => []
  }
})

defineEmits(['close'])

const modalTitle = computed(() => {
  if (!props.item) return 'Ball tarixi'
  return `Ball o'zgarishi #${props.item.id}`
})

function formatDate(date) {
  return dayjs(date).format('D MMM YYYY')
}

function formatDateTime(date) {
  return dayjs(date).format('D MMMM YYYY, HH:mm')
}

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

function getChangeTypeLabel(type) {
  const labels = {
    grade: 'Baholash',
    score_update: 'Ball yangilash',
    multiplier: 'Ko\'paytiruvchi',
    reset: 'Qayta o\'rnatish',
    bonus: 'Bonus'
  }
  return labels[type] || type
}

function getChangeTypeClass(type) {
  const classes = {
    grade: 'bg-success-100 text-success-700',
    score_update: 'bg-primary-100 text-primary-700',
    multiplier: 'bg-warning-100 text-warning-700',
    reset: 'bg-gray-100 text-gray-700',
    bonus: 'bg-purple-100 text-purple-700'
  }
  return classes[type] || 'bg-gray-100 text-gray-700'
}

function getChangeTypeIcon(type) {
  const icons = {
    grade: AcademicCapIcon,
    score_update: ArrowPathIcon,
    multiplier: SparklesIcon,
    reset: ArrowPathIcon,
    bonus: SparklesIcon
  }
  return icons[type] || ClockIcon
}

function getChangeTypeIconClass(type) {
  const classes = {
    grade: 'bg-success-100 text-success-600',
    score_update: 'bg-primary-100 text-primary-600',
    multiplier: 'bg-warning-100 text-warning-600',
    reset: 'bg-gray-100 text-gray-600',
    bonus: 'bg-purple-100 text-purple-600'
  }
  return classes[type] || 'bg-gray-100 text-gray-600'
}

function getValueChangeClass(item) {
  if (item.new_value > item.old_value) return 'text-success-600'
  if (item.new_value < item.old_value) return 'text-danger-600'
  return 'text-gray-900'
}

function getDifferenceClass(item) {
  const diff = item.new_value - item.old_value
  if (diff > 0) return 'bg-success-100 text-success-700'
  if (diff < 0) return 'bg-danger-100 text-danger-700'
  return 'bg-gray-100 text-gray-700'
}

function getDifferenceIcon(item) {
  const diff = item.new_value - item.old_value
  if (diff > 0) return ArrowUpIcon
  if (diff < 0) return ArrowDownIcon
  return MinusIcon
}

function getDifferenceText(item) {
  const diff = item.new_value - item.old_value
  if (diff > 0) return `+${diff}`
  if (diff < 0) return `${diff}`
  return '0'
}
</script>
