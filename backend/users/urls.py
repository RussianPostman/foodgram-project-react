from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import Logout

# router_v1 = routers.DefaultRouter()
# router_v1.register('users', UserViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
