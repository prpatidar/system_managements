# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-23 06:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField()),
                ('taskname', models.CharField(max_length=30)),
                ('day', models.IntegerField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('employee_id', models.IntegerField()),
                ('spendtime', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]
