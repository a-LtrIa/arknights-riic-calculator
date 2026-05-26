<script setup>
import { ref, computed, watch } from 'vue'
import OperatorSelector from './OperatorSelector.vue'

const props = defineProps({
  operators: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update-config'])

// 设施类型
const facilityTypes = [
  { value: '制造站', label: '制造站', icon: '🔧' },
  { value: '贸易站', label: '贸易站', icon: '💰' },
  { value: '发电站', label: '发电站', icon: '⚡' },
  { value: '控制中枢', label: '控制中枢', icon: '🏢' },
  { value: '会客室', label: '会客室', icon: '🤝' },
  { value: '办公室', label: '办公室', icon: '📋' },
  { value: '宿舍', label: '宿舍', icon: '🏠' },
]

// 配方类型
const recipeTypes = [
  { value: '赤金', label: '赤金' },
  { value: '作战记录', label: '作战记录' },
  { value: '芯片', label: '芯片' },
]

// 设施列表
const facilities = ref([
  { id: 1, name: '制造站1', type: '制造站', level: 3, recipe: '赤金', operators: [] },
  { id: 2, name: '制造站2', type: '制造站', level: 3, recipe: '作战记录', operators: [] },
  { id: 3, name: '制造站3', type: '制造站', level: 3, recipe: '赤金', operators: [] },
  { id: 4, name: '贸易站1', type: '贸易站', level: 3, operators: [] },
  { id: 5, name: '贸易站2', type: '贸易站', level: 3, operators: [] },
  { id: 6, name: '控制中枢', type: '控制中枢', level: 5, operators: [] },
  { id: 7, name: '会客室', type: '会客室', level: 3, operators: [] },
  { id: 8, name: '办公室', type: '办公室', level: 3, operators: [] },
])

const activeFacility = ref(facilities.value[0])
const showOperatorSelector = ref(false)

// 获取设施最大人数
const getMaxOperators = (facilityType) => {
  const maxMap = {
    '制造站': 3,
    '贸易站': 3,
    '发电站': 1,
    '控制中枢': 5,
    '会客室': 2,
    '办公室': 1,
    '宿舍': 5,
  }
  return maxMap[facilityType] || 3
}

// 添加干员到设施
const addOperatorToFacility = (operator) => {
  const facility = activeFacility.value
  const maxOps = getMaxOperators(facility.type)
  
  if (facility.operators.length < maxOps) {
    facility.operators.push({
      name: operator.name,
      eliteLevel: 2
    })
    showOperatorSelector.value = false
    emitConfig()
  }
}

// 从设施移除干员
const removeOperator = (index) => {
  activeFacility.value.operators.splice(index, 1)
  emitConfig()
}

// 更新干员精英等级
const updateEliteLevel = (index, level) => {
  activeFacility.value.operators[index].eliteLevel = parseInt(level)
  emitConfig()
}

// 生成配置数据
const emitConfig = () => {
  const config = {}
  facilities.value.forEach(facility => {
    if (facility.operators.length > 0) {
      config[facility.name] = {
        '类型': facility.type,
        '等级': facility.level,
        '进驻干员': facility.operators.map(op => ({
          '名称': op.name,
          '精英等级': op.eliteLevel
        }))
      }
      if (facility.type === '制造站') {
        config[facility.name]['配方类型'] = facility.recipe
      }
    }
  })
  emit('update-config', config)
}

// 监听配方变化
watch(() => activeFacility.value?.recipe, () => {
  emitConfig()
})
</script>

<template>
  <div class="facility-configurator">
    <div class="config-header">
      <h2>设施配置</h2>
      <p>选择设施并配置进驻干员</p>
    </div>
    
    <div class="facility-tabs">
      <button
        v-for="facility in facilities"
        :key="facility.id"
        class="facility-tab"
        :class="{ active: activeFacility?.id === facility.id }"
        @click="activeFacility = facility"
      >
        <span class="facility-icon">{{ facilityTypes.find(t => t.value === facility.type)?.icon || '🏭' }}</span>
        <span class="facility-name">{{ facility.name }}</span>
        <span class="operator-count" v-if="facility.operators.length > 0">
          {{ facility.operators.length }}/{{ getMaxOperators(facility.type) }}
        </span>
      </button>
    </div>
    
    <div class="facility-detail" v-if="activeFacility">
      <div class="facility-info">
        <h3>{{ activeFacility.name }}</h3>
        <div class="facility-meta">
          <span class="badge">{{ activeFacility.type }}</span>
          <span class="badge">Lv.{{ activeFacility.level }}</span>
        </div>
      </div>
      
      <!-- 配方选择（仅制造站） -->
      <div class="recipe-selector" v-if="activeFacility.type === '制造站'">
        <label>生产配方:</label>
        <select v-model="activeFacility.recipe">
          <option v-for="recipe in recipeTypes" :key="recipe.value" :value="recipe.value">
            {{ recipe.label }}
          </option>
        </select>
      </div>
      
      <!-- 干员列表 -->
      <div class="operators-section">
        <div class="section-header">
          <h4>进驻干员</h4>
          <span class="capacity">
            {{ activeFacility.operators.length }}/{{ getMaxOperators(activeFacility.type) }}
          </span>
        </div>
        
        <div class="operators-list">
          <div
            v-for="(op, index) in activeFacility.operators"
            :key="index"
            class="operator-item"
          >
            <span class="operator-name">{{ op.name }}</span>
            <select
              class="elite-select"
              :value="op.eliteLevel"
              @change="updateEliteLevel(index, $event.target.value)"
            >
              <option value="0">E0</option>
              <option value="1">E1</option>
              <option value="2">E2</option>
            </select>
            <button class="remove-btn" @click="removeOperator(index)">×</button>
          </div>
          
          <button
            v-if="activeFacility.operators.length < getMaxOperators(activeFacility.type)"
            class="add-operator-btn"
            @click="showOperatorSelector = true"
          >
            + 添加干员
          </button>
        </div>
      </div>
    </div>
    
    <!-- 干员选择弹窗 -->
    <OperatorSelector
      v-if="showOperatorSelector"
      :operators="operators"
      @select="addOperatorToFacility"
      @close="showOperatorSelector = false"
    />
  </div>
</template>

<style scoped>
.facility-configurator {
  padding: 1.5rem;
}

.config-header {
  margin-bottom: 1.5rem;
}

.config-header h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 0.25rem;
}

.config-header p {
  color: #666;
  font-size: 0.875rem;
}

.facility-tabs {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

.facility-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.facility-tab:hover {
  border-color: #667eea;
}

.facility-tab.active {
  border-color: #667eea;
  background: #f0f4ff;
}

.facility-icon {
  font-size: 1.25rem;
}

.facility-name {
  font-weight: 500;
}

.operator-count {
  font-size: 0.75rem;
  padding: 0.125rem 0.375rem;
  background: #667eea;
  color: white;
  border-radius: 999px;
}

.facility-detail {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
}

.facility-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.facility-info h3 {
  font-size: 1.25rem;
  color: #333;
}

.facility-meta {
  display: flex;
  gap: 0.5rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  background: #667eea;
  color: white;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.recipe-selector {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
}

.recipe-selector label {
  font-weight: 500;
  color: #666;
}

.recipe-selector select {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  min-width: 150px;
}

.operators-section {
  background: white;
  border-radius: 8px;
  padding: 1rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h4 {
  font-size: 1rem;
  color: #333;
}

.capacity {
  font-size: 0.875rem;
  color: #666;
}

.operators-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.operator-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.operator-name {
  flex: 1;
  font-weight: 500;
}

.elite-select {
  padding: 0.375rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.875rem;
}

.remove-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: #ff4757;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.25rem;
  transition: background 0.2s;
}

.remove-btn:hover {
  background: #ff3344;
}

.add-operator-btn {
  padding: 0.75rem;
  border: 2px dashed #ddd;
  border-radius: 8px;
  background: transparent;
  color: #667eea;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.add-operator-btn:hover {
  border-color: #667eea;
  background: #f0f4ff;
}
</style>
