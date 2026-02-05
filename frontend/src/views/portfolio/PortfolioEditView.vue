<template>
  <div class="animate-fade-in">
    <LoadingSpinner v-if="isLoading" fullscreen text="Yuklanmoqda..." />
    
    <template v-else-if="portfolio">
      <!-- Page header -->
      <div class="mb-6">
        <RouterLink :to="`/portfolios/${portfolio.id}`" class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-2">
          <ArrowLeftIcon class="w-4 h-4 mr-1" />
          Orqaga
        </RouterLink>
        <h1 class="text-2xl font-bold text-gray-900">Portfolioni tahrirlash</h1>
        <p class="mt-1 text-sm text-gray-500">
          Portfolio ma'lumotlarini yangilang
        </p>
      </div>
      
      <!-- Form -->
      <div class="card">
        <form @submit.prevent="handleSubmit" class="card-body space-y-6">
          <!-- Title -->
          <div>
            <label for="title" class="form-label">Sarlavha <span class="text-danger-500">*</span></label>
            <input
              id="title"
              v-model="form.title"
              type="text"
              class="form-input"
              :class="{ 'border-danger-500': errors.title }"
              placeholder="Portfolio sarlavhasi"
            />
            <p v-if="errors.title" class="form-error">{{ errors.title }}</p>
          </div>
          
          <!-- Category -->
          <div>
            <label for="category" class="form-label">Kategoriya <span class="text-danger-500">*</span></label>
            <select
              id="category"
              v-model="form.category"
              class="form-input"
              :class="{ 'border-danger-500': errors.category }"
            >
              <option value="">Kategoriyani tanlang</option>
              <option v-for="cat in PORTFOLIO_CATEGORIES" :key="cat.value" :value="cat.value">
                {{ cat.label }}
              </option>
            </select>
            <p v-if="errors.category" class="form-error">{{ errors.category }}</p>
          </div>
          
          <!-- Description -->
          <div>
            <label for="description" class="form-label">Tavsif <span class="text-danger-500">*</span></label>
            <textarea
              id="description"
              v-model="form.description"
              rows="6"
              class="form-input"
              :class="{ 'border-danger-500': errors.description }"
              placeholder="Portfolio haqida batafsil ma'lumot..."
            ></textarea>
            <p v-if="errors.description" class="form-error">{{ errors.description }}</p>
          </div>
          
          <!-- Is Public -->
          <div class="flex items-center gap-3">
            <input
              id="is_public"
              v-model="form.is_public"
              type="checkbox"
              class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
            />
            <label for="is_public" class="text-sm text-gray-700">
              Ommaviy qilish (barchaga ko'rsatish)
            </label>
          </div>
          
          <!-- Warning for teachers -->
          <AlertBox v-if="userStore.isTeacher && portfolio.status !== 'pending'" type="warning">
            Diqqat! Tahrirlash natijasida portfolio statusi "Kutilmoqda" ga qaytadi va qayta ko'rib chiqiladi.
          </AlertBox>
          
          <!-- Actions -->
          <div class="flex items-center justify-end gap-4 pt-4 border-t border-gray-200">
            <RouterLink :to="`/portfolios/${portfolio.id}`" class="btn-secondary">
              Bekor qilish
            </RouterLink>
            <button type="submit" class="btn-primary" :disabled="isSubmitting">
              <LoadingSpinner v-if="isSubmitting" size="xs" color="white" />
              <span v-else>Saqlash</span>
            </button>
          </div>
        </form>
      </div>
    </template>
    
    <EmptyState 
      v-else
      title="Portfolio topilmadi"
      action-text="Ortga qaytish"
      @action="$router.push('/portfolios')"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner, AlertBox, EmptyState } from '@/components/common'
import { usePortfolioStore, useUserStore } from '@/stores'
import { PORTFOLIO_CATEGORIES } from '@/services'

const route = useRoute()
const router = useRouter()
const portfolioStore = usePortfolioStore()
const userStore = useUserStore()

const portfolio = ref(null)
const isLoading = ref(true)
const isSubmitting = ref(false)

const form = reactive({
  title: '',
  category: '',
  description: '',
  is_public: false
})

const errors = reactive({
  title: '',
  category: '',
  description: ''
})

onMounted(async () => {
  try {
    const data = await portfolioStore.fetchPortfolio(route.params.id)
    portfolio.value = data
    
    // Populate form
    form.title = data.title
    form.category = data.category
    form.description = data.description
    form.is_public = data.is_public
  } catch (error) {
    console.error('Failed to fetch portfolio:', error)
  } finally {
    isLoading.value = false
  }
})

function validate() {
  let isValid = true
  errors.title = ''
  errors.category = ''
  errors.description = ''
  
  if (!form.title.trim()) {
    errors.title = 'Sarlavha kiritish majburiy'
    isValid = false
  }
  
  if (!form.category) {
    errors.category = 'Kategoriya tanlash majburiy'
    isValid = false
  }
  
  if (!form.description.trim()) {
    errors.description = 'Tavsif kiritish majburiy'
    isValid = false
  } else if (form.description.length < 50) {
    errors.description = 'Tavsif kamida 50 ta belgidan iborat bo\'lishi kerak'
    isValid = false
  }
  
  return isValid
}

async function handleSubmit() {
  if (!validate()) return
  
  isSubmitting.value = true
  try {
    await portfolioStore.updatePortfolio(portfolio.value.id, {
      title: form.title.trim(),
      category: form.category,
      description: form.description.trim(),
      is_public: form.is_public
    })
    
    router.push(`/portfolios/${portfolio.value.id}`)
  } catch (error) {
    console.error('Failed to update portfolio:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>
