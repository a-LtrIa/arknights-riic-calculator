from rest_framework import serializers
from .models import Facility, FacilityConfiguration, Recipe


class FacilitySerializer(serializers.ModelSerializer):
    """设施序列化器"""
    facility_type_display = serializers.CharField(source='get_facility_type_display', read_only=True)
    
    class Meta:
        model = Facility
        fields = ['id', 'name', 'facility_type', 'facility_type_display', 'level',
                  'base_capacity', 'base_efficiency', 'power_consumption', 
                  'max_operators', 'created_at', 'updated_at']


class FacilityListSerializer(serializers.ModelSerializer):
    """设施列表序列化器（简化版）"""
    facility_type_display = serializers.CharField(source='get_facility_type_display', read_only=True)
    
    class Meta:
        model = Facility
        fields = ['id', 'name', 'facility_type', 'facility_type_display', 'level']


class FacilityConfigurationSerializer(serializers.ModelSerializer):
    """设施配置序列化器"""
    
    class Meta:
        model = FacilityConfiguration
        fields = ['id', 'name', 'description', 'configuration_data', 'created_at', 'updated_at']


class RecipeSerializer(serializers.ModelSerializer):
    """配方序列化器"""
    recipe_type_display = serializers.CharField(source='get_recipe_type_display', read_only=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'recipe_type', 'recipe_type_display', 
                  'production_time', 'materials', 'output', 'warehouse_space']
