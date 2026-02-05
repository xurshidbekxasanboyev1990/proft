<template>
  <BaseModal :is-open="isOpen" title="Ball sozlamalari" size="md" @close="$emit('close')">
    <div class="space-y-6">
      <!-- Use custom score toggle -->
      <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
        <div>
          <p class="font-medium text-gray-900">Maxsus ball sozlamalari</p>
          <p class="text-sm text-gray-500">Kategoriya standart ballidan farqli ball qo'llash</p>
        </div>
        <button
          type="button"
          @click="form.use_custom_score = !form.use_custom_score"
          :class="[
            'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
            form.use_custom_score ? 'bg-primary-600' : 'bg-gray-200'
          ]"
        >
          <span
            :class="[
              'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
              form.use_custom_score ? 'translate-x-5' : 'translate-x-0'
            ]"
          />
        </button>
      </div>

      <!-- Custom score settings -->
      <div v-if="form.use_custom_score" class="space-y-4">
        <!-- Max score -->
        <div>
          <label class="form-label">Maksimal ball</label>
          <input
            v-model.number="form.custom_max_score"
            type="number"
            min="1"
            max="1000"
            class="form-input"
            placeholder="100"
          />
          <p class="text-xs text-gray-400 mt-1">Kategoriya standarti: {{ categoryDefaultScore }} ball</p>
        </div>

        <!-- Min score -->
        <div>
          <label class="form-label">Minimal ball</label>
          <input
            v-model.number="form.custom_min_score"
            type="number"
            min="0"
            :max="form.custom_max_score || 100"
            class="form-input"
            placeholder="0"
          />
        </div>

        <!-- Score multiplier -->
        <div>
          <label class="form-label">Ball ko'paytiruvchi (multiplier)</label>
          <div class="flex items-center gap-4">
            <input
              v-model.number="form.score_multiplier"
              type="range"
              min="0.5"
              max="3"
              step="0.1"
              class="flex-1"
            />
            <span class="text-lg font-bold text-primary-600 w-16 text-center">{{ form.score_multiplier }}x</span>
          </div>
          <p class="text-xs text-gray-400 mt-1">
            Misol: 80 ball × {{ form.score_multiplier }} = {{ (80 * form.score_multiplier).toFixed(1) }} yakuniy ball
          </p>
        </div>

        <!-- Preset multipliers -->
        <div>
          <label class="form-label">Tez tanlash</label>
          <div class="flex gap-2">
            <button
              v-for="preset in multiplierPresets"
              :key="preset.value"
              type="button"
              @click="form.score_multiplier = preset.value"
              :class="[
                'px-3 py-1.5 text-sm rounded-lg border transition-colors',
                form.score_multiplier === preset.value
                  ? 'bg-primary-100 border-primary-500 text-primary-700'
                  : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
              ]"
            >
              {{ preset.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- Score note -->
      <div>
        <label class="form-label">Izoh</label>
        <textarea
          v-model="form.score_note"
          rows="2"
          class="form-input"
          placeholder="Ball sozlamalari haqida izoh..."
        ></textarea>
      </div>

      <!-- Preview -->
      <div class="p-4 bg-primary-50 rounded-lg">
        <p class="text-sm font-medium text-primary-900 mb-2">Ball hisoblash formulasi:</p>
        <code class="text-sm text-primary-700">
          yakuniy_ball = xom_ball × {{ form.score_multiplier || 1 }}
        </code>
      </div>
    </div>

    <template #footer>
      <button @click="$emit('close')" class="btn-secondary">Bekor qilish</button>
      <button @click="handleSave" class="btn-primary">Saqlash</button>
    </template>
  </BaseModal>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { BaseModal } from '@/components/common'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  assignment: {
    type: Object,
    default: () => ({})
  },
  category: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])

const form = reactive({
  use_custom_score: props.assignment?.use_custom_score || false,
  custom_max_score: props.assignment?.custom_max_score || 100,
  custom_min_score: props.assignment?.custom_min_score || 0,
  score_multiplier: props.assignment?.score_multiplier || 1,
  score_note: props.assignment?.score_note || ''
})

const categoryDefaultScore = computed(() => {
  return props.category?.default_score || props.assignment?.max_score || 100
})

const multiplierPresets = [
  { value: 0.5, label: '0.5x' },
  { value: 1, label: '1x (standart)' },
  { value: 1.5, label: '1.5x' },
  { value: 2, label: '2x bonus' },
  { value: 3, label: '3x super' }
]

function handleSave() {
  emit('save', {
    use_custom_score: form.use_custom_score,
    custom_max_score: form.use_custom_score ? form.custom_max_score : null,
    custom_min_score: form.use_custom_score ? form.custom_min_score : null,
    score_multiplier: form.score_multiplier,
    score_note: form.score_note
  })
}
</script>
