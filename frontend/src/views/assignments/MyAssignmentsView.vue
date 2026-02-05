<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 sm:mb-8">
      <div>
        <h1 class="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-900 dark:text-white">
          Mening topshiriqlarim
        </h1>
        <p class="mt-1 sm:mt-2 text-sm text-gray-500 dark:text-slate-400">
          Sizga tayinlangan barcha topshiriqlar
        </p>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6 sm:mb-8">
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-4 sm:p-5 border border-gray-100 dark:border-slate-700 hover:shadow-lg transition-shadow">
        <div class="flex items-center gap-3">
          <div class="p-2.5 sm:p-3 rounded-xl bg-gray-100 dark:bg-slate-700">
            <FolderIcon class="w-5 h-5 sm:w-6 sm:h-6 text-gray-600 dark:text-slate-300" />
          </div>
          <div>
            <p class="text-xs sm:text-sm font-medium text-gray-500 dark:text-slate-400">Jami</p>
            <p class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white">{{ myAssignments.length }}</p>
          </div>
        </div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-4 sm:p-5 border border-gray-100 dark:border-slate-700 hover:shadow-lg transition-shadow">
        <div class="flex items-center gap-3">
          <div class="p-2.5 sm:p-3 rounded-xl bg-amber-100 dark:bg-amber-900/30">
            <ClockIcon class="w-5 h-5 sm:w-6 sm:h-6 text-amber-600 dark:text-amber-400" />
          </div>
          <div>
            <p class="text-xs sm:text-sm font-medium text-gray-500 dark:text-slate-400">Kutilmoqda</p>
            <p class="text-xl sm:text-2xl font-bold text-amber-600 dark:text-amber-400">{{ pendingCount }}</p>
          </div>
        </div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-4 sm:p-5 border border-gray-100 dark:border-slate-700 hover:shadow-lg transition-shadow">
        <div class="flex items-center gap-3">
          <div class="p-2.5 sm:p-3 rounded-xl bg-emerald-100 dark:bg-emerald-900/30">
            <CheckCircleIcon class="w-5 h-5 sm:w-6 sm:h-6 text-emerald-600 dark:text-emerald-400" />
          </div>
          <div>
            <p class="text-xs sm:text-sm font-medium text-gray-500 dark:text-slate-400">Bajarildi</p>
            <p class="text-xl sm:text-2xl font-bold text-emerald-600 dark:text-emerald-400">{{ completedCount }}</p>
          </div>
        </div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-4 sm:p-5 border border-gray-100 dark:border-slate-700 hover:shadow-lg transition-shadow">
        <div class="flex items-center gap-3">
          <div class="p-2.5 sm:p-3 rounded-xl bg-red-100 dark:bg-red-900/30">
            <ExclamationCircleIcon class="w-5 h-5 sm:w-6 sm:h-6 text-red-600 dark:text-red-400" />
          </div>
          <div>
            <p class="text-xs sm:text-sm font-medium text-gray-500 dark:text-slate-400">Muddati o'tgan</p>
            <p class="text-xl sm:text-2xl font-bold text-red-600 dark:text-red-400">{{ overdueCount }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs / Filters -->
    <div class="mb-6 overflow-x-auto scrollbar-hide -mx-4 px-4 sm:mx-0 sm:px-0">
      <div class="inline-flex items-center gap-2 p-1.5 bg-gray-100 dark:bg-slate-800 rounded-2xl min-w-max">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="activeTab = tab.value"
          class="relative px-4 sm:px-5 py-2.5 text-sm font-semibold rounded-xl transition-all duration-200"
          :class="activeTab === tab.value 
            ? 'bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-400 shadow-sm' 
            : 'text-gray-600 dark:text-slate-400 hover:text-gray-900 dark:hover:text-white'"
        >
          <span class="flex items-center gap-2">
            {{ tab.label }}
            <span 
              v-if="tab.count > 0" 
              class="px-2 py-0.5 text-xs font-bold rounded-full"
              :class="activeTab === tab.value 
                ? 'bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400' 
                : 'bg-gray-200 dark:bg-slate-600 text-gray-600 dark:text-slate-400'"
            >
              {{ tab.count }}
            </span>
          </span>
        </button>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
      <div v-for="i in 6" :key="i" class="bg-white dark:bg-slate-800 rounded-2xl p-5 animate-pulse">
        <div class="h-4 bg-gray-200 dark:bg-slate-700 rounded w-3/4 mb-4"></div>
        <div class="h-3 bg-gray-200 dark:bg-slate-700 rounded w-1/2 mb-6"></div>
        <div class="grid grid-cols-2 gap-3 mb-4">
          <div class="h-16 bg-gray-200 dark:bg-slate-700 rounded-xl"></div>
          <div class="h-16 bg-gray-200 dark:bg-slate-700 rounded-xl"></div>
        </div>
        <div class="h-12 bg-gray-200 dark:bg-slate-700 rounded-xl"></div>
      </div>
    </div>

    <!-- Assignments list -->
    <div v-else-if="filteredAssignments.length > 0" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
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
    <div 
      v-else
      class="flex flex-col items-center justify-center py-12 sm:py-16 px-4"
    >
      <div class="w-20 h-20 sm:w-24 sm:h-24 mb-6 rounded-2xl bg-gray-100 dark:bg-slate-800 flex items-center justify-center">
        <FolderIcon class="w-10 h-10 sm:w-12 sm:h-12 text-gray-400 dark:text-slate-500" />
      </div>
      <h3 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 text-center">
        {{ emptyTitle }}
      </h3>
      <p class="text-sm text-gray-500 dark:text-slate-400 text-center max-w-sm">
        {{ emptyDescription }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  FolderIcon, 
  ClockIcon, 
  CheckCircleIcon, 
  ExclamationCircleIcon 
} from '@heroicons/vue/24/outline'
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
