
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from .views import time_sheet_form_page_view , timesheet_page_view , manager_timesheet_page_view, client_timesheet_page_view, time_sheet_action_page_view, time_sheet_manager_action_page_view

urlpatterns = [
  
    
    url(r'^timesheetform/(?P<employee_id>\d+)/(?P<project_id>\d+)/(?P<day>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' , time_sheet_form_page_view , name='timesheetform' ) ,
    url(r'^timesheet/(?P<employee_id>\d+)/(?P<project_id>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' , timesheet_page_view , name='timesheet' ) ,
    url(r'^clienttimesheet/(?P<employeeid>\d+)/(?P<project_id>\d+)/(?P<client_id>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' , client_timesheet_page_view , name='clienttimesheet' ) ,
    url(r'^managertimesheet/(?P<employeeid>\d+)/(?P<project_id>\d+)/(?P<manager_id>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' , manager_timesheet_page_view , name='managertimesheet' ) ,
    url(r'^timesheetaction/(?P<employee_id>\d+)/(?P<project_id>\d+)/(?P<day>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' , time_sheet_action_page_view , name='timesheetaction' ) ,
    url(r'^timesheetmanageraction/(?P<employee_id>\d+)/(?P<project_id>\d+)/(?P<manager_id>\d+)/(?P<day>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' , time_sheet_manager_action_page_view , name='timesheetmanageraction' ) ,
] 
