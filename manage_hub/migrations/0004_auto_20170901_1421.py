# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_hub', '0003_auto_20170901_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hub',
            name='deleted_time',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
