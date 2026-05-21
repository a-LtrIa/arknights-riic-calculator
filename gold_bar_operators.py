"""
明日方舟基建 - 制造站干员类
包含所有90名制造站干员
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class 加成结果:
    """计算结果"""
    干员名称: str = ""
    赤金加成: float = 0.0
    作战记录加成: float = 0.0
    源石加成: float = 0.0
    通用加成: float = 0.0
    仓库加成: int = 0
    心情修正: float = 0.0
    特殊加成: dict = field(default_factory=dict)

    @property
    def 总加成(self) -> float:
        return self.赤金加成 + self.作战记录加成 + self.源石加成 + self.通用加成

    def __str__(self) -> str:
        parts = []
        if self.通用加成:
            parts.append(f"通用+{self.通用加成}%")
        if self.赤金加成:
            parts.append(f"赤金+{self.赤金加成}%")
        if self.作战记录加成:
            parts.append(f"作战记录+{self.作战记录加成}%")
        if self.源石加成:
            parts.append(f"源石+{self.源石加成}%")
        if self.仓库加成:
            parts.append(f"仓库+{self.仓库加成}")
        if self.心情修正 != 0:
            parts.append(f"心情{'+' if self.心情修正 > 0 else ''}{self.心情修正}")
        return f"{self.干员名称}: {', '.join(parts) if parts else '无加成'} (总计: {self.总加成}%)"


class 制造站干员基类(ABC):
    def __init__(self, 精英等级: int = 0):
        self.精英等级 = 精英等级

    @abstractmethod
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        pass

    @property
    @abstractmethod
    def 干员名称(self) -> str:
        pass


def 获取上下文数值(上下文: dict, 键: str, 默认值=0):
    if 上下文 is None:
        return 默认值
    return 上下文.get(键, 默认值)


# ==================== 第一批干员 (A-L) ====================

class Castle_3(制造站干员基类):
    """Castle-3 - 作战指导录像"""
    @property
    def 干员名称(self) -> str:
        return "Castle-3"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=30.0)


class Miss_Christine(制造站干员基类):
    """Miss.Christine - 午休好去处"""
    @property
    def 干员名称(self) -> str:
        return "Miss.Christine"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=10, 心情修正=-0.25)


class 克洛丝(制造站干员基类):
    """克洛丝 - 慢性子"""
    @property
    def 干员名称(self) -> str:
        return "克洛丝"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0, 特殊加成={"暖机": {"初始": 15, "每小时": 2, "最大": 25}})


class 冬时_E0(制造站干员基类):
    """冬时 - 科学改造"""
    @property
    def 干员名称(self) -> str:
        return "冬时"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=5)


class 冬时_E1(制造站干员基类):
    """冬时 - 流程优化"""
    @property
    def 干员名称(self) -> str:
        return "冬时"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=10, 仓库加成=5)


class 刻俄柏_E0(制造站干员基类):
    """刻俄柏 - "都想要" """
    @property
    def 干员名称(self) -> str:
        return "刻俄柏"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=8, 心情修正=-0.25)


class 刻俄柏_E2(制造站干员基类):
    """刻俄柏 - "等不及" """
    @property
    def 干员名称(self) -> str:
        return "刻俄柏"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=20.0, 特殊加成={"暖机": {"初始": 20, "每小时": 1, "最大": 25}})


class 卡缇(制造站干员基类):
    """卡缇 - 仓库整备·α"""
    @property
    def 干员名称(self) -> str:
        return "卡缇"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=6, 通用加成=10)


class 卡达_E0(制造站干员基类):
    """卡达 - Vlog"""
    @property
    def 干员名称(self) -> str:
        return "卡达"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 特殊加成={"作战记录心情减免": 0.25})


class 卡达_E1(制造站干员基类):
    """卡达 - 剪辑·β"""
    @property
    def 干员名称(self) -> str:
        return "卡达"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=15)


class 历阵锐枪芬_E0(制造站干员基类):
    """历阵锐枪芬 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "历阵锐枪芬"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 历阵锐枪芬_E2(制造站干员基类):
    """历阵锐枪芬 - 重聚时光"""
    @property
    def 干员名称(self) -> str:
        return "历阵锐枪芬"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=10.0, 特殊加成={"A1小队": {"每个干员": 10}})


class 史都华德(制造站干员基类):
    """史都华德 - 标准化·β"""
    @property
    def 干员名称(self) -> str:
        return "史都华德"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 圣约送葬人_E0(制造站干员基类):
    """圣约送葬人 - 送葬人·α"""
    @property
    def 干员名称(self) -> str:
        return "圣约送葬人"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=30.0)


class 圣约送葬人_E1(制造站干员基类):
    """圣约送葬人 - 送葬人·β"""
    @property
    def 干员名称(self) -> str:
        return "圣约送葬人"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=35.0)


class 地灵_E0(制造站干员基类):
    """地灵 - 地质学·α"""
    @property
    def 干员名称(self) -> str:
        return "地灵"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=30.0)


