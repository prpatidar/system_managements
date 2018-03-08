
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from timesheet.api.views import employee_project_timesheet_page_view


urlpatterns = [
    
    url(r'^employees/(?P<employee_id>\d+)/projects/(?P<project_id>\d+)/timesheet/$', employee_project_timesheet_page_view ),
    
]
