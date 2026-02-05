<template>
  <div class="animate-pulse">
    <!-- Card Skeleton -->
    <div v-if="type === 'card'" class="card">
      <div class="card-body space-y-4">
        <div class="h-4 bg-gray-200 rounded w-3/4"></div>
        <div class="space-y-2">
          <div class="h-3 bg-gray-200 rounded"></div>
          <div class="h-3 bg-gray-200 rounded w-5/6"></div>
        </div>
        <div class="flex gap-2 pt-2">
          <div class="h-6 bg-gray-200 rounded w-20"></div>
          <div class="h-6 bg-gray-200 rounded w-16"></div>
        </div>
      </div>
    </div>
    
    <!-- Table Row Skeleton -->
    <div v-else-if="type === 'table-row'" class="flex items-center gap-4 p-4 border-b border-gray-200">
      <div class="h-10 w-10 bg-gray-200 rounded-full"></div>
      <div class="flex-1 space-y-2">
        <div class="h-4 bg-gray-200 rounded w-1/3"></div>
        <div class="h-3 bg-gray-200 rounded w-1/2"></div>
      </div>
      <div class="h-6 bg-gray-200 rounded w-20"></div>
    </div>
    
    <!-- Text Skeleton -->
    <div v-else-if="type === 'text'" class="space-y-2">
      <div 
        v-for="i in lines" 
        :key="i" 
        class="h-3 bg-gray-200 rounded"
        :class="{ 'w-3/4': i === lines }"
      ></div>
    </div>
    
    <!-- Avatar Skeleton -->
    <div v-else-if="type === 'avatar'" class="flex items-center gap-3">
      <div class="h-10 w-10 bg-gray-200 rounded-full"></div>
      <div class="space-y-1">
        <div class="h-4 bg-gray-200 rounded w-24"></div>
        <div class="h-3 bg-gray-200 rounded w-16"></div>
      </div>
    </div>
    
    <!-- Stats Card Skeleton -->
    <div v-else-if="type === 'stats'" class="card p-6">
      <div class="flex items-center gap-4">
        <div class="h-12 w-12 bg-gray-200 rounded-lg"></div>
        <div class="space-y-2">
          <div class="h-3 bg-gray-200 rounded w-20"></div>
          <div class="h-6 bg-gray-200 rounded w-16"></div>
        </div>
      </div>
    </div>
    
    <!-- Default/Generic Skeleton -->
    <div v-else class="space-y-3">
      <div class="h-4 bg-gray-200 rounded w-full"></div>
      <div class="h-4 bg-gray-200 rounded w-5/6"></div>
      <div class="h-4 bg-gray-200 rounded w-4/6"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'card', 'table-row', 'text', 'avatar', 'stats'].includes(value)
  },
  lines: {
    type: Number,
    default: 3
  }
})
</script>