class 地灵_E1(制造站干员基类):
    """地灵 - 地质学·β"""
    @property
    def 干员名称(self) -> str:
        return "地灵"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=35.0)


class 多萝西_E0(制造站干员基类):
    """多萝西 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "多萝西"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 多萝西_E2(制造站干员基类):
    """多萝西 - 莱茵科技·α"""
    @property
    def 干员名称(self) -> str:
        return "多萝西"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0, 特殊加成={"莱茵科技每个": 5})


class 夜刀(制造站干员基类):
    """夜刀 - 仓库整备·α"""
    @property
    def 干员名称(self) -> str:
        return "夜刀"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=6, 通用加成=10)


class 夜烟(制造站干员基类):
    """夜烟 - 金属工艺·α"""
    @property
    def 干员名称(self) -> str:
        return "夜烟"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 赤金加成=30.0)


class 娜仁图亚(制造站干员基类):
    """娜仁图亚 - 齐心沙盗"""
    @property
    def 干员名称(self) -> str:
        return "娜仁图亚"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        宿舍等级列表 = 获取上下文数值(上下文, "宿舍等级列表", [])
        return 加成结果(干员名称=self.干员名称, 赤金加成=sum(宿舍等级列表) * 1.0)


class 娜斯提(制造站干员基类):
    """娜斯提 - 造价高昂"""
    @property
    def 干员名称(self) -> str:
        return "娜斯提"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        莱茵数量 = min(获取上下文数值(上下文, "莱茵生命干员数", 0), 5)
        return 加成结果(干员名称=self.干员名称, 赤金加成=莱茵数量 * 3.0)


class 导火索_E0(制造站干员基类):
    """导火索 - 行动派"""
    @property
    def 干员名称(self) -> str:
        return "导火索"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=20.0, 仓库加成=-8)


class 导火索_E2(制造站干员基类):
    """导火索 - 收纳达人"""
    @property
    def 干员名称(self) -> str:
        return "导火索"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=16, 心情修正=-0.25)


class 帕拉斯_E0(制造站干员基类):
    """帕拉斯 - 服从指令"""
    @property
    def 干员名称(self) -> str:
        return "帕拉斯"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 帕拉斯_E2(制造站干员基类):
    """帕拉斯 - 服从指令·α"""
    @property
    def 干员名称(self) -> str:
        return "帕拉斯"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=30.0)


class 异客_E0(制造站干员基类):
    """异客 - 商业谈判"""
    @property
    def 干员名称(self) -> str:
        return "异客"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 异客_E1(制造站干员基类):
    """异客 - 商业谈判·α"""
    @property
    def 干员名称(self) -> str:
        return "异客"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=30.0)


class 异客_E2(制造站干员基类):
    """异客 - 商业谈判·β"""
    @property
    def 干员名称(self) -> str:
        return "异客"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=35.0)


class 弑君者_E0(制造站干员基类):
    """弑君者 - 战略纵横"""
    @property
    def 干员名称(self) -> str:
        return "弑君者"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=20.0)


class 弑君者_E2(制造站干员基类):
    """弑君者 - 战略纵横·α"""
    @property
    def 干员名称(self) -> str:
        return "弑君者"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        控制中枢干员 = 获取上下文数值(上下文, "控制中枢干员数", 0)
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0 + 控制中枢干员 * 2)


class 引星棘刺_E0(制造站干员基类):
    """引星棘刺 - 金属工艺·α"""
    @property
    def 干员名称(self) -> str:
        return "引星棘刺"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 赤金加成=30.0)


class 引星棘刺_E2(制造站干员基类):
    """引星棘刺 - 原质塑金副产物"""
    @property
    def 干员名称(self) -> str:
        return "引星棘刺"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        贸易站数量 = 获取上下文数值(上下文, "贸易站数量", 0)
        return 加成结果(干员名称=self.干员名称, 赤金加成=贸易站数量 * 3.0)


class 怒潮凛冬_E0(制造站干员基类):
    """怒潮凛冬 - 战略纵横·α"""
    @property
    def 干员名称(self) -> str:
        return "怒潮凛冬"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 怒潮凛冬_E1(制造站干员基类):
    """怒潮凛冬 - 战略纵横·β"""
    @property
    def 干员名称(self) -> str:
        return "怒潮凛冬"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=30.0)


class 怒潮凛冬_E2(制造站干员基类):
    """怒潮凛冬 - 冰霜先锋·α"""
    @property
    def 干员名称(self) -> str:
        return "怒潮凛冬"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=35.0)


class 截云_E0(制造站干员基类):
    """截云 - 人间烟火"""
    @property
    def 干员名称(self) -> str:
        return "截云"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        人间烟火 = 获取上下文数值(上下文, "人间烟火", 0)
        return 加成结果(干员名称=self.干员名称, 通用加成=人间烟火 // 3)


class 截云_E2(制造站干员基类):
    """截云 - 巫术结晶"""
    @property
    def 干员名称(self) -> str:
        return "截云"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        巫术结晶 = 获取上下文数值(上下文, "巫术结晶", 0)
        return 加成结果(干员名称=self.干员名称, 通用加成=巫术结晶)


class 掠风_E0(制造站干员基类):
    """掠风 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "掠风"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 掠风_E2(制造站干员基类):
    """掠风 - 配合意识"""
    @property
    def 干员名称(self) -> str:
        return "掠风"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        其他加成 = 获取上下文数值(上下文, "其他干员加成总计", 0)
        return 加成结果(干员名称=self.干员名称, 通用加成=min(其他加成 * 0.05, 40))


