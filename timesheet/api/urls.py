
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from timesheet.api import views


urlpatterns = [
    
    url(r'^employees/(?P<employee_id>\d+)/projects/(?P<project_id>\d+)/timesheet/$', views.EmployeeProjectTimeSheetView.as_view() ),
    
]
