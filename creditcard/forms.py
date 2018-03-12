from django import forms
from django.db import models 
from django.forms import ModelForm

from creditcard.models import Card 

# form to manipulate credit card information
class CardForm(ModelForm):

     class Meta:
         model = Card
         fields = ['card_number', 'cvv_number' ]
       
