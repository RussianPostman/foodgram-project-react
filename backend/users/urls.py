from django.urls import include, path
from rest_framework import routers

from .views import CustomUserViewSet, FollowMixin, FollowListMixin


router_v1 = routers.DefaultRouter()
router_v1.register(r'(?P<user_id>\d+)/subscribe',
                   FollowMixin,
                   basename='subscribe')
router_v1.register('subscriptions',
                   FollowListMixin,
                   basename='subscriptions')
router_v1.register('', CustomUserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include(router_v1.urls)),
]
