from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rest_framework import routers
from rest_framework import viewsets
from rest_framework import generics

from users.views import index_page_view


urlpatterns = [
	url(r'^api/', include('users.api.urls')),
	url(r'^api/', include('project.api.urls')),
    url(r'^api/', include('timesheet.api.urls')),
    url(r'^api/', include('creditcard.api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^timesheet/', include('timesheet.urls')),
    url(r'^creditcard/', include('creditcard.urls')),
    url(r'^$', index_page_view , name='index'),
]
# urlpatterns = format_suffix_patterns(urlpatterns , allowed=['json', 'html'])