
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from users import views


urlpatterns = [
    
    url(r'^home',views.HomePageView.as_view() ,name='home'),
    url(r'^client/(?P<manager_id>\d+)/$' ,views.ClientPageView.as_view()  , name='client' ) ,
    url(r'^employee/(?P<manager_id>\d+)/$' ,views.EmployeePageView.as_view()  , name='employee' ) ,
    url(r'^createclient/(?P<manager_id>\d+)/$' ,views.CreateClientPageView.as_view()  , name='createclient' ) ,
    url(r'^updateprofile/(?P<employee_id>\d+)/$' ,views.UpdateProfilePageView.as_view()  , name='updateprofile' ) ,
    url(r'^createemployee/(?P<manager_id>\d+)/$' ,views.CreateEmployeePageView.as_view()  , name='createemployee' ) ,
    url(r'^deleteprofile/(?P<employee_id>\d+)/(?P<manager_id>\d+)/$' ,views.DeleteProfilePageView.as_view()  , name='deleteprofile' ) ,
    url(r'^deleteclient/(?P<employee_id>\d+)/(?P<manager_id>\d+)/$' ,views.DeleteClientPageView.as_view()  , name='deleteclient' ) ,
    
]
