from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacilityViewSet, FacilityConfigurationViewSet, RecipeViewSet

router = DefaultRouter()
router.register(r'facilities', FacilityViewSet)
router.register(r'configurations', FacilityConfigurationViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
