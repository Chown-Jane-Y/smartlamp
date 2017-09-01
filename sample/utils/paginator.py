# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.serializers import ValidationError


# 分页功能
def paginator_this(request, list_in):
    try:
        page_size = int(request.GET.get('pageSize', 0))
        page_index = int(request.GET.get('pageIndex', 0))
    except (TypeError, ValueError):
        raise ValidationError('pageIndex and pageSize is not Integer!')
    if page_size == 0 or page_index == 0:
        return list_in
    try:
        list_in = list_in.order_by('id')
        paginator = Paginator(list_in, page_size)
        list_out = paginator.page(page_index)
    except PageNotAnInteger:
        raise ValidationError('PageNotAnInteger!')
    except EmptyPage:
        raise ValidationError('EmptyPage!')
    return list_out
