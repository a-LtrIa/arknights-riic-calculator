#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取制造站干员并分析其基建效率
"""

import json
import re

def extract_manufacturing_operators():
    """提取所有制造站干员"""
    with open('base_skills.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    manufacturing_ops = {}
    
    for operator_name, skills in data.items():
        manufacturing_skills = []
        for skill in skills:
            if skill.get('room') == '制造站':
                manufacturing_skills.append(skill)
        
        if manufacturing_skills:
            manufacturing_ops[operator_name] = manufacturing_skills
    
    return manufacturing_ops

def parse_productivity_bonus(description):
    """从技能描述中解析生产力加成"""
    bonuses = {
        'productivity': 0,  # 生产力加成
        'gold_bonus': 0,    # 赤金特化加成
        'exp_bonus': 0,     # 作战记录特化加成
        'warehouse': 0,     # 仓库加成
        'mood_reduce': 0,   # 心情减免
        'special': []       # 特殊效果
    }
    
    desc = description
    
    # 通用生产力加成
    # 匹配 "生产力+X%" 或 "生产力+X" 或 "+X%生产力"
    productivity_patterns = [
        r'生产力\+?(\d+)%',
        r'\+?(\d+)%生产力',
        r'生产力.*?\+(\d+)%',
    ]
    
    for pattern in productivity_patterns:
        match = re.search(pattern, desc)
        if match:
            bonuses['productivity'] = int(match.group(1))
            break
    
    # 赤金/贵金属加成
    if '贵金属' in desc or '赤金' in desc:
        gold_match = re.search(r'(\d+)%', desc)
        if gold_match and '生产力' in desc:
            bonuses['gold_bonus'] = int(gold_match.group(1))
    
    # 作战记录加成
    if '作战记录' in desc:
        exp_match = re.search(r'(\d+)%', desc)
        if exp_match and '生产力' in desc:
            bonuses['exp_bonus'] = int(exp_match.group(1))
    
    # 仓库容量
    warehouse_match = re.search(r'仓库容量上限\+(\d+)', desc)
    if warehouse_match:
        bonuses['warehouse'] = int(warehouse_match.group(1))
    
    # 心情消耗减免
    mood_match = re.search(r'心情每小时消耗-([\d.]+)', desc)
    if mood_match:
        bonuses['mood_reduce'] = float(mood_match.group(1))
    
    # 特殊技能识别
    if '慢性子' in desc or '等不及' in desc:
        bonuses['special'].append('gradual_boost')
        # 最终加成25%
        if bonuses['productivity'] == 0:
            bonuses['productivity'] = 25
    
    if '归零' in desc:
        bonuses['special'].append('reset_others')
    
    if '红松骑士团' in desc:
        bonuses['special'].append('red_pine_knights')
    
    if '配合意识' in desc:
        bonuses['special'].append('cooperation')
    
    if '自动化' in desc:
        bonuses['special'].append('automation')
    
    if '金属工艺' in desc:
        bonuses['special'].append('metal_craft')
    
    return bonuses

def analyze_operator_efficiency(operator_name, skills):
    """分析干员的基建效率"""
    analysis = {
        'name': operator_name,
        'skills': [],
        'best_for': [],  # 最适合的生产类型
        'efficiency_rating': 0,  # 效率评级
        'notes': []  # 备注
    }
    
    total_productivity = 0
    has_gold_bonus = False
    has_exp_bonus = False
    
    for skill in skills:
        bonuses = parse_productivity_bonus(skill['description'])
        
        skill_analysis = {
            'condition': skill['condition'],
            'skill_name': skill['skill_name'],
            'description': skill['description'],
            'bonuses': bonuses
        }
        
        analysis['skills'].append(skill_analysis)
        
        # 统计加成
        if bonuses['productivity'] > total_productivity:
            total_productivity = bonuses['productivity']
        
        if bonuses['gold_bonus'] > 0:
            has_gold_bonus = True
        
        if bonuses['exp_bonus'] > 0:
            has_exp_bonus = True
        
        # 特殊备注
        if 'gradual_boost' in bonuses['special']:
            analysis['notes'].append('暖机技能：需要时间达到最大效率')
        
        if 'reset_others' in bonuses['special']:
            analysis['notes'].append('注意：会清空其他干员生产力加成')
        
        if bonuses['warehouse'] > 0:
            analysis['notes'].append(f"仓库容量+{bonuses['warehouse']}")
    
    # 判断最适合的生产类型
    if has_gold_bonus and not has_exp_bonus:
        analysis['best_for'].append('赤金')
    elif has_exp_bonus and not has_gold_bonus:
        analysis['best_for'].append('作战记录')
    elif has_gold_bonus and has_exp_bonus:
        analysis['best_for'].append('赤金')
        analysis['best_for'].append('作战记录')
    else:
        analysis['best_for'].append('通用')
    
    # 计算效率评级
    if total_productivity >= 30:
        analysis['efficiency_rating'] = 5  # S级
    elif total_productivity >= 25:
        analysis['efficiency_rating'] = 4  # A级
    elif total_productivity >= 20:
        analysis['efficiency_rating'] = 3  # B级
    elif total_productivity >= 15:
        analysis['efficiency_rating'] = 2  # C级
    else:
        analysis['efficiency_rating'] = 1  # D级
    
    analysis['max_productivity'] = total_productivity
    
    return analysis

def main():
    # 提取制造站干员
    manufacturing_ops = extract_manufacturing_operators()
    print(f"找到 {len(manufacturing_ops)} 个制造站干员")
    
    # 分析每个干员
    analyzed_ops = {}
    for op_name, skills in manufacturing_ops.items():
        analysis = analyze_operator_efficiency(op_name, skills)
        analyzed_ops[op_name] = analysis
    
    # 保存原始数据
    with open('manufacturing_operators.json', 'w', encoding='utf-8') as f:
        json.dump(manufacturing_ops, f, ensure_ascii=False, indent=2)
    
    # 保存分析后的数据
    with open('manufacturing_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analyzed_ops, f, ensure_ascii=False, indent=2)
    
    # 打印概览
    print("\n=== 制造站干员效率概览 ===")
    print("\n【赤金特化干员】")
    for op_name, analysis in analyzed_ops.items():
        if '赤金' in analysis['best_for'] and analysis['max_productivity'] > 0:
            rating = '★' * analysis['efficiency_rating']
            print(f"  {op_name}: +{analysis['max_productivity']}% {rating}")
    
    print("\n【高通用效率干员 (25%+)】")
    for op_name, analysis in analyzed_ops.items():
        if analysis['max_productivity'] >= 25:
            rating = '★' * analysis['efficiency_rating']
            best_for = '/'.join(analysis['best_for'])
            print(f"  {op_name}: +{analysis['max_productivity']}% [{best_for}] {rating}")
    
    print("\n数据已保存到:")
    print("  - manufacturing_operators.json (原始数据)")
    print("  - manufacturing_analysis.json (分析数据)")

if __name__ == '__main__':
    main()
