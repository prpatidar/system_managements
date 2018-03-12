
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from timesheet import views
urlpatterns = [
  
    
    url(r'^timesheetform/(?P<employee_id>\d+)/(?P<project_id>\d+)/(?P<day>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' ,views.TimeSheetFormPageView.as_view()  , name='timesheetform' ) ,
    url(r'^timesheet/(?P<employee_id>\d+)/(?P<project_id>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' ,views.TimeSheetPageView.as_view()  , name='timesheet' ) ,
    url(r'^clienttimesheet/(?P<employeeid>\d+)/(?P<project_id>\d+)/(?P<client_id>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' , views.ClientTimeSheetPageView.as_view() , name='clienttimesheet' ) ,
    url(r'^clientpayment/(?P<employee_id>\d+)/(?P<project_id>\d+)/(?P<client_id>\d+)/(?P<day>\d+)/(?P<month>\d+)/(?P<year>\d+)/(?P<period>\d+)/$' , views.ClientPaymentPageView.as_view() , name='clientpayment' ) ,
    url(r'^managertimesheet/(?P<employeeid>\d+)/(?P<project_id>\d+)/(?P<manager_id>\d+)/(?P<month>\d+)/(?P<year>\d+)/$' , views.ManagerTimeSheetPageView.as_view() , name='managertimesheet' ) ,
    url(r'^timesheetaction/(?P<employee_id>\d+)/(?P<project_id>\d+)/(?P<day>\d+)/(?P<month>\d+)/(?P<year>\d+)/(?P<period>\d+)/$' , views.TimeSheetActionPageView.as_view() , name='timesheetaction' ) ,
    url(r'^timesheetmanageraction/(?P<employee_id>\d+)/(?P<project_id>\d+)/(?P<manager_id>\d+)/(?P<day>\d+)/(?P<month>\d+)/(?P<year>\d+)/(?P<period>\d+)/$' , views.TimeSheetManagerActionPageView.as_view() , name='timesheetmanageraction' ) ,
] 
