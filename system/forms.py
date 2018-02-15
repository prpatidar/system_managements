from django import forms
from django.db import models 
from .models import User , Project , Task
from django.forms import ModelForm


class EmployeeForm(ModelForm):
     class Meta:
         model = User
         fields = ['first_name','last_name','email', 'username','role']
       

class ProjectForm(ModelForm):
	  class Meta:
	  	 model = Project
	  	 fields = ['title','discription','status','startdate','enddate']


class TaskForm(ModelForm):
	  class Meta:
	  	 model = Task
	  	 fields = ['project_id','title','discription','startdate','enddate']
         
