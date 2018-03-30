# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-28 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditcard', '0003_auto_20180328_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_type',
            field=models.CharField(choices=[('mastercard', 'Mastercard'), ('amex', 'American Express'), ('maestro', 'Maestro'), ('visa', 'Visa'), ('visa_electron', 'Visa Electron')], default='mastercard', max_length=20),
        ),
    ]
