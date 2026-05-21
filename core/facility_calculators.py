"""
设施效率计算器模块
包含所有基建设施的效率计算器
"""

from .base_classes import (
    STATION_LEVEL_BONUS, STATION_LEVEL_CAPACITY, STATION_LEVEL_POWER,
    TRADE_STATION_BASE_EFFICIENCY, TRADE_STATION_ORDER_LIMIT, TRADE_STATION_POWER,
    特殊变量存储器
)
from .operator_classes import 创建干员实例, 默认干员


# ====================== 发电站基础数据 ======================
POWER_STATION_POWER = {
    1: 60,
    2: 130,
    3: 270,
}

POWER_STATION_CAPACITY = {
    1: 1,  # 进驻人员上限
    2: 1,
    3: 1,
}

POWER_STATION_POWER_DRAIN = {
    1: 0,
    2: 0,
    3: 0,
}

# 发电站基础充能速度：每个工作的干员+5%
POWER_STATION_BASE_CHARGING = 5


class 发电站效率计算器:
    """
    发电站效率计算器
    主要功能：提供电力 + 提升无人机充能速度
    """

    def __init__(self, 等级: int, 进驻干员列表: list, 特殊变量: 特殊变量存储器 = None):
        self.等级 = 等级
        self.进驻干员 = 进驻干员列表
        self.特殊变量 = 特殊变量
        self.干员实例列表 = []

    def 初始化干员(self):
        """初始化干员实例"""
        for op in self.进驻干员:
            name = op["名称"]
            elite = op["精英等级"]
            self.干员实例列表.append(创建干员实例(name, elite, self.特殊变量))

    def 计算效率(self) -> dict:
        """计算发电站效率"""
        self.初始化干员()

        干员充能加成 = 0.0
        详情 = []
        for 干员 in self.干员实例列表:
            效率 = 干员.计算效率()
            # 发电站干员提供充能速度加成
            if hasattr(干员, '基本属性') and '无人机充能' in 干员.基本属性:
                干员充能加成 += 干员.基本属性['无人机充能']
            详情.append({
                "干员": 干员.__class__.__name__,
                "精英等级": 干员.精英等级,
                "效率": 效率,
                "基本属性": 干员.基本属性
            })

        # 基础充能速度 + 干员充能加成
        基础充能 = POWER_STATION_BASE_CHARGING if self.进驻干员 else 0
        总充能速度 = 基础充能 + 干员充能加成

        return {
            "发电站等级": self.等级,
            "提供电力": POWER_STATION_POWER[self.等级],
            "基础充能速度": f"+{基础充能}%",
            "干员充能加成": f"+{干员充能加成:.1f}%",
            "总充能速度": f"+{总充能速度:.1f}%",
            "进驻人员": len(self.进驻干员),
            "干员详情": 详情,
        }


# ====================== 会客室基础数据 ======================
RECEPTION_FRIEND_SLOTS = {
    1: 10,
    2: 20,
    3: 35,
}

RECEPTION_POWER = {
    1: 10,
    2: 30,
    3: 60,
}


class 会客室效率计算器:
    """
    会客室效率计算器
    主要功能：线索搜集速度加成、好友位、助战设置
    """

    def __init__(self, 等级: int, 进驻干员列表: list, 特殊变量: 特殊变量存储器 = None):
        self.等级 = 等级
        self.进驻干员 = 进驻干员列表
        self.特殊变量 = 特殊变量
        self.干员实例列表 = []

    def 初始化干员(self):
        """初始化干员实例"""
        for op in self.进驻干员:
            name = op["名称"]
            elite = op["精英等级"]
            self.干员实例列表.append(创建干员实例(name, elite, self.特殊变量))

    def 计算效率(self) -> dict:
        """计算会客室效率"""
        self.初始化干员()

        干员线索加成 = 0.0
        详情 = []
        for 干员 in self.干员实例列表:
            # 会客室的效率值取自线索速度
            if hasattr(干员, '基本属性') and '线索速度' in 干员.基本属性:
                线索速度 = 干员.基本属性['线索速度']
                干员线索加成 += 线索速度
            else:
                线索速度 = 0.0
            详情.append({
                "干员": 干员.名称 if hasattr(干员, '名称') else 干员.__class__.__name__,
                "精英等级": 干员.精英等级,
                "效率": 线索速度,
                "基本属性": 干员.基本属性
            })

        return {
            "会客室等级": self.等级,
            "提供好友位": RECEPTION_FRIEND_SLOTS[self.等级],
            "干员线索加成": f"+{干员线索加成:.1f}%",
            "电力消耗": RECEPTION_POWER[self.等级],
            "进驻人员": len(self.进驻干员),
            "干员详情": 详情,
        }


