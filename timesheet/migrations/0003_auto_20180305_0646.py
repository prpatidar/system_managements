# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-05 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0002_auto_20180228_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='spendtime',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
