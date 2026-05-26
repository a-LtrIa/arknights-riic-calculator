<script setup>
import { ref, computed } from 'vue'
import operatorsData from '../data/operators_with_skills.json'

const props = defineProps({
  room: { type: Object, required: true },
})

const emit = defineEmits(['assign', 'remove', 'close'])

// Load operators from JSON file (filter out unobtainable ones) with skills
const allOperatorsWithSkills = Object.values(operatorsData)
  .flat()
  .filter(op => !op.isNotObtainable)

const allOperators = allOperatorsWithSkills.map((op, idx) => ({
  id: idx + 1,
  name: op.name,
  elite: 0,
  rarity: parseInt(op.rarity?.replace('TIER_', '')) || 1,
  morale: 50,
  profession: op.profession_label || '先锋',
  avatar: null,
  skills: op.skills || [],
}))

const operators = ref(allOperators)

const searchQuery = ref('')
const selectedProfession = ref('all')
const selectedOperator = ref(null)

const professions = ['all', '先锋', '近卫', '重装', '狙击', '术师', '医疗', '辅助', '特种']

// Map room type to Chinese room name used in skills
const roomTypeMap = {
  trade: '贸易站',
  manufacturing: '制造站',
  power: '发电站',
  control: '控制中枢',
  dormitory: '宿舍',
  meeting: '会客室',
  workshop: '加工站',
  office: '办公室',
  training: '训练室',
}

const filteredOperators = computed(() => {
  const roomName = roomTypeMap[props.room.type] || props.room.type

  // First filter
  let filtered = operators.value.filter(op => {
    if (searchQuery.value && !op.name.includes(searchQuery.value)) return false
    if (selectedProfession.value !== 'all' && op.profession !== selectedProfession.value) return false
    if (props.room.operators.some(o => o.name === op.name)) return false
    return true
  })

  // Sort: operators with matching room skill first
  filtered.sort((a, b) => {
    const aHasRoom = a.skills.some(s => s.room === roomName)
    const bHasRoom = b.skills.some(s => s.room === roomName)
    if (aHasRoom && !bHasRoom) return -1
    if (!aHasRoom && bHasRoom) return 1
    return b.rarity - a.rarity // Then sort by rarity
  })

  return filtered
})

const maxOps = computed(() => {
  const map = {
    control: 5, dormitory: 5, trade: 3, manufacturing: 3,
    power: 1, meeting: 2, workshop: 1, office: 1, training: 1,
  }
  return map[props.room.type] || 3
})

const roomColor = computed(() => {
  const map = {
    trade: 'var(--color-trade)',
    manufacturing: 'var(--color-manufacturing)',
    power: 'var(--color-power)',
    control: 'var(--color-control)',
    dormitory: 'var(--color-dormitory)',
    meeting: 'var(--color-meeting)',
    workshop: 'var(--color-workshop)',
    office: 'var(--color-office)',
    training: 'var(--color-training)',
  }
  return map[props.room.type] || '#666'
})

const selectOperator = (op) => {
  selectedOperator.value = selectedOperator.value?.id === op.id ? null : op
}

const confirmAssign = () => {
  if (selectedOperator.value) {
    emit('assign', selectedOperator.value)
    selectedOperator.value = null
  }
}

const hasMatchingSkill = (op) => {
  const roomName = roomTypeMap[props.room.type] || props.room.type
  return op.skills?.some(s => s.room === roomName) || false
}

const removeAll = () => {
  for (let i = props.room.operators.length - 1; i >= 0; i--) {
    emit('remove', i)
  }
}

const rarityColor = (rarity) => {
  const colors = { 6: '#ff6b6b', 5: '#feca57', 4: '#48dbfb', 3: '#1dd1a1', 2: '#a29bfe', 1: '#dfe6e9' }
  return colors[rarity] || '#dfe6e9'
}
</script>

