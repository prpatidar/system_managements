# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-20 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_timesheet_project_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='spendtime',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
