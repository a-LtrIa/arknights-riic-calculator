"""
贸易站效率计算器模块 - 完整版
支持订单模拟、赤金概率计算、特殊订单处理
"""

import math
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

from .base_classes import (
    TRADE_STATION_BASE_EFFICIENCY,
    TRADE_STATION_ORDER_LIMIT,
    TRADE_STATION_POWER,
    TRADE_STATION_OPERATOR_CAPACITY,
    TRADE_LONGMEN_ORDER,
    TRADE_MINING_ORDER,
    特殊变量存储器
)
from .operator_classes import 创建干员实例


class 谈判策略(Enum):
    """谈判策略类型"""
    LONGMEN = "龙门商法"  # 高收益长周期
    MINING = "开采协力"   # 低收益短周期


@dataclass
class 订单:
    """订单数据类"""
    赤金需求: int
    龙门币: int
    时长_分钟: int
    订单类型: str = "常规"
    特殊标签: str = ""

    @property
    def 时长_小时(self) -> float:
        return self.时长_分钟 / 60

    @property
    def 收益_时(self) -> float:
        """每小时收益（龙门币/时）"""
        return self.龙门币 / self.时长_小时 if self.时长_小时 > 0 else 0


@dataclass
class 订单概率分布:
    """订单概率分布"""
    赤金2概率: float = 0.0
    赤金3概率: float = 0.0
    赤金4概率: float = 0.0


@dataclass
class 特殊订单效果:
    """特殊订单效果"""
    名称: str
    赤金加成: int = 0
    龙门币加成: int = 0
    时长加成_分钟: int = 0
    概率倍率: float = 1.0
    优先级: int = 0  # 数字越大优先级越高


# 特殊订单定义
SPECIAL_ORDERS = {
    "佩佩": 特殊订单效果(名称="特别独占订单", 优先级=5, 赤金加成=0, 龙门币加成=0, 时长加成_分钟=270),  # 4:30:00固定
    "可露希尔": 特殊订单效果(名称="可露希尔特别订单", 优先级=4, 赤金加成=0, 龙门币加成=200, 时长加成_分钟=0),
    "U-Official": 特殊订单效果(名称="尤里卡订单", 优先级=3, 赤金加成=0, 龙门币加成=0),
    "但书": 特殊订单效果(名称="违约订单", 优先级=2, 赤金加成=1, 龙门币加成=500),
    "龙舌兰": 特殊订单效果(名称="龙舌兰订单", 优先级=1, 赤金加成=0, 龙门币加成=250),
}

# α级技能（降低2赤金概率，提升4赤金概率）
ALPHA_SKILLS = ["裁缝·α", "手工艺品·α", "鉴定师的眼光", "懂行"]
# β级技能（大幅降低2/3赤金概率，极大提升4赤金概率）
BETA_SKILLS = ["裁缝·β", "手工艺品·β", "鉴定师的手段"]


