# -*- coding: utf-8 -*-
from manage_hubs.models import Hubs
from django.contrib.auth.models import Group
from django.db import models

from manage_users.models import Accounts


class Lamps(models.Model):
    sn = models.CharField(max_length=16)
    sequence = models.CharField(max_length=8)
    status = models.SmallIntegerField(default=0)    # （1：正常，2：故障）
    type = models.SmallIntegerField(default=1)      # （1：钠灯，2：LED）
    hub_id = models.ForeignKey(Hubs, related_name='lamp_set', verbose_name=u"所属集控")
    is_repeater = models.BooleanField(default='False')
    rf_band = models.CharField(max_length=20)
    channel = models.CharField(max_length=20)
    address = models.CharField(max_length=60)
    registered_time = models.DateField(auto_now_add=True)
    longitude = models.FloatField(max_length=8)
    latitude = models.FloatField(max_length=8)
    memo = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(db_index=True, null=True)

    def __unicode__(self):
        return self.name
