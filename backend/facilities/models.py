from django.db import models


class Facility(models.Model):
    """设施模型"""
    FACILITY_TYPE_CHOICES = [
        ('manufacturing', '制造站'),
        ('trading', '贸易站'),
        ('power', '发电站'),
        ('dormitory', '宿舍'),
        ('office', '办公室'),
        ('reception', '会客室'),
        ('training', '训练室'),
        ('control', '控制中枢'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='设施名称')
    facility_type = models.CharField(
        max_length=50, 
        choices=FACILITY_TYPE_CHOICES,
        verbose_name='设施类型'
    )
    level = models.IntegerField(default=1, verbose_name='等级')
    
    # 设施基础属性
    base_capacity = models.IntegerField(default=0, verbose_name='基础容量')
    base_efficiency = models.FloatField(default=0, verbose_name='基础效率(%)')
    power_consumption = models.IntegerField(default=0, verbose_name='电力消耗')
    
    # 最大进驻人数
    max_operators = models.IntegerField(default=3, verbose_name='最大进驻人数')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '设施'
        verbose_name_plural = '设施'
        ordering = ['facility_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_facility_type_display()})"


class FacilityConfiguration(models.Model):
    """设施配置模型"""
    name = models.CharField(max_length=100, verbose_name='配置名称')
    description = models.TextField(blank=True, verbose_name='配置描述')
    
    # 设施配置数据
    configuration_data = models.JSONField(default=dict, verbose_name='配置数据')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '设施配置'
        verbose_name_plural = '设施配置'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    """制造配方模型"""
    RECIPE_TYPE_CHOICES = [
        ('gold', '赤金'),
        ('exp', '作战记录'),
        ('pure_gold', '提纯源岩'),
        ('device', '装置'),
        ('chip', '芯片'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='配方名称')
    recipe_type = models.CharField(
        max_length=50,
        choices=RECIPE_TYPE_CHOICES,
        verbose_name='配方类型'
    )
    
    # 生产时间(分钟)
    production_time = models.IntegerField(verbose_name='生产时间(分钟)')
    
    # 原材料
    materials = models.JSONField(default=dict, verbose_name='原材料')
    
    # 产出
    output = models.JSONField(default=dict, verbose_name='产出')
    
    # 仓库占用
    warehouse_space = models.IntegerField(default=1, verbose_name='仓库占用')
    
    class Meta:
        verbose_name = '配方'
        verbose_name_plural = '配方'
        ordering = ['recipe_type', 'name']
    
    def __str__(self):
        return self.name