# ====================== 加工站基础数据 ======================
PROCESSING_POWER = {
    1: 10,
    2: 30,
    3: 60,
}


class 加工站效率计算器:
    """
    加工站效率计算器
    主要功能：加工副产物概率加成
    """

    def __init__(self, 等级: int, 进驻干员列表: list, 特殊变量: 特殊变量存储器 = None):
        self.等级 = 等级
        self.进驻干员 = 进驻干员列表
        self.特殊变量 = 特殊变量
        self.干员实例列表 = []

    def 初始化干员(self):
        """初始化干员实例"""
        for op in self.进驻干员:
            name = op["名称"]
            elite = op["精英等级"]
            self.干员实例列表.append(创建干员实例(name, elite, self.特殊变量))

    def 计算效率(self) -> dict:
        """计算加工站效率"""
        self.初始化干员()

        干员副产物加成 = 0.0
        详情 = []
        for 干员 in self.干员实例列表:
            效率 = 干员.计算效率()
            if hasattr(干员, '基本属性') and '副产物概率' in 干员.基本属性:
                干员副产物加成 += 干员.基本属性['副产物概率']
            详情.append({
                "干员": 干员.__class__.__name__,
                "精英等级": 干员.精英等级,
                "效率": 效率,
                "基本属性": 干员.基本属性
            })

        return {
            "加工站等级": self.等级,
            "干员副产物加成": f"+{干员副产物加成:.1f}%",
            "电力消耗": PROCESSING_POWER[self.等级],
            "进驻人员": len(self.进驻干员),
            "干员详情": 详情,
        }


# ====================== 办公室基础数据 ======================
OFFICE_RECRUIT_SLOTS = {
    1: 2,
    2: 3,
    3: 4,
}

OFFICE_POWER = {
    1: 10,
    2: 30,
    3: 60,
}


class 办公室效率计算器:
    """
    办公室效率计算器
    主要功能：公开招募栏位、人脉资源联络速度
    """

    def __init__(self, 等级: int, 进驻干员列表: list, 特殊变量: 特殊变量存储器 = None):
        self.等级 = 等级
        self.进驻干员 = 进驻干员列表
        self.特殊变量 = 特殊变量
        self.干员实例列表 = []

    def 初始化干员(self):
        """初始化干员实例"""
        for op in self.进驻干员:
            name = op["名称"]
            elite = op["精英等级"]
            self.干员实例列表.append(创建干员实例(name, elite, self.特殊变量))

    def 计算效率(self) -> dict:
        """计算办公室效率"""
        self.初始化干员()

        干员联络加成 = 0.0
        详情 = []
        for 干员 in self.干员实例列表:
            # 办公室的效率值取自联络速度
            if hasattr(干员, '基本属性') and '联络速度' in 干员.基本属性:
                联络速度 = 干员.基本属性['联络速度']
                干员联络加成 += 联络速度
            else:
                联络速度 = 0.0
            详情.append({
                "干员": 干员.名称 if hasattr(干员, '名称') else 干员.__class__.__name__,
                "精英等级": 干员.精英等级,
                "效率": 联络速度,
                "基本属性": 干员.基本属性
            })

        # 基础联络速度+5%，干员加成累加
        基础联络 = 5
        总联络速度 = 基础联络 + 干员联络加成

        return {
            "办公室等级": self.等级,
            "提供招募位": OFFICE_RECRUIT_SLOTS[self.等级],
            "基础联络速度": f"+{基础联络}%",
            "干员联络加成": f"+{干员联络加成:.1f}%",
            "总联络速度": f"+{总联络速度:.1f}%",
            "电力消耗": OFFICE_POWER[self.等级],
            "进驻人员": len(self.进驻干员),
            "干员详情": 详情,
        }


# ====================== 训练室基础数据 ======================
TRAINING_MASTERY_LIMIT = {
    1: 1,
    2: 2,
    3: 3,
}

TRAINING_POWER = {
    1: 10,
    2: 30,
    3: 60,
}


