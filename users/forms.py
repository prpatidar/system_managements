from django import forms
from django.db import models 
from django.forms import ModelForm

from users.models import User 

# form to create a employee under login manager
class EmployeeForm(ModelForm):

     class Meta:
         model = User
         fields = ['first_name', 'last_name' , 'email' , 'username' , 'role']
         widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email Address'}),
            'username': forms.TextInput(attrs={'placeholder': 'username'}),
            }