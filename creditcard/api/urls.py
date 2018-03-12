
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from creditcard.api import views 

urlpatterns = [
    
    url(r'^clients/(?P<client_id>\d+)/creditcards/$', views.ClientCreditCardsView.as_view() ),
 ]