class 训练室效率计算器:
    """
    训练室效率计算器
    主要功能：技能专精训练速度加成
    训练位+协助位结构
    """

    def __init__(self, 等级: int, 进驻干员列表: list, 特殊变量: 特殊变量存储器 = None):
        self.等级 = 等级
        self.进驻干员 = 进驻干员列表
        self.特殊变量 = 特殊变量
        self.干员实例列表 = []

    def 初始化干员(self):
        """初始化干员实例"""
        for op in self.进驻干员:
            name = op["名称"]
            elite = op["精英等级"]
            self.干员实例列表.append(创建干员实例(name, elite, self.特殊变量))

    def 计算效率(self) -> dict:
        """计算训练室效率"""
        self.初始化干员()

        干员训练加成 = 0.0
        详情 = []
        for 干员 in self.干员实例列表:
            效率 = 干员.计算效率()
            if hasattr(干员, '基本属性') and '训练速度' in 干员.基本属性:
                干员训练加成 += 干员.基本属性['训练速度']
            详情.append({
                "干员": 干员.__class__.__name__,
                "精英等级": 干员.精英等级,
                "效率": 效率,
                "基本属性": 干员.基本属性
            })

        # 协助位基础+5%，干员加成累加
        基础训练 = 5 if len(self.进驻干员) > 1 else 0
        总训练速度 = 基础训练 + 干员训练加成

        return {
            "训练室等级": self.等级,
            "专精等级上限": TRAINING_MASTERY_LIMIT[self.等级],
            "基础训练速度": f"+{基础训练}%" if 基础训练 else "0%",
            "干员训练加成": f"+{干员训练加成:.1f}%",
            "总训练速度": f"+{总训练速度:.1f}%",
            "电力消耗": TRAINING_POWER[self.等级],
            "进驻人员": len(self.进驻干员),
            "干员详情": 详情,
        }


# ====================== 宿舍基础数据 ======================
DORMITORY_MOOD_RECOVERY = {
    1: 1.5 + 0.1 * 1,  # 1.6
    2: 1.5 + 0.1 * 2,  # 1.7
    3: 1.5 + 0.1 * 3,  # 1.8
    4: 1.5 + 0.1 * 4,  # 1.9
    5: 1.5 + 0.1 * 5,  # 2.0
}

DORMITORY_CAPACITY = 5  # 每间宿舍5个位置

DORMITORY_ATMOSPHERE_MAX = {
    1: 2000,
    2: 3000,
    3: 4000,
    4: 5000,
    5: 6000,
}


class 宿舍效率计算器:
    """
    宿舍效率计算器
    主要功能：干员心情恢复
    """

    def __init__(self, 等级: int, 进驻干员列表: list, 氛围值: int = None, 特殊变量: 特殊变量存储器 = None):
        self.等级 = 等级
        self.进驻干员 = 进驻干员列表
        # 默认氛围值为等级上限
        self.氛围值 = 氛围值 if 氛围值 is not None else DORMITORY_ATMOSPHERE_MAX.get(等级, 0)
        self.特殊变量 = 特殊变量
        self.干员实例列表 = []

    def 初始化干员(self):
        """初始化干员实例"""
        for op in self.进驻干员:
            name = op["名称"]
            elite = op["精英等级"]
            try:
                self.干员实例列表.append(创建干员实例(name, elite, self.特殊变量))
            except ValueError:
                # 宿舍可以进驻任意干员，未知干员使用默认属性
                self.干员实例列表.append(默认干员(name, elite))

    def 计算效率(self) -> dict:
        """计算宿舍效率"""
        self.初始化干员()

        干员心情加成 = 0.0
        详情 = []
        for 干员 in self.干员实例列表:
            # 宿舍的心情恢复从基本属性的心情恢复字段获取
            if hasattr(干员, '基本属性') and '心情恢复' in 干员.基本属性:
                心情恢复 = 干员.基本属性['心情恢复']
                干员心情加成 += 心情恢复
            else:
                心情恢复 = 0.0
            详情.append({
                "干员": 干员.名称 if hasattr(干员, '名称') else 干员.__class__.__name__,
                "精英等级": 干员.精英等级,
                "效率": 心情恢复,  # 使用心情恢复值
                "基本属性": 干员.基本属性
            })

        # 基础心情恢复 + 氛围值加成(0.0004*氛围) + 干员加成
        氛围加成 = 0.0004 * self.氛围值
        基础恢复 = DORMITORY_MOOD_RECOVERY[self.等级]
        总恢复速度 = 基础恢复 + 氛围加成 + 干员心情加成

        return {
            "宿舍等级": self.等级,
            "基础心情恢复": f"+{基础恢复:.2f}/时",
            "氛围加成": f"+{氛围加成:.2f}/时",
            "干员心情加成": f"+{干员心情加成:.2f}/时",
            "总恢复速度": f"+{总恢复速度:.2f}/时",
            "氛围值": self.氛围值,
            "进驻人员": len(self.进驻干员),
            "干员详情": 详情,
        }


