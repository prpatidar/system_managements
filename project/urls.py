from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

from .views import employee_project_page_view, project_page_view, task_page_view 
from .views import update_task_page_view,update_date_page_view, employee_task_page_view 
from .views import create_project_page_view, create_task_page_view, delete_project_page_view 


urlpatterns = [  
    url(r'^updatetask/(?P<task_id>\d+)/$', update_task_page_view, name='updatetask'),
    url(r'^updatedate/(?P<task_id>\d+)/$', update_date_page_view, name='updatedate'),
    url(r'^employeetask/(?P<project_id>\d+)/(?P<employee_id>\d+)/$', employee_task_page_view, name='employeetask'),
    url(r'^employeeprojects/(?P<employee_id>\d+)/$', employee_project_page_view, name='employeeprojects'),
    url(r'^project/(?P<manager_id>\d+)/$', project_page_view, name='project'),
    url(r'^task/(?P<project_id>\d+)/(?P<manager_id>\d+)/$', task_page_view, name='task'),
    url(r'^createproject/(?P<manager_id>\d+)/$', create_project_page_view, name='createproject'),
    url(r'^createtask/(?P<project_id>\d+)/(?P<manager_id>\d+)/$', create_task_page_view, name='createtask'),
    url(r'^deleteproject/(?P<project_id>\d+)/(?P<manager_id>\d+)/$', delete_project_page_view, name='deleteproject'),
]