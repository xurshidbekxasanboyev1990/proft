<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">O'qituvchilar</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Barcha o'qituvchilar ro'yxati va ularning statistikasi
        </p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1 relative">
          <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="O'qituvchi qidirish..."
            class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <select
          v-model="selectedDepartment"
          class="px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">Barcha kafedralar</option>
          <option v-for="dept in departments" :key="dept.id" :value="dept.id">
            {{ dept.name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <span class="ml-3 text-gray-600 dark:text-gray-400">Yuklanmoqda...</span>
    </div>

    <!-- Teachers Grid -->
    <div v-else-if="filteredTeachers.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="teacher in filteredTeachers"
        :key="teacher.id"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow"
      >
        <div class="flex items-start gap-4">
          <div class="w-14 h-14 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-bold text-lg">
            {{ getInitials(teacher.full_name) }}
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-semibold text-gray-900 dark:text-white truncate">
              {{ teacher.full_name }}
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
              {{ teacher.department || 'Kafedra ko\'rsatilmagan' }}
            </p>
          </div>
        </div>

        <!-- Stats -->
        <div class="mt-4 grid grid-cols-3 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <div class="text-center">
            <p class="text-lg font-bold text-gray-900 dark:text-white">{{ teacher.portfolio_count || 0 }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Portfolio</p>
          </div>
          <div class="text-center">
            <p class="text-lg font-bold text-gray-900 dark:text-white">{{ teacher.submission_count || 0 }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Javoblar</p>
          </div>
          <div class="text-center">
            <p class="text-lg font-bold text-blue-600 dark:text-blue-400">{{ teacher.total_score || 0 }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Ball</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-4 flex gap-2">
          <button
            @click="viewTeacherDetails(teacher)"
            class="flex-1 px-3 py-2 text-sm font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 dark:text-blue-300 dark:bg-blue-900/30 dark:hover:bg-blue-900/50 rounded-lg transition-colors"
          >
            Batafsil
          </button>
          <button
            @click="viewTeacherPortfolios(teacher)"
            class="flex-1 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 dark:text-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors"
          >
            Portfoliolari
          </button>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-12 text-center">
      <UsersIcon class="w-16 h-16 mx-auto text-gray-300 dark:text-gray-600" />
      <h3 class="mt-4 text-lg font-medium text-gray-900 dark:text-white">O'qituvchilar topilmadi</h3>
      <p class="mt-2 text-gray-500 dark:text-gray-400">Qidiruv so'zini o'zgartirib ko'ring</p>
    </div>

    <!-- Teacher Detail Modal -->
    <TransitionRoot appear :show="isDetailModalOpen" as="template">
      <Dialog as="div" @close="isDetailModalOpen = false" class="relative z-50">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/50" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4">
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-lg bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
                <div class="p-6">
                  <div class="flex items-start gap-4">
                    <div class="w-16 h-16 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-bold text-xl">
                      {{ getInitials(selectedTeacher?.full_name) }}
                    </div>
                    <div class="flex-1">
                      <DialogTitle class="text-xl font-bold text-gray-900 dark:text-white">
                        {{ selectedTeacher?.full_name }}
                      </DialogTitle>
                      <p class="text-gray-500 dark:text-gray-400">{{ selectedTeacher?.email }}</p>
                    </div>
                    <button @click="isDetailModalOpen = false" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
                      <XMarkIcon class="w-5 h-5 text-gray-500" />
                    </button>
                  </div>

                  <div class="mt-6 space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                      <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl">
                        <p class="text-sm text-gray-500 dark:text-gray-400">Kafedra</p>
                        <p class="font-semibold text-gray-900 dark:text-white">{{ selectedTeacher?.department || '-' }}</p>
                      </div>
                      <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl">
                        <p class="text-sm text-gray-500 dark:text-gray-400">Jami ball</p>
                        <p class="font-semibold text-blue-600 dark:text-blue-400">{{ selectedTeacher?.total_score || 0 }}</p>
                      </div>
                    </div>
                    <div class="grid grid-cols-3 gap-4">
                      <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl text-center">
                        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ selectedTeacher?.portfolio_count || 0 }}</p>
                        <p class="text-xs text-gray-500 dark:text-gray-400">Portfolio</p>
                      </div>
                      <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl text-center">
                        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ selectedTeacher?.submission_count || 0 }}</p>
                        <p class="text-xs text-gray-500 dark:text-gray-400">Javoblar</p>
                      </div>
                      <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl text-center">
                        <p class="text-2xl font-bold text-green-600 dark:text-green-400">{{ selectedTeacher?.approved_count || 0 }}</p>
                        <p class="text-xs text-gray-500 dark:text-gray-400">Tasdiqlangan</p>
                      </div>
                    </div>
                  </div>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionRoot,
  TransitionChild
} from '@headlessui/vue'
import {
  MagnifyingGlassIcon,
  UsersIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()

const loading = ref(true)
const searchQuery = ref('')
const selectedDepartment = ref('')
const isDetailModalOpen = ref(false)
const selectedTeacher = ref(null)

// Mock data for DEV_MODE
const teachers = ref([
  {
    id: 1,
    full_name: 'Aliyev Bobur Karimovich',
    email: 'b.aliyev@university.uz',
    department: 'Informatika kafedrasi',
    portfolio_count: 12,
    submission_count: 45,
    approved_count: 38,
    total_score: 850
  },
  {
    id: 2,
    full_name: 'Karimova Dilnoza Rustamovna',
    email: 'd.karimova@university.uz',
    department: 'Matematika kafedrasi',
    portfolio_count: 8,
    submission_count: 32,
    approved_count: 28,
    total_score: 720
  },
  {
    id: 3,
    full_name: 'Rahimov Jasur Olimovich',
    email: 'j.rahimov@university.uz',
    department: 'Fizika kafedrasi',
    portfolio_count: 15,
    submission_count: 56,
    approved_count: 50,
    total_score: 980
  },
  {
    id: 4,
    full_name: 'Sodiqova Malika Anvarovna',
    email: 'm.sodiqova@university.uz',
    department: 'Informatika kafedrasi',
    portfolio_count: 6,
    submission_count: 24,
    approved_count: 20,
    total_score: 480
  },
  {
    id: 5,
    full_name: 'Toshmatov Sardor Bahodirovich',
    email: 's.toshmatov@university.uz',
    department: 'Matematika kafedrasi',
    portfolio_count: 10,
    submission_count: 38,
    approved_count: 32,
    total_score: 650
  },
  {
    id: 6,
    full_name: 'Xolmatova Sevinch Faxriddinovna',
    email: 's.xolmatova@university.uz',
    department: 'Fizika kafedrasi',
    portfolio_count: 9,
    submission_count: 35,
    approved_count: 30,
    total_score: 590
  }
])

const departments = ref([
  { id: 1, name: 'Informatika kafedrasi' },
  { id: 2, name: 'Matematika kafedrasi' },
  { id: 3, name: 'Fizika kafedrasi' }
])

const filteredTeachers = computed(() => {
  let result = teachers.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(t => 
      t.full_name.toLowerCase().includes(query) ||
      t.email.toLowerCase().includes(query)
    )
  }

  if (selectedDepartment.value) {
    const dept = departments.value.find(d => d.id === selectedDepartment.value)
    if (dept) {
      result = result.filter(t => t.department === dept.name)
    }
  }

  return result
})

const getInitials = (name) => {
  if (!name) return 'U'
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
}

const viewTeacherDetails = (teacher) => {
  selectedTeacher.value = teacher
  isDetailModalOpen.value = true
}

const viewTeacherPortfolios = (teacher) => {
  // Navigate to portfolios filtered by teacher
  router.push({ name: 'admin-approvals', query: { teacher: teacher.id } })
}

onMounted(() => {
  // Simulate loading
  setTimeout(() => {
    loading.value = false
  }, 500)
})
</script>