<template>
  <div class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center bg-black/70 backdrop-blur-sm" @click.self="emit('close')">
    <div class="operator-panel">
      <!-- Header -->
      <div class="panel-header">
        <div class="flex items-center gap-3">
          <div class="w-1 h-8 rounded-full" :style="{ background: roomColor }"></div>
          <div>
            <div class="text-base-200 font-mono text-sm font-semibold">{{ room.subtype || room.type }}</div>
            <div class="text-base-400 text-xs font-mono">进驻管理 · {{ props.room.operators.length }}/{{ maxOps }}</div>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button
            v-if="props.room.operators.length > 0"
            class="px-3 py-1.5 text-xs font-mono text-red-400 border border-red-400/30 rounded-md hover:bg-red-400/10 transition-colors cursor-pointer"
            @click="removeAll"
          >
            一键撤离
          </button>
          <button class="panel-close-btn cursor-pointer" @click="emit('close')">&times;</button>
        </div>
      </div>

      <!-- Room Operators -->
      <div v-if="props.room.operators.length > 0" class="current-operators">
        <div class="section-label">
          已进驻
          <span class="text-base-500 font-mono text-xs">{{ props.room.operators.length }}/{{ maxOps }}</span>
        </div>
        <div class="flex flex-wrap gap-2">
          <div
            v-for="(op, idx) in props.room.operators"
            :key="idx"
            class="current-op-chip"
          >
            <div class="current-op-avatar">
              <span class="text-base-400 text-lg">{{ op.name?.charAt(0) || '?' }}</span>
            </div>
            <div class="current-op-info">
              <span class="current-op-name">{{ op.name || '未知干员' }}</span>
              <div class="flex items-center gap-1.5">
                <span class="text-[10px] font-mono px-1 py-0.5 rounded bg-base-700/50 text-base-300">E{{ op.elite || op.eliteLevel || 0 }}</span>
                <div class="morale-bar-mini">
                  <div class="morale-fill-mini" :style="{ width: (op.morale || 75) + '%' }"></div>
                </div>
              </div>
            </div>
            <button class="remove-op-btn cursor-pointer" @click="emit('remove', idx)">×</button>
          </div>
        </div>
      </div>

      <!-- Available Operators -->
      <div class="panel-body">
        <div class="section-label">候补干员</div>

        <!-- Filters -->
        <div class="flex gap-2 mb-3">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索干员名称..."
            class="search-input"
          />
          <select v-model="selectedProfession" class="profession-select">
            <option value="all">全部职业</option>
            <option v-for="p in professions.slice(1)" :key="p" :value="p">{{ p }}</option>
          </select>
        </div>

        <!-- Operator Grid -->
        <div class="operator-grid">
          <div
            v-for="op in filteredOperators"
            :key="op.id"
            class="operator-card"
            :class="{
              selected: selectedOperator?.id === op.id,
              'skill-match': hasMatchingSkill(op)
            }"
            @click="selectOperator(op)"
          >
            <div class="op-avatar">
              <span class="op-avatar-text">{{ op.name?.charAt(0) || '?' }}</span>
              <div class="op-rarity-badge" :style="{ background: rarityColor(op.rarity) }">
                {{ op.rarity }}
              </div>
              <div v-if="hasMatchingSkill(op)" class="skill-match-badge" :title="'适合' + roomTypeMap[props.room.type]">
                ★
              </div>
            </div>
            <div class="op-info">
              <div class="op-name-row">
                <span class="op-name">{{ op.name }}</span>
                <span class="op-profession text-base-500">{{ op.profession }}</span>
              </div>
              <div class="op-meta-row">
                <span class="elite-badge">E{{ op.elite }}</span>
                <div class="morale-bar">
                  <div class="morale-fill" :class="{ 'morale-low': op.morale < 40, 'morale-mid': op.morale >= 40 && op.morale < 70 }" :style="{ width: op.morale + '%' }"></div>
                </div>
                <span class="morale-text font-mono text-xs text-base-500">{{ op.morale }}%</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredOperators.length === 0" class="text-center text-base-500 font-mono text-xs py-8">
          暂无可用干员
        </div>
      </div>

      <!-- Action -->
      <div class="panel-footer">
        <button
          class="assign-btn"
          :class="{ active: selectedOperator }"
          :disabled="!selectedOperator || props.room.operators.length >= maxOps"
          @click="confirmAssign"
        >
          {{ !selectedOperator ? '请选择干员' : props.room.operators.length >= maxOps ? '已满员' : `进驻 ${selectedOperator.name}` }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.operator-panel {
  width: 100%;
  max-width: 560px;
  max-height: 80vh;
  background: #1a1a1a;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px 16px 0 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.5);
}

@media (min-width: 640px) {
  .operator-panel {
    border-radius: 16px;
    max-height: 75vh;
  }
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}

.panel-close-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  font-size: 20px;
  color: #6b7280;
  transition: all 0.2s;
}

