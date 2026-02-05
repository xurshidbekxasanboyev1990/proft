<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Mening topshiriqlarim</h1>
        <p class="mt-1 text-sm text-gray-500">
          Sizga tayinlangan barcha topshiriqlar
        </p>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <StatsCard 
        title="Jami" 
        :value="myAssignments.length" 
        icon="folder" 
        color="gray" 
      />
      <StatsCard 
        title="Kutilmoqda" 
        :value="pendingCount" 
        icon="clock" 
        color="warning" 
      />
      <StatsCard 
        title="Bajarildi" 
        :value="completedCount" 
        icon="check" 
        color="success" 
      />
      <StatsCard 
        title="Muddati o'tgan" 
        :value="overdueCount" 
        icon="exclamation" 
        color="danger" 
      />
    </div>

    <!-- Filters -->
    <div class="flex items-center gap-4 mb-6">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        @click="activeTab = tab.value"
        class="px-4 py-2 text-sm font-medium rounded-lg transition-colors"
        :class="activeTab === tab.value 
          ? 'bg-primary-100 text-primary-700' 
          : 'text-gray-600 hover:bg-gray-100'"
      >
        {{ tab.label }}
        <span 
          v-if="tab.count > 0" 
          class="ml-1.5 px-2 py-0.5 text-xs rounded-full"
          :class="activeTab === tab.value ? 'bg-primary-200' : 'bg-gray-200'"
        >
          {{ tab.count }}
        </span>
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <SkeletonLoader v-for="i in 4" :key="i" type="card" />
    </div>

    <!-- Assignments list -->
    <div v-else-if="filteredAssignments.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <AssignmentCard
        v-for="assignment in filteredAssignments"
        :key="assignment.id"
        :assignment="assignment"
        :show-actions="true"
        :can-edit="false"
        :can-delete="false"
      />
    </div>

    <!-- Empty state -->
    <EmptyState
      v-else
      :title="emptyTitle"
      :description="emptyDescription"
      type="folder"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { StatsCard, SkeletonLoader, EmptyState } from '@/components/common'
import { AssignmentCard } from '@/components/assignments'
import { useAssignmentStore } from '@/stores'

const assignmentStore = useAssignmentStore()

const isLoading = computed(() => assignmentStore.isLoading)
const myAssignments = computed(() => assignmentStore.myAssignments)

const activeTab = ref('all')

const pendingCount = computed(() => 
  myAssignments.value.filter(a => a.status === 'pending' || a.status === 'in_progress').length
)

const completedCount = computed(() => 
  myAssignments.value.filter(a => a.status === 'completed').length
)

const overdueCount = computed(() => 
  myAssignments.value.filter(a => a.status === 'overdue').length
)

const tabs = computed(() => [
  { value: 'all', label: 'Barchasi', count: myAssignments.value.length },
  { value: 'pending', label: 'Kutilmoqda', count: pendingCount.value },
  { value: 'completed', label: 'Bajarildi', count: completedCount.value },
  { value: 'overdue', label: "Muddati o'tgan", count: overdueCount.value }
])

const filteredAssignments = computed(() => {
  if (activeTab.value === 'all') {
    return myAssignments.value
  }
  if (activeTab.value === 'pending') {
    return myAssignments.value.filter(a => a.status === 'pending' || a.status === 'in_progress')
  }
  if (activeTab.value === 'completed') {
    return myAssignments.value.filter(a => a.status === 'completed')
  }
  if (activeTab.value === 'overdue') {
    return myAssignments.value.filter(a => a.status === 'overdue')
  }
  return myAssignments.value
})

const emptyTitle = computed(() => {
  if (activeTab.value === 'pending') return "Kutilayotgan topshiriq yo'q"
  if (activeTab.value === 'completed') return "Bajarilgan topshiriq yo'q"
  if (activeTab.value === 'overdue') return "Muddati o'tgan topshiriq yo'q"
  return "Sizga topshiriq tayinlanmagan"
})

const emptyDescription = computed(() => {
  if (activeTab.value === 'pending') return "Barcha topshiriqlar bajarilgan"
  if (activeTab.value === 'completed') return "Hali biror topshiriq bajarilmagan"
  if (activeTab.value === 'overdue') return "Barcha topshiriqlar o'z vaqtida bajarilgan"
  return "Yangi topshiriqlar bu yerda ko'rinadi"
})

onMounted(() => {
  assignmentStore.fetchMyAssignments()
})
</script>
