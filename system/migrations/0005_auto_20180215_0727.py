# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-15 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_project_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='employee_id',
        ),
        migrations.AlterField(
            model_name='project',
            name='enddate',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='startdate',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, default='Pending', max_length=30),
        ),
        migrations.AlterField(
            model_name='task',
            name='enddate',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='startdate',
            field=models.DateTimeField(blank=True),
        ),
    ]
