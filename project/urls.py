from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

from project import views

urlpatterns = [  

    url(r'^updatetask/(?P<task_id>\d+)/$', views.UpdateTaskPageView.as_view(), name='updatetask'),
    url(r'^updateproject/(?P<project_id>\d+)/(?P<manager_id>\d+)/$', views.UpdateProjectPageView.as_view(), name='updateproject'),
    url(r'^employeetask/(?P<project_id>\d+)/(?P<employee_id>\d+)/$', views.EmployeeTaskPageView.as_view(), name='employeetask'),
    url(r'^clientprojects/(?P<client_id>\d+)/$', views.ClientProjectPageView.as_view(), name='clientprojects'),
    url(r'^employeeprojects/(?P<employee_id>\d+)/$', views.EmployeeProjectPageView.as_view(), name='employeeprojects'),
    url(r'^project/(?P<manager_id>\d+)/$', views.ProjectPageView.as_view(), name='project'),
    url(r'^task/(?P<project_id>\d+)/(?P<manager_id>\d+)/$', views.TaskPageView.as_view(), name='task'),
    url(r'^createproject/(?P<manager_id>\d+)/$', views.CreateProjectPageView.as_view(), name='createproject'),
    url(r'^createtask/(?P<project_id>\d+)/(?P<manager_id>\d+)/$', views.CreateTaskPageView.as_view(), name='createtask'),
    url(r'^deleteproject/(?P<project_id>\d+)/(?P<manager_id>\d+)/$', views.DeleteProjectPageView.as_view(), name='deleteproject'),
    url(r'^deletetask/(?P<project_id>\d+)/(?P<manager_id>\d+)/(?P<task_id>\d+)/$', views.DeleteTaskPageView.as_view(), name='deletetask'),
    url(r'^projectform/$', views.ProjectFormPageView.as_view(), name='projectform'),
       
]