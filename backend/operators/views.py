from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Operator
from .serializers import OperatorSerializer, OperatorListSerializer


class OperatorViewSet(viewsets.ModelViewSet):
    """干员视图集"""
    queryset = Operator.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rarity', 'profession']
    search_fields = ['name', 'base_skill_e0', 'base_skill_e1', 'base_skill_e2']
    ordering_fields = ['rarity', 'name', 'created_at']
    ordering = ['-rarity', 'name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OperatorListSerializer
        return OperatorSerializer
    
    @action(detail=False, methods=['get'])
    def by_facility(self, request):
        """按设施类型获取干员"""
        facility_type = request.query_params.get('facility_type')
        if facility_type:
            operators = self.queryset.filter(applicable_facilities__contains=[facility_type])
            serializer = OperatorListSerializer(operators, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def by_tag(self, request):
        """按技能标签获取干员"""
        tag = request.query_params.get('tag')
        if tag:
            operators = self.queryset.filter(skill_tags__contains=[tag])
            serializer = OperatorListSerializer(operators, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def tags(self, request):
        """获取所有技能标签"""
        all_tags = set()
        for op in self.queryset:
            all_tags.update(op.skill_tags)
        return Response(sorted(list(all_tags)))
