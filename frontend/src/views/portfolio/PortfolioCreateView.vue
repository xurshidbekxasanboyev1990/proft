<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="mb-6">
      <RouterLink to="/portfolios" class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-2">
        <ArrowLeftIcon class="w-4 h-4 mr-1" />
        Orqaga
      </RouterLink>
      <h1 class="text-2xl font-bold text-gray-900">Yangi portfolio</h1>
      <p class="mt-1 text-sm text-gray-500">
        Yangi portfolio yaratish uchun quyidagi formani to'ldiring
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
          <p class="text-xs text-gray-400 mt-1">Minimum 50 ta belgi</p>
        </div>
        
        <!-- File Upload -->
        <div>
          <label class="form-label">Fayllar (ixtiyoriy)</label>
          <FileUpload
            v-model="form.files"
            :max-files="10"
            :max-size="10 * 1024 * 1024"
            :upload-progress="uploadProgress"
          />
          <p class="text-xs text-gray-400 mt-1">PDF, DOC, DOCX, JPG, PNG, PPT formatlarida max 10 ta fayl</p>
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
        
        <!-- Actions -->
        <div class="flex items-center justify-end gap-4 pt-4 border-t border-gray-200">
          <RouterLink to="/portfolios" class="btn-secondary">
            Bekor qilish
          </RouterLink>
          <button type="submit" class="btn-primary" :disabled="isSubmitting">
            <LoadingSpinner v-if="isSubmitting" size="xs" color="white" />
            <span v-else>Yaratish</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner, FileUpload } from '@/components/common'
import { usePortfolioStore } from '@/stores'
import { PORTFOLIO_CATEGORIES, portfolioService } from '@/services'

const router = useRouter()
const portfolioStore = usePortfolioStore()

const form = reactive({
  title: '',
  category: '',
  description: '',
  is_public: false,
  files: []
})

const errors = reactive({
  title: '',
  category: '',
  description: ''
})

const isSubmitting = ref(false)
const uploadProgress = ref(0)

function validate() {
  let isValid = true
  errors.title = ''
  errors.category = ''
  errors.description = ''
  
  if (!form.title.trim()) {
    errors.title = 'Sarlavha kiritish majburiy'
    isValid = false
  } else if (form.title.length < 3) {
    errors.title = 'Sarlavha kamida 3 ta belgidan iborat bo\'lishi kerak'
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
    // Create portfolio
    const result = await portfolioStore.createPortfolio({
      title: form.title.trim(),
      category: form.category,
      description: form.description.trim(),
      is_public: form.is_public
    })
    
    // Upload files if any
    if (form.files.length > 0 && result.portfolio?.id) {
      uploadProgress.value = 0
      await portfolioService.uploadAttachments(
        result.portfolio.id, 
        form.files,
        (progress) => { uploadProgress.value = progress }
      )
    }
    
    router.push(`/portfolios/${result.portfolio.id}`)
  } catch (error) {
    console.error('Failed to create portfolio:', error)
  } finally {
    isSubmitting.value = false
    uploadProgress.value = 0
  }
}
</script>