class 斑点(制造站干员基类):
    """斑点 - 金属工艺·α"""
    @property
    def 干员名称(self) -> str:
        return "斑点"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 赤金加成=30.0)


class 断罪者_E0(制造站干员基类):
    """断罪者 - 作战指导录像"""
    @property
    def 干员名称(self) -> str:
        return "断罪者"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=30.0)


class 断罪者_E1(制造站干员基类):
    """断罪者 - 拳术指导录像"""
    @property
    def 干员名称(self) -> str:
        return "断罪者"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=35.0)


class 星源_E0(制造站干员基类):
    """星源 - 莱茵科技·α"""
    @property
    def 干员名称(self) -> str:
        return "星源"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 星源_E1(制造站干员基类):
    """星源 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "星源"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 星源_E2(制造站干员基类):
    """星源 - 莱茵科技·β"""
    @property
    def 干员名称(self) -> str:
        return "星源"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 月见夜_E0(制造站干员基类):
    """月见夜 - 作战指导录像"""
    @property
    def 干员名称(self) -> str:
        return "月见夜"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=30.0)


class 月见夜_E1(制造站干员基类):
    """月见夜 - 拳术指导录像"""
    @property
    def 干员名称(self) -> str:
        return "月见夜"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=35.0)


class 杏仁_E0(制造站干员基类):
    """杏仁 - 小奇思"""
    @property
    def 干员名称(self) -> str:
        return "杏仁"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 赤金加成=25.0, 心情修正=0.25)


class 杏仁_E2(制造站干员基类):
    """杏仁 - 挑大梁"""
    @property
    def 干员名称(self) -> str:
        return "杏仁"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        黑钢数量 = min(获取上下文数值(上下文, "黑钢国际干员数", 0), 3)
        return 加成结果(干员名称=self.干员名称, 赤金加成=黑钢数量 * 2.0, 心情修正=-0.15)


class 杰西卡_E0(制造站干员基类):
    """杰西卡 - 仓库整备·α"""
    @property
    def 干员名称(self) -> str:
        return "杰西卡"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=6, 通用加成=10)


class 杰西卡_E1(制造站干员基类):
    """杰西卡 - 仓库整备·β"""
    @property
    def 干员名称(self) -> str:
        return "杰西卡"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=10, 通用加成=15)


class 梅尔_E0(制造站干员基类):
    """梅尔 - 莱茵科技·α"""
    @property
    def 干员名称(self) -> str:
        return "梅尔"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 梅尔_E2(制造站干员基类):
    """梅尔 - 莱茵科技·β"""
    @property
    def 干员名称(self) -> str:
        return "梅尔"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 森蚺_E0(制造站干员基类):
    """森蚺 - 仓库整备·α"""
    @property
    def 干员名称(self) -> str:
        return "森蚺"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=6, 通用加成=10)


class 森蚺_E2(制造站干员基类):
    """森蚺 - 工程机器人·α"""
    @property
    def 干员名称(self) -> str:
        return "森蚺"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        机器人 = min(获取上下文数值(上下文, "工程机器人数量", 0), 64)
        return 加成结果(干员名称=self.干员名称, 通用加成=(机器人 // 8) * 5)


class 槐琥_E0(制造站干员基类):
    """槐琥 - 配合意识"""
    @property
    def 干员名称(self) -> str:
        return "槐琥"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        其他加成 = 获取上下文数值(上下文, "其他干员加成总计", 0)
        return 加成结果(干员名称=self.干员名称, 通用加成=min(其他加成 * 0.05, 40))


class 槐琥_E2(制造站干员基类):
    """槐琥 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "槐琥"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 水月_E0(制造站干员基类):
    """水月 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "水月"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 水月_E2(制造站干员基类):
    """水月 - 标准化·β"""
    @property
    def 干员名称(self) -> str:
        return "水月"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 泡普员_E0(制造站干员基类):
    """泡普员 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "泡普员"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 泡普员_E1(制造站干员基类):
    """泡普员 - 仓库整备·β"""
    @property
    def 干员名称(self) -> str:
        return "泡普员"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=10, 通用加成=10)


class 泡泡_E0(制造站干员基类):
    """泡泡 - 仓库整备·α"""
    @property
    def 干员名称(self) -> str:
        return "泡泡"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=6, 通用加成=10)


class 泡泡_E1(制造站干员基类):
    """泡泡 - 仓库整备·β"""
    @property
    def 干员名称(self) -> str:
        return "泡泡"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=10, 通用加成=15)


