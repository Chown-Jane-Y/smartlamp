# _*_ coding: utf-8 _*_
from django.db import models

from manage_users.models import Accounts


class GroupProfile(models.Model):
    name = models.CharField(unique=True, max_length=250)
    to_accounts = models.ManyToManyField(Accounts, related_name="group_profile_set")

    def __unicode__(self):
        return self.name

