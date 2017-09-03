from rest_framework import serializers
from manage_user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'email', 'is_superuser', 'is_active')

    # is_deleted = serializers.BooleanField(default=False)
    # created_time = serializers.DateTimeField(allow_null=True)
    # updated_time = serializers.DateTimeField(allow_null=True)
    # deleted_time = serializers.DateTimeField(allow_null=True)

