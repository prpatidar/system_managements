# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-27 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stripetoken',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
