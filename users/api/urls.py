
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
    url(r'^employees/$',views.AllEmployeesView.as_view()  ),
    url(r'^employees/(?P<employee_id>\d+)/$',views.EmployeeView.as_view()  ),
    url(r'^managers/$',login_required(views.AllManagersView.as_view()) ),
    url(r'^clients/$',views.AllClientsView.as_view()  ),
    url(r'^clients/(?P<client_id>\d+)/$',views.ClientView.as_view()  ),
    
 ]