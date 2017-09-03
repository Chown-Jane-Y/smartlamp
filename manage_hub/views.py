# coding: utf-8
from django.db.models import Q
from manage_hub.models import Hub
from manage_hub.serializers import HubSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import datetime
from utils.constants import *


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
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        List all hubs.
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """

        queryset = self.filter_queryset(self.get_queryset())

        # 多条件动态模糊查询，无需查询的字段不传进来
        query_params = request.query_params
        print('query_params：', query_params)

        Q_sn = Q()
        Q_registered_time = Q()
        Q_others = Q()
        for kw in query_params:
            if kw == 'sn' and ',' in query_params[kw]:
                # sn逗号查询，如['20160805,20170911']，进行or联结
                for sn in query_params[kw].split(','):
                    print(Q_sn.add(Q(**{kw + '__icontains': sn}), Q.OR))     # icontains: case-insensitive
            elif kw == 'sn' and ',' not in query_params[kw]:
                Q_sn.add(Q(**{kw + '__icontains': query_params[kw]}), Q.AND)

            if kw == 'registered_time':
                print(query_params[kw].split('~'))
                if query_params[kw].split('~')[0] == '':
                    # 没有起始日期：registered_time=~2017-09-04
                    date2 = query_params[kw].split('~')[1]
                    start_date = datetime.date(MIN_YEAR, MIN_MONTH, MIN_DAY)
                    end_date = datetime.date(
                        int(date2.split('-')[0]),
                        int(date2.split('-')[1]),
                        int(date2.split('-')[2])
                    )
                elif query_params[kw].split('~')[1] == '':
                    # 没有截至日期：registered_time=2017-07-01~
                    date1 = query_params[kw].split('~')[0]
                    start_date = datetime.date(
                        int(date1.split('-')[0]),
                        int(date1.split('-')[1]),
                        int(date1.split('-')[2])
                    )
                    end_date = datetime.date(MAX_YEAR, MAX_MONTH, MAX_DAY)
                else:
                    date1 = query_params[kw].split('~')[0]
                    date2 = query_params[kw].split('~')[1]
                    start_date = datetime.date(
                        int(date1.split('-')[0]),
                        int(date1.split('-')[1]),
                        int(date1.split('-')[2]))
                    end_date = datetime.date(
                        int(date2.split('-')[0]),
                        int(date2.split('-')[1]),
                        int(date2.split('-')[2]))
                Q_registered_time = Q(registered_time__range=(start_date, end_date))

            if kw not in ['sn', 'registered_time']:
                Q_others.add(Q(**{kw + '__icontains': query_params[kw]}), Q.AND)

        queryset = queryset.filter(Q_sn, Q_registered_time, Q_others)

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

        instance = self.get_object()
        instance.is_deleted = True
        instance.deleted_time = datetime.datetime.now()
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
