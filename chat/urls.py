from django.conf.urls import url
from django.contrib import admin
from chat.views import index


urlpatterns = [
    url(r'^$', index, name='chat_index'),  # The start point for index view
]