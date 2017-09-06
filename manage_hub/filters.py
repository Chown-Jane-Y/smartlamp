# coding: utf-8
from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Hub


class HubFilter(filters.FilterSet):
    """
    Filter of hubs.
    """

    sn = filters.CharFilter(name='sn', method='sn_filter', lookup_expr='icontains')
    address = filters.CharFilter(name='address', lookup_expr='icontains')
    memo = filters.CharFilter(name='memo', lookup_expr='icontains')
    start_time = filters.DateFilter(name='registered_time', lookup_expr='gte')
    end_time = filters.DateFilter(name='registered_time', lookup_expr='lte')

    class Meta:
        model = Hub
        fields = (
            'id',
            'sn',           # fuzzy query
            'status',
            'rf_band',
            'channel',
            'address',      # fuzzy query
            'start_time',
            'end_time',     # registered time in range(start_time, end_time)
            'longitude',
            'latitude',
            'memo'          # fuzzy query
        )

    @staticmethod
    def sn_filter(queryset, name, value):
        """
        自定义过滤方法，sn可以包含逗号，如'2016,2017'，进行or查询
        查询sn中包含'2016'或'2017'的所有集控
        
        允许'2016,2017' , '2016,' , '2016, 2017' , '2016 ,2017'等形式
        """

        value = value.replace(' ', '')

        Q_sn = Q()
        for sn in value.split(','):
            if sn:
                Q_sn.add(Q(**{'sn__icontains': sn}), Q.OR)

        queryset = queryset.filter(Q_sn)
        return queryset
