from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from . import views

urlpatterns = [  
    url(r'^home',views.HomePageView.as_view(),name='home'),
    url(r'^employeetask',views.EmployeeTaskPageView.as_view(),name='employeetask'),
    url(r'^employee',views.EmployeePageView.as_view(),name='employee'),
    url(r'^project',views.ProjectPageView.as_view(),name='project'),
    url(r'^task/(?P<projectid>\d+)/$',views.TaskPageView.as_view(),name='task'),
    url(r'^createemployee',views.CreateEmployeePageView.as_view(),name='createemployee'),
    url(r'^createproject',views.CreateProjectPageView.as_view(),name='createproject'),
    url(r'^createtask/(?P<projectid>\d+)/$',views.CreateTaskPageView.as_view(),name='createtask'),
    
]
