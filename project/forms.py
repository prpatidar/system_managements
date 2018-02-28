from django import forms
from django.db import models 
from django.forms import ModelForm

from .models import Project, Task 


class ProjectForm(ModelForm):

     class Meta:
        model = Project
        fields = ['title', 'discription', 'status', 'startdate', 'enddate' ]

class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['project', 'title', 'discription', 'startdate', 'enddate']
