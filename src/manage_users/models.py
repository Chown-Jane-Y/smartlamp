# _*_ coding: utf-8 _*_
from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class Accounts(AbstractUser):
    creator = models.ForeignKey('self', default='', null=True, related_name='creator_set')
    role = models.ManyToManyField(Group, max_length=20, related_name='role_set')
    code_public = models.IntegerField(default=0, null=True)
    code_group = models.IntegerField(default=0, null=True)

    def __unicode__(self):
        return self.username