class 泰拉大陆调查团(制造站干员基类):
    """泰拉大陆调查团 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "泰拉大陆调查团"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 洋灰_E0(制造站干员基类):
    """洋灰 - 地质学·α"""
    @property
    def 干员名称(self) -> str:
        return "洋灰"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=30.0)


class 洋灰_E1(制造站干员基类):
    """洋灰 - 地质学·β"""
    @property
    def 干员名称(self) -> str:
        return "洋灰"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=35.0)


class 流星_E0(制造站干员基类):
    """流星 - 作战指导录像"""
    @property
    def 干员名称(self) -> str:
        return "流星"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=30.0)


class 流星_E1(制造站干员基类):
    """流星 - 狙击教程"""
    @property
    def 干员名称(self) -> str:
        return "流星"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=35.0)


class 海沫_E0(制造站干员基类):
    """海沫 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "海沫"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 海沫_E2(制造站干员基类):
    """海沫 - 配合意识"""
    @property
    def 干员名称(self) -> str:
        return "海沫"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        其他加成 = 获取上下文数值(上下文, "其他干员加成总计", 0)
        return 加成结果(干员名称=self.干员名称, 通用加成=min(其他加成 * 0.05, 40))


class 淬羽赫默_E0(制造站干员基类):
    """淬羽赫默 - 莱茵科技·α"""
    @property
    def 干员名称(self) -> str:
        return "淬羽赫默"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 淬羽赫默_E2(制造站干员基类):
    """淬羽赫默 - 莱茵科技·β"""
    @property
    def 干员名称(self) -> str:
        return "淬羽赫默"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


# ==================== 第二批干员 (M-Z) ====================

class 清流(制造站干员基类):
    """清流 - 再生能源"""
    @property
    def 干员名称(self) -> str:
        return "清流"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        贸易站数量 = 获取上下文数值(上下文, "贸易站数量", 0)
        return 加成结果(干员名称=self.干员名称, 赤金加成=贸易站数量 * 20.0)


class 清道夫_E0(制造站干员基类):
    """清道夫 - 标准化·β"""
    @property
    def 干员名称(self) -> str:
        return "清道夫"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 清道夫_E1(制造站干员基类):
    """清道夫 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "清道夫"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 温米(制造站干员基类):
    """温米 - 金属工艺·α"""
    @property
    def 干员名称(self) -> str:
        return "温米"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 赤金加成=30.0)


class 温蒂_E0(制造站干员基类):
    """温蒂 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "温蒂"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 温蒂_E1(制造站干员基类):
    """温蒂 - 仓库整备·β"""
    @property
    def 干员名称(self) -> str:
        return "温蒂"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=10, 通用加成=15)


class 温蒂_E2(制造站干员基类):
    """温蒂 - 配合意识"""
    @property
    def 干员名称(self) -> str:
        return "温蒂"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        其他加成 = 获取上下文数值(上下文, "其他干员加成总计", 0)
        return 加成结果(干员名称=self.干员名称, 通用加成=min(其他加成 * 0.05, 40))


class 溯光星源_E0(制造站干员基类):
    """溯光星源 - 莱茵科技·α"""
    @property
    def 干员名称(self) -> str:
        return "溯光星源"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 溯光星源_E2(制造站干员基类):
    """溯光星源 - 莱茵科技·β"""
    @property
    def 干员名称(self) -> str:
        return "溯光星源"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 火神_E0(制造站干员基类):
    """火神 - 仓库整备·α"""
    @property
    def 干员名称(self) -> str:
        return "火神"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=6, 通用加成=10)


class 火神_E1(制造站干员基类):
    """火神 - 仓库整备·β"""
    @property
    def 干员名称(self) -> str:
        return "火神"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=10, 通用加成=15)


class 火神_E2(制造站干员基类):
    """火神 - 配合意识"""
    @property
    def 干员名称(self) -> str:
        return "火神"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        其他加成 = 获取上下文数值(上下文, "其他干员加成总计", 0)
        return 加成结果(干员名称=self.干员名称, 通用加成=min(其他加成 * 0.05, 40))


class 灰毫_E0(制造站干员基类):
    """灰毫 - 红松骑士团·α"""
    @property
    def 干员名称(self) -> str:
        return "灰毫"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 灰毫_E2(制造站干员基类):
    """灰毫 - 红松骑士团·β"""
    @property
    def 干员名称(self) -> str:
        return "灰毫"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        红松数量 = min(获取上下文数值(上下文, "红松骑士团干员数", 0), 4)
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0 + 红松数量 * 5.0)


