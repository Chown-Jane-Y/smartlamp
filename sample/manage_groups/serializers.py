# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from manage_hubs.models import Hubs
from manage_users.models import Accounts
from utils.hub_handler import HubHandler as RGWbox
from utils.hub_handler.space_handler import RGWSpaceHandler as RGWbox_Space


class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    def create(self, validated_data):
        model_class = self.Meta.model
        user = Accounts.objects.get(id=self.initial_data['owner'])
        rgwbox = RGWbox()
        keys = rgwbox.create_user('group-' + validated_data['name'])
        if keys is None:
            raise ValidationError('RGW Group Create Denied!')
        instance = model_class.objects.create(**validated_data)
        bucket = Hubs(
            name=('group-' + instance.name + '-bucket1'),
            group=instance,
            s3_access_key=keys[0],
            s3_secret_key=keys[1])
        bucket.save()
        space_bucket = RGWbox_Space(
            access_key=bucket.s3_access_key,
            secret_key=bucket.s3_secret_key)
        if space_bucket.bucket_create(bucket.name):
            user.groups.add(instance)
            return instance
        else:
            bucket.delete()
            rgwbox.remove_user('group-' + instance.name)
            instance.delete()
            raise ValidationError('RGW Bucket Create Denied!')

    def get_owner(self, obj):
        [self, ].count(self)
        user = obj.user_set.all().first()
        data = {
            "id": user.id,
            "username": user.username}
        return data

    def validate_name(self, values):
        [self, ].count(self)
        queryset = Group.objects.filter(name=values)
        if queryset.exists():
            raise ValidationError('Group has existed!')
        return values

    class Meta:
        model = Group
        fields = ["id", "name", "owner"]
