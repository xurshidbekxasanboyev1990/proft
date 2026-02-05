<template>
  <div class="card hover:shadow-md transition-shadow">
    <div class="card-body">
      <!-- Header -->
      <div class="flex items-start justify-between mb-3">
        <StatusBadge :variant="portfolio.status" dot>
          {{ portfolio.status_display }}
        </StatusBadge>
        
        <!-- Actions dropdown -->
        <Menu as="div" class="relative">
          <MenuButton class="p-1 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors">
            <EllipsisVerticalIcon class="w-5 h-5" />
          </MenuButton>
          
          <transition
            enter-active-class="transition duration-100 ease-out"
            enter-from-class="transform scale-95 opacity-0"
            enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0"
          >
            <MenuItems class="absolute right-0 mt-1 w-48 origin-top-right bg-white rounded-lg shadow-lg ring-1 ring-black/5 focus:outline-none py-1 z-10">
              <MenuItem v-slot="{ active }">
                <RouterLink 
                  :to="`/portfolios/${portfolio.id}`"
                  :class="[active ? 'bg-gray-50' : '', 'flex items-center gap-2 px-4 py-2 text-sm text-gray-700']"
                >
                  <EyeIcon class="w-4 h-4" />
                  Ko'rish
                </RouterLink>
              </MenuItem>
              <MenuItem v-slot="{ active }">
                <RouterLink 
                  :to="`/portfolios/${portfolio.id}/edit`"
                  :class="[active ? 'bg-gray-50' : '', 'flex items-center gap-2 px-4 py-2 text-sm text-gray-700']"
                >
                  <PencilIcon class="w-4 h-4" />
                  Tahrirlash
                </RouterLink>
              </MenuItem>
              <MenuItem v-slot="{ active }">
                <button 
                  @click="$emit('delete', portfolio)"
                  :class="[active ? 'bg-gray-50' : '', 'flex items-center gap-2 w-full px-4 py-2 text-sm text-danger-600']"
                >
                  <TrashIcon class="w-4 h-4" />
                  O'chirish
                </button>
              </MenuItem>
            </MenuItems>
          </transition>
        </Menu>
      </div>
      
      <!-- Title -->
      <RouterLink :to="`/portfolios/${portfolio.id}`" class="block group">
        <h3 class="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors mb-2 line-clamp-1">
          {{ portfolio.title }}
        </h3>
      </RouterLink>
      
      <!-- Description -->
      <p class="text-sm text-gray-500 line-clamp-2 mb-4">
        {{ portfolio.description }}
      </p>
      
      <!-- Meta info -->
      <div class="flex items-center gap-4 text-xs text-gray-400">
        <span class="flex items-center gap-1">
          <FolderIcon class="w-4 h-4" />
          {{ portfolio.category_display }}
        </span>
        <span class="flex items-center gap-1">
          <CalendarIcon class="w-4 h-4" />
          {{ formatDate(portfolio.created_at) }}
        </span>
      </div>
      
      <!-- Review info -->
      <div v-if="portfolio.reviewed_by" class="mt-4 pt-4 border-t border-gray-100">
        <div class="flex items-center gap-2 text-xs text-gray-500">
          <div class="w-6 h-6 bg-gray-100 rounded-full flex items-center justify-center">
            <UserIcon class="w-3 h-3 text-gray-400" />
          </div>
          <span>{{ portfolio.reviewed_by.username }}</span>
          <span>•</span>
          <span>{{ formatDate(portfolio.reviewed_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import { 
  EllipsisVerticalIcon, 
  EyeIcon, 
  PencilIcon, 
  TrashIcon,
  FolderIcon,
  CalendarIcon,
  UserIcon
} from '@heroicons/vue/24/outline'
import { StatusBadge } from '@/components/common'
import dayjs from 'dayjs'

defineProps({
  portfolio: {
    type: Object,
    required: true
  }
})

defineEmits(['delete'])

function formatDate(date) {
  return dayjs(date).format('D MMM, YYYY')
}
</script>
