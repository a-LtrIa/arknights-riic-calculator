"""
效率计算引擎
整合原有的核心计算逻辑
"""
import sys
import os

# 添加core目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.base_classes import 特殊变量存储器, 全局计数计算器
from core.operator_classes import 创建干员实例


class EfficiencyCalculator:
    """效率计算器"""
    
    def __init__(self, configuration_data):
        """
        初始化计算器
        configuration_data: 设施配置数据
        """
        self.configuration_data = configuration_data
        self.special_vars = 特殊变量存储器()
        self.global_counter = 全局计数计算器()
        
    def calculate_facility_efficiency(self, facility_name, facility_data):
        """
        计算单个设施的效率
        """
        facility_type = facility_data.get('类型', '')
        operators = facility_data.get('进驻干员', [])
        recipe_type = facility_data.get('配方类型', '')
        
        results = {
            'facility_name': facility_name,
            'facility_type': facility_type,
            'operators': [],
            'total_efficiency': 0,
            'details': {}
        }
        
        for op_data in operators:
            op_name = op_data.get('名称', '')
            elite_level = op_data.get('精英等级', 0)
            
            try:
                # 创建干员实例
                operator = 创建干员实例(
                    op_name, 
                    elite_level, 
                    self.special_vars,
                    self.configuration_data,
                    facility_name
                )
                
                # 计算特殊技能
                if hasattr(operator, '计算特殊技能'):
                    operator.计算特殊技能()
                
                # 计算效率
                if hasattr(operator, '计算效率'):
                    if facility_type == '制造站':
                        efficiency = operator.计算效率(配方类型=recipe_type)
                    else:
                        efficiency = operator.计算效率()
                else:
                    efficiency = 0
                
                results['operators'].append({
                    'name': op_name,
                    'elite_level': elite_level,
                    'efficiency': efficiency
                })
                results['total_efficiency'] += efficiency
                
            except Exception as e:
                results['operators'].append({
                    'name': op_name,
                    'elite_level': elite_level,
                    'efficiency': 0,
                    'error': str(e)
                })
        
        return results
    
    def calculate_all(self):
        """
        计算所有设施的效率
        """
        all_results = []
        
        for facility_name, facility_data in self.configuration_data.items():
            if isinstance(facility_data, dict) and '类型' in facility_data:
                result = self.calculate_facility_efficiency(facility_name, facility_data)
                all_results.append(result)
        
        return {
            'facilities': all_results,
            'special_variables': self.special_vars.获取所有变量()
        }


def calculate_efficiency_api(configuration_data):
    """
    API接口：计算效率
    """
    calculator = EfficiencyCalculator(configuration_data)
    return calculator.calculate_all()
