# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-28 10:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(max_length=100, verbose_name='\u64cd\u4f5c\u8d44\u6e90\u7c7b\u578b')),
                ('content_id', models.CharField(max_length=100, verbose_name='\u64cd\u4f5c\u8d44\u6e90\u7f16\u53f7')),
                ('action_type', models.CharField(max_length=100, verbose_name='\u52a8\u4f5c\u7c7b\u578b')),
                ('running_status', models.CharField(max_length=100, verbose_name='\u6267\u884c\u7ed3\u679c')),
                ('running_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u6267\u884c\u65f6\u95f4')),
            ],
        ),
    ]