.panel-close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #d1d5db;
}

.current-operators {
  padding: 12px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}

.section-label {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.current-op-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px 6px 6px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  min-width: 160px;
}

.current-op-avatar {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: linear-gradient(135deg, #2a2a2a, #333);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.current-op-info {
  flex: 1;
  min-width: 0;
}

.current-op-name {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 600;
  color: #d1d5db;
}

.remove-op-btn {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: #6b7280;
  font-size: 16px;
  border-radius: 4px;
  transition: all 0.2s;
  flex-shrink: 0;
}

.remove-op-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.morale-bar-mini {
  width: 40px;
  height: 3px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  overflow: hidden;
}

.morale-fill-mini {
  height: 100%;
  background: linear-gradient(90deg, #22c55e, #4ade80);
  border-radius: 2px;
  transition: width 0.5s ease;
}

.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 14px 20px;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  color: #d1d5db;
  font-family: var(--font-mono);
  font-size: 12px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: rgba(255, 255, 255, 0.2);
}

.search-input::placeholder {
  color: #4a4a4a;
}

.profession-select {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  color: #d1d5db;
  font-family: var(--font-mono);
  font-size: 12px;
  outline: none;
  cursor: pointer;
  min-width: 100px;
  transition: border-color 0.2s;
}

.profession-select:focus {
  border-color: rgba(255, 255, 255, 0.2);
}

.operator-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 6px;
}

.operator-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.operator-card:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.12);
}

.operator-card.selected {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
}

.op-avatar {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: linear-gradient(135deg, #2a2a2a, #3a3a3a);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.op-avatar-text {
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 700;
  color: #9ca3af;
  text-shadow: 0 0 8px rgba(255, 255, 255, 0.1);
}

.op-rarity-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  font-size: 7px;
  font-weight: 700;
  font-family: var(--font-mono);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.3);
}

.op-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.op-name-row {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.op-name {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 600;
  color: #d1d5db;
}

.op-profession {
  font-size: 10px;
}

.op-meta-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.elite-badge {
  font-family: var(--font-mono);
  font-size: 9px;
  padding: 1px 4px;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.06);
  color: #9ca3af;
  font-weight: 600;
  flex-shrink: 0;
}

.morale-bar {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  overflow: hidden;
  max-width: 80px;
}

.morale-fill {
  height: 100%;
  background: linear-gradient(90deg, #22c55e, #4ade80);
  border-radius: 2px;
  transition: width 0.5s ease;
}

.morale-fill.morale-low {
  background: linear-gradient(90deg, #ef4444, #f87171);
}

.morale-fill.morale-mid {
  background: linear-gradient(90deg, #eab308, #facc15);
}

.morale-text {
  flex-shrink: 0;
}

.panel-footer {
  padding: 12px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}

.assign-btn {
  width: 100%;
  padding: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  color: #6b7280;
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.assign-btn.active {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
  color: #60a5fa;
}

.assign-btn.active:hover {
  background: rgba(59, 130, 246, 0.25);
}

.assign-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Skill match indicator */
.operator-card.skill-match {
  background: rgba(139, 92, 246, 0.08);
  border-color: rgba(139, 92, 246, 0.25);
}

.operator-card.skill-match:hover {
  background: rgba(139, 92, 246, 0.12);
  border-color: rgba(139, 92, 246, 0.35);
}

.skill-match-badge {
  position: absolute;
  bottom: -4px;
  left: -4px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  color: white;
  font-size: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>