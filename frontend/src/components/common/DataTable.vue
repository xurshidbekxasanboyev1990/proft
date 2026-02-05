<template>
  <div class="overflow-hidden">
    <!-- Table wrapper -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <!-- Header -->
        <thead class="bg-gray-50">
          <tr>
            <!-- Checkbox column -->
            <th v-if="selectable" class="w-12 px-4 py-3">
              <input
                type="checkbox"
                :checked="isAllSelected"
                :indeterminate="isIndeterminate"
                @change="toggleSelectAll"
                class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
            </th>
            
            <!-- Data columns -->
            <th
              v-for="column in columns"
              :key="column.key"
              :class="[
                'px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
                column.sortable ? 'cursor-pointer hover:text-gray-700' : '',
                column.class
              ]"
              :style="column.width ? { width: column.width } : {}"
              @click="column.sortable && onSort(column.key)"
            >
              <div class="flex items-center gap-1">
                <span>{{ column.label }}</span>
                <template v-if="column.sortable">
                  <ChevronUpDownIcon v-if="sortKey !== column.key" class="w-4 h-4 text-gray-400" />
                  <ChevronUpIcon v-else-if="sortOrder === 'asc'" class="w-4 h-4 text-primary-600" />
                  <ChevronDownIcon v-else class="w-4 h-4 text-primary-600" />
                </template>
              </div>
            </th>
            
            <!-- Actions column -->
            <th v-if="$slots.actions" class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">
              Amallar
            </th>
          </tr>
        </thead>
        
        <!-- Body -->
        <tbody class="bg-white divide-y divide-gray-200">
          <!-- Loading state -->
          <template v-if="loading">
            <tr v-for="i in skeletonRows" :key="i">
              <td v-if="selectable" class="px-4 py-4">
                <div class="w-4 h-4 bg-gray-200 rounded animate-pulse"></div>
              </td>
              <td v-for="col in columns" :key="col.key" class="px-4 py-4">
                <div class="h-4 bg-gray-200 rounded animate-pulse" :style="{ width: `${Math.random() * 40 + 40}%` }"></div>
              </td>
              <td v-if="$slots.actions" class="px-4 py-4 text-right">
                <div class="w-8 h-8 bg-gray-200 rounded animate-pulse inline-block"></div>
              </td>
            </tr>
          </template>
          
          <!-- Empty state -->
          <tr v-else-if="data.length === 0">
            <td :colspan="totalColumns" class="px-4 py-12 text-center">
              <slot name="empty">
                <div class="flex flex-col items-center">
                  <InboxIcon class="w-12 h-12 text-gray-300 mb-3" />
                  <p class="text-gray-500">{{ emptyText }}</p>
                </div>
              </slot>
            </td>
          </tr>
          
          <!-- Data rows -->
          <tr
            v-else
            v-for="(row, rowIndex) in data"
            :key="rowKey ? row[rowKey] : rowIndex"
            :class="[
              'transition-colors',
              hoverable ? 'hover:bg-gray-50' : '',
              isSelected(row) ? 'bg-primary-50' : ''
            ]"
          >
            <!-- Checkbox -->
            <td v-if="selectable" class="px-4 py-4">
              <input
                type="checkbox"
                :checked="isSelected(row)"
                @change="toggleSelect(row)"
                class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
            </td>
            
            <!-- Data cells -->
            <td
              v-for="column in columns"
              :key="column.key"
              class="px-4 py-4 text-sm"
              :class="column.cellClass"
            >
              <slot :name="`cell-${column.key}`" :row="row" :value="getCellValue(row, column.key)">
                {{ getCellValue(row, column.key) }}
              </slot>
            </td>
            
            <!-- Actions -->
            <td v-if="$slots.actions" class="px-4 py-4 text-right">
              <slot name="actions" :row="row" :index="rowIndex"></slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Pagination -->
    <div v-if="pagination" class="px-4 py-3 border-t border-gray-200 flex items-center justify-between">
      <div class="text-sm text-gray-500">
        {{ paginationInfo }}
      </div>
      <div class="flex items-center gap-2">
        <button
          :disabled="!pagination.has_previous"
          @click="$emit('page-change', pagination.page - 1)"
          class="px-3 py-1.5 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Oldingi
        </button>
        <span class="text-sm text-gray-600">
          {{ pagination.page }} / {{ pagination.total_pages }}
        </span>
        <button
          :disabled="!pagination.has_next"
          @click="$emit('page-change', pagination.page + 1)"
          class="px-3 py-1.5 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Keyingi
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { 
  ChevronUpDownIcon, 
  ChevronUpIcon, 
  ChevronDownIcon,
  InboxIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  columns: {
    type: Array,
    required: true
    // { key: 'name', label: 'Name', sortable: true, width: '200px', class: '', cellClass: '' }
  },
  data: {
    type: Array,
    default: () => []
  },
  rowKey: {
    type: String,
    default: 'id'
  },
  loading: {
    type: Boolean,
    default: false
  },
  selectable: {
    type: Boolean,
    default: false
  },
  hoverable: {
    type: Boolean,
    default: true
  },
  pagination: {
    type: Object,
    default: null
    // { page: 1, total_pages: 10, total_count: 100, has_next: true, has_previous: false }
  },
  emptyText: {
    type: String,
    default: "Ma'lumot topilmadi"
  },
  skeletonRows: {
    type: Number,
    default: 5
  }
})

const emit = defineEmits(['page-change', 'sort', 'select', 'select-all'])

const selected = ref([])
const sortKey = ref('')
const sortOrder = ref('asc')

const totalColumns = computed(() => {
  let count = props.columns.length
  if (props.selectable) count++
  return count + 1 // +1 for actions
})

const isAllSelected = computed(() => {
  return props.data.length > 0 && selected.value.length === props.data.length
})

const isIndeterminate = computed(() => {
  return selected.value.length > 0 && selected.value.length < props.data.length
})

const paginationInfo = computed(() => {
  if (!props.pagination) return ''
  const { page, page_size, total_count } = props.pagination
  const start = (page - 1) * (page_size || 20) + 1
  const end = Math.min(page * (page_size || 20), total_count)
  return `${start}-${end} / ${total_count} ta`
})

function getCellValue(row, key) {
  return key.split('.').reduce((obj, k) => obj?.[k], row) ?? '-'
}

function isSelected(row) {
  const key = props.rowKey ? row[props.rowKey] : row
  return selected.value.includes(key)
}

function toggleSelect(row) {
  const key = props.rowKey ? row[props.rowKey] : row
  const index = selected.value.indexOf(key)
  if (index === -1) {
    selected.value.push(key)
  } else {
    selected.value.splice(index, 1)
  }
  emit('select', selected.value)
}

function toggleSelectAll() {
  if (isAllSelected.value) {
    selected.value = []
  } else {
    selected.value = props.data.map(row => props.rowKey ? row[props.rowKey] : row)
  }
  emit('select-all', selected.value)
}

function onSort(key) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
  emit('sort', { key: sortKey.value, order: sortOrder.value })
}
</script>