# ====================== 控制中枢基础数据 ======================
CONTROL_MOOD_REDUCTION = 0.05  # 每个工作干员-0.05心情消耗

CONTROL_CAPACITY = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
}


class 控制中枢效率计算器:
    """
    控制中枢效率计算器
    主要功能：全员心情消耗减免
    """

    def __init__(self, 等级: int, 进驻干员列表: list, 全员心情消耗减免: float = 0, 特殊变量: 特殊变量存储器 = None):
        self.等级 = 等级
        self.进驻干员 = 进驻干员列表
        self.全员心情消耗减免 = 全员心情消耗减免
        self.特殊变量 = 特殊变量
        self.干员实例列表 = []

    def 初始化干员(self):
        """初始化干员实例"""
        for op in self.进驻干员:
            name = op["名称"]
            elite = op["精英等级"]
            self.干员实例列表.append(创建干员实例(name, elite, self.特殊变量))

    def 计算效率(self) -> dict:
        """计算控制中枢效率"""
        self.初始化干员()

        干员心情减免 = 0.0
        详情 = []
        for 干员 in self.干员实例列表:
            效率 = 干员.计算效率()
            if hasattr(干员, '基本属性') and '心情减免' in 干员.基本属性:
                干员心情减免 += 干员.基本属性['心情减免']
            详情.append({
                "干员": 干员.__class__.__name__,
                "精英等级": 干员.精英等级,
                "效率": 效率,
                "基本属性": 干员.基本属性
            })

        # 基础心情消耗减免 + 干员心情减免
        基础减免 = len(self.进驻干员) * CONTROL_MOOD_REDUCTION
        总减免 = 基础减免 + 干员心情减免 + self.全员心情消耗减免

        return {
            "控制中枢等级": self.等级,
            "基础心情减免": f"-{基础减免:.2f}/时",
            "干员心情减免": f"-{干员心情减免:.2f}/时",
            "全员心情减免": f"-{self.全员心情消耗减免:.2f}/时",
            "总心情减免": f"-{总减免:.2f}/时",
            "进驻人员": len(self.进驻干员),
            "干员详情": 详情,
        }


# ====================== 活动室基础数据 ======================
ACTIVITY_ATMOSPHERE_LIMIT = {
    1: 1000,
    2: 3000,
    3: 5000,
}


class 活动室效率计算器:
    """
    活动室效率计算器
    主要功能：活动信赖获取
    无电力消耗
    """

    def __init__(self, 等级: int, 使用干员: dict = None, 氛围值: int = 0, 特殊变量: 特殊变量存储器 = None):
        self.等级 = 等级
        self.使用干员 = 使用干员  # 活动室不是进驻，是"使用"
        self.氛围值 = 氛围值
        self.特殊变量 = 特殊变量
        self.干员实例 = None

    def 初始化干员(self):
        """初始化干员实例"""
        if self.使用干员:
            name = self.使用干员["名称"]
            elite = self.使用干员["精英等级"]
            self.干员实例 = 创建干员实例(name, elite, self.特殊变量)

    def 计算效率(self) -> dict:
        """计算活动室效率"""
        self.初始化干员()

        干员信赖加成 = 0.0
        if self.干员实例:
            效率 = self.干员实例.计算效率()
            if hasattr(self.干员实例, '基本属性') and '信赖加成' in self.干员实例.基本属性:
                干员信赖加成 = self.干员实例.基本属性['信赖加成']
            详情 = [{
                "干员": self.干员实例.__class__.__name__,
                "精英等级": self.干员实例.精英等级,
                "效率": 效率,
                "基本属性": self.干员实例.基本属性
            }]
        else:
            详情 = []

        # 氛围值影响信赖获取
        氛围加成 = self.氛围值 / 1000 * 10  # 每1000氛围+10%

        return {
            "活动室等级": self.等级,
            "氛围值上限": ACTIVITY_ATMOSPHERE_LIMIT[self.等级],
            "当前氛围值": self.氛围值,
            "氛围加成": f"+{氛围加成:.1f}%",
            "干员信赖加成": f"+{干员信赖加成:.1f}%" if 干员信赖加成 else "0%",
            "使用干员": self.使用干员["名称"] if self.使用干员 else "无",
            "干员详情": 详情,
        }


# ====================== 贸易站效率计算器（从station_calculator导入） ======================
# 贸易站计算器已在 trade_station_calculator.py 中定义


# ====================== 制造站效率计算器（从station_calculator导入） ======================
# 制造站计算器已在 station_calculator.py 中定义