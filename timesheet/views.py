
import calendar, datetime
from collections import OrderedDict

from django import forms
from django.conf import settings
from django.template import loader
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.shortcuts import render , redirect
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from users.forms import EmployeeForm
from timesheet.models import TimeSheet
from project.models import Project, Task 
from timesheet.forms import TimeSheetForm
from project.forms import ProjectForm ,TaskForm


class TimeSheetPageView(View):

    def get(self, request, employee_id, project_id, month,year):
        response = {'employee_id': employee_id, 'month' : month , 'year' : year} 
        c=calendar.TextCalendar(calendar.MONDAY)
        days = []
        month = int(month)
        year = int(year)
        totaldays = 0
        for i in c.itermonthdays(year, month):
            days.append(i)
            totaldays += 1 
        response['project'] = Project.objects.get(id=project_id)
        response['timesheets']=TimeSheet.objects.filter(project_id=project_id, month=month, employee_id=employee_id,year=year)
        response['days'] = days
        response['previousmonth'] = month-1
        if month == 1 :
            response['previousmonth'] = 12
        response['nextmonth'] = month + 1 
        if month ==12 :
            response['nextmonth'] = 1
        response['previousyear'] = year-1
        response['nextyear'] = year + 1
        date = datetime.datetime.now().date()
        daylist = []
        today = date.day
        if year == date.year and month == date.month :
            i=today
            while i > today-7 and i > 0  :
                daylist.append(i)
                i = i-1   
        if today < 7 and month == date.month-1 and year==date.year :
            while today < 7 :
                daylist.append(days[totaldays-5])
                totaldays -= 1
                today += 1
        print daylist
       #TimeSheet.objects.all().delete()
        response['daylist'] = daylist
        response['today'] = date.day
        response['currentyear'] = date.year
        response['currentmonth'] = date.month
        response['monthname'] = calendar.month_name[month]
        tasks=Task.objects.filter(employee_id=employee_id, project_id=project_id)
        tasklist=[]
        for task in tasks :
            if task.enddate :
                if task.startdate <= date and task.enddate >= date :
                    tasklist.append(task.title)
            elif task.startdate :
                if task.startdate <= date :
                    tasklist.append(task.title)
        response['tasklist'] = tasklist
        return render(request,'timesheet/timesheet.html', response )
             

timesheet_page_view = TimeSheetPageView.as_view()


class TimeSheetFormPageView(View):
    
    def post(self, request, employee_id, project_id, day, month, year):
        day=request.POST.get('day')
        print "hloo"+day
        c=calendar.TextCalendar(calendar.MONDAY)
        date=datetime.datetime.now()
        try :
            timesheet=TimeSheet.objects.get(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year)
        except ObjectDoesNotExist :
            timesheet = None 
        if timesheet :
            timesheet.taskname=request.POST.get('taskname')
            timesheet.spendtime=request.POST.get('spendtime')
            timesheet.save()
        else :
            form=TimeSheetForm()
            f=form.save(commit=False)
            f.day=day
            f.project_id=project_id
            f.employee_id=employee_id
            f.month=month
            f.year=year
            f.spendtime=request.POST.get('spendtime')
            f.taskname =request.POST.get('taskname')
            f.save()

        return redirect(reverse('timesheet' ,kwargs ={'employee_id': employee_id, 'project_id' : project_id, 'month' : month, 'year': year}))

time_sheet_form_page_view = TimeSheetFormPageView.as_view()

class TimeSheetActionPageView(View):

    def get(self, request, employee_id, project_id, day, month, year , period):
         period = int(period)
         day_int = int(day)
         if period == 1 :
            TimeSheet.objects.filter(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year,status="pending").update(status="submit")
            TimeSheet.objects.filter(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year,status="rejected").update(status="submit",reject_comment="")
         if period == 2 :
            i = day_int
            while (i > day_int-8) :
                TimeSheet.objects.filter(month=month, day=i, employee_id=employee_id, project_id=project_id, year=year,status="pending").update(status="submit")
                TimeSheet.objects.filter(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year,status="rejected").update(status="submit",reject_comment="")
                i = i-1
         if period == '3' :
            i = day_int
            while i < 32 :
                TimeSheet.objects.filter(month=month, day=i, employee_id=employee_id, project_id=project_id, year=year,status="pending").update(status="submit")
                TimeSheet.objects.filter(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year,status="rejected").update(status="submit",reject_comment="")
                i = i+1
         
         t = TimeSheet.objects.filter(employee_id=employee_id)
         for t in t :
            print t.status , t.reject_comment,t.month,t.year,t.day
         return redirect(reverse('timesheet' ,kwargs ={'employee_id': employee_id, 'project_id' : project_id, 'month' : month, 'year': year}))
    
