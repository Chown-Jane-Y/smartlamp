# coding: utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICE = ((0, '超级管理员'), (1, '管理员'), (2, '用户'))

    name = models.CharField(max_length=30)
    # role = models.BooleanField(choices=ROLE_CHOICE)
    # email = models.EmailField(max_length=100, null=True, blank=True)
    # is_deleted = models.BooleanField(default=False)
    # created_time = models.DateTimeField(auto_now_add=True)
    # updated_time = models.DateTimeField(auto_now=True)
    # deleted_time = models.DateTimeField(db_index=True, null=True, blank=True)

    def __str__(self):
        return self.name
