<script setup>
import { ref, reactive } from 'vue'
import OperatorPanel from './OperatorPanel.vue'

const buildMode = ref(false)
const selectedRoom = ref(null)
const showBuildMenu = ref(null)
const showOperatorPanel = ref(false)

const roomTypes = {
  control: { label: '控制中枢', color: 'var(--color-control)', maxOps: 5 },
  dormitory: { label: '宿舍', color: 'var(--color-dormitory)', maxOps: 5 },
  trade: { label: '贸易站', color: 'var(--color-trade)', maxOps: 3 },
  manufacturing: { label: '制造站', color: 'var(--color-manufacturing)', maxOps: 3 },
  power: { label: '发电站', color: 'var(--color-power)', maxOps: 1 },
  meeting: { label: '会客室', color: 'var(--color-meeting)', maxOps: 2 },
  workshop: { label: '加工站', color: 'var(--color-workshop)', maxOps: 1 },
  office: { label: '办公室', color: 'var(--color-office)', maxOps: 1 },
  training: { label: '训练室', color: 'var(--color-training)', maxOps: 1 },
  empty: { label: '可建造', color: '#4a4a4a', maxOps: 0 },
  corridor: { label: '走廊', color: '#333333', maxOps: 0 },
}

// Left wing: 9 rooms, 3 columns
const leftWingRooms = reactive([
  // Row 1
  { id: 'left-0', type: 'trade', subtype: '贸易站 001', level: 3, operators: [], built: true },
  { id: 'left-1', type: 'manufacturing', subtype: '制造站 001', level: 3, operators: [], built: true },
  { id: 'left-2', type: 'power', subtype: '发电站 001', level: 3, operators: [], built: true },
  // Row 2 (offset by half card)
  { id: 'left-3', type: 'trade', subtype: '贸易站 002', level: 3, operators: [], built: true },
  { id: 'left-4', type: 'manufacturing', subtype: '制造站 002', level: 3, operators: [], built: true },
  { id: 'left-5', type: 'power', subtype: '发电站 002', level: 3, operators: [], built: true },
  // Row 3
  { id: 'left-6', type: 'trade', subtype: '贸易站 003', level: 3, operators: [], built: true },
  { id: 'left-7', type: 'manufacturing', subtype: '制造站 003', level: 3, operators: [], built: true },
  { id: 'left-8', type: 'power', subtype: '发电站 003', level: 3, operators: [], built: true },
])

// Right wing: 4 rooms (single column)
const rightWingRooms = reactive([
  { id: 'right-0', type: 'meeting', subtype: '会客室', level: 3, operators: [], built: true },
  { id: 'right-1', type: 'workshop', subtype: '加工站', level: 3, operators: [], built: true },
  { id: 'right-2', type: 'office', subtype: '办公室', level: 3, operators: [], built: true },
  { id: 'right-3', type: 'training', subtype: '训练室', level: 3, operators: [], built: true },
])

// Core: 5 dormitories + 1 control center (same height)
const coreRooms = reactive([
  { id: 'core-0', type: 'control', subtype: '控制中枢', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-1', type: 'dormitory', subtype: '宿舍 001', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-2', type: 'dormitory', subtype: '宿舍 002', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-3', type: 'dormitory', subtype: '宿舍 003', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-4', type: 'dormitory', subtype: '宿舍 004', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-5', type: 'dormitory', subtype: '宿舍 005', level: 5, operators: [], built: true, span: 1 },
])

// Corridor rooms
const leftCorridor = reactive({ id: 'corridor-left', type: 'corridor', subtype: '走廊', level: 0, operators: [], built: true })
const rightCorridor = reactive({ id: 'corridor-right', type: 'corridor', subtype: '走廊', level: 0, operators: [], built: true })

const getRoomStatus = (room) => {
  if (!room.built) return '未建造'
  if (room.type === 'corridor') return ''
  if (room.type === 'control') return '运行中'
  const statusMap = {
    trade: '洽谈中',
    manufacturing: '生产中',
    power: '供电中',
    dormitory: '休息中',
    meeting: '会客中',
    workshop: '加工中',
    office: '办公中',
    training: '训练中',
  }
  return statusMap[room.type] || '运行中'
}

const getColorVar = (type) => {
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
    empty: '#4a4a4a',
    corridor: '#333',
  }
  return map[type] || '#666'
}

