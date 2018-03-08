
from django.contrib import admin
from django.conf.urls import url
# from rest_framework import routers
from django.conf.urls import include

from users.api.views import all_employees_page_view , employee_page_view , managers_page_view, clients_page_view ,client_page_view

urlpatterns = [
    
    url(r'^employees/$', all_employees_page_view ),
    url(r'^employees/(?P<employee_id>\d+)/$', employee_page_view ),
    url(r'^managers/$', managers_page_view ),
    url(r'^clients/$', clients_page_view ),
    url(r'^clients/(?P<client_id>\d+)/$', client_page_view ),
    
 ]