<script setup>
import { ref, reactive, computed } from 'vue'
import OperatorPanel from './OperatorPanel.vue'
import operatorsData from '../data/operators_with_skills.json'

const buildMode = ref(false)
const overviewMode = ref(false)
const selectedRoom = ref(null)
const showBuildMenu = ref(null)
const showEditMenu = ref(null)
const showOperatorPanel = ref(false)
const selectedOperators = ref([]) // For batch operations

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

// Load operators from JSON file (filter out unobtainable ones)
const allOperators = Object.values(operatorsData)
  .flat()
  .filter(op => !op.isNotObtainable)
  .map(op => ({
    name: op.name,
    rarity: op.rarity,
    rarityLabel: op.rarity_label,
    profession: op.profession_label,
    elite: 0,
    level: 1,
  }))

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

// Core: 4 dormitories + 1 control center
const coreRooms = reactive([
  { id: 'core-0', type: 'control', subtype: '控制中枢', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-1', type: 'dormitory', subtype: '宿舍 001', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-2', type: 'dormitory', subtype: '宿舍 002', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-3', type: 'dormitory', subtype: '宿舍 003', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-4', type: 'dormitory', subtype: '宿舍 004', level: 5, operators: [], built: true, span: 1 },
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
    if (!room.built || room.type === 'empty') {
      showBuildMenu.value = room
      showEditMenu.value = null
    } else {
      // All built rooms can be edited (level + demolish)
      showEditMenu.value = room
      showBuildMenu.value = null
    }
    return
  }
  if (room.built && room.type !== 'corridor' && room.type !== 'empty') {
    selectedRoom.value = room
    showOperatorPanel.value = true
  }
}

// Check if room belongs to left wing
const isLeftWingRoom = (room) => {
  return leftWingRooms.includes(room)
}

// Check if room type can be changed (only left wing)
const canChangeType = (room) => {
  return isLeftWingRoom(room)
}

