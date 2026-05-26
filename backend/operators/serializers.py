from rest_framework import serializers
from .models import Operator, OperatorSkill


class OperatorSkillSerializer(serializers.ModelSerializer):
    """干员技能序列化器"""
    elite_level_display = serializers.CharField(source='get_elite_level_display', read_only=True)
    
    class Meta:
        model = OperatorSkill
        fields = ['id', 'elite_level', 'elite_level_display', 'skill_name', 
                  'description', 'efficiency_bonus', 'special_effects', 'recipe_types']


class OperatorSerializer(serializers.ModelSerializer):
    """干员序列化器"""
    skills = OperatorSkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Operator
        fields = ['id', 'name', 'rarity', 'profession', 'base_skill_e0', 
                  'base_skill_e1', 'base_skill_e2', 'skill_tags', 
                  'applicable_facilities', 'skills', 'created_at', 'updated_at']


class OperatorListSerializer(serializers.ModelSerializer):
    """干员列表序列化器（简化版）"""
    
    class Meta:
        model = Operator
        fields = ['id', 'name', 'rarity', 'profession', 'skill_tags', 'applicable_facilities']
