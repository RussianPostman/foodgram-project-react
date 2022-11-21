from django.urls import include, path
from rest_framework import routers

from .views import CustomUserViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('', CustomUserViewSet)

urlpatterns = [
    # path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include(router_v1.urls)),
]
