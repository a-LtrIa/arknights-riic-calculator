# 明日方舟基建仿真计算工具 - 项目进度文档

## 项目概述

一个基于 Vue 3 + Vite 开发的明日方舟基建仿真计算工具，目前主要实现制造站（特别是赤金制造）的仿真计算，支持干员技能计算、宿舍联动、生产力分析等功能。

## 技术栈

- **前端框架**: Vue 3 (Composition API)
- **构建工具**: Vite 5
- **语言**: JavaScript (ES Modules)
- **开发服务器**: http://localhost:5173/

## 项目结构

```
base-calculator/
├── data/                          # 数据文件
│   ├── base_skills.json          # 原始基建技能数据
│   ├── operators.json            # 干员基础数据
│   ├── manufacturing_operators.json  # 制造站干员提取数据
│   └── manufacturing_analysis.json   # 制造站干员分析数据
├── src/
│   ├── components/
│   │   ├── ManufacturingStation.vue   # 制造站主组件（UI界面）
│   │   └── App.vue                    # 根组件
│   ├── core/                      # 核心计算逻辑
│   │   ├── constants.js          # 基础数据常量
│   │   ├── manufacturingCalculator.js # 制造站计算器
│   │   ├── operatorUtils.js      # 干员工具函数
│   │   ├── specialSkillsSystem.js     # 特殊技能系统
│   │   ├── OperatorClass.js      # 干员类系统（新架构）
│   │   ├── operatorCalculator.js      # 基于类的计算器
│   │   └── operatorExamples.js   # 类系统使用示例
│   ├── main.js                   # 入口文件
│   └── style.css                 # 全局样式
├── package.json
└── vite.config.js
```

## 已完成功能

### 1. 基础制造站计算 ✅
- [x] 制造站等级配置（1-3级）
- [x] 基础生产力计算
- [x] 干员人数基础加成（每人+1%）
- [x] 无人机协助加速计算
- [x] 心情消耗计算
- [x] 仓库容量计算

**相关文件**:
- `src/core/constants.js` - 定义基础数据常量
- `src/core/manufacturingCalculator.js` - 核心计算器

### 2. 干员数据提取与分析 ✅
- [x] 从原始数据提取制造站干员
- [x] 解析干员技能描述
- [x] 计算基础效率评级
- [x] 识别特化类型（赤金/作战记录/通用）

**相关文件**:
- `data/extract_manufacturing_ops.py` - Python提取脚本
- `data/manufacturing_operators.json` - 提取后的干员数据

### 3. 干员选择与UI ✅
- [x] 干员列表展示（按效率排序）
- [x] 干员筛选（全部/赤金特化/高效率）
- [x] 干员搜索功能
- [x] 已选干员管理（添加/移除）
- [x] 干员效率实时显示

**相关文件**:
- `src/components/ManufacturingStation.vue`

### 4. 特殊技能系统 ✅

#### 4.1 迷迭香 - 感知信息/思维链环系统
- [x] 感知信息计算（宿舍内特定干员）
- [x] 思维链环转化（1:1）
- [x] 生产力加成计算
  - 精英0: 每2点思维链环+1%
  - 精英2: 每1点思维链环+1%

#### 4.2 截云 - 人间烟火/巫术结晶系统
- [x] 人间烟火计算
- [x] 巫术结晶转化（每5点→1点）
- [x] 生产力加成（每点巫术结晶+1%）

#### 4.3 黍 - 人间烟火直接加成
- [x] 人间烟火计算
- [x] 生产力加成（每3点+1%）

**相关文件**:
- `src/core/specialSkillsSystem.js` - 旧版实现
- `src/core/OperatorClass.js` - 类系统实现

### 5. 宿舍配置系统 ✅
- [x] 4个宿舍配置界面
- [x] 宿舍干员添加/移除
- [x] 感知信息干员统计
- [x] 人间烟火干员统计
- [x] 宿舍与制造站联动计算

**相关文件**:
- `src/components/ManufacturingStation.vue` - 宿舍配置UI

### 6. 类系统架构 ✅

#### 6.1 基础类设计
- [x] `BaseOperator` - 所有干员的基类
- [x] `StandardOperator` - 固定效率干员
- [x] `SynergyOperator` - 联动型干员
- [x] `ConditionalOperator` - 条件型干员

#### 6.2 特殊干员类
- [x] `Rosmontis` - 迷迭香类
- [x] `Jieyun` - 截云类
- [x] `Shu` - 黍类

#### 6.3 工厂模式
- [x] `OperatorFactory` - 根据数据自动创建干员实例

**相关文件**:
- `src/core/OperatorClass.js` - 类定义
- `src/core/operatorCalculator.js` - 基于类的计算器
- `src/core/operatorExamples.js` - 使用示例

