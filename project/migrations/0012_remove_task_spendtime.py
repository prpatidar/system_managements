# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-05 10:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_auto_20180329_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='spendtime',
        ),
    ]
