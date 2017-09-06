# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.db import models

from manage_users.models import Accounts


class Hubs(models.Model):
    sn = models.CharField(max_length=16)
    status = models.SmallIntegerField()      # （1：正常，2：故障，3：脱网）
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
