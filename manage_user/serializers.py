from rest_framework import serializers
from manage_user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id')  # 'name', 'user', 'email', 'is_deleted', 'created_time', 'updated_time', 'deleted_time')

    # is_deleted = serializers.BooleanField(default=False)
    # created_time = serializers.DateTimeField(allow_null=True)
    # updated_time = serializers.DateTimeField(allow_null=True)
    # deleted_time = serializers.DateTimeField(allow_null=True)

