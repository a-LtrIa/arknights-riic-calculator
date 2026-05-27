<script setup>
import { ref, reactive, computed, watch } from 'vue'
import OperatorPanel from './OperatorPanel.vue'
import operatorsData from '../data/operators_with_skills.json'

const buildMode = ref(false)
const overviewMode = ref(false)
const selectedRoom = ref(null)
const showBuildMenu = ref(null)
const showEditMenu = ref(null)
const showOperatorPanel = ref(false)
const selectedOperators = ref([])

const STORAGE_KEY = 'riic-config'

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

const leftWingRooms = reactive([
  { id: 'left-0', type: 'trade', subtype: '贸易站 001', level: 3, operators: [], built: true, negotiationStrategy: '龙门商法' },
  { id: 'left-1', type: 'manufacturing', subtype: '制造站 001', level: 3, operators: [], built: true },
  { id: 'left-2', type: 'power', subtype: '发电站 001', level: 3, operators: [], built: true },
  { id: 'left-3', type: 'trade', subtype: '贸易站 002', level: 3, operators: [], built: true, negotiationStrategy: '龙门商法' },
  { id: 'left-4', type: 'manufacturing', subtype: '制造站 002', level: 3, operators: [], built: true },
  { id: 'left-5', type: 'power', subtype: '发电站 002', level: 3, operators: [], built: true },
  { id: 'left-6', type: 'trade', subtype: '贸易站 003', level: 3, operators: [], built: true, negotiationStrategy: '龙门商法' },
  { id: 'left-7', type: 'manufacturing', subtype: '制造站 003', level: 3, operators: [], built: true },
  { id: 'left-8', type: 'power', subtype: '发电站 003', level: 3, operators: [], built: true },
])

const rightWingRooms = reactive([
  { id: 'right-0', type: 'meeting', subtype: '会客室', level: 3, operators: [], built: true },
  { id: 'right-1', type: 'workshop', subtype: '加工站', level: 3, operators: [], built: true },
  { id: 'right-2', type: 'office', subtype: '办公室', level: 3, operators: [], built: true },
  { id: 'right-3', type: 'training', subtype: '训练室', level: 3, operators: [], built: true },
])

const coreRooms = reactive([
  { id: 'core-0', type: 'control', subtype: '控制中枢', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-1', type: 'dormitory', subtype: '宿舍 001', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-2', type: 'dormitory', subtype: '宿舍 002', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-3', type: 'dormitory', subtype: '宿舍 003', level: 5, operators: [], built: true, span: 1 },
  { id: 'core-4', type: 'dormitory', subtype: '宿舍 004', level: 5, operators: [], built: true, span: 1 },
])

const leftCorridor = reactive({ id: 'corridor-left', type: 'corridor', subtype: '走廊', level: 0, operators: [], built: true })
const rightCorridor = reactive({ id: 'corridor-right', type: 'corridor', subtype: '走廊', level: 0, operators: [], built: true })

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

const saveConfig = () => {
  const config = {
    leftWing: leftWingRooms.map(r => ({ ...r })),
    rightWing: rightWingRooms.map(r => ({ ...r })),
    core: coreRooms.map(r => ({ ...r })),
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(config))
}

const loadConfig = () => {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    try {
      const config = JSON.parse(saved)
      if (config.leftWing) {
        config.leftWing.forEach((savedRoom, idx) => {
          if (leftWingRooms[idx]) {
            Object.assign(leftWingRooms[idx], savedRoom)
          }
        })
      }
      if (config.rightWing) {
        config.rightWing.forEach((savedRoom, idx) => {
          if (rightWingRooms[idx]) {
            Object.assign(rightWingRooms[idx], savedRoom)
          }
        })
      }
      if (config.core) {
        config.core.forEach((savedRoom, idx) => {
          if (coreRooms[idx]) {
            Object.assign(coreRooms[idx], savedRoom)
          }
        })
      }
    } catch (e) {
      console.error('Failed to load config:', e)
    }
  }
}

loadConfig()

watch([leftWingRooms, rightWingRooms, coreRooms], () => {
  saveConfig()
}, { deep: true })

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

