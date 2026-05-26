#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入干员数据到数据库
"""
import os
import sys
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'riic_calculator.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from operators.models import Operator


def import_operators():
    """从operators.json导入干员数据"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'operators.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        operators = json.load(f)
    
    created_count = 0
    for op_name in operators:
        # 检查是否已存在
        if not Operator.objects.filter(name=op_name).exists():
            Operator.objects.create(
                name=op_name,
                rarity=3,  # 默认稀有度
                skill_tags=[],
                applicable_facilities=[]
            )
            created_count += 1
            print(f"创建干员: {op_name}")
    
    print(f"\n总共导入 {created_count} 个干员")


if __name__ == '__main__':
    import_operators()
