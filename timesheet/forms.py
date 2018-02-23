from django import forms
from django.db import models 
from django.forms import ModelForm

from timesheet.models import TimeSheet


class TimeSheetForm(ModelForm):
	  class Meta :
	  	 model = TimeSheet
	  	 fields = ['taskname','day','month','year','employee_id','spendtime']
         
