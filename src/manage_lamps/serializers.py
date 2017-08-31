# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from manage_hubs.models import Hubs
from manage_files.views import create_file
from manage_users.models import Accounts
from utils.authentication import auth_functions
from utils.hub_handler.space_handler import RGWSpaceHandler as RGWbox_Space
from .models import Lamps


class FilesSerializer(serializers.ModelSerializer):
    uploader = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    permission = serializers.SerializerMethodField()

    def create(self, validated_data):
        uploader = Accounts.objects.get(id=self.initial_data['uploader'])
        group_id = self.initial_data["group"] if 'group' in self.initial_data else None
        directory = self.initial_data["directory"] if 'directory' in self.initial_data else None
        file_type = self.initial_data["type"] if 'type' in self.initial_data else None
        the_file = self.initial_data["file"] if 'file' in self.initial_data else None
        if not group_id or len(group_id) == 0:
            group_id = None
        if not directory or len(directory) == 0:
            directory = None
        if not the_file or len(the_file) == 0:
            raise ValidationError("No Files For Upload!")
        (group, user) = (None, None)
        if file_type == "PUB":
            group = Group.objects.get(name="user")
            bucket = Hubs.objects.get(group=group)
            (access_key, secret_key) = (bucket.s3_access_key, bucket.s3_secret_key)
        elif file_type == "GRO":
            group = Group.objects.get(pk=int(group_id))
            bucket = Hubs.objects.get(group=group)
            (access_key, secret_key) = (bucket.s3_access_key, bucket.s3_secret_key)
        else:
            user = uploader
            bucket = Hubs.objects.get(account=user)
            (access_key, secret_key) = (bucket.s3_access_key, bucket.s3_secret_key)
        instance = create_file(uploader=uploader, user=user, group=group,
                               the_file=the_file, directory=directory,
                               file_type=file_type, bucket=bucket)
        if instance is False:
            raise ValidationError("File Exist!")
        space = RGWbox_Space(access_key=access_key, secret_key=secret_key)
        if space.single_object_upload(bucket_name=bucket.name, object_name=instance.uuid,
                                      file_object=the_file):
            return instance
        else:
            instance.delete()
            raise ValidationError("Upload File Failed!")

    def get_uploader(self, obj):
        [self, ].count(self)
        if obj.uploader:
            data = {
                "id": obj.uploader.id,
                "username": obj.uploader.username
            }
        else:
            data = None
        return data

    def get_account(self, obj):
        [self, ].count(self)
        if obj.account:
            data = {
                "id": obj.account.id,
                "username": obj.account.username
            }
        else:
            data = None
        return data

    def get_group(self, obj):
        [self, ].count(self)
        if obj.group:
            data = {
                "id": obj.group.id,
                "name": obj.group.name
            }
        else:
            data = None
        return data

    def get_permission(self, obj):
        [self, ].count(self)
        if obj.is_shared is False:
            return None
        permission_code = obj.code
        permission_group = auth_functions(permission_code, 'files')
        # permission_group = [str(x) for x, y in permission_group.iteritems() if y is True]
        return permission_group

    class Meta:
        model = Lamps
        fields = [
            "id",
            "name",
            "type",
            "size",
            "is_file",
            # "if_shared",
            "uploader",
            # "manage_users",
            "group",
            "account",
            "directory",
            "create_time",
            "update_time",
            "permission"
        ]
