<script setup>
import { computed } from 'vue'

const props = defineProps({
  results: {
    type: Object,
    default: null
  }
})

// 计算总效率
const totalEfficiency = computed(() => {
  if (!props.results?.facilities) return 0
  return props.results.facilities.reduce((sum, f) => sum + (f.total_efficiency || 0), 0)
})

// 按设施类型分组
const facilitiesByType = computed(() => {
  if (!props.results?.facilities) return {}
  
  const grouped = {}
  props.results.facilities.forEach(facility => {
    const type = facility.facility_type || '其他'
    if (!grouped[type]) {
      grouped[type] = []
    }
    grouped[type].push(facility)
  })
  return grouped
})

// 获取效率颜色
const getEfficiencyColor = (efficiency) => {
  if (efficiency >= 100) return '#27ae60'
  if (efficiency >= 75) return '#2ecc71'
  if (efficiency >= 50) return '#f39c12'
  if (efficiency >= 25) return '#e67e22'
  return '#e74c3c'
}

// 获取进度条宽度
const getProgressWidth = (efficiency) => {
  return Math.min(efficiency, 100) + '%'
}
</script>

<template>
  <div class="efficiency-display">
    <div class="results-header">
      <h2>效率计算结果</h2>
      <div v-if="results" class="total-efficiency">
        <span class="label">总效率</span>
        <span class="value" :style="{ color: getEfficiencyColor(totalEfficiency) }">
          {{ totalEfficiency.toFixed(1) }}%
        </span>
      </div>
    </div>
    
    <div v-if="!results" class="empty-state">
      <div class="empty-icon">📊</div>
      <p>请先配置设施干员</p>
      <p class="hint">在左侧选择设施并添加干员后，效率将自动计算</p>
    </div>
    
    <div v-else class="results-content">
      <div v-for="(facilities, type) in facilitiesByType" :key="type" class="facility-group">
        <h3 class="group-title">{{ type }}</h3>
        
        <div class="facility-list">
          <div
            v-for="facility in facilities"
            :key="facility.facility_name"
            class="facility-card"
          >
            <div class="facility-header">
              <span class="facility-name">{{ facility.facility_name }}</span>
              <span class="facility-efficiency" :style="{ color: getEfficiencyColor(facility.total_efficiency) }">
                {{ facility.total_efficiency.toFixed(1) }}%
              </span>
            </div>
            
            <div class="efficiency-bar">
              <div
                class="efficiency-progress"
                :style="{ width: getProgressWidth(facility.total_efficiency), background: getEfficiencyColor(facility.total_efficiency) }"
              ></div>
            </div>
            
            <div class="operators-detail">
              <div
                v-for="op in facility.operators"
                :key="op.name"
                class="operator-row"
              >
                <span class="op-name">{{ op.name }}</span>
                <span class="op-elite">E{{ op.elite_level }}</span>
                <span class="op-efficiency" :style="{ color: getEfficiencyColor(op.efficiency) }">
                  +{{ op.efficiency.toFixed(1) }}%
                </span>
              </div>
            </div>
            
            <div v-if="facility.details" class="facility-details">
              <div v-for="(value, key) in facility.details" :key="key" class="detail-item">
                <span class="detail-key">{{ key }}:</span>
                <span class="detail-value">{{ value }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 特殊变量显示 -->
      <div v-if="results.special_variables && Object.keys(results.special_variables).length > 0" class="special-variables">
        <h3 class="group-title">特殊变量</h3>
        <div class="variables-grid">
          <div
            v-for="(value, key) in results.special_variables"
            :key="key"
            class="variable-item"
          >
            <span class="variable-name">{{ key }}</span>
            <span class="variable-value">{{ value }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.efficiency-display {
  padding: 1.5rem;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.results-header h2 {
  font-size: 1.5rem;
  color: #333;
}

.total-efficiency {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.total-efficiency .label {
  font-size: 0.75rem;
  color: #666;
  text-transform: uppercase;
}

.total-efficiency .value {
  font-size: 2rem;
  font-weight: 700;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #999;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state p {
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

.empty-state .hint {
  font-size: 0.875rem;
  color: #bbb;
}

.results-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.facility-group {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1rem;
}

.group-title {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.facility-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.facility-card {
  background: white;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.facility-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.facility-name {
  font-weight: 600;
  color: #333;
}

.facility-efficiency {
  font-size: 1.25rem;
  font-weight: 700;
}

.efficiency-bar {
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.efficiency-progress {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.operators-detail {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.operator-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.op-name {
  flex: 1;
  font-weight: 500;
}

.op-elite {
  padding: 0.125rem 0.5rem;
  background: #667eea;
  color: white;
  border-radius: 4px;
  font-size: 0.75rem;
}

.op-efficiency {
  font-weight: 600;
  min-width: 60px;
  text-align: right;
}

.facility-details {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e0e0e0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.detail-item {
  display: flex;
  gap: 0.25rem;
  font-size: 0.75rem;
}

.detail-key {
  color: #666;
}

.detail-value {
  color: #333;
  font-weight: 500;
}

.special-variables {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1rem;
}

.variables-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.75rem;
}

.variable-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
}

.variable-name {
  font-size: 0.875rem;
  color: #666;
}

.variable-value {
  font-weight: 600;
  color: #667eea;
}
</style>