// Get max level for room type
const getMaxLevel = (room) => {
  if (room.type === 'control') return 6
  if (room.type === 'dormitory') return 5
  return 3
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

// Edit menu functions
const closeEditMenu = () => {
  showEditMenu.value = null
}

const changeRoomType = (room, newType) => {
  const typeNames = {
    trade: '贸易站',
    manufacturing: '制造站',
    power: '发电站',
  }
  room.type = newType
  room.subtype = typeNames[newType] || newType
  room.level = 3
  room.operators = []
}

const changeRoomLevel = (room, newLevel) => {
  room.level = newLevel
}

const demolishRoom = (room) => {
  room.type = 'empty'
  room.subtype = ''
  room.level = 0
  room.operators = []
  room.built = false
  showEditMenu.value = null
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

// Power system
const powerByLevel = { 1: 60, 2: 130, 3: 270 }

// Power consumption by room type and level
const powerConsumptionByLevel = {
  control: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 },
  dormitory: { 1: -10, 2: -20, 3: -30, 4: -45, 5: -65 },
  trade: { 1: -10, 2: -30, 3: -60 },
  manufacturing: { 1: -10, 2: -30, 3: -60 },
  power: { 1: 0, 2: 0, 3: 0 }, // Power stations don't consume
  meeting: { 1: -10, 2: -30, 3: -60 },
  workshop: { 1: -10, 2: -10, 3: -10 },
  office: { 1: -10, 2: -10, 3: -10 },
  training: { 1: -10, 2: -30, 3: -60 },
  corridor: { 1: 0 },
  empty: { 1: 0 },
}

const showPowerDetail = ref(false)

const getPowerGeneration = (room) => {
  if (room.type !== 'power' || !room.built) return 0
  return powerByLevel[room.level] || 0
}

const getPowerConsumption = (room) => {
  if (!room.built || room.type === 'empty' || room.type === 'corridor') return 0
  const levelMap = powerConsumptionByLevel[room.type]
  if (!levelMap) return 0
  // Use room level, or the highest available level if room.level exceeds
  const level = Math.min(room.level || 1, Object.keys(levelMap).length)
  return levelMap[level] || 0
}

const totalPowerGeneration = computed(() => {
  let total = 0
  leftWingRooms.forEach(room => { total += getPowerGeneration(room) })
  coreRooms.forEach(room => { total += getPowerGeneration(room) })
  rightWingRooms.forEach(room => { total += getPowerGeneration(room) })
  return total
})

const totalPowerConsumption = computed(() => {
  let total = 0
  leftWingRooms.forEach(room => { total += getPowerConsumption(room) })
  coreRooms.forEach(room => { total += getPowerConsumption(room) })
  rightWingRooms.forEach(room => { total += getPowerConsumption(room) })
  return Math.abs(total)
})

const netPower = computed(() => {
  return totalPowerGeneration.value - totalPowerConsumption.value
})

// Get all rooms with their power info for detail view
const getPowerDetailRooms = () => {
  const allRooms = [...leftWingRooms, ...coreRooms, ...rightWingRooms]
  return allRooms.filter(room => room.built && room.type !== 'empty' && room.type !== 'corridor')
    .map(room => ({
      ...room,
      generation: getPowerGeneration(room),
      consumption: getPowerConsumption(room),
    }))
}

// Drone system
const droneCapacity = 235
const baseDronePerDay = 240 // 1 drone per 6 minutes = 240/day
const baseChargingSpeed = 1 // 1 drone / 6 minutes

// Calculate drone bonus from power station operators
const getDroneBonus = (room) => {
  if (room.type !== 'power' || !room.built || room.operators.length === 0) return 0
  // Base work bonus is always 5%
  let bonus = 0.05
  // Add operator-specific bonuses based on their skills
  room.operators.forEach(op => {
    // These would be looked up from operator skills data
    // Simplified: check if operator has drone-related skill
    const allOps = Object.values(operatorsData).flat()
    const opData = allOps.find(o => o.name === op.name)
    if (opData?.skills) {
      opData.skills.forEach(skill => {
        if (skill.room === '发电站' && skill.description.includes('充能')) {
          // Extract percentage from description like "+20%"
          const match = skill.description.match(/\+(\d+)%/)
          if (match) {
            bonus += parseInt(match[1]) / 100
          }
        }
      })
    }
  })
  return bonus
}

const totalDroneBonus = computed(() => {
  let bonus = 0
  leftWingRooms.forEach(room => { bonus += getDroneBonus(room) })
  coreRooms.forEach(room => { bonus += getDroneBonus(room) })
  rightWingRooms.forEach(room => { bonus += getDroneBonus(room) })
  return bonus
})

const dailyDroneProduction = computed(() => {
  return Math.floor(baseDronePerDay * (1 + totalDroneBonus.value))
})

// Overview mode functions
const getAllRoomsGrouped = () => {
  const allRooms = [...leftWingRooms, ...coreRooms, ...rightWingRooms]
  const builtRooms = allRooms.filter(room => room.built && room.type !== 'corridor' && room.type !== 'empty')

  // Group by type
  const grouped = {}
  builtRooms.forEach(room => {
    if (!grouped[room.type]) {
      grouped[room.type] = []
    }
    grouped[room.type].push(room)
  })

  return grouped
}

const getEmptySlots = (room) => {
  const max = maxOperators(room)
  const current = operatorCount(room)
  return max - current
}

const batchAssignMode = ref(false)
const batchAssignRoom = ref(null)
const selectedOperatorDetail = ref(null)

const toggleOperatorSelection = (operator, roomId) => {
  const key = `${roomId}-${operator.name}`
  const idx = selectedOperators.value.indexOf(key)
  if (idx > -1) {
    selectedOperators.value.splice(idx, 1)
  } else {
    // Check if we can add more (limit by available slots)
    const roomIdOnly = roomId.replace('-batch', '')
    const room = [...leftWingRooms, ...coreRooms, ...rightWingRooms].find(r => r.id === roomIdOnly)
    if (room) {
      const emptySlots = getEmptySlots(room)
      const currentSelected = selectedOperators.value.filter(k => k.startsWith(roomId + '-')).length
      if (currentSelected >= emptySlots) {
        return // Don't add more if at capacity
      }
    }
    selectedOperators.value.push(key)
  }
}

const isOperatorSelected = (operator, roomId) => {
  return selectedOperators.value.includes(`${roomId}-${operator.name}`)
}

const showOperatorSkills = (operator) => {
  selectedOperatorDetail.value = operator
}

const hideOperatorSkills = () => {
  selectedOperatorDetail.value = null
}

const getOperatorSkills = (operatorName) => {
  const allOps = Object.values(operatorsData).flat()
  const op = allOps.find(o => o.name === operatorName)
  return op?.skills || []
}

// Map skill room name to room type
const getRoomTypeFromSkill = (roomName) => {
  const roomMap = {
    '发电站': 'power',
    '制造站': 'manufacturing',
    '贸易站': 'trade',
    '宿舍': 'dormitory',
    '控制中枢': 'control',
    '加工站': 'workshop',
    '办公室': 'office',
    '训练室': 'training',
    '会客室': 'meeting',
  }
  return roomMap[roomName] || 'empty'
}

const startBatchAssign = (room) => {
  batchAssignRoom.value = room
  batchAssignMode.value = true
  selectedOperatorDetail.value = null
}

const confirmBatchAssign = (operators) => {
  if (!batchAssignRoom.value) return
  const max = maxOperators(batchAssignRoom.value)
  const current = operatorCount(batchAssignRoom.value)
  const available = max - current

  operators.slice(0, available).forEach(op => {
    batchAssignRoom.value.operators.push({ ...op })
  })

  batchAssignMode.value = false
  batchAssignRoom.value = null
}

const cancelBatchAssign = () => {
  batchAssignMode.value = false
  batchAssignRoom.value = null
}

const removeSelectedOperators = () => {
  const allRooms = [...leftWingRooms, ...coreRooms, ...rightWingRooms]
  selectedOperators.value.forEach(key => {
    const [roomId, ...nameParts] = key.split('-')
    const operatorName = nameParts.join('-')
    const room = allRooms.find(r => r.id === roomId)
    if (room) {
      const opIndex = room.operators.findIndex(op => op.name === operatorName)
      if (opIndex > -1) {
        room.operators.splice(opIndex, 1)
      }
    }
  })
  selectedOperators.value = []
}

const clearSelection = () => {
  selectedOperators.value = []
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
        <button
          class="text-xs px-3 py-1.5 rounded font-mono transition-colors cursor-pointer"
          :class="overviewMode ? 'bg-dormitory/20 text-dormitory-light border border-dormitory/30' : 'bg-base-600/50 text-base-300 border border-base-500/30 hover:bg-base-600'"
          @click="overviewMode = !overviewMode"
        >
          进驻总览
        </button>
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
        <div class="h-4 w-px bg-base-700"></div>
        <!-- Power & Drone Stats -->
        <div class="flex items-center gap-4 px-3 py-1 bg-base-800/50 rounded">
          <div
            class="flex items-center gap-1.5 cursor-pointer hover:bg-base-700/50 px-2 py-1 rounded transition-colors"
            @click="showPowerDetail = !showPowerDetail"
          >
            <span class="text-power-light text-sm">⚡</span>
            <span class="text-xs font-mono" :class="netPower >= 0 ? 'text-power-light' : 'text-red-400'">
              {{ totalPowerConsumption }}/{{ totalPowerGeneration }}
            </span>
            <span class="text-xs text-base-500">电力</span>
          </div>
          <div class="h-3 w-px bg-base-700"></div>
          <div class="flex items-center gap-1.5">
            <span class="text-control-light text-sm">🤖</span>
            <span class="text-xs font-mono text-base-300">{{ dailyDroneProduction }}</span>
            <span class="text-xs text-base-500">/天</span>
            <span class="text-xs text-base-600">({{ droneCapacity }})</span>
          </div>
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
                  <span
                    v-if="showPowerDetail && (getPowerGeneration(room) > 0 || getPowerConsumption(room) < 0)"
                    class="power-badge"
                    :class="getPowerGeneration(room) > 0 ? 'power-gen' : 'power-cons'"
                  >
                    {{ getPowerGeneration(room) > 0 ? '+' : '' }}{{ getPowerGeneration(room) || getPowerConsumption(room) }}
                  </span>
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
                  <span
                    v-if="showPowerDetail && (getPowerGeneration(room) > 0 || getPowerConsumption(room) < 0)"
                    class="power-badge"
                    :class="getPowerGeneration(room) > 0 ? 'power-gen' : 'power-cons'"
                  >
                    {{ getPowerGeneration(room) > 0 ? '+' : '' }}{{ getPowerGeneration(room) || getPowerConsumption(room) }}
                  </span>
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
                  <span
                    v-if="showPowerDetail && (getPowerGeneration(room) > 0 || getPowerConsumption(room) < 0)"
                    class="power-badge"
                    :class="getPowerGeneration(room) > 0 ? 'power-gen' : 'power-cons'"
                  >
                    {{ getPowerGeneration(room) > 0 ? '+' : '' }}{{ getPowerGeneration(room) || getPowerConsumption(room) }}
                  </span>
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
                <span
                  v-if="showPowerDetail && (getPowerGeneration(coreRooms[0]) > 0 || getPowerConsumption(coreRooms[0]) < 0)"
                  class="power-badge"
                  :class="getPowerGeneration(coreRooms[0]) > 0 ? 'power-gen' : 'power-cons'"
                >
                  {{ getPowerGeneration(coreRooms[0]) > 0 ? '+' : '' }}{{ getPowerGeneration(coreRooms[0]) || getPowerConsumption(coreRooms[0]) }}
                </span>
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
                  <span
                    v-if="showPowerDetail && (getPowerGeneration(room) > 0 || getPowerConsumption(room) < 0)"
                    class="power-badge"
                    :class="getPowerGeneration(room) > 0 ? 'power-gen' : 'power-cons'"
                  >
                    {{ getPowerGeneration(room) > 0 ? '+' : '' }}{{ getPowerGeneration(room) || getPowerConsumption(room) }}
                  </span>
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
                <span
                  v-if="showPowerDetail && (getPowerGeneration(room) > 0 || getPowerConsumption(room) < 0)"
                  class="power-badge"
                  :class="getPowerGeneration(room) > 0 ? 'power-gen' : 'power-cons'"
                >
                  {{ getPowerGeneration(room) > 0 ? '+' : '' }}{{ getPowerGeneration(room) || getPowerConsumption(room) }}
                </span>
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

    <!-- Edit Room Menu (Build Mode) -->
    <Teleport to="body">
      <div v-if="showEditMenu" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm" @click.self="closeEditMenu">
        <div class="build-menu">
          <div class="build-menu-header">
            <span class="text-base-200 font-mono text-sm">编辑房间</span>
            <button class="text-base-500 hover:text-base-200 transition-colors text-lg leading-none cursor-pointer" @click="closeEditMenu">&times;</button>
          </div>
          <div class="build-menu-body">
            <!-- Room Type Selection (only for left wing) -->
            <div v-if="isLeftWingRoom(showEditMenu)" class="edit-section">
              <span class="edit-label">房间类型</span>
              <div class="type-buttons">
                <button
                  v-for="bt in buildableTypes"
                  :key="bt.type"
                  class="type-btn"
                  :class="{ active: showEditMenu.type === bt.type }"
                  :style="{ '--accent': bt.color }"
                  @click="changeRoomType(showEditMenu, bt.type)"
                >
                  <span class="type-btn-icon">{{ bt.icon }}</span>
                  <span>{{ bt.label }}</span>
                </button>
              </div>
            </div>

            <!-- Level Adjustment -->
            <div class="edit-section">
              <span class="edit-label">房间等级</span>
              <div class="level-buttons">
                <button
                  v-for="lv in (showEditMenu.type === 'dormitory' ? 5 : showEditMenu.type === 'control' ? 6 : 3)"
                  :key="lv"
                  class="level-btn"
                  :class="{ active: showEditMenu.level === lv }"
                  @click="changeRoomLevel(showEditMenu, lv)"
                >
                  Lv.{{ lv }}
                </button>
              </div>
            </div>

            <!-- Demolish -->
            <div class="edit-section">
              <button class="demolish-btn" @click="demolishRoom(showEditMenu)">
                拆除房间
              </button>
            </div>
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

    <!-- Overview Mode Panel -->
    <Teleport to="body">
      <div v-if="overviewMode && !batchAssignMode" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm">
        <div class="overview-panel">
          <div class="overview-header">
            <span class="text-base-200 font-mono text-sm">进驻总览</span>
            <div class="flex items-center gap-3">
              <span v-if="selectedOperators.length > 0" class="text-xs text-dormitory-light">
                已选择 {{ selectedOperators.length }} 名干员
              </span>
              <button
                v-if="selectedOperators.length > 0"
                class="text-xs px-3 py-1 rounded bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30 cursor-pointer transition-colors"
                @click="removeSelectedOperators"
              >
                批量撤离
              </button>
              <button
                v-if="selectedOperators.length > 0"
                class="text-xs px-3 py-1 rounded bg-base-600/50 text-base-300 border border-base-500/30 hover:bg-base-600 cursor-pointer transition-colors"
                @click="clearSelection"
              >
                取消选择
              </button>
              <button class="text-base-500 hover:text-base-200 transition-colors text-lg leading-none cursor-pointer" @click="overviewMode = false">&times;</button>
            </div>
          </div>
          <div class="overview-body">
            <!-- Grouped by type -->
            <template v-for="(rooms, type) in getAllRoomsGrouped()" :key="type">
              <div class="overview-type-header">
                <span class="overview-type-label" :style="{ color: getColorVar(type) }">
                  {{ roomTypes[type]?.label }}
                </span>
                <span class="overview-type-count">{{ rooms.length }} 个设施</span>
              </div>
              <div
                v-for="room in rooms"
                :key="room.id"
                class="overview-room-row"
              >
                <div class="overview-room-info">
                  <div class="room-info-left">
                    <span class="room-info-name">{{ room.subtype }}</span>
                    <span class="level-badge" :class="`level-${room.type}`">Lv.{{ room.level }}</span>
                  </div>
                  <div class="room-info-right">
                    <span class="room-info-count">
                      <span class="text-base-400 text-xs mr-1">👤</span>
                      <span class="font-mono text-sm" :class="operatorCount(room) === maxOperators(room) ? 'text-power-light' : 'text-trade-light'">
                        {{ operatorCount(room) }}/{{ maxOperators(room) }}
                      </span>
                    </span>
                  </div>
                </div>
                <div class="overview-room-operators">
                  <!-- Existing operators -->
                  <div
                    v-for="(op, idx) in room.operators"
                    :key="idx"
                    class="overview-operator"
                    :class="{ selected: isOperatorSelected(op, room.id) }"
                    @click="toggleOperatorSelection(op, room.id)"
                  >
                    <div class="op-avatar">{{ op.name?.charAt(0) || '?' }}</div>
                    <div class="op-info">
                      <span class="op-name">{{ op.name || '干员' }}</span>
                      <span class="op-elite">精英{{ op.elite || 0 }} {{ op.level || 1 }}</span>
                    </div>
                    <div v-if="isOperatorSelected(op, room.id)" class="op-check">✓</div>
                  </div>
                  <!-- Empty slots -->
                  <div
                    v-for="slot in getEmptySlots(room)"
                    :key="'empty-' + slot"
                    class="overview-empty-slot"
                    @click="startBatchAssign(room)"
                  >
                    <span class="empty-slot-plus">+</span>
                    <span class="empty-slot-text">点击进驻</span>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Batch Assign Mode -->
      <div v-if="overviewMode && batchAssignMode" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm">
        <div class="overview-panel batch-assign-panel">
          <div class="overview-header">
            <span class="text-base-200 font-mono text-sm">批量进驻 - {{ batchAssignRoom?.subtype }}</span>
            <div class="flex items-center gap-3">
              <span class="text-xs text-base-400">
                剩余 {{ getEmptySlots(batchAssignRoom) }} 个空位
              </span>
              <button class="text-base-500 hover:text-base-200 transition-colors text-lg leading-none cursor-pointer" @click="cancelBatchAssign">&times;</button>
            </div>
          </div>
          <div class="batch-assign-content">
            <div class="batch-assign-list">
              <div
                v-for="(op, idx) in allOperators"
                :key="idx"
                class="batch-assign-operator"
                :class="{ selected: isOperatorSelected(op, batchAssignRoom?.id + '-batch') }"
                @click="toggleOperatorSelection(op, batchAssignRoom?.id + '-batch'); showOperatorSkills(op)"
              >
                <div class="op-avatar">{{ op.name?.charAt(0) || '?' }}</div>
                <div class="op-info">
                  <span class="op-name">{{ op.name }}</span>
                  <span class="op-elite">{{ op.rarityLabel }} {{ op.profession }}</span>
                </div>
                <div v-if="isOperatorSelected(op, batchAssignRoom?.id + '-batch')" class="op-check">✓</div>
              </div>
            </div>
            <!-- Skills Panel -->
            <div v-if="selectedOperatorDetail" class="skills-panel">
              <div class="skills-header">
                <span class="skills-op-name">{{ selectedOperatorDetail.name }}</span>
                <span class="skills-op-info">{{ selectedOperatorDetail.rarityLabel }} {{ selectedOperatorDetail.profession }}</span>
              </div>
              <div class="skills-list">
                <div
                  v-for="(skill, idx) in getOperatorSkills(selectedOperatorDetail.name)"
                  :key="idx"
                  class="skill-item"
                >
                  <div class="skill-name">{{ skill.skill_name }}</div>
                  <div class="skill-room" :style="{ color: getColorVar(getRoomTypeFromSkill(skill.room)) }">
                    {{ skill.room }}
                  </div>
                  <div class="skill-desc">{{ skill.description }}</div>
                </div>
                <div v-if="getOperatorSkills(selectedOperatorDetail.name).length === 0" class="no-skills">
                  暂无基建技能
                </div>
              </div>
            </div>
          </div>
          <div class="batch-assign-actions">
            <button class="cancel-btn" @click="cancelBatchAssign">取消</button>
            <button
              class="confirm-btn"
              :disabled="selectedOperators.filter(k => k.startsWith(batchAssignRoom?.id + '-batch')).length === 0"
              @click="() => {
                const ops = selectedOperators
                  .filter(k => k.startsWith(batchAssignRoom?.id + '-batch'))
                  .map(k => {
                    const name = k.replace(batchAssignRoom?.id + '-batch-', '')
                    return allOperators.find(o => o.name === name)
                  })
                  .filter(Boolean)
                confirmBatchAssign(ops)
              }"
            >
              确认进驻 ({{ selectedOperators.filter(k => k.startsWith(batchAssignRoom?.id + '-batch')).length }})
            </button>
          </div>
        </div>
      </div>
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
  padding-top: 110px; /* offset top by 1 card */
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
  padding-top: 60px; /* offset by 1 card + gap */
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
  min-width: 180px;
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

.room-power {
  margin-top: 4px;
  padding-top: 4px;
  border-top: 1px solid rgba(255, 255, 255, 0.04);
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

.power-badge {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 3px;
  margin-left: 4px;
}

.power-gen {
  color: #22c55e;
  background: rgba(34, 197, 94, 0.15);
}

.power-cons {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

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

/* Edit Menu */
.edit-section {
  padding: 8px 6px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.edit-section:last-child {
  border-bottom: none;
}

.edit-label {
  display: block;
  font-size: 10px;
  font-family: var(--font-mono);
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}

.type-buttons {
  display: flex;
  gap: 6px;
}

.type-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 10px 8px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  cursor: pointer;
  transition: all 0.2s ease;
  color: #9ca3af;
  font-size: 11px;
}

.type-btn:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: var(--accent, rgba(255, 255, 255, 0.15));
  color: #d1d5db;
}

.type-btn.active {
  background: rgba(var(--accent-rgb, 59, 130, 246), 0.15);
  border-color: var(--accent, rgba(255, 255, 255, 0.2));
  color: var(--accent, #d1d5db);
}

.type-btn-icon {
  font-size: 20px;
}

.level-buttons {
  display: flex;
  gap: 6px;
}

.level-btn {
  flex: 1;
  padding: 8px 12px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  cursor: pointer;
  transition: all 0.2s ease;
  color: #9ca3af;
  font-size: 11px;
  font-family: var(--font-mono);
}

.level-btn:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.15);
  color: #d1d5db;
}

.level-btn.active {
  background: rgba(234, 179, 8, 0.15);
  border-color: rgba(234, 179, 8, 0.4);
  color: #eab308;
}

.demolish-btn {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  cursor: pointer;
  transition: all 0.2s ease;
  color: #ef4444;
  font-size: 12px;
  font-family: var(--font-mono);
}

.demolish-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.4);
}

