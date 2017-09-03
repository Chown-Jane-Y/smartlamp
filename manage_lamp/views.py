from manage_lamp.models import Lamp
from manage_lamp.serializers import LampSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, list_route
import datetime


class LampViewSet(viewsets.ModelViewSet):
    queryset = Lamp.objects.all().filter(is_deleted=False)
    serializer_class = LampSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Display one lamp by id.
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        List all lamps.
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        print('=============list===============')
        print(kwargs)
        print(request.query_params)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a lamp by id. 
        Set 'is_deleted' as True, and set the 'deleted_time' as time_now.
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        print('===============destroy ', kwargs['pk'], '===================')
        instance = self.get_object()
        instance.is_deleted = True
        instance.deleted_time = datetime.datetime.now()
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(url_path='test12')
    def test(self, request):
        return Response({'success': True, 'msg': '操作成功'})

