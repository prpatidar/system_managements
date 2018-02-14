from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from . import views

urlpatterns = [  
    url(r'^home',views.HomePageView.as_view(),name='home'),
    url(r'^employee',views.EmployeePageView.as_view(),name='employee'),
    url(r'^createemployee',views.CreateEmployeePageView.as_view(),name='createemployee'),
]
