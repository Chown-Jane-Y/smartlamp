from rest_framework import serializers
from manage_hub.models import Hub


class HubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hub
        fields = ('sn', 'status', 'rf_band', 'channel', 'address', 'registered_time', 'longitude', 'latitude',
                  'memo', 'is_deleted', 'created_time', 'updated_time', 'deleted_time')

    sn = serializers.CharField(read_only=True)
    # status = serializers.IntegerField()
    # rf_band = serializers.CharField()
    # channel = serializers.CharField()
    # address = serializers.CharField()
    # registered_time = serializers.DateTimeField()
    # longitude = serializers.FloatField()
    # latitude = serializers.FloatField()
    memo = serializers.CharField(allow_blank=True)
    is_deleted = serializers.BooleanField(default=False)
    # created_time = serializers.DateTimeField(allow_null=True)
    # updated_time = serializers.DateTimeField(allow_null=True)
    # deleted_time = serializers.DateTimeField(allow_null=True)

