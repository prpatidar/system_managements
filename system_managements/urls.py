from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

from users.views import index_page_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^timesheet/', include('timesheet.urls')),
    url('', index_page_view , name='index'),
]
