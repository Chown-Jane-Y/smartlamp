from manage_hub.models import Hub
from manage_hub.serializers import HubSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import datetime


class HubViewSet(viewsets.ModelViewSet):
    queryset = Hub.objects.all().filter(is_deleted=False)
    serializer_class = HubSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Display one hub by id.
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        instance = self.get_object()        # manage_hub.models.Hub
        serializer = self.get_serializer(instance)  # manage_hub.serializers.HubSerializer
        print(serializer.data)           # rest_framework.utils.serializer_helpers.ReturnDict
        print(type(Response(serializer.data).data))
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        List all hubs.
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        print('=============list===============')
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
        Delete a hub by id. 
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
