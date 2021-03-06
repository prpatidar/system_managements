
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from project.api import views

urlpatterns = [
    
    url(r'^projects/$', views.AllProjectsView.as_view() ),
    url(r'^createproject/$', views.CreateProjectApiView.as_view() ),
    url(r'^editproject/$', views.EditProjectsApiView.as_view() ),
    url(r'^deleteproject/$', views.DeleteProjectsApiView.as_view() ),
    url(r'^editproject/(?P<project_id>\d+)/$', views.EditProjectApiView.as_view() ),
    url(r'^deleteproject/(?P<project_id>\d+)/$', views.DeleteProjectApiView.as_view() ),
    url(r'^projects/(?P<project_id>\d+)/$', views.ProjectView.as_view() ),
    url(r'^projects/(?P<project_id>\d+)/tasks/$', views.TasksView.as_view() ),
    url(r'^projects/(?P<project_id>\d+)/tasks/(?P<task_id>\d+)/$', views.TaskView.as_view() ),
    url(r'^employees/(?P<employee_id>\d+)/projects/$', views.EmployeeProjectsView.as_view() ),
    url(r'^employees/(?P<employee_id>\d+)/projects/(?P<project_id>\d+)/$', views.EmployeeProjectView.as_view() ),
]