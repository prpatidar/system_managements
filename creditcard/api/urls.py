
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from creditcard.api.views import client_creditcards_page_view

urlpatterns = [
    
    url(r'^clients/(?P<client_id>\d+)/creditcards/$', client_creditcards_page_view ),
    
 ]