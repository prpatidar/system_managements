
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from project.api.views import all_projects_page_view , project_page_view , all_tasks_page_view , employee_project_page_view, employee_projects_page_view ,tasks_page_view, task_page_view

urlpatterns = [
    
    url(r'^projects/$', all_projects_page_view ),
    url(r'^projects/(?P<project_id>\d+)/$', project_page_view ),
    url(r'^projects/(?P<project_id>\d+)/tasks/$', tasks_page_view ),
    url(r'^projects/(?P<project_id>\d+)/tasks/(?P<task_id>\d+)/$', task_page_view ),
    url(r'^projects/tasks/$', all_tasks_page_view ),
    url(r'^employees/(?P<employee_id>\d+)/projects/$', employee_projects_page_view ),
    url(r'^employees/(?P<employee_id>\d+)/projects/(?P<project_id>\d+)/$', employee_project_page_view ),
    
    
    
]
