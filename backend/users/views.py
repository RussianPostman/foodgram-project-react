from djoser.views import UserViewSet
from rest_framework import mixins, viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from app.models import Follow
from app.serializers import FollowSerializer
from app.pagination import CustomPagination

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Переопределение сериализатора для соответствия ТЗ"""

    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.all()


class FollowListMixin(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Отображениее списка модели подписок"""

    serializer_class = FollowSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class FollowMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Создание и удаление модели подписок"""

    serializer_class = FollowSerializer
    queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        author = get_object_or_404(User, pk=user_id)

        instance = Follow.objects.filter(
            user=request.user, author=author)

        if not instance:
            raise serializers.ValidationError(
                'Вы не подписаны на этого пользователя'
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