### 7. 数据可视化 ✅
- [x] 生产力分析面板
- [x] 特殊技能详情展示
- [x] 产出统计（日/周/月）
- [x] 心情消耗显示
- [x] 仓库信息展示
- [x] 详细报告（JSON格式）

## 核心算法说明

### 1. 生产力计算公式
```
总生产力 = 基础生产力 + 干员技能加成 + 特殊技能加成

基础生产力 = 制造站固有生产力 + 干员人数 × 1%
- 1级制造站: 1.0 (100%)
- 2级制造站: 1.0 (100%)
- 3级制造站: 1.03 (103%)
```

### 2. 生产时间计算
```
实际生产时间 = 基础生产时间 / 总生产力

赤金基础时间: 72分钟
例: 总生产力130%时，实际时间 = 72 / 1.3 ≈ 55.4分钟
```

### 3. 日产量计算
```
日产量 = (24小时 × 60分钟) / 实际生产时间 + 无人机加成

无人机加成 = 无人机次数 × 3分钟 / 实际生产时间
```

### 4. 迷迭香技能链
```
感知信息 = 宿舍内感知信息干员数量
思维链环 = 感知信息 (1:1转化)
生产力加成 = 思维链环 × 1% (精2)
```

## 使用示例

### 示例1: 创建标准干员
```javascript
import { StandardOperator } from './src/core/OperatorClass.js'

const operator = new StandardOperator('干员A', 30, {
  productType: 'gold',  // 只加成赤金
  rarity: 5
})

const context = {
  manufacturingOperators: ['干员A'],
  dormOperators: [],
  productType: 'gold'
}

console.log(operator.calculateProductivity(context))  // 0.3 (30%)
```

### 示例2: 创建联动干员
```javascript
import { SynergyOperator } from './src/core/OperatorClass.js'

// 基础25%，当车尔尼在场时+5%
const operator = new SynergyOperator('联动干员', 25, {
  operators: ['车尔尼'],
  bonus: 5
})

const context = {
  manufacturingOperators: ['联动干员', '车尔尼'],
  dormOperators: [],
  productType: 'gold'
}

console.log(operator.calculateProductivity(context))  // 0.3 (30%)
```

### 示例3: 创建条件干员
```javascript
import { ConditionalOperator } from './src/core/OperatorClass.js'

const operator = new ConditionalOperator('条件干员', [
  {
    description: '基础效率',
    bonus: 20,
    check: () => true
  },
  {
    description: '宿舍有车尔尼时',
    bonus: 5,
    check: (ctx) => ctx.dormOperators.flat().includes('车尔尼')
  }
])
```

### 示例4: 使用计算器
```javascript
import { ManufacturingCalculator } from './src/core/manufacturingCalculator.js'

const calculator = new ManufacturingCalculator({
  stationLevel: 3,
  productType: 'gold',
  operators: ['迷迭香', '干员A', '干员B'],
  droneAssistance: 50,
  dormOperators: [
    ['车尔尼', '黑键', '絮雨'],
    ['夕', '令']
  ]
})

const result = calculator.calculateDailyOutput()
console.log(result)
```

## 待开发功能

### 高优先级
- [ ] 作战记录制造支持
- [ ] 贸易站仿真计算
- [ ] 发电站仿真计算
- [ ] 控制中枢加成计算
- [ ] 会客室/加工站支持

### 中优先级
- [ ] 暖机技能实现（如克洛丝）
- [ ] 心情恢复计算
- [ ] 换班策略优化
- [ ] 多设施联动计算

### 低优先级
- [ ] 历史数据记录
- [ ] 数据导出功能
- [ ] 用户配置保存
- [ ] 响应式布局优化

## 技术债务

1. **数据文件较大**: `manufacturing_operators.json` 包含完整技能描述，可考虑精简
2. **类系统与旧系统并存**: 需要逐步迁移旧代码到类系统
3. **缺乏单元测试**: 核心计算逻辑需要测试覆盖
4. **类型安全**: JavaScript 缺乏类型检查，可考虑迁移到 TypeScript

## 最近更新

### 2025-05-20
- ✅ 实现干员类系统架构
- ✅ 完成迷迭香、截云、黍的特殊技能类
- ✅ 更新制造站计算器使用新类系统
- ✅ 添加类系统使用示例

### 2025-05-19
- ✅ 实现宿舍配置界面
- ✅ 完成特殊技能可视化展示
- ✅ 实现感知信息/思维链环计算

## 运行项目

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

## 参考资料

- [PRTS Wiki - 罗德岛基建/制造站](https://prts.wiki/w/罗德岛基建/制造站)
- 明日方舟游戏内数据

---

**文档版本**: 1.0  
**最后更新**: 2025-05-20  
**项目状态**: 开发中
