from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import SerializerMethodField
from django.contrib.auth import get_user_model

from app.models import Follow

User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор регистрации юзера в соответствии с ТЗ"""

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CustomUserSerializer(UserSerializer):
    """Сериализатор отображения юзера в соответствии с ТЗ"""

    is_subscribed = SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request', None)
        if request:
            current_user = request.user

        return Follow.objects.filter(
            user=current_user.id,
            author=obj.id).exists()
