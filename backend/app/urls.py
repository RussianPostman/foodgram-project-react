from django.urls import include, path
from rest_framework import routers

from .views import TegViewSet, RecipeWiewSet

router_v1 = routers.DefaultRouter()
router_v1.register('tags', TegViewSet)
router_v1.register('recipes', RecipeWiewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include(router_v1.urls)),
]
