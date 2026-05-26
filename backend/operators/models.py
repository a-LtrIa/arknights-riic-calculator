from django.db import models


class Operator(models.Model):
    """干员模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='干员名称')
    rarity = models.IntegerField(default=3, verbose_name='稀有度')
    profession = models.CharField(max_length=50, blank=True, verbose_name='职业')
    
    # 基建技能
    base_skill_e0 = models.TextField(blank=True, verbose_name='E0基建技能')
    base_skill_e1 = models.TextField(blank=True, verbose_name='E1基建技能')
    base_skill_e2 = models.TextField(blank=True, verbose_name='E2基建技能')
    
    # 技能类型标签
    skill_tags = models.JSONField(default=list, verbose_name='技能标签')
    
    # 适用设施
    applicable_facilities = models.JSONField(default=list, verbose_name='适用设施')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '干员'
        verbose_name_plural = '干员'
        ordering = ['-rarity', 'name']
    
    def __str__(self):
        return self.name


class OperatorSkill(models.Model):
    """干员基建技能详情"""
    SKILL_ELITE_CHOICES = [
        (0, 'E0'),
        (1, 'E1'),
        (2, 'E2'),
    ]
    
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name='skills')
    elite_level = models.IntegerField(choices=SKILL_ELITE_CHOICES, verbose_name='精英等级')
    skill_name = models.CharField(max_length=100, verbose_name='技能名称')
    description = models.TextField(verbose_name='技能描述')
    
    # 效率加成
    efficiency_bonus = models.FloatField(default=0, verbose_name='效率加成(%)')
    
    # 特殊效果
    special_effects = models.JSONField(default=dict, verbose_name='特殊效果')
    
    # 适用配方类型
    recipe_types = models.JSONField(default=list, verbose_name='适用配方类型')
    
    class Meta:
        verbose_name = '干员技能'
        verbose_name_plural = '干员技能'
        unique_together = ['operator', 'elite_level', 'skill_name']
    
    def __str__(self):
        return f"{self.operator.name} - {self.skill_name}"