class 炎熔_E0(制造站干员基类):
    """炎熔 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "炎熔"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 炎熔_E1(制造站干员基类):
    """炎熔 - 地质学·α"""
    @property
    def 干员名称(self) -> str:
        return "炎熔"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=30.0)


class 烈夏_E0(制造站干员基类):
    """烈夏 - 仓库整备·α"""
    @property
    def 干员名称(self) -> str:
        return "烈夏"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=6, 通用加成=10)


class 烈夏_E2(制造站干员基类):
    """烈夏 - 冬日补养计划"""
    @property
    def 干员名称(self) -> str:
        return "烈夏"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=30.0, 心情修正=-0.25)


class 玛露西尔_E0(制造站干员基类):
    """玛露西尔 - 作战指导录像"""
    @property
    def 干员名称(self) -> str:
        return "玛露西尔"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=30.0)


class 玛露西尔_E2(制造站干员基类):
    """玛露西尔 - 拳术指导录像"""
    @property
    def 干员名称(self) -> str:
        return "玛露西尔"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=35.0)


class 白雪_E0(制造站干员基类):
    """白雪 - 地质学·α"""
    @property
    def 干员名称(self) -> str:
        return "白雪"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=30.0)


class 白雪_E1(制造站干员基类):
    """白雪 - 地质学·β"""
    @property
    def 干员名称(self) -> str:
        return "白雪"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=35.0)


class 白面鸮_E0(制造站干员基类):
    """白面鸮 - 莱茵科技·α"""
    @property
    def 干员名称(self) -> str:
        return "白面鸮"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 白面鸮_E2(制造站干员基类):
    """白面鸮 - 莱茵科技·β"""
    @property
    def 干员名称(self) -> str:
        return "白面鸮"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 石棉_E0(制造站干员基类):
    """石棉 - 地质学·α"""
    @property
    def 干员名称(self) -> str:
        return "石棉"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=30.0)


class 石棉_E1(制造站干员基类):
    """石棉 - 地质学·β"""
    @property
    def 干员名称(self) -> str:
        return "石棉"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=35.0)


class 石英_E0(制造站干员基类):
    """石英 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "石英"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 石英_E1(制造站干员基类):
    """石英 - 仓库整备·α"""
    @property
    def 干员名称(self) -> str:
        return "石英"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=6, 通用加成=10)


class 砾(制造站干员基类):
    """砾 - 金属工艺·β"""
    @property
    def 干员名称(self) -> str:
        return "砾"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 赤金加成=35.0)


class 稀音_E0(制造站干员基类):
    """稀音 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "稀音"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 稀音_E1(制造站干员基类):
    """稀音 - 摄影指导·α"""
    @property
    def 干员名称(self) -> str:
        return "稀音"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=30.0)


class 米格鲁_E0(制造站干员基类):
    """米格鲁 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "米格鲁"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 米格鲁_E1(制造站干员基类):
    """米格鲁 - 仓库整备·β"""
    @property
    def 干员名称(self) -> str:
        return "米格鲁"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=10, 通用加成=15)


class 红云_E0(制造站干员基类):
    """红云 - 作战指导录像"""
    @property
    def 干员名称(self) -> str:
        return "红云"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=30.0)


class 红云_E1(制造站干员基类):
    """红云 - 狙击教程"""
    @property
    def 干员名称(self) -> str:
        return "红云"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=35.0)


class 红豆_E0(制造站干员基类):
    """红豆 - 标准化·β"""
    @property
    def 干员名称(self) -> str:
        return "红豆"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 红豆_E1(制造站干员基类):
    """红豆 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "红豆"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 维伊_E0(制造站干员基类):
    """维伊 - 商业谈判"""
    @property
    def 干员名称(self) -> str:
        return "维伊"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 维伊_E1(制造站干员基类):
    """维伊 - 商业谈判·α"""
    @property
    def 干员名称(self) -> str:
        return "维伊"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=30.0)


class 维伊_E2(制造站干员基类):
    """维伊 - 商业谈判·β"""
    @property
    def 干员名称(self) -> str:
        return "维伊"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=35.0)


class 罗比菈塔_E0(制造站干员基类):
    """罗比菈塔 - 地质学·α"""
    @property
    def 干员名称(self) -> str:
        return "罗比菈塔"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=30.0)


class 罗比菈塔_E2(制造站干员基类):
    """罗比菈塔 - 地质学·β"""
    @property
    def 干员名称(self) -> str:
        return "罗比菈塔"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=35.0)


class 至简_E0(制造站干员基类):
    """至简 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "至简"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 至简_E1(制造站干员基类):
    """至简 - 得心应手"""
    @property
    def 干员名称(self) -> str:
        return "至简"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0, 仓库加成=6)


class 艾雅法拉_E0(制造站干员基类):
    """艾雅法拉 - 标准化·β"""
    @property
    def 干员名称(self) -> str:
        return "艾雅法拉"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 艾雅法拉_E2(制造站干员基类):
    """艾雅法拉 - 火山"""
    @property
    def 干员名称(self) -> str:
        return "艾雅法拉"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=30.0)


