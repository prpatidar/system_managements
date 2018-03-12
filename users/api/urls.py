
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from users.api import views

urlpatterns = [
    
    url(r'^employees/$',views.AllEmployeesView.as_view()  ),
    url(r'^employees/(?P<employee_id>\d+)/$',views.EmployeeView.as_view()  ),
    url(r'^managers/$',views.AllManagersView.as_view()  ),
    url(r'^clients/$',views.AllClientsView.as_view()  ),
    url(r'^clients/(?P<client_id>\d+)/$',views.ClientView.as_view()  ),
    
 ]