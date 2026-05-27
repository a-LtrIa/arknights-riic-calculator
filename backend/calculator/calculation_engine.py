"""
效率计算引擎
整合原有的核心计算逻辑
"""
import sys
import os

# 添加core目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

from core import (
    基建模拟器,
    制造站效率计算器,
    贸易站效率计算器,
    发电站效率计算器,
    会客室效率计算器,
    加工站效率计算器,
    办公室效率计算器,
    训练室效率计算器,
    宿舍效率计算器,
    控制中枢效率计算器,
    活动室效率计算器,
)
from core.trade_station_calculator import 谈判策略


def calculate_efficiency_api(configuration_data):
    """
    API接口：计算效率
    configuration_data: 设施配置数据，格式与example_config.json相同
    支持谈判策略参数："谈判策略": "龙门商法" 或 "开采协力"
    """
    # 创建基建模拟器
    模拟器 = 基建模拟器(configuration_data)

    # 遍历所有配置项，自动注册设施
    for 设施名, 设施数据 in configuration_data.items():
        if not isinstance(设施数据, dict):
            continue

        类型 = 设施数据.get("类型", "")
        等级 = 设施数据.get("等级", 1)
        产物 = 设施数据.get("产物", "")
        进驻干员 = 设施数据.get("进驻干员", [])
        氛围值 = 设施数据.get("氛围值", 0)
        谈判策略_str = 设施数据.get("谈判策略", "龙门商法")  # 默认龙门商法
        # 转换为枚举
        谈判策略_enum = 谈判策略.LONGMEN if 谈判策略_str == "龙门商法" else 谈判策略.MINING

        # 根据类型注册设施
        设施 = None
        if 类型 == "制造站":
            设施 = 制造站效率计算器(
                等级=等级,
                进驻干员列表=进驻干员,
                产物=产物
            )
        elif 类型 == "贸易站":
            设施 = 贸易站效率计算器(
                等级=等级,
                进驻干员列表=进驻干员,
                产物=产物,
                配置数据=configuration_data,
                设施名称=设施名,
                谈判策略=谈判策略_enum
            )
        elif 类型 == "发电站":
            设施 = 发电站效率计算器(
                等级=等级,
                进驻干员列表=进驻干员
            )
        elif 类型 == "会客室":
            设施 = 会客室效率计算器(
                等级=等级,
                进驻干员列表=进驻干员
            )
        elif 类型 == "加工站":
            设施 = 加工站效率计算器(
                等级=等级,
                进驻干员列表=进驻干员
            )
        elif 类型 == "办公室":
            设施 = 办公室效率计算器(
                等级=等级,
                进驻干员列表=进驻干员
            )
        elif 类型 == "训练室":
            设施 = 训练室效率计算器(
                等级=等级,
                进驻干员列表=进驻干员
            )
        elif 类型 == "宿舍":
            设施 = 宿舍效率计算器(
                等级=等级,
                进驻干员列表=进驻干员,
                氛围值=氛围值 if 氛围值 > 0 else None
            )
        elif 类型 == "控制中枢":
            设施 = 控制中枢效率计算器(
                等级=等级,
                进驻干员列表=进驻干员
            )
        elif 类型 == "活动室":
            使用干员 = 进驻干员[0] if 进驻干员 else None
            设施 = 活动室效率计算器(
                等级=等级,
                使用干员=使用干员,
                氛围值=氛围值
            )
        else:
            continue

        if 设施:
            模拟器.注册设施(设施, 设施名)

    # 运行模拟器
    结果 = 模拟器.运行()

    # 整理返回结果
    return {
        'facilities': 结果,
        'special_variables': dict(模拟器.特殊变量.变量字典)
    }
