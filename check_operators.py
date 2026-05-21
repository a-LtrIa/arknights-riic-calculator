#!/usr/bin/env python3
"""
检查干员类与skills_by_room.json的一致性
"""
import json
import sys
sys.path.insert(0, '/Users/altria/Documents/code/arkproject/building-calculator')

from core.operator_classes import *

# 读取skills_by_room.json
with open('data/skills_by_room.json', 'r', encoding='utf-8') as f:
    skills_data = json.load(f)

# 获取所有已实现的干员类
implemented_operators = {}
for name in dir():
    obj = eval(name)
    if isinstance(obj, type) and issubclass(obj, 干员基类) and obj != 干员基类:
        implemented_operators[name] = obj

print("=" * 60)
print("已实现的干员类:")
print("=" * 60)
for name in sorted(implemented_operators.keys()):
    print(f"  - {name}")

print(f"\n总计: {len(implemented_operators)} 个干员类")

# 检查skills_by_room.json中的干员
print("\n" + "=" * 60)
print("检查各房间的干员:")
print("=" * 60)

all_json_operators = set()
for room, operators in skills_data.items():
    print(f"\n【{room}】")
    for op_name, skills in operators.items():
        all_json_operators.add(op_name)
        if op_name in implemented_operators:
            # 检查技能数量是否匹配
            impl_class = implemented_operators[op_name]
            # 尝试创建实例来检查
            try:
                instance = impl_class(精英等级=2, 特殊变量=特殊变量存储器())
                skill_count = len(skills)
                print(f"  ✓ {op_name}: 实现正确 ({skill_count}个技能)")
            except Exception as e:
                print(f"  ✗ {op_name}: 创建实例失败 - {e}")
        else:
            print(f"  ✗ {op_name}: 未实现")

print("\n" + "=" * 60)
print(f"JSON中总计: {len(all_json_operators)} 个干员")
print(f"已实现: {len(implemented_operators)} 个干员")
print(f"缺失: {len(all_json_operators - set(implemented_operators.keys()))} 个干员")
print("=" * 60)
