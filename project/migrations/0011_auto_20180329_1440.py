# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-29 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20180329_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Started', 'Started'), ('Completed', 'Completed')], default='Pending', max_length=30),
        ),
    ]
