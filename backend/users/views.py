from djoser.views import UserViewSet
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
