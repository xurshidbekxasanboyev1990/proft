<template>
  <Doughnut :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  ArcElement,
  Title,
  Tooltip,
  Legend
)

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  showLegend: {
    type: Boolean,
    default: true
  },
  cutout: {
    type: String,
    default: '60%'
  }
})

const chartData = computed(() => ({
  labels: props.data.labels || [],
  datasets: [{
    data: props.data.values || props.data.data || [],
    backgroundColor: props.data.colors || defaultColors,
    borderColor: '#ffffff',
    borderWidth: 3,
    hoverOffset: 8
  }]
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  cutout: props.cutout,
  plugins: {
    legend: {
      display: props.showLegend,
      position: 'bottom',
      labels: {
        usePointStyle: true,
        padding: 16,
        font: {
          size: 12
        }
      }
    },
    title: {
      display: !!props.title,
      text: props.title,
      font: {
        size: 16,
        weight: 'bold'
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleFont: { size: 14 },
      bodyFont: { size: 13 },
      padding: 12,
      cornerRadius: 8,
      callbacks: {
        label: function(context) {
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const value = context.parsed
          const percentage = ((value / total) * 100).toFixed(1)
          return `${context.label}: ${value} (${percentage}%)`
        }
      }
    }
  }
}))

const defaultColors = [
  '#6366F1', // primary
  '#22C55E', // success
  '#F59E0B', // warning
  '#EF4444', // danger
  '#8B5CF6', // purple
  '#EC4899', // pink
  '#06B6D4', // cyan
  '#14B8A6'  // teal
]
</script>