/* Overview Panel */
.overview-panel {
  background: #1a1a1a;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  width: 800px;
  max-width: 95vw;
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}

.overview-body {
  padding: 12px;
  overflow-y: auto;
  flex: 1;
}

.overview-type-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  margin-bottom: 4px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.overview-type-label {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.overview-type-count {
  font-size: 10px;
  color: #6b7280;
}

.overview-room-row {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  padding: 10px 12px;
  margin-bottom: 6px;
}

.overview-room-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

.room-info-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.room-info-name {
  font-size: 12px;
  color: #d1d5db;
}

.room-info-right {
  display: flex;
  align-items: center;
}

.room-info-count {
  display: flex;
  align-items: center;
}

.overview-room-operators {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.overview-operator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 8px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.overview-operator:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.overview-operator.selected {
  background: rgba(139, 92, 246, 0.15);
  border-color: rgba(139, 92, 246, 0.3);
}

.op-avatar {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  background: linear-gradient(135deg, #374151, #1f2937);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  color: #d1d5db;
}

.op-info {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.op-name {
  font-size: 11px;
  color: #d1d5db;
}

.op-elite {
  font-size: 9px;
  color: #6b7280;
  font-family: var(--font-mono);
}

.op-check {
  color: #a78bfa;
  font-size: 12px;
}

.overview-empty {
  font-size: 11px;
  color: #4b5563;
  padding: 4px 0;
}

/* Empty Slot */
.overview-empty-slot {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 90px;
}

.overview-empty-slot:hover {
  background: rgba(139, 92, 246, 0.1);
  border-color: rgba(139, 92, 246, 0.3);
  border-style: solid;
}

.empty-slot-plus {
  font-size: 14px;
  color: #6b7280;
  font-weight: 600;
}

.overview-empty-slot:hover .empty-slot-plus {
  color: #a78bfa;
}

.empty-slot-text {
  font-size: 10px;
  color: #6b7280;
}

.overview-empty-slot:hover .empty-slot-text {
  color: #a78bfa;
}

/* Batch Assign */
.batch-assign-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 8px;
  margin-bottom: 16px;
  max-height: 400px;
  overflow-y: auto;
}

.batch-assign-panel {
  width: 1000px;
}

.batch-assign-content {
  display: flex;
  gap: 16px;
  padding: 12px;
  flex: 1;
  overflow: hidden;
}

.batch-assign-list {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 8px;
  max-height: 400px;
  overflow-y: auto;
  align-content: start;
}

.batch-assign-operator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.batch-assign-operator:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.batch-assign-operator.selected {
  background: rgba(139, 92, 246, 0.15);
  border-color: rgba(139, 92, 246, 0.3);
}

.batch-assign-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.cancel-btn {
  padding: 8px 20px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.2s ease;
  color: #9ca3af;
  font-size: 12px;
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #d1d5db;
}

.confirm-btn {
  padding: 8px 20px;
  border-radius: 6px;
  background: rgba(139, 92, 246, 0.2);
  border: 1px solid rgba(139, 92, 246, 0.3);
  cursor: pointer;
  transition: all 0.2s ease;
  color: #a78bfa;
  font-size: 12px;
}

.confirm-btn:hover:not(:disabled) {
  background: rgba(139, 92, 246, 0.3);
}

.confirm-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Skills Panel */
.skills-panel {
  width: 280px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 12px;
  max-height: 400px;
  overflow-y: auto;
}

.skills-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.skills-op-name {
  font-size: 14px;
  font-weight: 600;
  color: #d1d5db;
}

.skills-op-info {
  font-size: 11px;
  color: #6b7280;
}

.skills-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skill-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 6px;
  padding: 10px;
}

.skill-name {
  font-size: 12px;
  font-weight: 600;
  color: #d1d5db;
  margin-bottom: 4px;
}

.skill-room {
  font-size: 10px;
  font-family: var(--font-mono);
  text-transform: uppercase;
  margin-bottom: 6px;
}

.skill-desc {
  font-size: 11px;
  color: #9ca3af;
  line-height: 1.4;
}

.no-skills {
  font-size: 12px;
  color: #6b7280;
  text-align: center;
  padding: 20px;
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