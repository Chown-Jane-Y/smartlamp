# -*- coding: utf-8 -*-
from manage_hub.models import Hub
from django.db import models


class Lamp(models.Model):
    TYPE_CHOICE = ((1, '钠灯'), (2, 'LED'))
    STATUS_CHOICE = ((1, '正常'), (2, '故障'))

    sn = models.CharField(max_length=16)
    sequence = models.CharField(max_length=8)
    status = models.SmallIntegerField(default=0, choices=STATUS_CHOICE)    # （1：正常，2：故障）
    type = models.SmallIntegerField(default=1, choices=TYPE_CHOICE)        # （1：钠灯，2：LED）
    # hub_id = models.ForeignKey(Hub, related_name='lamp_set', verbose_name=u"所属集控")
    hub_sn = models.CharField(max_length=16)
    is_repeated = models.BooleanField(default='False')
    rf_band = models.CharField(max_length=20)
    channel = models.CharField(max_length=20)
    address = models.CharField(max_length=60)
    registered_time = models.DateField()
    longitude = models.FloatField(max_length=8)
    latitude = models.FloatField(max_length=8)
    memo = models.CharField(max_length=255, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    deleted_time = models.DateTimeField(db_index=True, null=True, blank=True)

    def __unicode__(self):
        return self.sn