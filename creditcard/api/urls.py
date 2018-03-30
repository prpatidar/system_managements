
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from creditcard.api import views 

urlpatterns = [

    url(r'^createcreditcard/$',  views.CreateCreditCardApiView.as_view(), name='createcreditcard'),
    url(r'^creditcards/$', views.ClientCreditCardsView.as_view() ),
    url(r'^makeprimary/$', views.CreditCardsView.as_view() ),
    url(r'^makeprimary/(?P<card_id>\d+)/$', views.CreditCardView.as_view() ),
 	url(r'^deletecard/$', views.CreditCardsView.as_view() ),
    url(r'^deletecard/(?P<card_id>\d+)/$', views.DeleteCreditCardView.as_view() ),
 
 
 ]