class 芬_E0(制造站干员基类):
    """芬 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "芬"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 芬_E1(制造站干员基类):
    """芬 - 仓库整备·β"""
    @property
    def 干员名称(self) -> str:
        return "芬"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=10, 通用加成=15)


class 苍苔(制造站干员基类):
    """苍苔 - 金属工艺·α"""
    @property
    def 干员名称(self) -> str:
        return "苍苔"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 赤金加成=30.0)


class 薄绿_E0(制造站干员基类):
    """薄绿 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "薄绿"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 薄绿_E1(制造站干员基类):
    """薄绿 - 地质学·α"""
    @property
    def 干员名称(self) -> str:
        return "薄绿"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=30.0)


class 蛇屠箱(制造站干员基类):
    """蛇屠箱 - 仓库整备·β"""
    @property
    def 干员名称(self) -> str:
        return "蛇屠箱"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=10, 通用加成=10)


class 裁度_E0(制造站干员基类):
    """裁度 - 量体裁衣"""
    @property
    def 干员名称(self) -> str:
        return "裁度"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=20.0, 心情修正=0.25)


class 裁度_E2(制造站干员基类):
    """裁度 - 得心应手"""
    @property
    def 干员名称(self) -> str:
        return "裁度"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0, 仓库加成=6)


class 裂响(制造站干员基类):
    """裂响 - "连轴转" """
    @property
    def 干员名称(self) -> str:
        return "裂响"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=35.0, 心情修正=0.25)


class 褐果_E0(制造站干员基类):
    """褐果 - 标准化·α"""
    @property
    def 干员名称(self) -> str:
        return "褐果"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 褐果_E1(制造站干员基类):
    """褐果 - 地质学·α"""
    @property
    def 干员名称(self) -> str:
        return "褐果"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=30.0)


class 调香师(制造站干员基类):
    """调香师 - 标准化·β"""
    @property
    def 干员名称(self) -> str:
        return "调香师"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 豆苗_E0(制造站干员基类):
    """豆苗 - 磐蟹·豆豆"""
    @property
    def 干员名称(self) -> str:
        return "豆苗"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 豆苗_E1(制造站干员基类):
    """豆苗 - 磐蟹·阿盘"""
    @property
    def 干员名称(self) -> str:
        return "豆苗"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=8, 心情修正=-0.25)


class 贝娜(制造站干员基类):
    """贝娜 - "可靠"助手"""
    @property
    def 干员名称(self) -> str:
        return "贝娜"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=-20.0, 仓库加成=17, 心情修正=-0.25)


class 赫默_E0(制造站干员基类):
    """赫默 - 莱茵科技·α"""
    @property
    def 干员名称(self) -> str:
        return "赫默"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 赫默_E2(制造站干员基类):
    """赫默 - 莱茵科技·β"""
    @property
    def 干员名称(self) -> str:
        return "赫默"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 远牙_E0(制造站干员基类):
    """远牙 - 红松骑士团·α"""
    @property
    def 干员名称(self) -> str:
        return "远牙"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 远牙_E2(制造站干员基类):
    """远牙 - 红松骑士团·β"""
    @property
    def 干员名称(self) -> str:
        return "远牙"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        红松数量 = min(获取上下文数值(上下文, "红松骑士团干员数", 0), 4)
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0 + 红松数量 * 5.0)


class 迷迭香_0超感(制造站干员基类):
    """迷迭香 - 超感 (精英0)"""
    @property
    def 干员名称(self) -> str:
        return "迷迭香"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 特殊加成={"感知信息": 获取上下文数值(上下文, "感知信息", 0)})


class 迷迭香_0念力(制造站干员基类):
    """迷迭香 - 念力 (精英0)"""
    @property
    def 干员名称(self) -> str:
        return "迷迭香"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        思维链环 = 获取上下文数值(上下文, "思维链环", 0)
        return 加成结果(干员名称=self.干员名称, 通用加成=思维链环 // 2)


class 迷迭香_2意识实体(制造站干员基类):
    """迷迭香 - 意识实体 (精英2)"""
    @property
    def 干员名称(self) -> str:
        return "迷迭香"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        思维链环 = 获取上下文数值(上下文, "思维链环", 0)
        return 加成结果(干员名称=self.干员名称, 通用加成=思维链环)


class 酒神_E0(制造站干员基类):
    """酒神 - 镜中影"""
    @property
    def 干员名称(self) -> str:
        return "酒神"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=20.0, 心情修正=-0.25)


class 酒神_E2(制造站干员基类):
    """酒神 - 戏中人"""
    @property
    def 干员名称(self) -> str:
        return "酒神"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=35.0, 心情修正=-0.25)


class 野鬃_E0(制造站干员基类):
    """野鬃 - 红松骑士团·α"""
    @property
    def 干员名称(self) -> str:
        return "野鬃"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=15.0)


class 野鬃_E2(制造站干员基类):
    """野鬃 - 红松骑士团·β"""
    @property
    def 干员名称(self) -> str:
        return "野鬃"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        红松数量 = min(获取上下文数值(上下文, "红松骑士团干员数", 0), 4)
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0 + 红松数量 * 5.0)


