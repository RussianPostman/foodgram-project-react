from djoser.serializers import UserCreateSerializer

class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name', 'last_name',  'password',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


