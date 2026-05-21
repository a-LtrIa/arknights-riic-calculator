"""
贸易站效率计算器模块
"""

import math

from .base_classes import (
    TRADE_STATION_BASE_EFFICIENCY,
    TRADE_STATION_ORDER_LIMIT,
    TRADE_STATION_POWER,
    TRADE_LONGMEN_ORDER,
    TRADE_MINING_ORDER,
    特殊变量存储器
)
from .operator_classes import 创建干员实例


class 贸易站效率计算器:
    """
    贸易站效率计算器（支持蕾缪安-能天使羁绊检测）
    输入：等级、干员列表、产物、特殊变量存储器（已预先计算好）、配置数据、设施名称
    输出：设施基础效率 + 干员效率
    """

    def __init__(self, 等级: int, 进驻干员列表: list, 产物: str = "龙门币",
                 特殊变量: 特殊变量存储器 = None, 配置数据: dict = None, 设施名称: str = None):
        self.等级 = 等级
        self.进驻干员 = 进驻干员列表
        self.产物 = 产物
        self.特殊变量 = 特殊变量
        self.配置数据 = 配置数据
        self.设施名称 = 设施名称
        self.干员实例列表 = []
        self.订单上限加成 = 0  # 订单上限加成

    def 初始化干员(self):
        """初始化干员实例"""
        for op in self.进驻干员:
            name = op["名称"]
            elite = op["精英等级"]
            # 传入配置数据和设施名称，供蕾缪安等干员使用
            干员实例 = 创建干员实例(name, elite, self.特殊变量, self.配置数据, self.设施名称)
            self.干员实例列表.append(干员实例)

    def 计算效率(self) -> dict:
        """计算贸易站效率：基础效率 + 干员效率"""
        self.初始化干员()

        干员总效率 = 0.0
        订单上限加成 = 0
        详情 = []

        for 干员 in self.干员实例列表:
            效率 = 干员.计算效率()
            干员总效率 += 效率

            # 构建详情信息
            详情项 = {
                "干员": 干员.__class__.__name__,
                "精英等级": 干员.精英等级,
                "效率": math.floor(效率),
                "基本属性": 干员.基本属性
            }

            # 如果是蕾缪安且触发了羁绊，添加标记
            if 干员.__class__.__name__ == "蕾缪安" and 效率 > 20:
                详情项["羁绊"] = "与能天使相伴+25%"

            详情.append(详情项)

            # 累加订单上限加成
            if "订单上限" in 干员.基本属性:
                订单上限加成 += 干员.基本属性["订单上限"]

        # 基础效率：每进驻1名干员+1%
        干员数量 = len(self.进驻干员)
        基础效率 = 100 + (干员数量 * TRADE_STATION_BASE_EFFICIENCY)

        # 检查全局贸易加成（如望的权变技能）
        全局贸易加成 = 0.0
        if self.特殊变量:
            全局贸易加成 = self.特殊变量.获取变量("全局贸易加成")

        # 总效率 = 基础效率 + 干员效率 + 全局贸易加成
        总效率 = 基础效率 + 干员总效率 + 全局贸易加成

        # 向下取整（明日方舟效率计算规则）
        总效率取整 = math.floor(总效率)

        # 构建公式和计算过程（模块化显示信息）
        if 全局贸易加成 > 0:
            公式 = "总效率 = 基础效率 + 干员效率 + 全局贸易加成"
            计算过程 = f"{基础效率:.0f}% + {math.floor(干员总效率)}% + {math.floor(全局贸易加成)}%"
        else:
            公式 = "总效率 = 基础效率 + 干员效率"
            计算过程 = f"{基础效率:.0f}% + {math.floor(干员总效率)}%"

        self.订单上限加成 = 订单上限加成

        return {
            "产物": self.产物,
            "贸易站等级": self.等级,
            "基础效率": f"{基础效率:.0f}%",
            "订单上限": TRADE_STATION_ORDER_LIMIT[self.等级] + 订单上限加成,
            "电力消耗": TRADE_STATION_POWER[self.等级],
            "干员总效率": f"{math.floor(干员总效率)}%",
            "总效率": f"{总效率取整}%",
            "公式": 公式,
            "计算过程": 计算过程,
            "干员详情": 详情,
        }
