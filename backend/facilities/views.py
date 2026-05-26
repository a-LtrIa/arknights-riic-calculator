from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Facility, FacilityConfiguration, Recipe
from .serializers import (FacilitySerializer, FacilityListSerializer, 
                          FacilityConfigurationSerializer, RecipeSerializer)


class FacilityViewSet(viewsets.ModelViewSet):
    """设施视图集"""
    queryset = Facility.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['facility_type', 'level']
    ordering_fields = ['facility_type', 'level', 'name']
    ordering = ['facility_type', 'level']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FacilityListSerializer
        return FacilitySerializer
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """按设施类型分组获取"""
        facilities = self.queryset.order_by('facility_type', 'level')
        result = {}
        for facility in facilities:
            facility_type = facility.get_facility_type_display()
            if facility_type not in result:
                result[facility_type] = []
            result[facility_type].append(FacilityListSerializer(facility).data)
        return Response(result)


class FacilityConfigurationViewSet(viewsets.ModelViewSet):
    """设施配置视图集"""
    queryset = FacilityConfiguration.objects.all()
    serializer_class = FacilityConfigurationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']


class RecipeViewSet(viewsets.ModelViewSet):
    """配方视图集"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['recipe_type']
    ordering_fields = ['recipe_type', 'production_time', 'name']
    ordering = ['recipe_type', 'name']
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """按配方类型分组获取"""
        recipes = self.queryset.order_by('recipe_type', 'name')
        result = {}
        for recipe in recipes:
            recipe_type = recipe.get_recipe_type_display()
            if recipe_type not in result:
                result[recipe_type] = []
            result[recipe_type].append(RecipeSerializer(recipe).data)
        return Response(result)
