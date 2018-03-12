from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from creditcard import views 

urlpatterns = [
    
    url(r'^creditcard/(?P<client_id>\d+)/$' , views.CreditcardPageView.as_view() , name='creditcard' ) ,
    url(r'^createcreditcard/(?P<client_id>\d+)/$' , views.CreateCreditCardPageView.as_view() , name='createcreditcard' ) ,
    url(r'^deletecreditcard/(?P<client_id>\d+)/(?P<card_id>\d+)/$' , views.DeleteCreditCardPageView.as_view() , name='deletecreditcard' ) ,
    url(r'^primarycreditcard/(?P<client_id>\d+)/(?P<card_id>\d+)/$' , views.PrimaryCreditCardPageView.as_view() , name='primarycreditcard' ) ,
    
]
