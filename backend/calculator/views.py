from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .calculation_engine import calculate_efficiency_api


class CalculatorViewSet(viewsets.ViewSet):
    """计算器视图集"""
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """
        计算基建效率
        
        请求体格式:
        {
            "制造站1": {
                "类型": "制造站",
                "等级": 3,
                "配方类型": "赤金",
                "进驻干员": [
                    {"名称": "干员A", "精英等级": 2},
                    {"名称": "干员B", "精英等级": 1}
                ]
            },
            "贸易站1": {
                "类型": "贸易站",
                "等级": 3,
                "进驻干员": [
                    {"名称": "干员C", "精英等级": 2}
                ]
            }
        }
        """
        configuration_data = request.data
        
        try:
            results = calculate_efficiency_api(configuration_data)
            return Response({
                'status': 'success',
                'data': results
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def calculate_facility(self, request):
        """
        计算单个设施效率
        
        请求体格式:
        {
            "facility_name": "制造站1",
            "facility_data": {
                "类型": "制造站",
                "等级": 3,
                "配方类型": "赤金",
                "进驻干员": [
                    {"名称": "干员A", "精英等级": 2}
                ]
            }
        }
        """
        facility_name = request.data.get('facility_name', '设施')
        facility_data = request.data.get('facility_data', {})
        
        try:
            from .calculation_engine import EfficiencyCalculator
            calculator = EfficiencyCalculator({facility_name: facility_data})
            result = calculator.calculate_facility_efficiency(facility_name, facility_data)
            return Response({
                'status': 'success',
                'data': result
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