time_sheet_action_page_view = TimeSheetActionPageView.as_view()


class TimeSheetManagerActionPageView(View):

    def get(self, request, employee_id, project_id, manager_id, day, month, year,period):
         period = int(period)
         day = int(day)
         if period == 1 :
            TimeSheet.objects.filter(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year,status="submit").update(status="aprove",reject_comment="")
         if period == 2 :
            i = day
            while (i > day-8) :
                TimeSheet.objects.filter(month=month, day=i, employee_id=employee_id, project_id=project_id, year=year,status="submit").update(status="aprove",reject_comment="")
                i = i-1
         if period == '3' :
            i = day
            while i < 32 :
                TimeSheet.objects.filter(month=month, day=i, employee_id=employee_id, project_id=project_id, year=year,status="submit").update(status="aprove",reject_comment="")
                i = i+1
        
         t = TimeSheet.objects.filter(employee_id=employee_id)
         for t in t :
            print t.status , t.reject_comment,t.month,t.year,t.day,project_id
         return redirect(reverse('managertimesheet' ,kwargs ={'employeeid': employee_id, 'project_id' : project_id, 'manager_id' :manager_id ,'month' : month, 'year': year}))

    def post(self, request, employee_id, project_id, manager_id, day, month, year,period):
         period = int(request.POST.get('period'))
         day=int(request.POST.get('day'))
         print day + period
         comment = request.POST.get('comment')
         if period == 1 :
            TimeSheet.objects.filter(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year,status="submit").update(status="rejected",reject_comment=comment)
         if period == 2 :
            i = day
            while i >= day-7 :
                TimeSheet.objects.filter(month=month, day=i, employee_id=employee_id, project_id=project_id, year=year,status="submit").update(status="rejected",reject_comment=comment)
                i = i-1
         if period == 3 :
            i = day
            while i <= 31 :
                TimeSheet.objects.filter(month=month, day=i, employee_id=employee_id, project_id=project_id, year=year,status="submit").update(status="rejected",reject_comment=comment)
                i = i+1

         t = TimeSheet.objects.all()
         return redirect(reverse('managertimesheet' ,kwargs ={'employeeid': employee_id, 'project_id' : project_id, 'manager_id' :manager_id , 'month' : month, 'year': year}))



time_sheet_manager_action_page_view = TimeSheetManagerActionPageView.as_view()



class ClientTimeSheetPageView(View):

    def get(self, request, employeeid, client_id, project_id, month,year):
        emp_id= request.GET.get('employee_id')
        if emp_id :
            employeeid=emp_id
        response = {'employeeid': employeeid, 'client_id' :client_id , 'month' : month , 'year' : year} 
        c=calendar.TextCalendar(calendar.MONDAY)
        days = []
        month = int(month)
        year = int(year)
        totaldays = 0
        for i in c.itermonthdays(year, month):
            days.append(i)
            totaldays += 1 
        response['project'] = Project.objects.get(id=project_id)
        response['timesheets']=TimeSheet.objects.filter(project_id=project_id, month=month, employee_id=employeeid,year=year)
        response['days'] = days
        response['previousmonth'] = month-1
        if month == 1 :
            response['previousmonth'] = 12
        response['nextmonth'] = month + 1 
        if month ==12 :
            response['nextmonth'] = 1
        response['previousyear'] = year-1
        response['nextyear'] = year + 1
        date = datetime.datetime.now().date()
        daylist = []
        today = date.day
        if year == date.year and month == date.month :
            i=today
            while i > today-7 and i > 0  :
                daylist.append(i)
                i = i-1   
        if today < 7 and month == date.month-1 and year==date.year :
            while today < 7 :
                daylist.append(days[totaldays-5])
                totaldays -= 1
                today += 1
       #TimeSheet.objects.all().delete()
        response['daylist'] = daylist
        response['today'] = date.day
        response['currentyear'] = date.year
        response['currentmonth'] = date.month
        response['monthname'] = calendar.month_name[month]
        tasks=Task.objects.filter(employee_id=employeeid, project_id=project_id)
        tasklist=[]
        for task in tasks :
            if task.enddate :
                if task.startdate <= date and task.enddate >= date :
                    tasklist.append(task.title)
            elif task.startdate :
                if task.startdate <= date :
                    tasklist.append(task.title)
        response['tasklist'] = tasklist
        response['employees'] = Task.objects.filter(project_id=project_id).values_list('employee_id', flat=True).distinct()
        print response['employees']
        return render(request,'timesheet/clienttimesheet.html', response )
             