class 钼铅_E0(制造站干员基类):
    """钼铅 - 行动派"""
    @property
    def 干员名称(self) -> str:
        return "钼铅"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=20.0, 仓库加成=-8)


class 钼铅_E2(制造站干员基类):
    """钼铅 - 收纳达人"""
    @property
    def 干员名称(self) -> str:
        return "钼铅"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=16, 心情修正=-0.25)


class 铅踝_E0(制造站干员基类):
    """铅踝 - 模糊视线"""
    @property
    def 干员名称(self) -> str:
        return "铅踝"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        心情落差 = 获取上下文数值(上下文, "心情落差", 0)
        惩罚 = (心情落差 // 4) * 5
        return 加成结果(干员名称=self.干员名称, 通用加成=max(30.0 - 惩罚, 0))


class 铅踝_E1(制造站干员基类):
    """铅踝 - 窗外雪啸"""
    @property
    def 干员名称(self) -> str:
        return "铅踝"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        心情落差 = 获取上下文数值(上下文, "心情落差", 0)
        if 心情落差 > 12:
            return 加成结果(干员名称=self.干员名称, 通用加成=10.0, 仓库加成=6)
        return 加成结果(干员名称=self.干员名称, 仓库加成=6)


class 锡兰(制造站干员基类):
    """锡兰 - 源石研究"""
    @property
    def 干员名称(self) -> str:
        return "锡兰"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 源石加成=35.0)


class 阿兰娜_E0(制造站干员基类):
    """阿兰娜 - 机械精通·α"""
    @property
    def 干员名称(self) -> str:
        return "阿兰娜"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        作业平台 = 获取上下文数值(上下文, "作业平台数量", 0)
        return 加成结果(干员名称=self.干员名称, 赤金加成=作业平台 * 5.0)


class 阿兰娜_E2(制造站干员基类):
    """阿兰娜 - 机械精通·β + 搭把手"""
    @property
    def 干员名称(self) -> str:
        return "阿兰娜"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        作业平台 = 获取上下文数值(上下文, "作业平台数量", 0)
        同站干员 = 获取上下文数值(上下文, "同制造站干员", [])
        return 加成结果(
            干员名称=self.干员名称,
            赤金加成=作业平台 * 10.0 + (15.0 if "温米" in 同站干员 else 0.0)
        )


class 阿罗玛_E0(制造站干员基类):
    """阿罗玛 - 净味香氛"""
    @property
    def 干员名称(self) -> str:
        return "阿罗玛"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 赤金加成=25.0, 心情修正=0.25)


class 阿罗玛_E2(制造站干员基类):
    """阿罗玛 - 例行清扫"""
    @property
    def 干员名称(self) -> str:
        return "阿罗玛"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=20.0, 特殊加成={"暖机": {"初始": 0, "每小时": 2, "最大": 20}})


class 雪猎_E0(制造站干员基类):
    """雪猎 - 虔信"""
    @property
    def 干员名称(self) -> str:
        return "雪猎"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=20.0, 心情修正=0.25)


class 雪猎_E2(制造站干员基类):
    """雪猎 - 独当一面"""
    @property
    def 干员名称(self) -> str:
        return "雪猎"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=30.0, 心情修正=0.25)


class 霜叶(制造站干员基类):
    """霜叶 - 作战指导录像"""
    @property
    def 干员名称(self) -> str:
        return "霜叶"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=30.0)


class 食铁兽_E0(制造站干员基类):
    """食铁兽 - 作战指导录像"""
    @property
    def 干员名称(self) -> str:
        return "食铁兽"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=30.0)


class 食铁兽_E2(制造站干员基类):
    """食铁兽 - 拳术指导录像"""
    @property
    def 干员名称(self) -> str:
        return "食铁兽"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 作战记录加成=35.0)


class 香草(制造站干员基类):
    """香草 - 标准化·β"""
    @property
    def 干员名称(self) -> str:
        return "香草"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 通用加成=25.0)


class 黍_E0(制造站干员基类):
    """黍 - 春雷响，万物长"""
    @property
    def 干员名称(self) -> str:
        return "黍"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 特殊加成={"制造站心情减免": 0.1})


