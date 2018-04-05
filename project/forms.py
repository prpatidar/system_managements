from django import forms
from django.db import models 
from django.forms import ModelForm

from .models import Project, Task 

# form to create the projects 
class ProjectForm(ModelForm):

     class Meta:
        model = Project
        fields = ['title', 'discription', 'status', 'startdate', 'enddate' ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'discription': forms.Textarea(attrs={'placeholder': 'Discription'}),
            'startdate': forms.TextInput(attrs={'class':'datepicker','placeholder': 'Start Date'}),
            'enddate': forms.TextInput(attrs={'class':'datepicker','placeholder': 'End Date'}),
            }
# form to create the taks for projects 
class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['project', 'title', 'discription', 'startdate', 'enddate']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'title'}),
            'discription': forms.Textarea(attrs={'placeholder': 'discription'}),
            'startdate': forms.TextInput(attrs={'class':'datepicker','placeholder': 'Start Date'}),
            'enddate': forms.TextInput(attrs={'class':'datepicker','placeholder': 'End Date'}),
            }

class UpdateProjectForm(ModelForm):

     class Meta:
        model = Project
        fields = ['title', 'discription', 'status', 'startdate', 'enddate' ,'hourlyrate','payment_type']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'discription': forms.Textarea(attrs={'placeholder': 'Discription'}),
            'startdate': forms.TextInput(attrs={'class':'datepicker','id':'startdate','placeholder': 'Start Date'}),
            'enddate': forms.TextInput(attrs={'class':'datepicker','id':'enddate','placeholder': 'End Date'}),
            'status': forms.Select(attrs={'class':'form-control','placeholder': 'Select Status'}),
            'hourlyrate': forms.TextInput(attrs={'placeholder': 'Hourly Rate'}),
            'payment_type': forms.Select(attrs={'class':'form-control','placeholder': 'Payment Type'}),
            
            }

class UpdateTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['estimatetime', 'startdate', 'enddate']
        widgets = {
            'estimatetime': forms.TextInput(attrs={'placeholder': 'Estimate Time'}),
            'startdate': forms.TextInput(attrs={'class':'datepicker','placeholder': 'Start Date'}),
            'enddate': forms.TextInput(attrs={'class':'datepicker','placeholder': 'End Date'}),
            }
