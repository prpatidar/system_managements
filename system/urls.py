from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from . import views

urlpatterns = [  
    url(r'^home',views.HomePageView.as_view(),name='home'),
    url(r'^updatetask/(?P<taskid>\d+)/$',views.UpdateTaskPageView.as_view(),name='updatetask'),
    url(r'^employee/(?P<managerid>\d+)/$',views.EmployeePageView.as_view(),name='employee'),
    url(r'^employeetask/(?P<projectid>\d+)/(?P<employeeid>\d+)/$',views.EmployeeTaskPageView.as_view(),name='employeetask'),
    url(r'^employeeprojects/(?P<employeeid>\d+)/$',views.EmployeeProjectPageView.as_view(),name='employeeprojects'),
    url(r'^project/(?P<managerid>\d+)/$',views.ProjectPageView.as_view(),name='project'),
    url(r'^task/(?P<projectid>\d+)/(?P<managerid>\d+)/$',views.TaskPageView.as_view(),name='task'),
    url(r'^createemployee/(?P<managerid>\d+)/$',views.CreateEmployeePageView.as_view(),name='createemployee'),
    url(r'^createproject/(?P<managerid>\d+)/$',views.CreateProjectPageView.as_view(),name='createproject'),
    url(r'^createtask/(?P<projectid>\d+)/(?P<managerid>\d+)/$',views.CreateTaskPageView.as_view(),name='createtask'),
    url(r'^updateprofile/(?P<employeeid>\d+)/$',views.UpdateProfilePageView.as_view(),name='updateprofile'),
    url(r'^deleteprofile/(?P<employeeid>\d+)/(?P<managerid>\d+)/$',views.DeleteProfilePageView.as_view(),name='deleteprofile'),
    url(r'^deleteproject/(?P<projectid>\d+)/(?P<managerid>\d+)/$',views.DeleteProjectPageView.as_view(),name='deleteproject'),
 
]
