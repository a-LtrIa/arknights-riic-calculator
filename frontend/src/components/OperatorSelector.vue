<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  operators: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['select', 'close'])

const searchQuery = ref('')
const selectedRarity = ref('all')
const selectedProfession = ref('all')

// 稀有度选项
const rarityOptions = [
  { value: 'all', label: '全部' },
  { value: '6', label: '6星' },
  { value: '5', label: '5星' },
  { value: '4', label: '4星' },
  { value: '3', label: '3星' },
  { value: '2', label: '2星' },
  { value: '1', label: '1星' },
]

// 职业选项
const professionOptions = [
  { value: 'all', label: '全部职业' },
  { value: '先锋', label: '先锋' },
  { value: '近卫', label: '近卫' },
  { value: '重装', label: '重装' },
  { value: '狙击', label: '狙击' },
  { value: '术师', label: '术师' },
  { value: '医疗', label: '医疗' },
  { value: '辅助', label: '辅助' },
  { value: '特种', label: '特种' },
]

// 过滤干员
const filteredOperators = computed(() => {
  console.log('OperatorSelector - props.operators:', props.operators?.length, props.operators)
  console.log('OperatorSelector - searchQuery:', searchQuery.value)
  console.log('OperatorSelector - selectedRarity:', selectedRarity.value)
  console.log('OperatorSelector - selectedProfession:', selectedProfession.value)
  
  if (!props.operators || props.operators.length === 0) {
    console.log('没有干员数据')
    return []
  }
  
  const result = props.operators.filter(op => {
    // 搜索过滤
    if (searchQuery.value) {
      const searchLower = searchQuery.value.toLowerCase()
      const nameLower = op.name?.toLowerCase() || ''
      if (!nameLower.includes(searchLower)) {
        return false
      }
    }
    
    return true
  })
  
  console.log('过滤后的结果数量:', result.length)
  return result
})

// 获取稀有度颜色
const getRarityColor = (rarity) => {
  const colors = {
    6: '#ff6b6b',
    5: '#feca57',
    4: '#48dbfb',
    3: '#1dd1a1',
    2: '#a29bfe',
    1: '#dfe6e9',
  }
  return colors[rarity] || '#dfe6e9'
}

const selectOperator = (operator) => {
  emit('select', operator)
}

const close = () => {
  emit('close')
}
</script>

<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h3>选择干员</h3>
        <button class="close-btn" @click="close">×</button>
      </div>
      
      <div class="filters">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索干员..."
          class="search-input"
        />
        
        <div class="filter-row">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索干员名称..."
            class="search-input"
          />
        </div>
      </div>
      
      <div>DEBUG: filteredOperators.length = {{ filteredOperators?.length }}</div>
      <div>DEBUG: first operator = {{ filteredOperators?.[0] }}</div>
      
      <div class="operators-list">
        <div
          v-for="(op, index) in filteredOperators"
          :key="op?.id || index"
          class="operator-item"
          @click="selectOperator(op)"
        >
          <span class="op-rarity">{{ op?.rarity }}★</span>
          <span class="op-name">{{ op?.name || '未知' }}</span>
        </div>
      </div>
      
      <div v-if="filteredOperators.length === 0" class="no-results">
        未找到匹配的干员
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h3 {
  font-size: 1.25rem;
  color: #333;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: #f0f0f0;
  border-radius: 8px;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #e0e0e0;
}

.filters {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.search-input {
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  width: 100%;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.filter-row {
  display: flex;
  gap: 0.75rem;
}

.filter-select {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.875rem;
}

.operators-grid {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 0.75rem;
}

.operator-card {
  display: flex;
  flex-direction: column;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}

.operator-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.operator-rarity {
  padding: 0.375rem 0.5rem;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  text-align: center;
}

.operator-info {
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.operator-name {
  font-weight: 500;
  color: #333;
  font-size: 0.875rem;
}

.operator-profession {
  font-size: 0.75rem;
  color: #666;
}

.no-results {
  padding: 3rem;
  text-align: center;
  color: #999;
}

.operators-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.operator-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.operator-item:hover {
  background: #e9ecef;
}

.op-rarity {
  font-size: 0.75rem;
  color: #667eea;
  font-weight: 600;
}

.op-name {
  flex: 1;
  font-weight: 500;
}
</style>
