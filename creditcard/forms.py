from django import forms
from django.db import models 
from django.forms import ModelForm

from creditcard.models import Card 


class CardForm(ModelForm):

     class Meta:
         model = Card
         fields = ['card_number', 'cvv_number' ]
       
