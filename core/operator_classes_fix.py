#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接修复刻俄柏和多萝西的技能实现
"""

# 读取文件
with open('/Users/altria/Documents/code/arkproject/building-calculator/core/operator_classes.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到刻俄柏类的起始和结束行
start_刻俄柏 = None
end_刻俄柏 = None
for i, line in enumerate(lines):
    if 'class 刻俄柏(干员基类):' in line:
        start_刻俄柏 = i
    if start_刻俄柏 is not None and end_刻俄柏 is None:
        if i > start_刻俄柏 and line.strip().startswith('class ') and '刻俄柏' not in line:
            end_刻俄柏 = i
            break

print(f"刻俄柏类: 起始行 {start_刻俄柏}, 结束行 {end_刻俄柏}")

# 新的刻俄柏类实现
new_刻俄柏 = '''class 刻俄柏(干员基类):
    """
    明日方舟 刻俄柏 基建技能类
        精英0: "都想要" - 进驻制造站时，仓库容量上限+8，心情每小时消耗-0.25
    精英2: "等不及" - 进驻制造站后，生产力首小时+20%，此后每小时+1%，最终达到+25%
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = []
        # E0: 基础属性
        self.基本属性 = {"仓库容量": 8, "心情消耗": -0.25}
        # 工作时长（小时），由外部设置
        self.工作时长 = 0.0

    def 设置工作时长(self, 小时: float):
        """设置工作时长（小时）"""
        self.工作时长 = 小时

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        """
        E2: 首小时+20%，此后每小时+1%，最终+25%
        """
        if self.精英等级 < 2:
            return 0.0

        # 计算效率：首小时20%，之后每小时+1%，上限25%
        基础效率 = 20.0
        额外效率 = min(self.工作时长 * 1.0, 5.0)  # 最多增加5%
        return 基础效率 + 额外效率


'''

# 找到多萝西类的起始和结束行
start_多萝西 = None
end_多萝西 = None
for i, line in enumerate(lines):
    if 'class 多萝西(干员基类):' in line:
        start_多萝西 = i
    if start_多萝西 is not None and end_多萝西 is None:
        if i > start_多萝西 and line.strip().startswith('class ') and '多萝西' not in line:
            end_多萝西 = i
            break

print(f"多萝西类: 起始行 {start_多萝西}, 结束行 {end_多萝西}")

# 新的多萝西类实现
new_多萝西 = '''class 多萝西(干员基类):
    """
    明日方舟 多萝西 基建技能类
        精英0: 源石技艺理论应用 - 进驻制造站时，当前制造站内每个莱茵科技类技能为自身+5%生产力
            莱茵科技类技能: 莱茵科技·α、莱茵科技·β、莱茵科技·γ
            拥有者: 赫默(E0)、白面鸮(E0)、梅尔(E0)、塞雷娅(E2)、多萝西(E2)
    精英2: 莱茵科技·β - 进驻制造站时，生产力+25%
    """
    # 莱茵科技类技能及其拥有者
    莱茵科技技能拥有者 = {
        "赫默": (0, "莱茵科技·α"),  # E0拥有
        "白面鸮": (0, "莱茵科技·α"),  # E0拥有
        "梅尔": (0, "莱茵科技·α"),  # E0拥有
        "塞雷娅": (2, "莱茵科技·β"),  # E2拥有
        "多萝西": (2, "莱茵科技·β"),  # E2拥有
    }

    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器, 配置数据: dict = None, 当前设施名: str = None):
        super().__init__(精英等级, 特殊变量, 配置数据, 当前设施名)
        self.特殊变量列表 = []
        self.基本属性 = {}

    def 计算莱茵科技数量(self) -> int:
        """计算当前制造站内的莱茵科技类技能数量"""
        if not self.配置数据 or not self.当前设施名:
            return 0
        设施数据 = self.配置数据.get(self.当前设施名, {})
        if not isinstance(设施数据, dict) or 设施数据.get("类型") != "制造站":
            return 0
        进驻干员列表 = 设施数据.get("进驻干员", [])
        count = 0
        for op in 进驻干员列表:
            name = op.get("名称", "")
            elite = op.get("精英等级", 0)
            # 检查干员是否拥有莱茵科技类技能
            if name in self.莱茵科技技能拥有者:
                所需精英, 技能名 = self.莱茵科技技能拥有者[name]
                if elite >= 所需精英:
                    count += 1
        return count

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        """
        E0: 每个莱茵科技类技能+5%生产力
        E2: 固定+25%生产力
        """
        if self.精英等级 >= 2:
            return 25.0
        else:
            莱茵数量 = self.计算莱茵科技数量()
            return 莱茵数量 * 5.0


'''

# 构建新的文件内容
new_lines = []

# 添加刻俄柏之前的所有行
new_lines.extend(lines[:start_刻俄柏])

# 添加新的刻俄柏类
new_lines.append(new_刻俄柏)

# 添加刻俄柏之后到多萝西之前的行
new_lines.extend(lines[end_刻俄柏:start_多萝西])

# 添加新的多萝西类
new_lines.append(new_多萝西)

# 添加多萝西之后的所有行
new_lines.extend(lines[end_多萝西:])

# 写入文件
with open('/Users/altria/Documents/code/arkproject/building-calculator/core/operator_classes.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("修复完成！")
print("\n修复内容：")
print("1. 刻俄柏 - 使用工作时长属性计算时间依赖效率")
print("   - 首小时: +20%")
print("   - 之后每小时: +1%")
print("   - 上限: +25%")
print("\n2. 多萝西 - 正确识别莱茵科技类技能拥有者")
print("   - 赫默/白面鸮/梅尔 (E0): 莱茵科技·α")
print("   - 塞雷娅/多萝西 (E2): 莱茵科技·β")
print("   - 每个技能为E0多萝西+5%生产力")
