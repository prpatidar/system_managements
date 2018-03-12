from django import forms
from django.db import models 
from django.forms import ModelForm

from .models import Project, Task 

# form to create the projects 
class ProjectForm(ModelForm):

     class Meta:
        model = Project
        fields = ['title', 'discription', 'status', 'startdate', 'enddate' ]

# form to create the taks for projects 
class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['project', 'title', 'discription', 'startdate', 'enddate']
