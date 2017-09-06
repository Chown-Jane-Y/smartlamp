# -*- coding: utf-8 -*-

import django.utils.timezone as timezone
from django.db import models

from manage_users.models import Accounts


class Logs(models.Model):
    user_id = models.ForeignKey(Accounts, related_name='log_set', verbose_name=u"操作用户编号")
    content_type = models.CharField(max_length=100, verbose_name=u"操作资源类型")
    content_id = models.CharField(max_length=100, verbose_name=u"操作资源编号")
    action_type = models.CharField(max_length=100, verbose_name=u"动作类型")
    running_status = models.CharField(max_length=100, verbose_name=u"执行结果")
    running_time = models.DateTimeField(default=timezone.now, verbose_name=u"执行时间")

    def __unicode__(self):
        return self.running_time
