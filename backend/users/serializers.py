from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import SerializerMethodField
from app.models import Follow
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
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
        if Follow.objects.filter(user=current_user.id, author=obj.id).exists():
            return True
        return False


# class FollowSerializer(CustomUserSerializer):
#     recipes = ShortResipeSerializer(many=True)

#     class Meta:
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed'
#         )
#         read_only_fields = (
#             'email',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'recipes'
#         )

#         def create(self, validated_data):
#             request = self.context.get('request', None)
#             author_id = self.context.get('request').parser_context.get(
#                 'kwargs').get('user_id')

#             current_user = request.user
#             author = get_object_or_404(User, pk=author_id)
#             Follow.objects.create(user=current_user, author=author)

#             return author
