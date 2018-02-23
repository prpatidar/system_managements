
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from .views import home_page_view , employee_page_view , create_employee_page_view , update_profile_page_view , delete_profile_page_view


urlpatterns = [
    
    url(r'^home',home_page_view,name='home'),
    url(r'^employee/(?P<manager_id>\d+)/$' , employee_page_view , name='employee' ) ,
    url(r'^createemployee/(?P<manager_id>\d+)/$' , create_employee_page_view , name='createemployee' ) ,
    url(r'^updateprofile/(?P<employee_id>\d+)/$' , update_profile_page_view , name='updateprofile' ) ,
    url(r'^deleteprofile/(?P<employee_id>\d+)/(?P<manager_id>\d+)/$' , delete_profile_page_view , name='deleteprofile' ) ,
    
]
