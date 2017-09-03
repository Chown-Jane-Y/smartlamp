# coding: utf-8
from manage_user.models import User
from manage_user.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import datetime


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Display one user by id.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()        # manage_user.models.User
        serializer = self.get_serializer(instance)  # manage_user.serializers.UserSerializer
        print(serializer.data)           # rest_framework.utils.serializer_helpers.ReturnDict
        print(type(Response(serializer.data).data))
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        List all users.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        print('=============user list===============')
        print(kwargs)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a user by id.
        Set 'is_deleted' as True, and set the 'deleted_time' as time_now.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        print('===============destroy user', kwargs['pk'], '===================')
        instance = self.get_object()
        instance.is_deleted = True
        instance.deleted_time = datetime.datetime.now()
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
