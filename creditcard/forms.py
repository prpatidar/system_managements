from django import forms
from django.db import models 
from django.forms import ModelForm

from creditcard.models import Card 

# form to manipulate credit card information
class CardForm(ModelForm):

     class Meta:
         model = Card
         fields = ['card_type','card_number', 'cvv_number' ,'expirydate']
         widgets = {
            'card_type': forms.Select(attrs={'class':'form-control','id':'card_type'}),
            'card_number': forms.TextInput(attrs={'class':'card_number','placeholder': 'Card Number'}),
            'cvv_number': forms.TextInput(attrs={'placeholder': 'CVV Number'}),
            'expirydate': forms.TextInput(attrs={'class':'datepicker','placeholder': 'Expiry Date  : MM/YYYY'}),
            }
