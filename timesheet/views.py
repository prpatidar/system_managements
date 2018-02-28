
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

    def get(self, request, employee_id, project_id, day, month, year):
        TimeSheet.objects.filter(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year).update(status="submit")
        return redirect(reverse('timesheet' ,kwargs ={'employee_id': employee_id, 'project_id' : project_id, 'month' : month, 'year': year}))

time_sheet_action_page_view = TimeSheetActionPageView.as_view()


class TimeSheetManagerActionPageView(View):

    def get(self, request, employee_id, project_id, manager_id, day, month, year):
        TimeSheet.objects.filter(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year).update(status="aprove")
        return redirect(reverse('managertimesheet' ,kwargs ={'employeeid': employee_id, 'project_id' : project_id, 'manager_id' :manager_id ,'month' : month, 'year': year}))


    def post(self, request, employee_id, project_id, manager_id, day, month, year):
         day=request.POST.get('day')
         print "hloo"+day
         comment = request.POST.get('comment')
         timesheet=TimeSheet.objects.get(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year)
         timesheet.status = "rejected"
         timesheet.reject_comment = comment
         timesheet.save()
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

    def get(self, request, employeeid,  project_id,manager_id, month,year):

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
        print response['employees']
        return render(request,'timesheet/managertimesheet.html', response )
             

manager_timesheet_page_view = ManagerTimeSheetPageView.as_view()

