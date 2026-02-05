<template>
  <div class="relative">
    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
      <MagnifyingGlassIcon class="w-5 h-5 text-gray-400" />
    </div>
    <input
      :value="modelValue"
      type="text"
      :placeholder="placeholder"
      class="block w-full pl-10 pr-10 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
      @input="onInput"
      @keydown.enter="onEnter"
    />
    <!-- Clear button -->
    <button
      v-if="modelValue"
      type="button"
      @click="clear"
      class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
    >
      <XMarkIcon class="w-5 h-5" />
    </button>
    <!-- Loading spinner -->
    <div v-if="loading" class="absolute inset-y-0 right-0 pr-3 flex items-center">
      <svg class="animate-spin w-5 h-5 text-primary-500" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { MagnifyingGlassIcon, XMarkIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Qidirish...'
  },
  debounce: {
    type: Number,
    default: 300
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'search', 'clear'])

let debounceTimeout = null

function onInput(event) {
  const value = event.target.value
  emit('update:modelValue', value)
  
  // Debounced search
  clearTimeout(debounceTimeout)
  debounceTimeout = setTimeout(() => {
    emit('search', value)
  }, props.debounce)
}

function onEnter() {
  clearTimeout(debounceTimeout)
  emit('search', props.modelValue)
}

function clear() {
  emit('update:modelValue', '')
  emit('clear')
  emit('search', '')
}
</script>