client_timesheet_page_view = ClientTimeSheetPageView.as_view()


class ManagerTimeSheetPageView(View):

    def get(self, request, employeeid,  project_id,manager_id, month, year ):
        emp_id= request.GET.get('employee_id')
        if emp_id :
            employeeid=emp_id
        response = {'employeeid': employeeid, 'manager_id' :manager_id , 'month' : month , 'year' : year} 
        c=calendar.TextCalendar(calendar.MONDAY)
        days = []
        month = int(month)
        year = int(year)
        totaldays = 0
        for i in c.itermonthdays(year, month):
            days.append(i)
            totaldays += 1 
        response['project'] = Project.objects.get(id=project_id)
        response['timesheets']=TimeSheet.objects.filter(project_id=project_id, month=month, employee_id=employeeid,year=year)
        response['days'] = days
        response['previousmonth'] = month-1
        if month == 1 :
            response['previousmonth'] = 12
        response['nextmonth'] = month + 1 
        if month ==12 :
            response['nextmonth'] = 1
        response['previousyear'] = year-1
        response['nextyear'] = year + 1
        date = datetime.datetime.now().date()
        daylist = []
        today = date.day
        if year == date.year and month == date.month :
            i=today
            while i > today-7 and i > 0  :
                daylist.append(i)
                i = i-1   
        if today < 7 and month == date.month-1 and year==date.year :
            while today < 7 :
                daylist.append(days[totaldays-5])
                totaldays -= 1
                today += 1
       #TimeSheet.objects.all().delete()
        response['daylist'] = daylist
        response['today'] = date.day
        response['currentyear'] = date.year
        response['currentmonth'] = date.month
        response['monthname'] = calendar.month_name[month]
        tasks=Task.objects.filter(employee_id=employeeid, project_id=project_id)
        tasklist=[]
        for task in tasks :
            if task.enddate :
                if task.startdate <= date and task.enddate >= date :
                    tasklist.append(task.title)
            elif task.startdate :
                if task.startdate <= date :
                    tasklist.append(task.title)
        response['tasklist'] = tasklist
        response['employees'] = Task.objects.filter(project_id=project_id).values_list('employee_id', flat=True).distinct()
        return render(request,'timesheet/managertimesheet.html', response )
             

manager_timesheet_page_view = ManagerTimeSheetPageView.as_view()

class ClientPaymentPageView(View):

    def get(self, request, employee_id, project_id, client_id, day, month, year, period):
         period = int(period)
         day = int(day)
         project = Project.objects.get(id= project_id)
         if period == 1 :
            try:
                timesheet = TimeSheet.objects.get(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year,status="aprove")
                if timesheet : 
                    timesheet.payment = timesheet.spendtime * project.hourlyrate 
                    print timesheet.payment
                    timesheet.save() 
            except ObjectDoesNotExist :
                print "nothing" 
         if period == 2 :
            i = day
            payment = 0
            while (i > day-7) :
                try:
                    timesheet = TimeSheet.objects.get(month=month, day=i, employee_id=employee_id, project_id=project_id, year=year,status="aprove")
                    if timesheet :
                        timesheet.payment = timesheet.spendtime * project.hourlyrate 
                        payment = payment + timesheet.payment
                        timesheet.save()
                except ObjectDoesNotExist :
                    print "nothing" 
                i = i-1
            print payment
         if period == 3 :
            i = 1
            payment = 0
            while i < 32 :
                try:
                    timesheet = TimeSheet.objects.get(month=month, day=i, employee_id=employee_id, project_id=project_id, year=year,status="aprove")
                    if timesheet :
                        timesheet.payment = timesheet.spendtime * project.hourlyrate 
                        payment = payment + timesheet.payment
                        timesheet.save()
                except ObjectDoesNotExist :
                    print "nothing" 
                i = i+1
            print payment
         project.save()
         # TimeSheet.objects.all().update(payment=0)
         t = TimeSheet.objects.filter(employee_id=employee_id)
         for t in t :
            print t.status , t.reject_comment,t.month,t.year,t.day,project_id
         return redirect(reverse('clienttimesheet' ,kwargs ={'employeeid': employee_id, 'project_id' : project_id, 'client_id' : client_id ,'month' : month, 'year': year}))

    
client_payment_page_view = ClientPaymentPageView.as_view()
