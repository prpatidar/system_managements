from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth import views as auth_views

from rest_framework import routers
from rest_framework import viewsets
from rest_framework import generics

from users.views import IndexPageView

urlpatterns = [
	url(r'^api/user/', include('users.api.urls')),
	url(r'^api/user/', include('project.api.urls')),
    url(r'^api/user/', include('timesheet.api.urls')),
    url(r'^api/user/', include('creditcard.api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^timesheet/', include('timesheet.urls')),
    url(r'^creditcard/', include('creditcard.urls')),
    url(r'^$', IndexPageView.as_view() , name='index'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    
]
# urlpatterns = format_suffix_patterns(urlpatterns , allowed=['json', 'html'])