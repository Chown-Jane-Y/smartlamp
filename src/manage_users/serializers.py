# -*- coding: utf-8 -*-
from manage_hubs.models import Hubs
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from api.users import GroupItemSerializer, UserItemSerializer
from manage_users.models import Accounts
from api.authentication import auth_get_data
from api.permission import auth_map


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, help_text="Required, string.")
    password = serializers.CharField(
        required=True, write_only=True, help_text="Required, string.")
    set_role = serializers.MultipleChoiceField(
        required=True, choices=['user', 'admin', 'group_admin'], write_only=True,
        help_text="Required, list of string like ['user', 'admin', 'group_admin']")
    role = serializers.SerializerMethodField()
    creator = UserItemSerializer(read_only=True)
    groups = GroupItemSerializer(many=True, read_only=True)
    permission = serializers.SerializerMethodField()

    def create(self, validated_data):
        model_class = self.Meta.model
        # rgwbox = RGWAdminHandler()
        # keys = rgwbox.create_user('user-' + validated_data['username'])
        keys = (333, 444)
        if keys is None:
            raise ValidationError("RGW User Create Denied!")
        role_set = validated_data["set_role"]
        del validated_data["set_role"]
        instance = model_class.objects.create(**validated_data)
        for role in role_set:
            instance.role.add(Group.objects.get(name=role))
        bucket = Hubs(
            name=('user-' + instance.username + '-bucket1'),
            account=instance,
            s3_access_key=keys[0],
            s3_secret_key=keys[1])
        bucket.save()
        return instance
        # space_bucket = RGWSpaceHandler(
        #     access_key=bucket.s3_access_key,
        #     secret_key=bucket.s3_secret_key)
        # if space_bucket.bucket_create(bucket_name=bucket.name):
        #     return instance
        # else:
        #     bucket.delete()
        #     rgwbox.remove_user('user-' + instance.username)
        #     instance.delete()
        #     raise ValidationError("RGW Bucket Create Denied!")

    @staticmethod
    def get_permission(obj):
        if obj.code_public is not None and obj.code_group is not None:
            code_public = auth_get_data(obj.code_public, 'users')
            code_group = auth_get_data(obj.code_group, 'users')
        else:
            code_public = None
            code_group = None
        data = {
            "public": code_public,
            "group": code_group}
        return data

    @staticmethod
    def get_role(obj):
        if obj.role:
            data = [x.name for x in obj.role.all()]
        else:
            data = None
        return data

    class Meta:
        model = Accounts
        read_only_fields = [
            "is_active",
            "email",
            "first_name",
            "last_name",
            "date_joined"
        ]
        fields = [
            "id",
            "username",
            "password",
            "is_active",
            "email",
            "first_name",
            "last_name",
            "set_role",
            "role",
            "date_joined",
            "creator",
            "groups",
            "permission"]


class UserPermissionSerializer(serializers.ModelSerializer):
    public = serializers.MultipleChoiceField(
        required=True, choices=[x.get('function_name') for x in auth_map.get('users') if x.get("description") != ''],
        style={"base_template": "checkbox_multiple.html"},
        write_only=True, help_text="Required")
    group = serializers.MultipleChoiceField(
        required=True, choices=[x.get('function_name') for x in auth_map.get('users') if x.get("description") != ''],
        style={"base_template": "checkbox_multiple.html"},
        write_only=True, help_text="Required")

    class Meta:
        model = Accounts
        fields = [
            "public",
            "group"]


class UserPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Accounts
        fields = [
            "old_password",
            "new_password"]


class UserInformationSerializer(serializers.ModelSerializer):
    set_role = serializers.MultipleChoiceField(
        required=True, choices=[],
		# required=True, choices=[x.name for x in Group.objects.all()],
        style={"base_template": "checkbox_multiple.html"},
        write_only=True, help_text="Required")
    first_name = serializers.CharField(required=False, write_only=True)
    last_name = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = Accounts
        fields = [
            "set_role",
            "first_name",
            "last_name"]


class UserEnableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accounts
        fields = []
