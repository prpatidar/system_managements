# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-27 06:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0003_auto_20180223_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='client',
            field=models.ForeignKey(blank=True, default=6, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]