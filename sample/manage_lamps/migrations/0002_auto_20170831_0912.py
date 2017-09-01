# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-31 01:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_hubs', '0001_initial'),
        ('manage_lamps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lamps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=16)),
                ('sequence', models.CharField(max_length=8)),
                ('status', models.SmallIntegerField(default=0)),
                ('type', models.SmallIntegerField(default=1)),
                ('is_repeater', models.BooleanField(default=b'False')),
                ('rf_band', models.CharField(max_length=20)),
                ('channel', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=60)),
                ('registered_time', models.DateField(auto_now_add=True)),
                ('longitude', models.FloatField(max_length=8)),
                ('latitude', models.FloatField(max_length=8)),
                ('memo', models.CharField(max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('delete_time', models.DateTimeField(db_index=True, null=True)),
                ('hub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lamp_set', to='manage_hubs.Hubs', verbose_name='\u6240\u5c5e\u96c6\u63a7')),
            ],
        ),
        migrations.DeleteModel(
            name='Files',
        ),
    ]
