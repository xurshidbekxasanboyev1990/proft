<template>
  <div class="animate-fade-in">
    <LoadingSpinner v-if="isLoading" fullscreen text="Yuklanmoqda..." />
    
    <template v-else-if="user">
      <!-- Page header -->
      <div class="mb-6">
        <RouterLink to="/admin/users" class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-2">
          <ArrowLeftIcon class="w-4 h-4 mr-1" />
          Orqaga
        </RouterLink>
        <h1 class="text-2xl font-bold text-gray-900">Foydalanuvchini tahrirlash</h1>
        <p class="mt-1 text-sm text-gray-500">
          {{ user.full_name || user.username }} ma'lumotlarini tahrirlang
        </p>
      </div>
      
      <div class="max-w-2xl">
        <div class="card">
          <form @submit.prevent="handleSubmit" class="card-body space-y-6">
            <AlertBox v-if="error" type="error" :message="error" @close="error = null" />
            <AlertBox v-if="success" type="success" :message="success" @close="success = null" />
            
            <!-- Username (read-only) -->
            <div>
              <label class="form-label">Username</label>
              <input
                :value="user.username"
                type="text"
                class="form-input bg-gray-50"
                disabled
              />
              <p class="form-helper">Username o'zgartirib bo'lmaydi</p>
            </div>
            
            <!-- Email -->
            <div>
              <label for="email" class="form-label">Email</label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                class="form-input"
                :class="{ 'border-danger-500': errors.email }"
                placeholder="email@example.com"
              />
              <p v-if="errors.email" class="form-error">{{ errors.email }}</p>
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <!-- First name -->
              <div>
                <label for="first_name" class="form-label">Ism</label>
                <input
                  id="first_name"
                  v-model="form.first_name"
                  type="text"
                  class="form-input"
                  placeholder="Ism"
                />
              </div>
              
              <!-- Last name -->
              <div>
                <label for="last_name" class="form-label">Familiya</label>
                <input
                  id="last_name"
                  v-model="form.last_name"
                  type="text"
                  class="form-input"
                  placeholder="Familiya"
                />
              </div>
            </div>
            
            <!-- Role -->
            <div>
              <label for="role" class="form-label">Rol <span class="text-danger-500">*</span></label>
              <select 
                id="role" 
                v-model="form.role" 
                class="form-input"
                :class="{ 'border-danger-500': errors.role }"
              >
                <option value="superadmin">Super Admin</option>
                <option value="admin">Admin</option>
                <option value="teacher">O'qituvchi</option>
              </select>
              <p v-if="errors.role" class="form-error">{{ errors.role }}</p>
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <!-- Department -->
              <div>
                <label for="department" class="form-label">Bo'lim</label>
                <input
                  id="department"
                  v-model="form.department"
                  type="text"
                  class="form-input"
                  placeholder="Bo'lim nomi"
                />
              </div>
              
              <!-- Position -->
              <div>
                <label for="position" class="form-label">Lavozim</label>
                <input
                  id="position"
                  v-model="form.position"
                  type="text"
                  class="form-input"
                  placeholder="Lavozim"
                />
              </div>
            </div>
            
            <!-- Is active -->
            <div class="flex items-center">
              <input
                id="is_active"
                v-model="form.is_active"
                type="checkbox"
                class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
              <label for="is_active" class="ml-2 text-sm text-gray-700">Faol foydalanuvchi</label>
            </div>
            
            <!-- Password section -->
            <div class="border-t border-gray-200 pt-6">
              <h3 class="text-sm font-medium text-gray-700 mb-4">Parolni o'zgartirish (ixtiyoriy)</h3>
              <div>
                <label for="password" class="form-label">Yangi parol</label>
                <input
                  id="password"
                  v-model="form.password"
                  type="password"
                  class="form-input"
                  :class="{ 'border-danger-500': errors.password }"
                  placeholder="••••••••"
                />
                <p v-if="errors.password" class="form-error">{{ errors.password }}</p>
                <p class="form-helper">Bo'sh qoldirsangiz, parol o'zgarmaydi</p>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="flex items-center justify-end gap-4 pt-4 border-t border-gray-200">
              <RouterLink to="/admin/users" class="btn-secondary">Bekor qilish</RouterLink>
              <button type="submit" class="btn-primary" :disabled="isSubmitting">
                <LoadingSpinner v-if="isSubmitting" size="xs" color="white" />
                <span v-else>Saqlash</span>
              </button>
            </div>
          </form>
        </div>
        
        <!-- Hemis info (if available) -->
        <div v-if="user.hemis_id" class="card mt-6">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900">Hemis ma'lumotlari</h2>
          </div>
          <div class="card-body space-y-3">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Hemis ID</span>
              <span class="font-medium text-gray-900">{{ user.hemis_id }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <EmptyState 
      v-else
      title="Foydalanuvchi topilmadi"
      action-text="Orqaga qaytish"
      @action="$router.push('/admin/users')"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner, AlertBox, EmptyState } from '@/components/common'
import { useUserStore } from '@/stores'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isLoading = ref(true)
const isSubmitting = ref(false)
const user = ref(null)
const error = ref(null)
const success = ref(null)
const errors = reactive({
  email: null,
  role: null,
  password: null
})

const form = reactive({
  email: '',
  first_name: '',
  last_name: '',
  role: '',
  department: '',
  position: '',
  is_active: true,
  password: ''
})

onMounted(async () => {
  try {
    const response = await userStore.fetchUserById(route.params.id)
    if (response) {
      user.value = response
      // Initialize form
      form.email = response.email || ''
      form.first_name = response.first_name || ''
      form.last_name = response.last_name || ''
      form.role = response.role || 'teacher'
      form.department = response.department || ''
      form.position = response.position || ''
      form.is_active = response.is_active ?? true
    }
  } catch (err) {
    console.error('Failed to fetch user:', err)
  } finally {
    isLoading.value = false
  }
})

function validateForm() {
  let isValid = true
  
  // Reset errors
  Object.keys(errors).forEach(key => errors[key] = null)
  
  if (form.email && !isValidEmail(form.email)) {
    errors.email = 'Email formati noto\'g\'ri'
    isValid = false
  }
  
  if (!form.role) {
    errors.role = 'Rolni tanlash majburiy'
    isValid = false
  }
  
  if (form.password && form.password.length < 8) {
    errors.password = 'Parol kamida 8 belgidan iborat bo\'lishi kerak'
    isValid = false
  }
  
  return isValid
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

async function handleSubmit() {
  if (!validateForm()) return
  
  isSubmitting.value = true
  error.value = null
  success.value = null
  
  try {
    const updateData = {
      email: form.email,
      first_name: form.first_name,
      last_name: form.last_name,
      role: form.role,
      department: form.department,
      position: form.position,
      is_active: form.is_active
    }
    
    // Only include password if it's set
    if (form.password) {
      updateData.password = form.password
    }
    
    await userStore.updateUser(user.value.id, updateData)
    success.value = 'Ma\'lumotlar muvaffaqiyatli saqlandi'
    form.password = '' // Clear password field
  } catch (err) {
    error.value = err.response?.data?.detail || 'Saqlashda xatolik yuz berdi'
    
    // Handle field-specific errors
    if (err.response?.data) {
      const data = err.response.data
      if (data.email) errors.email = data.email[0]
      if (data.password) errors.password = data.password[0]
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>
