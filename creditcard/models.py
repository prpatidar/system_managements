from __future__ import unicode_literals

from django.db import models

from users.models import User
        


class Card(models.Model):
    card_number = models.CharField(max_length=20)
    cvv_number = models.CharField(max_length=3)
    expirydate = models.DateField(null=True, blank=True)
    client = models.ForeignKey(User, blank=True)
    card_holder =models.CharField(max_length=10, null=True, blank=True)
    card_token = models.CharField(max_length=50, blank=True)
    primary =  models.BooleanField(default=False)