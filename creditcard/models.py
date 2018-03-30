from __future__ import unicode_literals

from django.db import models

from users.models import User
        
card_choices = ( 
    ('mastercard','Mastercard'),
    ('amex','American Express'),
    ('maestro','Maestro'),
    ('visa','Visa'),
    ('visa_electron','Visa Electron'),
 )
# model to store credit card related informantion
class Card(models.Model):
    card_type = models.CharField(max_length=20, choices=card_choices)
    card_number = models.CharField(max_length=20)
    cvv_number = models.CharField(max_length=3)
    expirydate = models.CharField(max_length=7)
    client = models.ForeignKey(User, blank=True)
    card_holder =models.CharField(max_length=10, null=True, blank=True)
    card_token = models.CharField(max_length=50, blank=True)
    primary =  models.BooleanField(default=False)