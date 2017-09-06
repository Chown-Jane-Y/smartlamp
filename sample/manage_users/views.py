# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api.message import MessageSuccess, MessageError
from api.users import UserProfileRenderer, ProfilePagination
from manage_users.models import Accounts
from manage_users.serializers import UserSerializer, UserPermissionSerializer, \
    UserPasswordSerializer, UserInformationSerializer, UserEnableSerializer
from api.authentication import auth_get_code
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend


# 用户相关的操作
# /users/
class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """用户相关的操作"""

    queryset = Accounts.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [JSONWebTokenAuthentication,]      # 使用JWT认证
    renderer_classes = [UserProfileRenderer, BrowsableAPIRenderer]      # 使用自定义的格式返回，同时支持framework的API页
    filter_backends = [DjangoFilterBackend, OrderingFilter]      # 使用自定义参数的分页
    pagination_class = ProfilePagination      # 使用自定义参数的分页
    filter_fields = ['is_active']   # 设置可搜索的条目
    ordering_fields = ['username', 'id']      # 设置可排序的条目
    ordering = ['id']      # 默认使用id排序

    def get_queryset(self):
        """重载获取QuerySet的方法"""
        user = Accounts.objects.get(id=self.request.user.id)
        role_list = [x.name for x in user.role.all()]
        queryset = self.queryset.all()
        if "admin" in role_list:
            queryset = queryset
        elif "group_admin" in role_list:
            queryset = queryset.filter(creator=user).exclude(id=self.request.user.id)
        else:
            queryset = Accounts.objects.filter(id=user.id)
        return queryset

    def list(self, request, *args, **kwargs):
        """列出所有用户 is_active：True表示可用用户，False表示禁用的用户"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """创建账户"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except ValidationError as e:
            return_message = MessageError(code=333, message=e.detail[0])
            return Response(return_message.data(), status=status.HTTP_201_CREATED)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        """指定用户信息"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """逻辑删除用户(禁用用户)"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        """重载后，加入RGW报错判断、创建人、密码存入功能"""
        try:
            serializer.save(
                creator=self.request.user,
                password=make_password(self.request.data["password"]))
        except ValidationError as e:
            raise ValidationError(e.detail[0])

    def perform_destroy(self, instance):
        """重载后，将逻辑删改为逻辑删除"""
        instance.is_active = False
        instance.save()

    @list_route(methods=['GET'])
    def profile(self, request, *args, **kwargs):
        """获取登录账户的信息"""
        instance = self.get_queryset().get(id=request.user.id)
        serializer = UserSerializer(instance)
        return_message = MessageSuccess(data=serializer.data)
        return Response(return_message.data(), status=status.HTTP_200_OK)

    @detail_route(methods=['DELETE'])
    def remove(self, request, *args, **kwargs):
        """彻底删除用户(不开放)"""
        instance = self.get_object()
        # buckets = Buckets.objects.filter(account=instance)
        # rgwbox_space = RGWSpaceHandler(
        #     access_key=buckets.first().s3_access_key,
        #     secret_key=buckets.first().s3_secret_key)
        # for bucket in buckets:
        #     if not rgwbox_space.bucket_delete(bucket_name=bucket.name):
        #         return_message = MessageError(code=1008, message="RGW Bucket Delete Denied!")
        #         return Response(return_message.data(), status=status.HTTP_200_OK)
        #     bucket.delete()
        # rgwbox = RGWAdminHandler()
        # if rgwbox.remove_user('user-' + instance.username) is False:
        #     return_message = MessageError(code=1009, message="RGW User Delete Denied!")
        #     return Response(return_message.data(), status=status.HTTP_200_OK)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserPermissionViewSet(viewsets.GenericViewSet):
    queryset = Accounts.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [JSONWebTokenAuthentication,]      # 使用JWT认证
    renderer_classes = [UserProfileRenderer, BrowsableAPIRenderer]  # 使用自定义的格式返回，同时支持framework的API页

    @detail_route(['PUT'])
    def permission(self, request, *args, **kwargs):
        """设置用户的权限 示例：http://127.0.0.1:8000/users/1/permission/?format=api"""
        instance = self.get_object()
        permission_public, permission_group = request.data["public"], request.data["group"]
        code_public = auth_get_code(permission_public, 'users')
        code_group = auth_get_code(permission_group, 'users')
        instance.code_public, instance.code_group = code_public, code_group
        instance.save()
        return_message = MessageSuccess(data="Set Permission Success!")
        return Response(return_message.data(), status=status.HTTP_200_OK)


class UserPasswordViewSet(viewsets.GenericViewSet):
    """用户修改密码"""
    queryset = Accounts.objects.all()
    serializer_class = UserPasswordSerializer
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [JSONWebTokenAuthentication,]      # 使用JWT认证
    renderer_classes = [UserProfileRenderer, BrowsableAPIRenderer]  # 使用自定义的格式返回，同时支持framework的API页

    @detail_route(methods=['PUT'])
    def password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data["new_password"]
        if not instance.check_password(serializer.validated_data["old_password"]):
            return_message = MessageError(code=1012, message="Old Password Wrong!")
            return Response(return_message.data(), status=status.HTTP_400_BAD_REQUEST)
        del serializer.validated_data["old_password"]
        del serializer.validated_data["new_password"]
        serializer.save(password=make_password(new_password))
        return_message = MessageSuccess(data="Change Password Success!")
        return Response(return_message.data(), status=status.HTTP_200_OK)


class UserInformationViewSet(viewsets.GenericViewSet):
    queryset = Accounts.objects.all()
    serializer_class = UserInformationSerializer
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [JSONWebTokenAuthentication,]      # 使用JWT认证
    renderer_classes = [UserProfileRenderer, BrowsableAPIRenderer]  # 使用自定义的格式返回，同时支持framework的API页

    @detail_route(methods=['PUT'])
    def information(self, request, *args, **kwargs):
        """修改角色，用户昵称 示例：http://127.0.0.1:8000/users/1/permission/?format=api"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        role_new_set = serializer.validated_data["set_role"]
        role_old_set = set([x.name for x in instance.role.all()])
        for group_name in role_new_set - role_old_set:
            group = Group.objects.get(name=group_name)
            instance.role.add(group)
        for group_name in role_old_set - role_new_set:
            group = Group.objects.get(name=group_name)
            instance.role.remove(group)
        del serializer.validated_data["set_role"]
        serializer.save()
        return_message = MessageSuccess(data="Update User Success!")
        return Response(return_message.data(), status=status.HTTP_200_OK)


class UserEnableViewSet(viewsets.GenericViewSet):
    queryset = Accounts.objects.all()
    serializer_class = UserEnableSerializer
    permission_classes = [IsAuthenticated, ]
    # authentication_classes = [JSONWebTokenAuthentication,]      # 使用JWT认证
    renderer_classes = [UserProfileRenderer, BrowsableAPIRenderer]  # 使用自定义的格式返回，同时支持framework的API页

    @detail_route(['PUT'])
    def enable(self, request, *args, **kwargs):
        """用户禁用恢复"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=True)
        return_message = MessageSuccess(data="Enable User Success!")
        return Response(return_message.data(), status=status.HTTP_200_OK)