class 黍_E2(制造站干员基类):
    """黍 - 稻禾厚，顺秋收"""
    @property
    def 干员名称(self) -> str:
        return "黍"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        人间烟火 = 获取上下文数值(上下文, "人间烟火", 0)
        return 加成结果(干员名称=self.干员名称, 通用加成=人间烟火 // 3)


class 黑角(制造站干员基类):
    """黑角 - 仓库整备·β"""
    @property
    def 干员名称(self) -> str:
        return "黑角"
    def 计算加成(self, 上下文: dict = None) -> 加成结果:
        return 加成结果(干员名称=self.干员名称, 仓库加成=10, 通用加成=10)


# ==================== 干员注册表 ====================

制造站干员注册表: dict = {
    "Castle-3": Castle_3,
    "Miss.Christine": Miss_Christine,
    "克洛丝": 克洛丝,
    "冬时": 冬时_E0,
    "刻俄柏": 刻俄柏_E0,
    "卡缇": 卡缇,
    "卡达": 卡达_E0,
    "历阵锐枪芬": 历阵锐枪芬_E0,
    "史都华德": 史都华德,
    "圣约送葬人": 圣约送葬人_E0,
    "地灵": 地灵_E0,
    "多萝西": 多萝西_E0,
    "夜刀": 夜刀,
    "夜烟": 夜烟,
    "娜仁图亚": 娜仁图亚,
    "娜斯提": 娜斯提,
    "导火索": 导火索_E0,
    "帕拉斯": 帕拉斯_E0,
    "异客": 异客_E0,
    "弑君者": 弑君者_E0,
    "引星棘刺": 引星棘刺_E0,
    "怒潮凛冬": 怒潮凛冬_E0,
    "截云": 截云_E0,
    "掠风": 掠风_E0,
    "斑点": 斑点,
    "断罪者": 断罪者_E0,
    "星源": 星源_E0,
    "月见夜": 月见夜_E0,
    "杏仁": 杏仁_E0,
    "杰西卡": 杰西卡_E0,
    "梅尔": 梅尔_E0,
    "森蚺": 森蚺_E0,
    "槐琥": 槐琥_E0,
    "水月": 水月_E0,
    "泡普员": 泡普员_E0,
    "泡泡": 泡泡_E0,
    "泰拉大陆调查团": 泰拉大陆调查团,
    "洋灰": 洋灰_E0,
    "流星": 流星_E0,
    "海沫": 海沫_E0,
    "淬羽赫默": 淬羽赫默_E0,
    "清流": 清流,
    "清道夫": 清道夫_E0,
    "温米": 温米,
    "温蒂": 温蒂_E0,
    "溯光星源": 溯光星源_E0,
    "火神": 火神_E0,
    "灰毫": 灰毫_E0,
    "炎熔": 炎熔_E0,
    "烈夏": 烈夏_E0,
    "玛露西尔": 玛露西尔_E0,
    "白雪": 白雪_E0,
    "白面鸮": 白面鸮_E0,
    "石棉": 石棉_E0,
    "石英": 石英_E0,
    "砾": 砾,
    "稀音": 稀音_E0,
    "米格鲁": 米格鲁_E0,
    "红云": 红云_E0,
    "红豆": 红豆_E0,
    "维伊": 维伊_E0,
    "罗比菈塔": 罗比菈塔_E0,
    "至简": 至简_E0,
    "艾雅法拉": 艾雅法拉_E0,
    "芬": 芬_E0,
    "苍苔": 苍苔,
    "薄绿": 薄绿_E0,
    "蛇屠箱": 蛇屠箱,
    "裁度": 裁度_E0,
    "裂响": 裂响,
    "褐果": 褐果_E0,
    "调香师": 调香师,
    "豆苗": 豆苗_E0,
    "贝娜": 贝娜,
    "赫默": 赫默_E0,
    "远牙": 远牙_E0,
    "迷迭香": 迷迭香_0超感,
    "酒神": 酒神_E0,
    "野鬃": 野鬃_E0,
    "钼铅": 钼铅_E0,
    "铅踝": 铅踝_E0,
    "锡兰": 锡兰,
    "阿兰娜": 阿兰娜_E0,
    "阿罗玛": 阿罗玛_E0,
    "雪猎": 雪猎_E0,
    "霜叶": 霜叶,
    "食铁兽": 食铁兽_E0,
    "香草": 香草,
    "黍": 黍_E0,
    "黑角": 黑角,
}


def 获取制造站干员(名称: str, 精英等级: int = 0) -> Optional[制造站干员基类]:
    """获取制造站干员实例"""
    干员类 = 制造站干员注册表.get(名称)
    if 干员类 is None:
        return None
    return 干员类(精英等级)


def 计算队伍加成(干员列表: List[str], 上下文: dict = None) -> 加成结果:
    """计算队伍总加成"""
    合计 = 加成结果(干员名称="队伍合计")

    for 名称 in 干员列表:
        干员 = 获取制造站干员(名称)
        if 干员:
            加成 = 干员.计算加成(上下文)
            合计.赤金加成 += 加成.赤金加成
            合计.作战记录加成 += 加成.作战记录加成
            合计.源石加成 += 加成.源石加成
            合计.通用加成 += 加成.通用加成
            合计.仓库加成 += 加成.仓库加成
            合计.心情修正 += 加成.心情修正

    return 合计


# ==================== 示例 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("明日方舟基建 - 制造站干员类 (共90名)")
    print("=" * 60)

    print("\n【示例干员加成】")
    for 名称 in ["夜烟", "砾", "赫默", "调香师", "迷迭香"]:
        干员 = 获取制造站干员(名称)
        if 干员:
            print(干员.计算加成())

    print("\n【队伍总计】")
    队伍 = ["夜烟", "砾", "斑点"]
    结果 = 计算队伍加成(队伍)
    print(f"队伍 {队伍}: {结果}")

