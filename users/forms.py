from django import forms
from django.db import models 
from django.forms import ModelForm

from users.models import User 


class EmployeeForm(ModelForm):

     class Meta:
         model = User
         fields = ['first_name', 'last_name' , 'email' , 'username' , 'role']
       
