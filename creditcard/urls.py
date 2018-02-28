from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from .views import creditcard_page_view, create_creditcard_page_view, delete_creditcard_page_view, primary_creditcard_page_view


urlpatterns = [
    
    url(r'^creditcard/(?P<client_id>\d+)/$' , creditcard_page_view , name='creditcard' ) ,
    url(r'^createcreditcard/(?P<client_id>\d+)/$' , create_creditcard_page_view , name='createcreditcard' ) ,
    url(r'^deletecreditcard/(?P<client_id>\d+)/(?P<card_id>\d+)/$' , delete_creditcard_page_view , name='deletecreditcard' ) ,
     url(r'^primarycreditcard/(?P<client_id>\d+)/(?P<card_id>\d+)/$' , primary_creditcard_page_view , name='primarycreditcard' ) ,
    
]