const getColorClass = (type) => {
  const map = {
    trade: 'accent-trade',
    manufacturing: 'accent-manufacturing',
    power: 'accent-power',
    control: 'accent-control',
    dormitory: 'accent-dormitory',
    meeting: 'accent-meeting',
    workshop: 'accent-workshop',
    office: 'accent-office',
    training: 'accent-training',
  }
  return map[type] || ''
}

const buildableTypes = [
  { type: 'trade', label: '贸易站', color: 'var(--color-trade)', icon: '💰' },
  { type: 'manufacturing', label: '制造站', color: 'var(--color-manufacturing)', icon: '🔧' },
  { type: 'power', label: '发电站', color: 'var(--color-power)', icon: '⚡' },
]

const handleRoomClick = (room) => {
  if (buildMode.value) {
    if (!room.built) {
      showBuildMenu.value = room
    }
    return
  }
  if (room.built && room.type !== 'corridor' && room.type !== 'empty') {
    selectedRoom.value = room
    showOperatorPanel.value = true
  }
}

const handleBuildSelect = (type) => {
  if (!showBuildMenu.value) return
  showBuildMenu.value.type = type
  showBuildMenu.value.built = true
  showBuildMenu.value.level = 3
  showBuildMenu.value.operators = []
  const typeNames = {
    trade: '贸易站',
    manufacturing: '制造站',
    power: '发电站',
  }
  showBuildMenu.value.subtype = typeNames[type] || type
  showBuildMenu.value = null
}

const closeBuildMenu = () => {
  showBuildMenu.value = null
}

const assignOperator = (operator) => {
  if (!selectedRoom.value) return
  const maxOps = roomTypes[selectedRoom.value.type]?.maxOps || 3
  if (selectedRoom.value.operators.length < maxOps) {
    selectedRoom.value.operators.push({ ...operator })
  }
}

const removeOperator = (index) => {
  if (!selectedRoom.value) return
  selectedRoom.value.operators.splice(index, 1)
}

const closeOperatorPanel = () => {
  showOperatorPanel.value = false
  selectedRoom.value = null
}

const operatorCount = (room) => {
  return room.operators?.length || 0
}

const maxOperators = (room) => {
  return roomTypes[room.type]?.maxOps || 0
}
</script>

