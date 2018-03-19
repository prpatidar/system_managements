
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include
from django.contrib.auth.decorators import login_required

from users.api import views

urlpatterns = [
    url(r'^login/$', views.LoginApiView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutApiView.as_view(), name='logout'),
    url(r'^changepassword/$', views.ChangePasswordView.as_view(), name='changepassword'),
    url(r'^forgetpassword/$', views.ForgetPasswordView.as_view(), name='forgetpassword'),
    url(r'^createuser/$',  views.CreateApiView.as_view(), name='create'),
    url(r'^createemployee/$',  views.CreateEmployeeApiView.as_view(), name='createemployee'),
    url(r'^editemployee/$',  views.EditEmployeesApiView.as_view(), name='editemployees'),
    url(r'^editemployee/(?P<employee_id>\d+)/$',  views.EditEmployeeApiView.as_view(), name='editemployee'),
    url(r'^createclient/$',  views.CreateClientApiView.as_view(), name='createclient'),
    url(r'^editclient/$',  views.EditClientsApiView.as_view(), name='editclients'),
    url(r'^editclient/(?P<client_id>\d+)/$',  views.EditClientApiView.as_view(), name='editclient'),
    url(r'^deleteemployee/$',  views.DeleteEmployeesApiView.as_view(), name='deleteemployees'),
    url(r'^deleteemployee/(?P<employee_id>\d+)/$',  views.DeleteEmployeeApiView.as_view(), name='deleteemployee'),
    url(r'^deleteclient/$',  views.DeleteClientsApiView.as_view(), name='deleteclients'),
    url(r'^deleteclient/(?P<client_id>\d+)/$',  views.DeleteClientApiView.as_view(), name='deleteclient'),
    url(r'^employees/$',views.AllEmployeesView.as_view()  ),
    url(r'^employees/(?P<employee_id>\d+)/$',views.EmployeeView.as_view()  ),
    url(r'^managers/$',views.AllManagersView.as_view()) ,
    url(r'^clients/$',views.AllClientsView.as_view()  ),
    url(r'^clients/(?P<client_id>\d+)/$',views.ClientView.as_view()  ),
    
]