from django import forms
from django.db import models
from .models import User
from django.forms import ModelForm


class EmployeeForm(ModelForm):
     class Meta:
         model = User
         fields = ['first_name','last_name','email', 'username','role']
