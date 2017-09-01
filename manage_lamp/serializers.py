from rest_framework import serializers
from manage_lamp.models import Lamp


class LampSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lamp
        fields = ('sn', 'sequence', 'status', 'type', 'hub_id', 'is_repeated', 'rf_band', 'channel', 'address',
                  'registered_time', 'longitude', 'latitude', 'memo', 'is_deleted', 'created_time', 'updated_time',
                  'deleted_time')

    sn = serializers.CharField(read_only=True)
    # sequence = serializers.CharField()
    # status = serializers.IntegerField()
    # type = serializers.CharField()
    # hub_id = serializers.IntegerField()
    is_repeated = serializers.BooleanField(default=False)
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

