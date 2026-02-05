<template>
  <BaseModal :is-open="isOpen" title="Kategoriya ball sozlamalari" size="md" @close="$emit('close')">
    <div class="space-y-6">
      <!-- Category info -->
      <div class="p-4 bg-gray-50 rounded-lg">
        <div class="flex items-center gap-3">
          <div
            class="w-4 h-4 rounded-full"
            :style="{ backgroundColor: category?.color || '#6366F1' }"
          ></div>
          <span class="font-medium text-gray-900">{{ category?.name }}</span>
        </div>
      </div>

      <!-- Default score -->
      <div>
        <label class="form-label">Standart maksimal ball</label>
        <input
          v-model.number="form.default_score"
          type="number"
          min="1"
          max="1000"
          class="form-input"
          placeholder="100"
        />
        <p class="text-xs text-gray-400 mt-1">Bu kategoriya topshiriqlari uchun standart ball</p>
      </div>

      <!-- Min score -->
      <div>
        <label class="form-label">Minimal qabul qilinadigan ball</label>
        <input
          v-model.number="form.min_score"
          type="number"
          min="0"
          :max="form.default_score"
          class="form-input"
          placeholder="0"
        />
        <p class="text-xs text-gray-400 mt-1">Bundan past ball qabul qilinmaydi</p>
      </div>

      <!-- Score weight -->
      <div>
        <label class="form-label">Kategoriya vazni (weight)</label>
        <div class="flex items-center gap-4">
          <input
            v-model.number="form.score_weight"
            type="range"
            min="0.1"
            max="3"
            step="0.1"
            class="flex-1"
          />
          <span class="text-lg font-bold text-primary-600 w-16 text-center">{{ form.score_weight }}</span>
        </div>
        <p class="text-xs text-gray-400 mt-1">
          Umumiy ballni hisoblashda ishlatiladi
        </p>
      </div>

      <!-- Weight presets -->
      <div>
        <label class="form-label">Tez tanlash</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="preset in weightPresets"
            :key="preset.value"
            type="button"
            @click="form.score_weight = preset.value"
            :class="[
              'px-3 py-1.5 text-sm rounded-lg border transition-colors',
              form.score_weight === preset.value
                ? 'bg-primary-100 border-primary-500 text-primary-700'
                : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
            ]"
          >
            {{ preset.label }}
          </button>
        </div>
      </div>

      <!-- Formula preview -->
      <div class="p-4 bg-primary-50 rounded-lg">
        <p class="text-sm font-medium text-primary-900 mb-2">Ball hisoblash formulasi:</p>
        <code class="text-sm text-primary-700">
          yakuniy_ball = xom_ball × {{ form.score_weight }} × topshiriq_multiplier
        </code>
        <div class="mt-3 text-xs text-primary-600">
          <p><strong>Misol:</strong> Agar xom_ball = 80, vazn = {{ form.score_weight }}</p>
          <p>yakuniy_ball = 80 × {{ form.score_weight }} = {{ (80 * form.score_weight).toFixed(1) }}</p>
        </div>
      </div>
    </div>

    <template #footer>
      <button @click="$emit('close')" class="btn-secondary">Bekor qilish</button>
      <button @click="handleSave" class="btn-primary" :disabled="isSaving">
        <LoadingSpinner v-if="isSaving" size="xs" color="white" />
        <span v-else>Saqlash</span>
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { BaseModal, LoadingSpinner } from '@/components/common'
import { categoryService } from '@/services'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  category: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'saved'])

const isSaving = ref(false)

const form = reactive({
  default_score: props.category?.default_score || 100,
  min_score: props.category?.min_score || 0,
  score_weight: props.category?.score_weight || 1.0
})

// Watch for category changes
watch(() => props.category, (newCat) => {
  if (newCat) {
    form.default_score = newCat.default_score || 100
    form.min_score = newCat.min_score || 0
    form.score_weight = newCat.score_weight || 1.0
  }
}, { immediate: true })

const weightPresets = [
  { value: 0.5, label: '0.5 - Kam muhim' },
  { value: 1.0, label: '1.0 - Standart' },
  { value: 1.5, label: '1.5 - Muhim' },
  { value: 2.0, label: '2.0 - Juda muhim' }
]

async function handleSave() {
  isSaving.value = true
  try {
    await categoryService.updateCategoryScore(props.category.id, {
      default_score: form.default_score,
      min_score: form.min_score,
      score_weight: form.score_weight
    })
    emit('saved', form)
    emit('close')
  } catch (error) {
    console.error('Failed to update category score:', error)
  } finally {
    isSaving.value = false
  }
}
</script>
