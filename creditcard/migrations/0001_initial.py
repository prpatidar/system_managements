# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-28 06:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=20)),
                ('cvv_number', models.TextField(max_length=3)),
                ('expirydate', models.DateField(blank=True, null=True)),
                ('card_holder', models.CharField(blank=True, max_length=10, null=True)),
                ('card_token', models.CharField(blank=True, max_length=50)),
                ('client', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]