<template>
  <div class="min-h-screen bg-base-900 text-base-200 font-sans select-none">
    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 z-50 h-14 bg-base-900/90 backdrop-blur-sm border-b border-base-700/50 flex items-center justify-between px-6">
      <div class="flex items-center gap-4">
        <span class="text-base-400 text-sm font-mono tracking-wider">ARKNIGHTS RIIC</span>
        <span class="text-base-600">|</span>
        <span class="text-base-300 text-sm">基建管理系统</span>
      </div>
      <div class="flex items-center gap-4">
        <span class="text-xs text-base-400 font-mono">v2.0.1</span>
        <div class="h-4 w-px bg-base-700"></div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-mono text-base-400" :class="{ 'text-control': buildMode }">建造模式</span>
          <button
            class="relative w-11 h-6 rounded-full transition-all duration-300 cursor-pointer"
            :class="buildMode ? 'bg-control' : 'bg-base-600'"
            @click="buildMode = !buildMode"
          >
            <span
              class="absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-md transition-all duration-300"
              :class="buildMode ? 'left-[22px]' : 'left-0.5'"
            ></span>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Layout -->
    <div class="pt-14 min-h-screen flex items-center justify-center p-6">
      <div class="riic-layout">
        <!-- Left Wing: 3 rows with staggered cards -->
        <div class="left-wing">
          <!-- Row 1: aligned left -->
          <div class="left-row left-row-1">
            <div
              v-for="room in [leftWingRooms[0], leftWingRooms[1], leftWingRooms[2]]"
              :key="room.id"
              class="room-card"
              :class="[getColorClass(room.type), { 'cursor-pointer': buildMode }]"
              @click="handleRoomClick(room)"
            >
              <div class="accent-bar" :style="{ background: getColorVar(room.type) }"></div>
              <div class="room-content">
                <div class="room-header">
                  <span class="room-name">{{ roomTypes[room.type]?.label }}</span>
                  <span class="level-badge" :class="`level-${room.type}`">Lv.{{ room.level }}</span>
                </div>
                <div class="room-subname-row">
                  <span class="room-subname">{{ room.subtype }}</span>
                </div>
                <div class="room-status">
                  <span class="status-dot" :style="{ background: getColorVar(room.type) }"></span>
                  <span class="status-text">{{ getRoomStatus(room) }}</span>
                </div>
                <div class="room-operators">
                  <span class="text-base-400 text-xs mr-1">👤</span>
                  <span class="font-mono text-sm" :class="operatorCount(room) === maxOperators(room) ? 'text-power-light' : 'text-trade-light'">{{ operatorCount(room) }}/{{ maxOperators(room) }}</span>
                </div>
              </div>
            </div>
          </div>
          <!-- Row 2: staggered -->
          <div class="left-row left-row-2">
            <div
              v-for="room in [leftWingRooms[3], leftWingRooms[4], leftWingRooms[5]]"
              :key="room.id"
              class="room-card"
              :class="[getColorClass(room.type), { 'cursor-pointer': buildMode }]"
              @click="handleRoomClick(room)"
            >
              <div class="accent-bar" :style="{ background: getColorVar(room.type) }"></div>
              <div class="room-content">
                <div class="room-header">
                  <span class="room-name">{{ roomTypes[room.type]?.label }}</span>
                  <span class="level-badge" :class="`level-${room.type}`">Lv.{{ room.level }}</span>
                </div>
                <div class="room-subname-row">
                  <span class="room-subname">{{ room.subtype }}</span>
                </div>
                <div class="room-status">
                  <span class="status-dot" :style="{ background: getColorVar(room.type) }"></span>
                  <span class="status-text">{{ getRoomStatus(room) }}</span>
                </div>
                <div class="room-operators">
                  <span class="text-base-400 text-xs mr-1">👤</span>
                  <span class="font-mono text-sm" :class="operatorCount(room) === maxOperators(room) ? 'text-power-light' : 'text-trade-light'">{{ operatorCount(room) }}/{{ maxOperators(room) }}</span>
                </div>
              </div>
            </div>
          </div>
          <!-- Row 3: staggered more -->
          <div class="left-row left-row-3">
            <div
              v-for="room in [leftWingRooms[6], leftWingRooms[7], leftWingRooms[8]]"
              :key="room.id"
              class="room-card"
              :class="[getColorClass(room.type), { 'cursor-pointer': buildMode }]"
              @click="handleRoomClick(room)"
            >
              <div class="accent-bar" :style="{ background: getColorVar(room.type) }"></div>
              <div class="room-content">
                <div class="room-header">
                  <span class="room-name">{{ roomTypes[room.type]?.label }}</span>
                  <span class="level-badge" :class="`level-${room.type}`">Lv.{{ room.level }}</span>
                </div>
                <div class="room-subname-row">
                  <span class="room-subname">{{ room.subtype }}</span>
                </div>
                <div class="room-status">
                  <span class="status-dot" :style="{ background: getColorVar(room.type) }"></span>
                  <span class="status-text">{{ getRoomStatus(room) }}</span>
                </div>
                <div class="room-operators">
                  <span class="text-base-400 text-xs mr-1">👤</span>
                  <span class="font-mono text-sm" :class="operatorCount(room) === maxOperators(room) ? 'text-power-light' : 'text-trade-light'">{{ operatorCount(room) }}/{{ maxOperators(room) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Left Corridor -->
        <div class="corridor-wrapper">
          <div
            class="corridor-card"
            @click="handleRoomClick(leftCorridor)"
          >
            <span class="corridor-icon">🏃</span>
            <span class="corridor-label">走廊</span>
          </div>
        </div>

        <!-- Core Grid: Fixed width -->
        <div class="core-grid">
          <!-- Control Center -->
          <div
            class="room-card control-card"
            :class="[getColorClass('control'), { 'cursor-pointer': buildMode }]"
            @click="handleRoomClick(coreRooms[0])"
          >
            <div class="accent-bar" :style="{ background: getColorVar('control') }"></div>
            <div class="room-content">
              <div class="room-header">
                <span class="room-name">{{ roomTypes['control']?.label }}</span>
                <span class="level-badge level-control">Lv.{{ coreRooms[0].level }}</span>
              </div>
              <div class="room-subname-row">
                <span class="room-subname">{{ coreRooms[0].subtype }}</span>
              </div>
              <div class="control-version">VER {{ coreRooms[0].level }}.0</div>
              <div class="room-status">
                <span class="status-dot" :style="{ background: getColorVar('control') }"></span>
                <span class="status-text">{{ getRoomStatus(coreRooms[0]) }}</span>
              </div>
              <div class="room-operators">
                <span class="text-base-400 text-xs mr-1">👤</span>
                <span class="font-mono text-sm text-control-light">{{ operatorCount(coreRooms[0]) }}/{{ maxOperators(coreRooms[0]) }}</span>
              </div>
            </div>
          </div>

          <!-- Rest of core rooms -->
          <div
            v-for="room in coreRooms.slice(1)"
            :key="room.id"
            class="room-card"
            :class="[
              room.type === 'empty' ? 'empty-card' : '',
              getColorClass(room.type),
              { 'cursor-pointer': buildMode }
            ]"
            @click="handleRoomClick(room)"
          >
            <template v-if="room.type === 'empty'">
              <div class="empty-slot" :class="{ 'build-mode-active': buildMode }">
                <template v-if="buildMode">
                  <div class="empty-plus">+</div>
                  <span class="empty-label">可建造</span>
                </template>
                <template v-else>
                  <span class="empty-label text-base-600">空置</span>
                </template>
              </div>
            </template>
            <template v-else>
              <div class="accent-bar" :style="{ background: getColorVar(room.type) }"></div>
              <div class="room-content">
                <div class="room-header">
                  <span class="room-name">{{ roomTypes[room.type]?.label }}</span>
                  <span class="level-badge" :class="`level-${room.type}`">Lv.{{ room.level }}</span>
                </div>
                <div class="room-subname-row">
                  <span class="room-subname">{{ room.subtype }}</span>
                </div>
                <div class="room-status">
                  <span class="status-dot" :style="{ background: getColorVar(room.type) }"></span>
                  <span class="status-text">{{ getRoomStatus(room) }}</span>
                </div>
                <div class="room-operators">
                  <span class="text-base-400 text-xs mr-1">👤</span>
                  <span class="font-mono text-sm" :class="operatorCount(room) === maxOperators(room) ? 'text-power-light' : 'text-trade-light'">{{ operatorCount(room) }}/{{ maxOperators(room) }}</span>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- Right Corridor -->
        <div class="corridor-wrapper">
          <div
            class="corridor-card"
            @click="handleRoomClick(rightCorridor)"
          >
            <span class="corridor-icon">🏃</span>
            <span class="corridor-label">走廊</span>
          </div>
        </div>

        <!-- Right Wing: 4 rooms -->
        <div class="right-wing">
          <div
            v-for="room in rightWingRooms"
            :key="room.id"
            class="room-card"
            :class="[getColorClass(room.type), { 'cursor-pointer': buildMode }]"
            @click="handleRoomClick(room)"
          >
            <div class="accent-bar" :style="{ background: getColorVar(room.type) }"></div>
            <div class="room-content">
              <div class="room-header">
                <span class="room-name">{{ roomTypes[room.type]?.label }}</span>
                <span class="level-badge" :class="`level-${room.type}`">Lv.{{ room.level }}</span>
              </div>
              <div class="room-subname-row">
                <span class="room-subname">{{ room.subtype }}</span>
              </div>
              <div class="room-status">
                <span class="status-dot" :style="{ background: getColorVar(room.type) }"></span>
                <span class="status-text">{{ getRoomStatus(room) }}</span>
              </div>
              <div class="room-operators">
                <span class="text-base-400 text-xs mr-1">👤</span>
                <span class="font-mono text-sm" :class="operatorCount(room) === maxOperators(room) ? 'text-power-light' : 'text-trade-light'">{{ operatorCount(room) }}/{{ maxOperators(room) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Build Mode Menu -->
    <Teleport to="body">
      <div v-if="showBuildMenu" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm" @click.self="closeBuildMenu">
        <div class="build-menu">
          <div class="build-menu-header">
            <span class="text-base-200 font-mono text-sm">选择建造类型</span>
            <button class="text-base-500 hover:text-base-200 transition-colors text-lg leading-none cursor-pointer" @click="closeBuildMenu">&times;</button>
          </div>
          <div class="build-menu-body">
            <button
              v-for="bt in buildableTypes"
              :key="bt.type"
              class="build-option"
              :style="{ '--accent': bt.color }"
              @click="handleBuildSelect(bt.type)"
            >
              <span class="build-option-icon">{{ bt.icon }}</span>
              <div class="build-option-info">
                <span class="build-option-name">{{ bt.label }}</span>
                <span class="build-option-desc" :style="{ color: bt.color }">点击建造</span>
              </div>
              <span class="build-arrow" :style="{ color: bt.color }">→</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Operator Panel -->
    <Teleport to="body">
      <OperatorPanel
        v-if="showOperatorPanel && selectedRoom"
        :room="selectedRoom"
        @assign="assignOperator"
        @remove="removeOperator"
        @close="closeOperatorPanel"
      />
    </Teleport>
  </div>
</template>

<style scoped>
.riic-layout {
  display: flex;
  align-items: stretch;
  gap: 6px;
  position: relative;
}

/* Left Wing: 3 rows with staggered cards */
.left-wing {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-top: calc(78px + 6px); /* offset top by 1 card */
}

.left-row {
  display: flex;
  gap: 6px;
}

/* Row 1: normal */
.left-row-1 {
  margin-left: calc(78px / 3 + 2px);
}

/* Row 2: stagger - shift left by 1/3 card */
.left-row-2 {
}

/* Row 3: stagger more - shift left by 2/3 card */
.left-row-3 {
  margin-left: calc(78px / 3 + 2px);
}

/* Corridor */
.corridor-wrapper {
  display: flex;
  align-items: stretch;
  min-width: 36px;
}

.corridor-card {
  width: 36px;
  background: #1a1a1a;
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.corridor-card:hover {
  background: #242424;
  border-color: rgba(255, 255, 255, 0.08);
}

.corridor-icon {
  font-size: 14px;
  animation: run-cycle 1.5s steps(2) infinite;
}

@keyframes run-cycle {
  0% { transform: translateX(-1px); }
  100% { transform: translateX(1px); }
}

.corridor-label {
  font-family: var(--font-mono);
  font-size: 8px;
  color: #4a4a4a;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  writing-mode: vertical-rl;
  text-orientation: mixed;
}

/* Core Grid: Fixed width, 1 column */
.core-grid {
  width: 220px;
  min-width: 220px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* Right Wing: 1 column, offset down by 1 card */
.right-wing {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-top: calc(78px + 6px); /* offset by 1 card + gap */
  width: 140px;
  min-width: 140px;
}

/* Room Card Base */
.room-card {
  position: relative;
  background: linear-gradient(135deg, #1e1e1e, #2a2a2a);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  min-height: 72px;
  min-width: 130px;
  width: 100%;
}

.room-card:hover {
  border-color: rgba(255, 255, 255, 0.2);
  background: linear-gradient(135deg, #242424, #303030);
}

.room-card.built:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.accent-bar {
  width: 3px;
  flex-shrink: 0;
  border-radius: 3px 0 0 3px;
}

.room-content {
  flex: 1;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 2px;
  min-width: 0;
}

.room-header {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.room-name {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: #d1d5db;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.room-subname {
  font-size: 10px;
  color: #6b7280;
}

.room-status {
  display: flex;
  align-items: center;
  gap: 4px;
}

.status-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.status-text {
  font-size: 10px;
  color: #9ca3af;
}

.room-operators {
  display: flex;
  align-items: center;
  font-size: 12px;
}

/* Control Center */
.control-card {
  border-color: rgba(249, 115, 22, 0.2);
  background: linear-gradient(135deg, #1e1e1e, #2a1f1a) !important;
}

.control-card:hover {
  border-color: rgba(249, 115, 22, 0.4) !important;
  background: linear-gradient(135deg, #242424, #33251e) !important;
}

.control-version {
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 700;
  color: #f97316;
  letter-spacing: 2px;
  text-shadow: 0 0 10px rgba(249, 115, 22, 0.3);
}

/* Level Badge */
.level-badge {
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.08);
  color: #9ca3af;
}

.level-badge.level-trade { color: var(--color-trade-light); background: rgba(59, 130, 246, 0.15); }
.level-badge.level-manufacturing { color: var(--color-manufacturing-light); background: rgba(234, 179, 8, 0.15); }
.level-badge.level-power { color: var(--color-power-light); background: rgba(34, 197, 94, 0.15); }
.level-badge.level-control { color: var(--color-control-light); background: rgba(249, 115, 22, 0.15); }
.level-badge.level-dormitory { color: var(--color-dormitory-light); background: rgba(139, 92, 246, 0.15); }
.level-badge.level-meeting { color: var(--color-meeting-light); background: rgba(236, 72, 153, 0.15); }
.level-badge.level-workshop { color: var(--color-workshop-light); background: rgba(20, 184, 166, 0.15); }
.level-badge.level-office { color: var(--color-office-light); background: rgba(99, 102, 241, 0.15); }
.level-badge.level-training { color: var(--color-training-light); background: rgba(239, 68, 68, 0.15); }

.room-subname-row {
  margin-top: -2px;
}

/* Empty Slot */
.empty-card {
  background: transparent !important;
  border-color: rgba(255, 255, 255, 0.04);
}

.empty-slot {
  width: 100%;
  height: 100%;
  min-height: 72px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px;
}

.empty-slot.build-mode-active {
  border: 1.5px dashed rgba(255, 255, 255, 0.15);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.empty-slot.build-mode-active:hover {
  border-color: rgba(255, 255, 255, 0.35);
  background: rgba(255, 255, 255, 0.03);
}

.empty-plus {
  font-size: 20px;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.25);
  line-height: 1;
  font-family: var(--font-mono);
}

.empty-label {
  font-family: var(--font-mono);
  font-size: 9px;
  color: #6b7280;
  letter-spacing: 1px;
  text-transform: uppercase;
}

/* Accent color borders on hover */
.accent-trade:hover { border-color: rgba(59, 130, 246, 0.3); }
.accent-manufacturing:hover { border-color: rgba(234, 179, 8, 0.3); }
.accent-power:hover { border-color: rgba(34, 197, 94, 0.3); }
.accent-control:hover { border-color: rgba(249, 115, 22, 0.3); }
.accent-dormitory:hover { border-color: rgba(139, 92, 246, 0.3); }
.accent-meeting:hover { border-color: rgba(236, 72, 153, 0.3); }
.accent-workshop:hover { border-color: rgba(20, 184, 166, 0.3); }
.accent-office:hover { border-color: rgba(99, 102, 241, 0.3); }
.accent-training:hover { border-color: rgba(239, 68, 68, 0.3); }

/* Build Menu */
.build-menu {
  background: #1a1a1a;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  width: 320px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.build-menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.build-menu-body {
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.build-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 8px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.06);
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  text-align: left;
}

.build-option:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: var(--accent, rgba(255, 255, 255, 0.15));
}

.build-option-icon {
  font-size: 22px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
}

.build-option-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.build-option-name {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 600;
  color: #d1d5db;
}

.build-option-desc {
  font-size: 11px;
  opacity: 0.8;
}

.build-arrow {
  font-size: 18px;
  font-family: var(--font-mono);
  transition: transform 0.2s ease;
}

.build-option:hover .build-arrow {
  transform: translateX(3px);
}

/* Responsive */
@media (max-width: 900px) {
  .riic-layout {
    flex-direction: column;
    align-items: center;
  }
  .left-wing {
    width: 100%;
    justify-content: center;
  }
  .core-grid {
    width: 100%;
    max-width: 300px;
  }
  .right-wing {
    width: 100%;
    max-width: 300px;
  }
}
</style>