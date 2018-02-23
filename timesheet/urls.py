
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from .views import time_sheet_form_page_view , timesheet_page_view 

urlpatterns = [
  
    url(r'^timesheetform/(?P<employee_id>\d+)/(?P<project_id>\d+)/(?P<day>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' , time_sheet_form_page_view , name='timesheetform' ) ,
    url(r'^timesheet/(?P<employee_id>\d+)/(?P<project_id>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' , timesheet_page_view , name='timesheet' ) ,
] 
