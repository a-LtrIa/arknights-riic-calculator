#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复第121-140个干员类的问题
"""

import re

# 读取文件
with open('/Users/altria/Documents/code/arkproject/building-calculator/core/operator_classes.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复黍 - E2人间烟火依赖
old_黍 = '''class 黍(干员基类):
    """
    明日方舟 黍 基建技能类
        精英0: 春雷响，万物长 - 进驻制造站时，当前制造站内所有干员心情每小时消耗-0.1...
    精英2: 稻禾厚，顺秋收 - 进驻制造站时，每3点人间烟火术语:人间烟火可影响巫术结晶相关技能由以下干员的基建技能提供夕、令、重岳...
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = []
        if 精英等级 >= 2:
            self.基本属性 = {"生产力": 0}
        else:
            self.基本属性 = {}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        return self.基本属性.get("生产力", 0)'''

new_黍 = '''class 黍(干员基类):
    """
    明日方舟 黍 基建技能类
        精英0: 春雷响，万物长 - 制造站内所有干员心情每小时消耗-0.1
        精英2: 稻禾厚，顺秋收 - 每3点人间烟火+5%生产力
            人间烟火由夕、令、重岳提供
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = []
        # E0: 心情消耗-0.1
        self.基本属性 = {"心情消耗": -0.1}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        """
        E2: 每3点人间烟火+5%生产力
        """
        if self.精英等级 >= 2:
            人间烟火 = self.特殊变量存储器.获取变量("人间烟火")
            return (人间烟火 // 3) * 5.0
        return 0.0'''

content = content.replace(old_黍, new_黍)

# 2. 修复佩佩 - 贸易站技能
old_佩佩 = '''class 佩佩(干员基类):
    """
    明日方舟 佩佩 基建技能类
        精英0: 多面逢源
    精英2: 慧眼独到
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = []
        self.基本属性 = {"订单效率": 0}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        return self.基本属性.get("订单效率", 0)'''

new_佩佩 = '''class 佩佩(干员基类):
    """
    明日方舟 佩佩 基建技能类
        精英0: 多面逢源 - 订单获取效率+20%，每有1条赤金生产线额外+5%
        精英2: 慧眼独到 - 订单获取效率+30%，每有1条赤金生产线额外+5%
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器, 配置数据: dict = None):
        super().__init__(精英等级, 特殊变量, 配置数据)
        self.特殊变量列表 = []
        self.基本属性 = {}

    def 计算赤金生产线数量(self) -> int:
        """计算基建内赤金生产线数量"""
        if not self.配置数据:
            return 0
        count = 0
        for 设施名, 设施数据 in self.配置数据.items():
            if isinstance(设施数据, dict):
                配方类型 = 设施数据.get("配方类型", "")
                if 配方类型 == "赤金":
                    count += 1
        return count

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        """
        E0: +20%，每赤金生产线+5%
        E2: +30%，每赤金生产线+5%
        """
        赤金线 = self.计算赤金生产线数量()
        if self.精英等级 >= 2:
            return 30.0 + 赤金线 * 5.0
        else:
            return 20.0 + 赤金线 * 5.0'''

content = content.replace(old_佩佩, new_佩佩)

# 3. 修复卡夫卡 - 贸易站技能
old_卡夫卡 = '''class 卡夫卡(干员基类):
    """
    明日方舟 卡夫卡 基建技能类
        精英0: 手工艺品·α
    精英2: 手工艺品·β
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = []
        self.基本属性 = {"订单效率": 0}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        return self.基本属性.get("订单效率", 0)'''

new_卡夫卡 = '''class 卡夫卡(干员基类):
    """
    明日方舟 卡夫卡 基建技能类
        精英0: 手工艺品·α - 订单获取效率+15%，每有1个类纸画材+5%
        精英2: 手工艺品·β - 订单获取效率+25%，每有1个类纸画材+5%
            类纸画材由以下干员提供: 夏栎、车尔尼等
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = ["类纸画材"]
        self.基本属性 = {}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        """
        E0: +15%，每类纸画材+5%
        E2: +25%，每类纸画材+5%
        """
        类纸画材 = self.特殊变量存储器.获取变量("类纸画材")
        if self.精英等级 >= 2:
            return 25.0 + 类纸画材 * 5.0
        else:
            return 15.0 + 类纸画材 * 5.0'''

content = content.replace(old_卡夫卡, new_卡夫卡)

# 4. 修复吉星 - 贸易站技能
old_吉星 = '''class 吉星(干员基类):
    """
    明日方舟 吉星 基建技能类
        精英0: 勤俭经营·α
    精英2: 勤俭经营·β
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = []
        self.基本属性 = {"订单效率": 0}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        return self.基本属性.get("订单效率", 0)'''

new_吉星 = '''class 吉星(干员基类):
    """
    明日方舟 吉星 基建技能类
        精英0: 勤俭经营·α - 订单获取效率+20%，每有1个类纸画材+5%
        精英2: 勤俭经营·β - 订单获取效率+30%，每有1个类纸画材+5%
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = ["类纸画材"]
        self.基本属性 = {}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        """
        E0: +20%，每类纸画材+5%
        E2: +30%，每类纸画材+5%
        """
        类纸画材 = self.特殊变量存储器.获取变量("类纸画材")
        if self.精英等级 >= 2:
            return 30.0 + 类纸画材 * 5.0
        else:
            return 20.0 + 类纸画材 * 5.0'''

content = content.replace(old_吉星, new_吉星)

# 5. 修复巫恋 - 裁缝技能
old_巫恋 = '''class 巫恋(干员基类):
    """
    明日方舟 巫恋 基建技能类
        精英0: 裁缝·α
    精英2: 低语
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = []
        self.基本属性 = {"订单效率": 0}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        return self.基本属性.get("订单效率", 0)'''

new_巫恋 = '''class 巫恋(干员基类):
    """
    明日方舟 巫恋 基建技能类
        精英0: 裁缝·α - 订单获取效率+30%，每有1个类纸画材+5%
        精英2: 低语 - 订单获取效率+40%，每有1个类纸画材+5%
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = ["类纸画材"]
        self.基本属性 = {}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        """
        E0: +30%，每类纸画材+5%
        E2: +40%，每类纸画材+5%
        """
        类纸画材 = self.特殊变量存储器.获取变量("类纸画材")
        if self.精英等级 >= 2:
            return 40.0 + 类纸画材 * 5.0
        else:
            return 30.0 + 类纸画材 * 5.0'''

content = content.replace(old_巫恋, new_巫恋)

# 6. 修复折光 - 贸易站技能
old_折光 = '''class 折光(干员基类):
    """
    明日方舟 折光 基建技能类
        精英0: 鉴定师的眼光
    精英2: 鉴定师的手段
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = []
        self.基本属性 = {"订单效率": 0}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        return self.基本属性.get("订单效率", 0)'''

new_折光 = '''class 折光(干员基类):
    """
    明日方舟 折光 基建技能类
        精英0: 鉴定师的眼光 - 订单获取效率+25%，每有1个类纸画材+5%
        精英2: 鉴定师的手段 - 订单获取效率+35%，每有1个类纸画材+5%
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = ["类纸画材"]
        self.基本属性 = {}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        """
        E0: +25%，每类纸画材+5%
        E2: +35%，每类纸画材+5%
        """
        类纸画材 = self.特殊变量存储器.获取变量("类纸画材")
        if self.精英等级 >= 2:
            return 35.0 + 类纸画材 * 5.0
        else:
            return 25.0 + 类纸画材 * 5.0'''

content = content.replace(old_折光, new_折光)

# 7. 修复拉普兰德 - 醉翁之意技能
old_拉普兰德 = '''class 拉普兰德(干员基类):
    """
    明日方舟 拉普兰德 基建技能类
        精英0: 醉翁之意·α
    精英2: 醉翁之意·β
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = []
        self.基本属性 = {"订单效率": 0}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        return self.基本属性.get("订单效率", 0)'''

new_拉普兰德 = '''class 拉普兰德(干员基类):
    """
    明日方舟 拉普兰德 基建技能类
        精英0: 醉翁之意·α - 当与德克萨斯在同一个贸易站时，订单获取效率+30%
        精英2: 醉翁之意·β - 当与德克萨斯在同一个贸易站时，订单获取效率+45%
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器, 配置数据: dict = None, 当前设施名: str = None):
        super().__init__(精英等级, 特殊变量, 配置数据, 当前设施名)
        self.特殊变量列表 = []
        self.基本属性 = {}

    def 检测德克萨斯同站(self) -> bool:
        """检测德克萨斯是否在同一贸易站"""
        if not self.配置数据 or not self.当前设施名:
            return False
        设施数据 = self.配置数据.get(self.当前设施名, {})
        if not isinstance(设施数据, dict) or 设施数据.get("类型") != "贸易站":
            return False
        进驻干员列表 = 设施数据.get("进驻干员", [])
        return any(op.get("名称") == "德克萨斯" for op in 进驻干员列表)

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        """
        与德克萨斯同站时:
        E0: +30%
        E2: +45%
        """
        if self.检测德克萨斯同站():
            if self.精英等级 >= 2:
                return 45.0
            else:
                return 30.0
        return 0.0'''

content = content.replace(old_拉普兰德, new_拉普兰德)

# 8. 修复明椒 - 裁缝技能
old_明椒 = '''class 明椒(干员基类):
    """
    明日方舟 明椒 基建技能类
        精英0: 裁缝·α
    精英2: 裁缝·β
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = []
        self.基本属性 = {"订单效率": 0}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        return self.基本属性.get("订单效率", 0)'''

new_明椒 = '''class 明椒(干员基类):
    """
    明日方舟 明椒 基建技能类
        精英0: 裁缝·α - 订单获取效率+25%，每有1个类纸画材+5%
        精英2: 裁缝·β - 订单获取效率+35%，每有1个类纸画材+5%
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = ["类纸画材"]
        self.基本属性 = {}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        """
        E0: +25%，每类纸画材+5%
        E2: +35%，每类纸画材+5%
        """
        类纸画材 = self.特殊变量存储器.获取变量("类纸画材")
        if self.精英等级 >= 2:
            return 35.0 + 类纸画材 * 5.0
        else:
            return 25.0 + 类纸画材 * 5.0'''

content = content.replace(old_明椒, new_明椒)

# 9. 修复桃金娘 - 谈判技能
old_桃金娘 = '''class 桃金娘(干员基类):
    """
    明日方舟 桃金娘 基建技能类
        精英0: 谈判
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器):
        super().__init__(精英等级, 特殊变量)
        self.特殊变量列表 = []
        self.基本属性 = {"订单效率": 0}

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        return self.基本属性.get("订单效率", 0)'''

new_桃金娘 = '''class 桃金娘(干员基类):
    """
    明日方舟 桃金娘 基建技能类
        精英0: 谈判 - 当与极境在同一个贸易站时，订单获取效率+30%
    """
    def __init__(self, 精英等级: int, 特殊变量: 特殊变量存储器, 配置数据: dict = None, 当前设施名: str = None):
        super().__init__(精英等级, 特殊变量, 配置数据, 当前设施名)
        self.特殊变量列表 = []
        self.基本属性 = {}

    def 检测极境同站(self) -> bool:
        """检测极境是否在同一贸易站"""
        if not self.配置数据 or not self.当前设施名:
            return False
        设施数据 = self.配置数据.get(self.当前设施名, {})
        if not isinstance(设施数据, dict) or 设施数据.get("类型") != "贸易站":
            return False
        进驻干员列表 = 设施数据.get("进驻干员", [])
        return any(op.get("名称") == "极境" for op in 进驻干员列表)

    def 计算特殊技能(self):
        pass

    def 计算效率(self) -> float:
        """
        与极境同站时: +30%
        """
        if self.检测极境同站():
            return 30.0
        return 0.0'''

content = content.replace(old_桃金娘, new_桃金娘)

# 写入文件
with open('/Users/altria/Documents/code/arkproject/building-calculator/core/operator_classes.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("修复完成！")
print("\n修复内容：")
print("1. 黍 - E2人间烟火依赖（每3点+5%）")
print("2. 佩佩 - 赤金生产线联动（每线+5%）")
print("3. 卡夫卡 - 类纸画材依赖（每个+5%）")
print("4. 吉星 - 类纸画材依赖（每个+5%）")
print("5. 巫恋 - 类纸画材依赖（每个+5%）")
print("6. 折光 - 类纸画材依赖（每个+5%）")
print("7. 拉普兰德 - 德克萨斯同站联动（E0+30%，E2+45%）")
print("8. 明椒 - 类纸画材依赖（每个+5%）")
print("9. 桃金娘 - 极境同站联动（+30%）")
