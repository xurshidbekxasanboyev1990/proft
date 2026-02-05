<template>
  <!-- Mobile sidebar backdrop -->
  <TransitionRoot :show="isOpen" as="template">
    <div class="lg:hidden">
      <TransitionChild
        as="template"
        enter="transition-opacity ease-linear duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="transition-opacity ease-linear duration-300"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-gray-900/80 z-40" @click="$emit('close')"></div>
      </TransitionChild>
      
      <TransitionChild
        as="template"
        enter="transition ease-in-out duration-300 transform"
        enter-from="-translate-x-full"
        enter-to="translate-x-0"
        leave="transition ease-in-out duration-300 transform"
        leave-from="translate-x-0"
        leave-to="-translate-x-full"
      >
        <div class="fixed inset-y-0 left-0 z-50 w-72 bg-white shadow-xl">
          <SidebarContent @close="$emit('close')" />
        </div>
      </TransitionChild>
    </div>
  </TransitionRoot>
  
  <!-- Desktop sidebar -->
  <div class="hidden lg:fixed lg:inset-y-0 lg:z-40 lg:flex lg:w-72 lg:flex-col">
    <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-white border-r border-gray-200 px-6 pb-4">
      <SidebarContent />
    </div>
  </div>
</template>

<script setup>
import { TransitionRoot, TransitionChild } from '@headlessui/vue'
import SidebarContent from './SidebarContent.vue'

defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close'])
</script>
