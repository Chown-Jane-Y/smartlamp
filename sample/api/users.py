# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer

from api.message import MessageSuccess
from manage_users.models import Accounts
from manage_groups.models import GroupProfile


class UserProfileRenderer(JSONRenderer):
    """自定义Response返回格式"""
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            pass
        elif "success" in data:
            return json.dumps(data)
        else:
            pass
        return_message = MessageSuccess(data={
            "users": data})
        return json.dumps(return_message.data())


class ProfilePagination(PageNumberPagination):
    """分页方法参数设置"""
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page_index'
    max_page_size = 100


class GroupItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupProfile
        fields = ["id", "name"]


class UserItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accounts
        fields = ["id", "username"]
