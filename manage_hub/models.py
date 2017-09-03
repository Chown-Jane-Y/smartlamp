# -*- coding: utf-8 -*-
from django.db import models


class Hub(models.Model):
    STATUS_CHOICE = ((1, '正常'), (2, '故障'), (3, '脱网'))

    sn = models.CharField(max_length=16)
    status = models.IntegerField(choices=STATUS_CHOICE)    # （1：正常，2：故障，3：脱网）
    rf_band = models.CharField(max_length=20)
    channel = models.CharField(max_length=20)
    address = models.CharField(max_length=60)
    longitude = models.FloatField(max_length=8)
    latitude = models.FloatField(max_length=8)
    memo = models.CharField(max_length=255, blank=True)
    registered_time = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    deleted_time = models.DateTimeField(db_index=True, null=True, blank=True)

    def __str__(self):
        """
        Display the sn of object instead of 'Hub object'. 
        """
        return self.sn

    def __unicode__(self):
        """
        Apply to python2 like __str__.
        """
        return self.sn

    class Meta:
        # verbose_name = '集控中心'
        # verbose_name_plural = verbose_name
        ordering = ('created_time', )