const getOpNumClass = (room) => {
  if (operatorCount(room) === maxOperators(room) && maxOperators(room) > 0) {
    const colorMap = {
      trade: 'text-trade',
      manufacturing: 'text-manufacturing',
      power: 'text-power',
      control: 'text-control',
      dormitory: 'text-dormitory',
      meeting: 'text-meeting',
      workshop: 'text-workshop',
      office: 'text-office',
      training: 'text-training',
    }
    return colorMap[room.type] || ''
  }
  return ''
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
  console.log('Room clicked:', room.id, room.subtype, 'type:', room.type)
  if (buildMode.value) {
    if (!room.built || room.type === 'empty') {
      showBuildMenu.value = room
      showEditMenu.value = null
    } else {
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

const isLeftWingRoom = (room) => {
  return leftWingRooms.includes(room)
}

const canChangeType = (room) => {
  return isLeftWingRoom(room)
}

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

const powerByLevel = { 1: 60, 2: 130, 3: 270 }

const powerConsumptionByLevel = {
  control: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 },
  dormitory: { 1: -10, 2: -20, 3: -30, 4: -45, 5: -65 },
  trade: { 1: -10, 2: -30, 3: -60 },
  manufacturing: { 1: -10, 2: -30, 3: -60 },
  power: { 1: 0, 2: 0, 3: 0 },
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

const getPowerDetailRooms = () => {
  const allRooms = [...leftWingRooms, ...coreRooms, ...rightWingRooms]
  return allRooms.filter(room => room.built && room.type !== 'empty' && room.type !== 'corridor')
    .map(room => ({
      ...room,
      generation: getPowerGeneration(room),
      consumption: getPowerConsumption(room),
    }))
}

const droneCapacity = 235
const baseDronePerDay = 240
const baseChargingSpeed = 1

const getDroneBonus = (room) => {
  if (room.type !== 'power' || !room.built || room.operators.length === 0) return 0
  let bonus = 0.05
  room.operators.forEach(op => {
    const allOps = Object.values(operatorsData).flat()
    const opData = allOps.find(o => o.name === op.name)
    if (opData?.skills) {
      opData.skills.forEach(skill => {
        if (skill.room === '发电站' && skill.description.includes('充能')) {
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

const getAllRoomsGrouped = () => {
  const allRooms = [...leftWingRooms, ...coreRooms, ...rightWingRooms]
  const builtRooms = allRooms.filter(room => room.built && room.type !== 'corridor' && room.type !== 'empty')
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
    const roomIdOnly = roomId.replace('-batch', '')
    const room = [...leftWingRooms, ...coreRooms, ...rightWingRooms].find(r => r.id === roomIdOnly)
    if (room) {
      const emptySlots = getEmptySlots(room)
      const currentSelected = selectedOperators.value.filter(k => k.startsWith(roomId + '-')).length
      if (currentSelected >= emptySlots) {
        return
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

const generateConfig = () => {
  const config = {}
  leftWingRooms.forEach((room, idx) => {
    if (room.built && room.type !== 'empty') {
      const name = room.subtype || `Left-${idx}`
      config[name] = {
        "类型": roomTypes[room.type]?.label || room.type,
        "等级": room.level,
        "进驻干员": room.operators.map(op => ({
          "名称": op.name,
          "精英等级": op.elite || 0
        }))
      }
      if (room.type === 'manufacturing') {
        config[name]["产物"] = "作战记录"
      } else if (room.type === 'trade') {
        config[name]["产物"] = "龙门币"
        config[name]["谈判策略"] = room.negotiationStrategy || "龙门商法"
      } else if (room.type === 'power') {
        config[name]["产物"] = "无人机"
      }
    }
  })
  rightWingRooms.forEach((room, idx) => {
    if (room.built && room.type !== 'empty') {
      const name = room.subtype || `Right-${idx}`
      config[name] = {
        "类型": roomTypes[room.type]?.label || room.type,
        "等级": room.level,
        "进驻干员": room.operators.map(op => ({
          "名称": op.name,
          "精英等级": op.elite || 0
        }))
      }
    }
  })
  coreRooms.forEach((room, idx) => {
    if (room.built && room.type !== 'empty') {
      const name = room.subtype || `Core-${idx}`
      config[name] = {
        "类型": roomTypes[room.type]?.label || room.type,
        "等级": room.level,
        "进驻干员": room.operators.map(op => ({
          "名称": op.name,
          "精英等级": op.elite || 0
        }))
      }
    }
  })
  return config
}

const calculationResult = ref(null)

const calculateEfficiency = async () => {
  const config = generateConfig()
  console.log('Sending config:', config)
  try {
    const response = await fetch('http://localhost:8000/api/calculator/calculator/calculate/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config)
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const result = await response.json()
    console.log('Calculation result:', result)
    calculationResult.value = result.data
  } catch (error) {
    console.error('Calculation error:', error)
    alert('计算失败: ' + error.message)
  }
}

const getOperatorSkills = (operatorName) => {
  const allOps = Object.values(operatorsData).flat()
  const op = allOps.find(o => o.name === operatorName)
  return op?.skills || []
}

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
  <div class="min-h-screen text-base-200 font-sans select-none">
    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 z-50 h-14 bg-[#e5e0d8] border-b border-black/10 flex items-center justify-between px-6">
      <div class="flex items-center gap-4">
        <span class="text-base-800 text-sm font-mono tracking-[0.2em]">ARKNIGHTS RIIC</span>
        <span class="text-base-400">|</span>
        <span class="text-base-500 text-xs font-mono tracking-wider">INFRASTRUCTURE MANAGEMENT SYSTEM</span>
      </div>
      <div class="flex items-center gap-4">
        <span class="text-[10px] text-base-500 font-mono tracking-[0.15em] border border-black/20 px-2 py-0.5">VER 2.0.1</span>
        <div class="h-4 w-px bg-black/15"></div>
        <button
          class="text-[10px] px-3 py-1.5 font-mono tracking-wider transition-colors cursor-pointer border"
          :class="overviewMode ? 'bg-dormitory/20 text-dormitory-dark border-dormitory/40' : 'bg-white/60 text-base-600 border-black/15 hover:text-base-800 hover:border-black/30'"
          @click="overviewMode = !overviewMode"
        >
          进驻总览
        </button>
        <button
          class="text-[10px] px-3 py-1.5 font-mono tracking-wider transition-colors border cursor-pointer"
          :class="calculationResult ? 'bg-power/20 text-power-dark border-power/40' : 'bg-white/60 text-base-600 border-black/15 hover:text-manufacturing-dark hover:border-manufacturing/40'"
          @click="calculateEfficiency"
        >
          计算效率
        </button>
        <div class="h-4 w-px bg-black/15"></div>
        <div class="flex items-center gap-2">
          <span class="text-[10px] font-mono tracking-wider text-base-500" :class="{ 'text-control-dark': buildMode }">建造模式</span>
          <button
            class="relative w-[38px] h-[20px] rounded-full transition-all duration-300 cursor-pointer border"
            :class="buildMode ? 'bg-control/30 border-control/50' : 'bg-black/10 border-black/20'"
            @click="buildMode = !buildMode"
          >
            <span
              class="absolute top-[2px] w-[14px] h-[14px] rounded-full shadow-md transition-all duration-300"
              :class="buildMode ? 'left-[20px] bg-control-dark' : 'left-[2px] bg-base-400'"
            ></span>
          </button>
        </div>
        <div class="h-4 w-px bg-black/15"></div>
        <div class="flex items-center gap-3 px-3 py-1 bg-white/60 border border-black/10 rounded-sm">
          <div
            class="flex items-center gap-1.5 cursor-pointer hover:bg-black/5 px-1.5 py-0.5 rounded-sm transition-colors"
            @click="showPowerDetail = !showPowerDetail"
          >
            <span class="text-[10px] text-power-dark font-mono">⚡</span>
            <span class="text-[11px] font-mono" :class="netPower >= 0 ? 'text-power-dark' : 'text-red-600'">
              {{ totalPowerConsumption }}/{{ totalPowerGeneration }}
            </span>
            <span class="text-[9px] text-base-500 font-mono">电力</span>
          </div>
          <div class="h-3 w-px bg-black/10"></div>
          <div class="flex items-center gap-1.5 px-1.5 py-0.5">
            <span class="text-[10px] text-control-dark font-mono">🤖</span>
            <span class="text-[11px] font-mono text-base-700">{{ dailyDroneProduction }}</span>
            <span class="text-[9px] text-base-500 font-mono">/天</span>
            <span class="text-[9px] text-base-400 font-mono">({{ droneCapacity }})</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Decorative separator line -->
    <div class="fixed top-14 left-0 right-0 z-40 flex items-center px-6 py-0.5 bg-[#e5e0d8]/90">
      <div class="flex-1 h-px bg-gradient-to-r from-transparent via-black/20 to-transparent"></div>
      <span class="mx-4 text-[8px] font-mono tracking-[0.3em] text-base-500">INFRA07 :: RHODES ISLAND :: RIIC SECTOR 7</span>
      <div class="flex-1 h-px bg-gradient-to-r from-transparent via-black/20 to-transparent"></div>
    </div>

    <!-- Main Layout -->
    <div class="pt-[72px] min-h-screen flex items-start justify-center p-6">
      <div class="bg-dark-pattern rounded-sm p-5">
        <div class="riic-layout">
          <!-- Left Wing -->
          <div class="left-wing">
            <div class="left-row left-row-1">
              <div
                v-for="room in [leftWingRooms[0], leftWingRooms[1], leftWingRooms[2]]"
                :key="room.id"
                class="room-card"
                :class="[getColorClass(room.type), { 'cursor-pointer': buildMode }]"
                @click="handleRoomClick(room)"
              >
                <div class="accent-strip" :style="{ background: getColorVar(room.type) }"></div>
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
                  <div class="room-subtype">{{ room.subtype }}</div>
                  <div class="room-footer">
                    <span class="status-indicator" :class="`status-${room.type}`">
                      {{ getRoomStatus(room) }} <span class="status-arrows">▶▶▶</span>
                    </span>
                    <span class="operator-count">
                      <span class="op-icon">i</span>
                      <span class="op-num" :class="getOpNumClass(room)">{{ operatorCount(room) }}/{{ maxOperators(room) }}</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="left-row left-row-2">
              <div
                v-for="room in [leftWingRooms[3], leftWingRooms[4], leftWingRooms[5]]"
                :key="room.id"
                class="room-card"
                :class="[getColorClass(room.type), { 'cursor-pointer': buildMode }]"
                @click="handleRoomClick(room)"
              >
                <div class="accent-strip" :style="{ background: getColorVar(room.type) }"></div>
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
                  <div class="room-subtype">{{ room.subtype }}</div>
                  <div class="room-footer">
                    <span class="status-indicator" :class="`status-${room.type}`">
                      {{ getRoomStatus(room) }} <span class="status-arrows">▶▶▶</span>
                    </span>
                    <span class="operator-count">
                      <span class="op-icon">i</span>
                      <span class="op-num" :class="getOpNumClass(room)">{{ operatorCount(room) }}/{{ maxOperators(room) }}</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="left-row left-row-3">
              <div
                v-for="room in [leftWingRooms[6], leftWingRooms[7], leftWingRooms[8]]"
                :key="room.id"
                class="room-card"
                :class="[getColorClass(room.type), { 'cursor-pointer': buildMode }]"
                @click="handleRoomClick(room)"
              >
                <div class="accent-strip" :style="{ background: getColorVar(room.type) }"></div>
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
                  <div class="room-subtype">{{ room.subtype }}</div>
                  <div class="room-footer">
                    <span class="status-indicator" :class="`status-${room.type}`">
                      {{ getRoomStatus(room) }} <span class="status-arrows">▶▶▶</span>
                    </span>
                    <span class="operator-count">
                      <span class="op-icon">i</span>
                      <span class="op-num" :class="getOpNumClass(room)">{{ operatorCount(room) }}/{{ maxOperators(room) }}</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Left Corridor -->
          <div class="corridor-wrapper" :style="{ paddingTop: '110px' }">
            <div class="corridor-square" @click="handleRoomClick(leftCorridor)">
              <span class="corridor-arrow">◀</span>
              <span class="corridor-runner">🏃</span>
              <span class="corridor-arrow">▶</span>
            </div>
            <div class="corridor-square" @click="handleRoomClick(leftCorridor)">
              <span class="corridor-arrow">◀</span>
              <span class="corridor-runner">🏃</span>
              <span class="corridor-arrow">▶</span>
            </div>
            <div class="corridor-square" @click="handleRoomClick(leftCorridor)">
              <span class="corridor-arrow">◀</span>
              <span class="corridor-runner">🏃</span>
              <span class="corridor-arrow">▶</span>
            </div>
          </div>

          <!-- Core Grid -->
          <div class="core-grid">
            <div
              class="room-card control-card"
              :class="[getColorClass('control'), { 'cursor-pointer': buildMode }]"
              @click="handleRoomClick(coreRooms[0])"
            >
              <div class="accent-strip" :style="{ background: getColorVar('control') }"></div>
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
                <div class="room-subtype">{{ coreRooms[0].subtype }}</div>
                <div class="control-version-display">
                  <span class="control-ver-text">VER {{ coreRooms[0].level }}.0</span>
                  <span class="control-ver-sub">LEVEL OF CONTROL_INTERFACE</span>
                </div>
                <div class="room-footer">
                  <span class="status-indicator status-control">
                    {{ getRoomStatus(coreRooms[0]) }} <span class="status-arrows">▶▶▶</span>
                  </span>
                  <span class="operator-count">
                    <span class="op-icon">i</span>
                    <span class="op-num" :class="getOpNumClass(coreRooms[0]) || 'text-control'">{{ operatorCount(coreRooms[0]) }}/{{ maxOperators(coreRooms[0]) }}</span>
                  </span>
                </div>
              </div>
            </div>

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
                <div class="accent-strip" :style="{ background: getColorVar(room.type) }"></div>
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
                  <div class="room-subtype">{{ room.subtype }}</div>
                  <div class="room-footer">
                    <span class="status-indicator" :class="`status-${room.type}`">
                      {{ getRoomStatus(room) }} <span class="status-arrows">▶▶▶</span>
                    </span>
                    <span class="operator-count">
                      <span class="op-icon">i</span>
                      <span class="op-num" :class="getOpNumClass(room)">{{ operatorCount(room) }}/{{ maxOperators(room) }}</span>
                    </span>
                  </div>
                </div>
              </template>
            </div>
          </div>

          <!-- Right Corridor -->
          <div class="corridor-wrapper" :style="{ paddingTop: '60px' }">
            <div class="corridor-square" @click="handleRoomClick(rightCorridor)">
              <span class="corridor-arrow">◀</span>
              <span class="corridor-runner">🏃</span>
              <span class="corridor-arrow">▶</span>
            </div>
            <div class="corridor-square" @click="handleRoomClick(rightCorridor)">
              <span class="corridor-arrow">◀</span>
              <span class="corridor-runner">🏃</span>
              <span class="corridor-arrow">▶</span>
            </div>
            <div class="corridor-square" @click="handleRoomClick(rightCorridor)">
              <span class="corridor-arrow">◀</span>
              <span class="corridor-runner">🏃</span>
              <span class="corridor-arrow">▶</span>
            </div>
            <div class="corridor-square" @click="handleRoomClick(rightCorridor)">
              <span class="corridor-arrow">◀</span>
              <span class="corridor-runner">🏃</span>
              <span class="corridor-arrow">▶</span>
            </div>
          </div>

          <!-- Right Wing -->
          <div class="right-wing">
            <div
              v-for="room in rightWingRooms"
              :key="room.id"
              class="room-card"
              :class="[getColorClass(room.type), { 'cursor-pointer': buildMode }]"
              @click="handleRoomClick(room)"
            >
              <div class="accent-strip" :style="{ background: getColorVar(room.type) }"></div>
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
                <div class="room-subtype">{{ room.subtype }}</div>
                <div class="room-footer">
                  <span class="status-indicator" :class="`status-${room.type}`">
                    {{ getRoomStatus(room) }} <span class="status-arrows">▶▶▶</span>
                  </span>
                  <span class="operator-count">
                    <span class="op-icon">i</span>
                    <span class="op-num" :class="getOpNumClass(room)">{{ operatorCount(room) }}/{{ maxOperators(room) }}</span>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Calculation Result Panel -->
    <div v-if="calculationResult" class="fixed top-14 left-0 right-0 z-40 bg-base-800/95 backdrop-blur-sm border-b border-base-700/50 max-h-[60vh] overflow-y-auto">
      <div class="max-w-6xl mx-auto p-4">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm font-mono text-manufacturing">📊 效率计算结果</span>
          <button class="text-base-500 hover:text-base-200 cursor-pointer" @click="calculationResult = null">×</button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          <div
            v-for="(data, facilityName) in calculationResult.facilities"
            :key="facilityName"
            class="bg-base-900/50 rounded border border-base-700/30 p-3"
          >
            <div class="text-xs font-mono text-base-300 mb-2">{{ facilityName }}</div>
            <div class="text-[10px] text-base-500 space-y-1">
              <template v-if="data['制造站等级']">
                <div class="text-xs text-base-400">{{ data['产物'] || '制造' }}</div>
                <div class="text-trade">效率: {{ (data['干员详情'] || []).filter(op => op['效率'] > 0).length > 0 ? (data['总效率'] || 0) : 0 }}</div>
                <div class="text-base-400">{{ data['公式'] }}</div>
                <div v-for="op in data['干员详情'] || []" :key="op['干员']" class="text-base-500">
                  {{ op['干员'] }}: +{{ op['效率'] }}%
                </div>
                <div class="mt-1 pt-1 border-t border-base-700/30 text-[9px] text-base-400">
                  <div>日估算: {{ data['日估算收益']?.['日产量'] || 0 }}{{ data['日估算收益']?.['单位'] || '' }}/天</div>
                </div>
              </template>
              <template v-else-if="data['贸易站等级']">
                <div class="text-xs text-base-400">{{ data['产物'] || '贸易' }}</div>
                <div class="text-trade">效率: {{ (data['干员详情'] || []).filter(op => op['效率'] > 0).length > 0 ? (data['总效率'] || 0) : 0 }}</div>
                <div class="text-base-400">{{ data['公式'] }}</div>
                <div v-for="op in data['干员详情'] || []" :key="op['干员']" class="text-base-500">
                  {{ op['干员'] }}: +{{ op['效率'] }}%
                </div>
                <div class="mt-1 pt-1 border-t border-base-700/30 text-[9px] text-base-400">
                  <div>策略: {{ data['谈判策略'] || '龙门商法' }}</div>
                  <div>赤金概率: {{ data['赤金概率']?.['2赤金'] || '0%' }} / {{ data['赤金概率']?.['3赤金'] || '0%' }} / {{ data['赤金概率']?.['4赤金'] || '0%' }}</div>
                  <div>日估算: {{ data['日估算收益']?.['龙门币收益'] || 0 }}龙门币 + {{ data['日估算收益']?.['赤金消耗'] || 0 }}赤金</div>
                </div>
              </template>
              <template v-else-if="data['发电站等级']">
                <div class="text-xs text-base-400">{{ data['产物'] || '电力' }}</div>
                <div class="text-power">电力: +{{ data['提供电力'] || 0 }}</div>
                <div class="text-base-400">充能: {{ data['总充能速度'] || 0 }}</div>
                <div class="mt-1 pt-1 border-t border-base-700/30 text-[9px] text-base-400">
                  <div>日估算: {{ data['日估算收益']?.['日发电量'] || 0 }}电力, {{ data['日估算收益']?.['日充能'] || 0 }}充能</div>
                </div>
              </template>
              <template v-else-if="data['宿舍等级']">
                <div class="text-xs text-base-400">{{ data['产物'] || '宿舍' }}</div>
                <div class="text-dormitory">
                  恢复: {{ (data['干员详情'] || []).filter(op => op['效率'] > 0).length > 0 ? (data['基础心情恢复'] + ' + ' + data['氛围加成'] + ' + ' + data['干员心情加成']) : '0/时' }}
                </div>
                <div v-for="op in data['干员详情'] || []" :key="op['干员']" class="text-base-500">
                  {{ op['干员'] }}: +{{ op['效率'] }}/时
                </div>
              </template>
              <template v-else-if="data['会客室等级']">
                <div class="text-xs text-base-400">{{ data['产物'] || '线索' }}</div>
                <div class="text-meeting">线索加成: {{ (data['干员详情'] || []).filter(op => op['效率'] > 0).length > 0 ? (data['干员线索加成'] || 0) : 0 }}</div>
                <div class="mt-1 pt-1 border-t border-base-700/30 text-[9px] text-base-400">
                  <div>好友位: {{ data['日估算收益']?.['好友位'] || 0 }}</div>
                </div>
              </template>
              <template v-else-if="data['加工站等级']">
                <div class="text-xs text-base-400">{{ data['产物'] || '加工' }}</div>
                <div class="text-workshop">副产品: {{ (data['干员详情'] || []).filter(op => op['效率'] > 0).length > 0 ? (data['干员副产物加成'] || 0) : 0 }}</div>
                <div class="mt-1 pt-1 border-t border-base-700/30 text-[9px] text-base-400">
                  <div>副产物概率: {{ data['日估算收益']?.['副产物概率'] || '0%' }}</div>
                </div>
              </template>
              <template v-else-if="data['办公室等级']">
                <div class="text-office">联络: {{ (data['干员详情'] || []).filter(op => op['效率'] > 0).length > 0 ? (data['总联络速度'] || 0) : 0 }}</div>
              </template>
              <template v-else-if="data['训练室等级']">
                <div class="text-training">训练: {{ (data['干员详情'] || []).filter(op => op['效率'] > 0).length > 0 ? (data['总训练速度'] || 0) : 0 }}</div>
              </template>
              <template v-else-if="data['控制中枢等级']">
                <div class="text-control">心情减免: {{ (data['进驻人员'] || 0) > 0 ? (data['总心情减免'] || 0) : 0 }}</div>
                <div class="text-base-400">进驻: {{ data['进驻人员'] || 0 }}</div>
              </template>
              <template v-else>
                <div class="text-base-500">-</div>
              </template>
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

    <!-- Edit Room Menu -->
    <Teleport to="body">
      <div v-if="showEditMenu" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm" @click.self="closeEditMenu">
        <div class="build-menu">
          <div class="build-menu-header">
            <span class="text-base-200 font-mono text-sm">编辑房间</span>
            <button class="text-base-500 hover:text-base-200 transition-colors text-lg leading-none cursor-pointer" @click="closeEditMenu">&times;</button>
          </div>
          <div class="build-menu-body">
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
              <span v-if="selectedOperators.length > 0" class="text-xs text-dormitory">
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
                      <span class="op-icon text-xs mr-1">i</span>
                      <span class="font-mono text-sm" :class="getOpNumClass(room)">
                        {{ operatorCount(room) }}/{{ maxOperators(room) }}
                      </span>
                    </span>
                  </div>
                </div>
                <div class="overview-room-operators">
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
  gap: 4px;
  position: relative;
}

/* Left Wing */
.left-wing {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding-top: 110px;
}

.left-row {
  display: flex;
  gap: 4px;
}

.left-row-1 {
  margin-left: calc(78px / 3 + 2px);
}

.left-row-2 {
}

.left-row-3 {
  margin-left: calc(78px / 3 + 2px);
}

/* ===== Corridor ===== */
.corridor-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 36px;
  gap: 4px;
}

.corridor-square {
  width: 36px;
  height: 73.5px;
  background: #1A1D20;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 2px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 1px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.corridor-square::before {
  content: '';
  position: absolute;
  inset: 2px;
  border: 1px solid rgba(255, 255, 255, 0.03);
  border-radius: 1px;
  pointer-events: none;
}

.corridor-square:hover {
  background: #202427;
  border-color: rgba(255, 255, 255, 0.12);
}

.corridor-arrow {
  font-size: 7px;
  color: #505050;
  font-family: var(--font-mono);
  line-height: 1;
  opacity: 0.5;
}

.corridor-runner {
  font-size: 12px;
  animation: run-cycle 1.2s steps(2) infinite;
  line-height: 1;
  filter: brightness(0.7);
}

@keyframes run-cycle {
  0% { transform: translateX(-1px); }
  100% { transform: translateX(1px); }
}

/* ===== Core Grid ===== */
.core-grid {
  width: 220px;
  min-width: 220px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* ===== Right Wing ===== */
.right-wing {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding-top: 60px;
  width: 140px;
  min-width: 140px;
}

/* ===== Room Card ===== */
.room-card {
  position: relative;
  background: #1A1D20;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 3px;
  overflow: hidden;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  min-height: 70px;
  min-width: 180px;
  width: 100%;
  clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 0 100%);
}

.room-card:hover {
  border-color: rgba(255, 255, 255, 0.12);
  background: #202427;
}

.room-card.built:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

/* Accent Strip - left side vertical colored bar */
.accent-strip {
  width: 4px;
  flex-shrink: 0;
  align-self: stretch;
}

.room-content {
  flex: 1;
  padding: 10px 10px 8px 8px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 3px;
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

.room-subtype {
  font-size: 9px;
  color: #6b7280;
  font-family: var(--font-mono);
}

.room-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1px;
}

/* Status Indicator */
.status-indicator {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 9px;
  font-family: var(--font-mono);
  font-weight: 500;
}

.status-trade { color: #9ca3af; }
.status-trade .status-arrows { color: var(--color-trade); }
.status-manufacturing { color: #9ca3af; }
.status-manufacturing .status-arrows { color: var(--color-manufacturing); }
.status-power { color: #9ca3af; }
.status-power .status-arrows { color: var(--color-power); }
.status-control { color: #9ca3af; }
.status-control .status-arrows { color: var(--color-control); }
.status-dormitory { color: #9ca3af; }
.status-dormitory .status-arrows { color: var(--color-dormitory); }
.status-meeting { color: #9ca3af; }
.status-meeting .status-arrows { color: var(--color-meeting); }
.status-workshop { color: #9ca3af; }
.status-workshop .status-arrows { color: var(--color-workshop); }
.status-office { color: #9ca3af; }
.status-office .status-arrows { color: var(--color-office); }
.status-training { color: #9ca3af; }
.status-training .status-arrows { color: var(--color-training); }

.status-arrows {
  font-size: 6px;
  letter-spacing: -1px;
  opacity: 0.7;
}

/* Operator Count */
.operator-count {
  display: flex;
  align-items: center;
  gap: 3px;
}

.op-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 13px;
  height: 13px;
  font-size: 8px;
  font-family: var(--font-mono);
  font-weight: 700;
  color: #9ca3af;
  border: 1px solid #505050;
  border-radius: 1px;
  background: rgba(255, 255, 255, 0.04);
  line-height: 1;
}

.op-num {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  color: #8FA3A6;
}

/* Level Badge */
.level-badge {
  font-family: var(--font-mono);
  font-size: 8px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.06);
  color: #9ca3af;
}

.level-badge.level-trade { color: var(--color-trade); background: rgba(75, 147, 168, 0.15); }
.level-badge.level-manufacturing { color: var(--color-manufacturing); background: rgba(212, 158, 53, 0.15); }
.level-badge.level-power { color: var(--color-power); background: rgba(82, 154, 113, 0.15); }
.level-badge.level-control { color: var(--color-control); background: rgba(192, 122, 59, 0.15); }
.level-badge.level-dormitory { color: var(--color-dormitory); background: rgba(122, 130, 138, 0.15); }
.level-badge.level-meeting { color: var(--color-meeting); background: rgba(168, 75, 75, 0.15); }
.level-badge.level-workshop { color: var(--color-workshop); background: rgba(74, 154, 142, 0.15); }
.level-badge.level-office { color: var(--color-office); background: rgba(107, 117, 153, 0.15); }
.level-badge.level-training { color: var(--color-training); background: rgba(184, 87, 87, 0.15); }

.power-badge {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 2px;
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

/* Control Center Version Display */
.control-version-display {
  display: flex;
  flex-direction: column;
  gap: 1px;
  margin: 2px 0;
  padding: 3px 6px;
  background: rgba(192, 122, 59, 0.08);
  border: 1px solid rgba(192, 122, 59, 0.15);
  border-radius: 2px;
}

.control-ver-text {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 700;
  color: var(--color-control);
  letter-spacing: 3px;
  text-shadow: 0 0 12px rgba(192, 122, 59, 0.2);
  line-height: 1.2;
}

.control-ver-sub {
  font-family: var(--font-mono);
  font-size: 7px;
  color: rgba(192, 122, 59, 0.5);
  letter-spacing: 1px;
  line-height: 1;
}

/* Control Card */
.control-card {
  border-color: rgba(192, 122, 59, 0.2) !important;
  min-height: 90px !important;
}

.control-card:hover {
  border-color: rgba(192, 122, 59, 0.35) !important;
  background: #202427 !important;
}

/* Empty Slot */
.empty-card {
  background: transparent !important;
  border-color: rgba(255, 255, 255, 0.04);
}

.empty-slot {
  width: 100%;
  height: 100%;
  min-height: 70px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px;
}

.empty-slot.build-mode-active {
  border: 1.5px dashed rgba(255, 255, 255, 0.15);
  border-radius: 2px;
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
.accent-trade:hover { border-color: rgba(75, 147, 168, 0.3); }
.accent-manufacturing:hover { border-color: rgba(212, 158, 53, 0.3); }
.accent-power:hover { border-color: rgba(82, 154, 113, 0.3); }
.accent-control:hover { border-color: rgba(192, 122, 59, 0.3); }
.accent-dormitory:hover { border-color: rgba(122, 130, 138, 0.3); }
.accent-meeting:hover { border-color: rgba(168, 75, 75, 0.3); }
.accent-workshop:hover { border-color: rgba(74, 154, 142, 0.3); }
.accent-office:hover { border-color: rgba(107, 117, 153, 0.3); }
.accent-training:hover { border-color: rgba(184, 87, 87, 0.3); }

/* Build Menu */
.build-menu {
  background: #1e1e1e;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
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
  border-radius: 4px;
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
  border-radius: 4px;
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
  border-radius: 4px;
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
  border-radius: 4px;
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
  border-radius: 4px;
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
  background: #1e1e1e;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
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
  border-radius: 4px;
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
  border-radius: 4px;
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
  border-radius: 3px;
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

.overview-empty-slot {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed rgba(255, 255, 255, 0.15);
  border-radius: 4px;
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
  border-radius: 4px;
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
  border-radius: 4px;
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
  border-radius: 4px;
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
  border-radius: 4px;
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
  border-radius: 4px;
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