class 贸易站效率计算器:
    """
    贸易站效率计算器（完整版）

    功能：
    1. 订单模拟（龙门商法/开采协力）
    2. 赤金概率计算（基于等级和干员技能）
    3. 特殊订单处理
    4. 每日收益估算
    5. 干员技能扩展接口
    """

    def __init__(self, 等级: int, 进驻干员列表: list, 产物: str = "龙门币",
                 特殊变量: 特殊变量存储器 = None, 配置数据: dict = None, 设施名称: str = None,
                 谈判策略: 谈判策略 = 谈判策略.LONGMEN):
        self.等级 = 等级
        self.进驻干员 = 进驻干员列表
        self.产物 = 产物
        self.特殊变量 = 特殊变量
        self.配置数据 = 配置数据
        self.设施名称 = 设施名称
        self.谈判策略 = 谈判策略
        self.干员实例列表 = []
        self.订单上限加成 = 0

        # 订单概率修正（干员技能可修改）
        self.概率修正 = 订单概率分布()

        # 特殊订单启用状态（干员技能可修改）
        self.特殊订单启用 = {name: False for name in SPECIAL_ORDERS}

        # 特殊订单持续时间修正（干员技能可修改）
        self.特殊订单时长修正 = {}

    def 初始化干员(self):
        """初始化干员实例"""
        for op in self.进驻干员:
            name = op["名称"]
            elite = op["精英等级"]
            干员实例 = 创建干员实例(name, elite, self.特殊变量, self.配置数据, self.设施名称)
            self.干员实例列表.append(干员实例)

    def 获取干员技能修正(self):
        """获取干员技能对订单概率和特殊订单的影响"""
        alpha_count = 0  # α级技能数量
        beta_count = 0   # β级技能数量

        for 干员 in self.干员实例列表:
            # 检查是否有订单概率修正技能
            for skill_name in getattr(干员, '技能列表', []):
                if skill_name in ALPHA_SKILLS:
                    alpha_count += 1
                if skill_name in BETA_SKILLS:
                    beta_count += 1

            # 检查特殊订单技能
            op_name = 干员.__class__.__name__
            if op_name in SPECIAL_ORDERS:
                self.特殊订单启用[op_name] = True

            # 调用干员的订单修正方法（如果存在）
            if hasattr(干员, '修正订单概率'):
                干员.修正订单概率(self.概率修正)

            if hasattr(干员, '修正特殊订单'):
                干员.修正特殊订单(self.特殊订单启用, self.特殊订单时长修正)

    def 获取基础赤金概率(self) -> 订单概率分布:
        """获取基础赤金概率（根据wiki数据）"""
        if self.等级 == 1:
            return 订单概率分布(赤金2概率=1.0, 赤金3概率=0.0, 赤金4概率=0.0)
        elif self.等级 == 2:
            return 订单概率分布(赤金2概率=0.6, 赤金3概率=0.4, 赤金4概率=0.0)
        else:  # Lv.3
            return 订单概率分布(赤金2概率=0.3, 赤金3概率=0.5, 赤金4概率=0.2)

    def 应用概率修正(self):
        """应用干员技能的概率修正"""
        base = self.获取基础赤金概率()
        alpha_count = 0
        beta_count = 0

        for 干员 in self.干员实例列表:
            for skill_name in getattr(干员, '技能列表', []):
                if skill_name in ALPHA_SKILLS:
                    alpha_count += 1
                if skill_name in BETA_SKILLS:
                    beta_count += 1

        # α级技能修正（需要累积工作3小时）
        if alpha_count > 0:
            # α级效果：降低2/3概率，提升4概率
            reduction = 0.15 * alpha_count  # 每级α降低15% 2赤金
            self.概率修正.赤金2概率 = max(0, base.赤金2概率 - reduction)
            self.概率修正.赤金3概率 = max(0, base.赤金3概率 - reduction * 1.3)
            self.概率修正.赤金4概率 = min(1.0, base.赤金4概率 + reduction * 2.3)

        # β级技能修正（需要累积工作5小时）
        if beta_count > 0:
            # β级效果：大幅降低2/3概率，极大提升4概率
            reduction = 0.25 * beta_count
            self.概率修正.赤金2概率 = max(0, base.赤金2概率 - reduction)
            self.概率修正.赤金3概率 = max(0, base.赤金3概率 - reduction * 1.6)
            self.概率修正.赤金4概率 = min(1.0, base.赤金4概率 + reduction * 3.6)

        # 归一化
        total = self.概率修正.赤金2概率 + self.概率修正.赤金3概率 + self.概率修正.赤金4概率
        if total > 0:
            self.概率修正.赤金2概率 /= total
            self.概率修正.赤金3概率 /= total
            self.概率修正.赤金4概率 /= total

        # 如果没有修正，使用基础概率
        if alpha_count == 0 and beta_count == 0:
            self.概率修正 = base

    def 生成订单(self, 策略: 谈判策略 = 谈判策略.LONGMEN) -> 订单:
        """生成一个订单"""
        # 确定赤金数量
        rand = random.random()
        if rand < self.概率修正.赤金2概率:
            赤金 = 2
        elif rand < self.概率修正.赤金2概率 + self.概率修正.赤金3概率:
            赤金 = 3
        else:
            赤金 = 4

        # 根据策略计算基础订单
        if 策略 == 谈判策略.LONGMEN:
            # 龙门商法
            base = TRADE_LONGMEN_ORDER.copy()
            base["赤金需求"] = 赤金  # 赤金需求随概率变化
            # 龙门的交付报酬与赤金需求相关：2赤金=1000, 3赤金=1500, 4赤金=2000
            base["龙门币"] = 赤金 * 500
        else:
            # 开采协力
            base = TRADE_MINING_ORDER.copy()
            base["赤金需求"] = 赤金

        # 检查是否有特殊订单
        特殊订单 = self.检查特殊订单(赤金)
        if 特殊订单:
            return 特殊订单

        return 订单(
            赤金需求=base["赤金需求"],
            龙门币=base["龙门币"],
            时长_分钟=base["时间_分钟"],
            订单类型="常规"
        )

    def 检查特殊订单(self, 赤金需求: int) -> Optional[订单]:
        """检查是否有可用的特殊订单"""
        # 按优先级排序
        sorted_orders = sorted(
            [(name, effect) for name, enabled in self.特殊订单启用.items() if enabled],
            key=lambda x: x[1].优先级,
            reverse=True
        )

        for name, effect in sorted_orders:
            # 特殊订单只有4赤金订单才能触发
            if 赤金需求 == 4:
                特殊订单 = 订单(
                    赤金需求=max(0, effect.赤金加成),  # 特别独占订单赤金为0
                    龙门币=effect.龙门币加成,
                    时长_分钟=effect.时长加成_分钟 or TRADE_LONGMEN_ORDER["时间_分钟"],
                    订单类型="特殊",
                    特殊标签=effect.名称
                )
                return 特殊订单

        return None

    def 模拟订单周期(self, 订单数: int, 策略: 谈判策略 = 谈判策略.LONGMEN) -> List[订单]:
        """模拟多个订单"""
        return [self.生成订单(策略) for _ in range(订单数)]

    def 计算日收益(self, 策略: 谈判策略 = 谈判策略.LONGMEN) -> Dict:
        """计算每日收益估算"""
        订单上限 = TRADE_STATION_ORDER_LIMIT[self.等级] + self.订单上限加成

        # 模拟一天（24小时）能完成的订单
        模拟订单 = self.模拟订单周期(订单上限, 策略)

        总龙门币 = 0
        总赤金 = 0
        总时间 = 0
        完成订单数 = 0

        # 获取效率
        效率 = self.获取总效率()

        # 如果效率为0，直接返回0
        if 效率 <= 0:
            return {
                "龙门币": 0,
                "赤金": 0,
                "订单数": 0,
                "总时长_分钟": 0,
                "效率": f"{效率:.1f}%"
            }

        for order in 模拟订单:
            # 计算该订单需要的时间（考虑效率加成）
            实际时长 = order.时长_分钟 / (效率 / 100)
            总时间 += 实际时长

            # 如果超过24小时，只计算24小时内的部分
            if 总时间 > 24 * 60:
                break

            总龙门币 += order.龙门币
            总赤金 += order.赤金需求
            完成订单数 += 1

        return {
            "龙门币": 总龙门币,
            "赤金": 总赤金,
            "订单数": 完成订单数,
            "总时长_分钟": 总时间,
            "效率": f"{效率:.1f}%"
        }

    def 获取总效率(self) -> float:
        """获取总订单获取效率"""
        干员数量 = len(self.进驻干员)
        基础效率 = 1 + 干员数量 * (TRADE_STATION_BASE_EFFICIENCY / 100)  # 1% per operator

        干员效率 = 0.0
        for 干员 in self.干员实例列表:
            if hasattr(干员, '计算效率'):
                干员效率 += 干员.计算效率()

        # 全局贸易加成
        全局贸易加成 = 0.0
        if self.特殊变量:
            全局贸易加成 = self.特殊变量.获取变量("全局贸易加成")

        # 效率公式：(基础效率 - 1) × 100% + 干员效率 + 全局贸易加成
        return (基础效率 - 1) * 100 + 干员效率 + 全局贸易加成

    def 计算效率(self) -> dict:
        """计算贸易站效率（完整版）"""
        self.初始化干员()
        self.获取干员技能修正()
        self.应用概率修正()

        干员总效率 = 0.0
        详情 = []

        for 干员 in self.干员实例列表:
            效率 = 干员.计算效率() if hasattr(干员, '计算效率') else 0
            干员总效率 += 效率

            详情项 = {
                "干员": 干员.__class__.__name__,
                "精英等级": 干员.精英等级,
                "效率": math.floor(效率),
                "基本属性": 干员.基本属性
            }
            详情.append(详情项)

            # 累加订单上限加成
            if "订单上限" in 干员.基本属性:
                self.订单上限加成 += 干员.基本属性["订单上限"]

        # 基础效率：每进驻1名干员获得1%的基础加成
        # 公式：(基础效率 - 1) × 100% + 干员效率
        干员数量 = len(self.进驻干员)
        基础效率 = 1 + 干员数量 * (TRADE_STATION_BASE_EFFICIENCY / 100)  # 1% per operator

        # 全局贸易加成
        全局贸易加成 = 0.0
        if self.特殊变量:
            全局贸易加成 = self.特殊变量.获取变量("全局贸易加成")

        # 总效率 = (基础效率 - 1) × 100% + 干员效率 + 全局贸易加成
        总效率 = (基础效率 - 1) * 100 + 干员总效率 + 全局贸易加成
        总效率取整 = math.floor(总效率)

        # 每日收益估算
        日收益 = self.计算日收益(self.谈判策略)

        # 构建公式
        if 全局贸易加成 > 0:
            公式 = "总效率 = (基础效率 - 1) × 100% + 干员效率 + 全局贸易加成"
            计算过程 = f"(基础效率:{基础效率:.2f} - 1) × 100% + {math.floor(干员总效率)}% + {math.floor(全局贸易加成)}% = {总效率取整}%"
        else:
            公式 = "总效率 = (基础效率 - 1) × 100% + 干员效率"
            计算过程 = f"(基础效率:{基础效率:.2f} - 1) × 100% + {math.floor(干员总效率)}% = {总效率取整}%"

        return {
            "产物": self.产物,
            "贸易站等级": self.等级,
            "进驻人数": 干员数量,
            "进驻上限": TRADE_STATION_OPERATOR_CAPACITY[self.等级],
            "基础效率": f"{基础效率:.2f}",
            "订单上限": TRADE_STATION_ORDER_LIMIT[self.等级] + self.订单上限加成,
            "电力消耗": TRADE_STATION_POWER[self.等级],
            "干员总效率": f"{math.floor(干员总效率)}%",
            "总效率": f"{总效率取整}%",
            "公式": 公式,
            "计算过程": 计算过程,
            "谈判策略": self.谈判策略.value,
            "赤金概率": {
                "2赤金": f"{self.概率修正.赤金2概率:.1%}",
                "3赤金": f"{self.概率修正.赤金3概率:.1%}",
                "4赤金": f"{self.概率修正.赤金4概率:.1%}",
            },
            "日估算收益": {
                "龙门币收益": 日收益["龙门币"],
                "赤金消耗": 日收益["赤金"],
                "完成订单数": 日收益["订单数"],
            },
            "干员详情": 详情,
        }


def 计算贸易站效率(等级: int, 进驻干员列表: list, 产物: str = "龙门币",
                   特殊变量: 特殊变量存储器 = None, 配置数据: dict = None,
                   设施名称: str = None, 谈判策略: str = "龙门商法") -> dict:
    """
    便捷函数：计算贸易站效率
    谈判策略可选："龙门商法" 或 "开采协力"
    """
    策略 = 谈判策略.LONGMEN if 谈判策略 == "龙门商法" else 谈判策略.MINING
    计算器 = 贸易站效率计算器(
        等级=等级,
        进驻干员列表=进驻干员列表,
        产物=产物,
        特殊变量=特殊变量,
        配置数据=配置数据,
        设施名称=设施名称,
        谈判策略=策略
    )
    return 计算器.计算效率()
