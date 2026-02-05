<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Mening ballarim</h1>
        <p class="mt-1 text-sm text-gray-500">
          Barcha baholangan ishlaringiz va umumiy ball statistikasi
        </p>
      </div>

      <!-- Export button -->
      <button
        @click="exportScores"
        class="inline-flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
      >
        <ArrowDownTrayIcon class="w-5 h-5" />
        Export
      </button>
    </div>

    <!-- Summary cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl p-6 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-primary-100 text-sm">Umumiy ball</p>
            <p class="text-3xl font-bold mt-1">{{ totalScore }}</p>
          </div>
          <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
            <TrophyIcon class="w-6 h-6" />
          </div>
        </div>
        <div class="mt-4 pt-4 border-t border-white/20">
          <div class="flex items-center justify-between text-sm">
            <span class="text-primary-100">Maksimal</span>
            <span class="font-medium">{{ maxPossibleScore }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">O'rtacha foiz</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ averagePercentage }}%</p>
          </div>
          <div class="w-12 h-12 bg-success-100 rounded-xl flex items-center justify-center">
            <ChartBarIcon class="w-6 h-6 text-success-600" />
          </div>
        </div>
        <div class="mt-4">
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="bg-success-500 h-2 rounded-full transition-all duration-500"
              :style="{ width: averagePercentage + '%' }"
            ></div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">Baholangan</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">{{ gradedCount }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
            <CheckCircleIcon class="w-6 h-6 text-blue-600" />
          </div>
        </div>
        <p class="mt-4 text-sm text-gray-500">
          {{ pendingCount }} ta tekshirilmoqda
        </p>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">Reyting</p>
            <p class="text-3xl font-bold text-gray-900 mt-1">#{{ ranking }}</p>
          </div>
          <div class="w-12 h-12 bg-warning-100 rounded-xl flex items-center justify-center">
            <StarIcon class="w-6 h-6 text-warning-600" />
          </div>
        </div>
        <p class="mt-4 text-sm text-gray-500">
          {{ totalTeachers }} o'qituvchi ichida
        </p>
      </div>
    </div>

    <!-- Score breakdown by category -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Category scores -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 class="font-semibold text-gray-900 mb-4">Kategoriya bo'yicha ballar</h3>
        <div class="space-y-4">
          <div 
            v-for="category in categoryScores" 
            :key="category.id"
            class="flex items-center gap-4"
          >
            <div 
              class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
              :style="{ backgroundColor: category.color + '20' }"
            >
              <FolderIcon class="w-5 h-5" :style="{ color: category.color }" />
            </div>
            <div class="flex-1">
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm font-medium text-gray-700">{{ category.name }}</span>
                <span class="text-sm text-gray-600">
                  {{ category.earned }} / {{ category.total }}
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="h-2 rounded-full transition-all duration-500"
                  :style="{ 
                    width: category.percentage + '%',
                    backgroundColor: category.color
                  }"
                ></div>
              </div>
            </div>
            <span 
              class="text-sm font-bold"
              :class="getPercentageColor(category.percentage)"
            >
              {{ category.percentage }}%
            </span>
          </div>
        </div>
      </div>

      <!-- Recent scores -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 class="font-semibold text-gray-900 mb-4">So'nggi ballar</h3>
        <div class="space-y-3">
          <div 
            v-for="score in recentScores" 
            :key="score.id"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <div class="flex items-center gap-3">
              <div 
                class="w-8 h-8 rounded-lg flex items-center justify-center"
                :class="getScoreBgClass(score.percentage)"
              >
                <span class="text-sm font-bold" :class="getScoreTextClass(score.percentage)">
                  {{ score.grade }}
                </span>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900">{{ score.assignment }}</p>
                <p class="text-xs text-gray-500">{{ formatDate(score.graded_at) }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium" :class="getPercentageColor(score.percentage)">
                {{ score.percentage }}%
              </p>
              <p class="text-xs text-gray-500">{{ score.grade }}/{{ score.max_score }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed scores table -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="p-6 border-b border-gray-200">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <h3 class="font-semibold text-gray-900">Batafsil ballar</h3>
          
          <!-- Filters -->
          <div class="flex items-center gap-4">
            <select
              v-model="filters.category"
              class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Barcha kategoriyalar</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
            <select
              v-model="filters.period"
              class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500"
            >
              <option value="all">Barcha vaqt</option>
              <option value="week">Oxirgi hafta</option>
              <option value="month">Oxirgi oy</option>
              <option value="semester">Semestr</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Topshiriq
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Kategoriya
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Sana
              </th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Ball
              </th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Foiz
              </th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Daraja
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr 
              v-for="score in filteredScores" 
              :key="score.id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4">
                <p class="text-sm font-medium text-gray-900">{{ score.assignment }}</p>
              </td>
              <td class="px-6 py-4">
                <span 
                  class="px-2 py-1 text-xs rounded-full"
                  :style="{ 
                    backgroundColor: score.category_color + '20',
                    color: score.category_color
                  }"
                >
                  {{ score.category }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                {{ formatDate(score.graded_at) }}
              </td>
              <td class="px-6 py-4 text-center">
                <span class="font-medium text-gray-900">{{ score.grade }}</span>
                <span class="text-gray-400">/{{ score.max_score }}</span>
              </td>
              <td class="px-6 py-4 text-center">
                <span 
                  class="font-medium"
                  :class="getPercentageColor(score.percentage)"
                >
                  {{ score.percentage }}%
                </span>
              </td>
              <td class="px-6 py-4 text-center">
                <span 
                  class="px-2 py-1 text-xs font-medium rounded-full"
                  :class="getGradeClass(score.percentage)"
                >
                  {{ getGradeLetter(score.percentage) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty state -->
      <div v-if="filteredScores.length === 0" class="p-12 text-center">
        <ChartBarIcon class="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-500">Hali baholangan ishlar yo'q</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  TrophyIcon,
  ChartBarIcon,
  CheckCircleIcon,
  StarIcon,
  FolderIcon,
  ArrowDownTrayIcon
} from '@heroicons/vue/24/outline'
import { formatDate } from '@/utils/date'
import { useToast } from 'vue-toastification'

const toast = useToast()

const filters = ref({
  category: '',
  period: 'all'
})

// Mock data
const totalScore = ref(425)
const maxPossibleScore = ref(500)
const averagePercentage = ref(85)
const gradedCount = ref(12)
const pendingCount = ref(3)
const ranking = ref(5)
const totalTeachers = ref(48)

const categories = ref([
  { id: '1', name: 'Ilmiy maqola', color: '#3B82F6' },
  { id: '2', name: 'Esse', color: '#10B981' },
  { id: '3', name: 'Loyiha', color: '#F59E0B' },
  { id: '4', name: 'Hisobot', color: '#8B5CF6' }
])

const categoryScores = ref([
  { id: '1', name: 'Ilmiy maqola', color: '#3B82F6', earned: 180, total: 200, percentage: 90 },
  { id: '2', name: 'Esse', color: '#10B981', earned: 85, total: 100, percentage: 85 },
  { id: '3', name: 'Loyiha', color: '#F59E0B', earned: 120, total: 150, percentage: 80 },
  { id: '4', name: 'Hisobot', color: '#8B5CF6', earned: 40, total: 50, percentage: 80 }
])

const recentScores = ref([
  { id: 1, assignment: 'Ilmiy maqola - Pedagogika', grade: 92, max_score: 100, percentage: 92, graded_at: new Date().toISOString() },
  { id: 2, assignment: 'Esse - Ta\'lim metodlari', grade: 45, max_score: 50, percentage: 90, graded_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString() },
  { id: 3, assignment: 'Loyiha hisoboti', grade: 78, max_score: 100, percentage: 78, graded_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString() },
  { id: 4, assignment: 'Ilmiy maqola - IT', grade: 88, max_score: 100, percentage: 88, graded_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString() }
])

const allScores = ref([
  { id: 1, assignment: 'Ilmiy maqola - Pedagogika', category: 'Ilmiy maqola', category_color: '#3B82F6', grade: 92, max_score: 100, percentage: 92, graded_at: new Date().toISOString() },
  { id: 2, assignment: 'Esse - Ta\'lim metodlari', category: 'Esse', category_color: '#10B981', grade: 45, max_score: 50, percentage: 90, graded_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString() },
  { id: 3, assignment: 'Loyiha hisoboti', category: 'Loyiha', category_color: '#F59E0B', grade: 78, max_score: 100, percentage: 78, graded_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString() },
  { id: 4, assignment: 'Ilmiy maqola - IT', category: 'Ilmiy maqola', category_color: '#3B82F6', grade: 88, max_score: 100, percentage: 88, graded_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString() },
  { id: 5, assignment: 'Haftalik hisobot', category: 'Hisobot', category_color: '#8B5CF6', grade: 40, max_score: 50, percentage: 80, graded_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString() },
  { id: 6, assignment: 'Esse - Innovatsiya', category: 'Esse', category_color: '#10B981', grade: 40, max_score: 50, percentage: 80, graded_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString() }
])

const filteredScores = computed(() => {
  let result = [...allScores.value]

  if (filters.value.category) {
    result = result.filter(s => 
      categories.value.find(c => c.id === filters.value.category)?.name === s.category
    )
  }

  if (filters.value.period !== 'all') {
    const now = new Date()
    let startDate
    switch (filters.value.period) {
      case 'week':
        startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
        break
      case 'month':
        startDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)
        break
      case 'semester':
        startDate = new Date(now.getTime() - 120 * 24 * 60 * 60 * 1000)
        break
    }
    result = result.filter(s => new Date(s.graded_at) >= startDate)
  }

  return result
})

function getPercentageColor(percentage) {
  if (percentage >= 90) return 'text-success-600'
  if (percentage >= 80) return 'text-blue-600'
  if (percentage >= 70) return 'text-warning-600'
  if (percentage >= 60) return 'text-orange-600'
  return 'text-danger-600'
}

function getScoreBgClass(percentage) {
  if (percentage >= 80) return 'bg-success-100'
  if (percentage >= 60) return 'bg-warning-100'
  return 'bg-danger-100'
}

function getScoreTextClass(percentage) {
  if (percentage >= 80) return 'text-success-700'
  if (percentage >= 60) return 'text-warning-700'
  return 'text-danger-700'
}

function getGradeClass(percentage) {
  if (percentage >= 90) return 'bg-success-100 text-success-700'
  if (percentage >= 80) return 'bg-blue-100 text-blue-700'
  if (percentage >= 70) return 'bg-warning-100 text-warning-700'
  if (percentage >= 60) return 'bg-orange-100 text-orange-700'
  return 'bg-danger-100 text-danger-700'
}

function getGradeLetter(percentage) {
  if (percentage >= 90) return 'A'
  if (percentage >= 80) return 'B'
  if (percentage >= 70) return 'C'
  if (percentage >= 60) return 'D'
  return 'F'
}

function exportScores() {
  toast.info('Ballar yuklab olinmoqda...')
  // Export logic
}

onMounted(() => {
  // Load data from API
})
</script>
