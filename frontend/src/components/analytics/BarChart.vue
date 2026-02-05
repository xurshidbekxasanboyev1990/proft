<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
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
  horizontal: {
    type: Boolean,
    default: false
  },
  stacked: {
    type: Boolean,
    default: false
  }
})

const chartData = computed(() => ({
  labels: props.data.labels || [],
  datasets: (props.data.datasets || []).map((dataset, index) => ({
    ...dataset,
    backgroundColor: dataset.backgroundColor || getColor(index),
    borderColor: dataset.borderColor || getColor(index),
    borderWidth: 0,
    borderRadius: 6,
    barPercentage: 0.7,
    categoryPercentage: 0.8
  }))
}))

const chartOptions = computed(() => ({
  indexAxis: props.horizontal ? 'y' : 'x',
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: props.showLegend && (props.data.datasets?.length > 1),
      position: 'top',
      labels: {
        usePointStyle: true,
        padding: 20
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
      cornerRadius: 8
    }
  },
  scales: {
    x: {
      stacked: props.stacked,
      grid: {
        display: false
      }
    },
    y: {
      stacked: props.stacked,
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.05)'
      }
    }
  }
}))

const colors = [
  '#6366F1', // primary
  '#22C55E', // success
  '#F59E0B', // warning
  '#EF4444', // danger
  '#8B5CF6', // purple
  '#EC4899', // pink
  '#06B6D4', // cyan
  '#14B8A6'  // teal
]

function getColor(index) {
  return colors[index % colors.length]
}
</script>
