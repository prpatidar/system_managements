# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-29 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditcard', '0005_auto_20180329_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_type',
            field=models.CharField(choices=[('mastercard', 'Mastercard'), ('amex', 'American Express'), ('maestro', 'Maestro'), ('visa', 'Visa'), ('visa_electron', 'Visa Electron')], max_length=20),
        ),
    ]
