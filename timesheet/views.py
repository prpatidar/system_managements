
import stripe
import smtplib
import calendar ,datetime
from datetime import  timedelta
from smtplib import SMTPException
from collections import OrderedDict

from django import forms
from django.conf import settings
from django.template import loader
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.shortcuts import render , redirect
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from creditcard.models import Card
from users.models import User
from users.forms import EmployeeForm
from timesheet.models import TimeSheet
from project.models import Project, Task 
from timesheet.forms import TimeSheetForm
from project.forms import ProjectForm ,TaskForm

#this a timesheet view for employees
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
            if task.startdate :
                if task.startdate <= date :
                    tasklist.append(task.title)
        response['tasklist'] = tasklist
        return render(request,'timesheet/timesheet.html', response )
             
#this a timesheet filling view for the employees
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
            timesheet.status="pending"
            timesheet.payment = 0
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

#this view is for employee action on their timesheet
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
    

#this a timesheet view for manager action on employees timesheet
class TimeSheetManagerActionPageView(View):

    def get(self, request, employee_id, project_id, manager_id, day, month, year,period):
         period = int(period)
         day = int(day)
         date = datetime.datetime.now().date()
         if period == 1 :
            TimeSheet.objects.filter(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year,status="submit").update(status="aprove",reject_comment="",approvaldate=date)
         if period == 2 :
            i = day
            while (i > day-8) :
                TimeSheet.objects.filter(month=month, day=i, employee_id=employee_id, project_id=project_id, year=year,status="submit").update(status="aprove",reject_comment="",approvaldate=date)
                i = i-1
         if period == '3' :
            i = day
            while i < 32 :
                TimeSheet.objects.filter(month=month, day=i, employee_id=employee_id, project_id=project_id, year=year,status="submit").update(status="aprove",reject_comment="",approvaldate=date)
                i = i+1
       
         project = Project.objects.get(id= project_id)
         stripe.api_key = "sk_test_6NXzQP1ksrl4ApeJn5TdJ9SW"
         client_id = project.client_id
         card = Card.objects.get(client_id=client_id,primary=True)
         customer = User.objects.get(id=client_id)
         try:
            timesheets = TimeSheet.objects.filter(project_id=project_id,employee_id=employee_id,status="aprove",payment = 0)
            for timesheet in timesheets:
                pastdate = datetime.datetime.now().date()-datetime.timedelta(days=5)
                if timesheet.approvaldate and timesheet.approvaldate < pastdate  : 
                    print "hello"
                    timesheet.payment = timesheet.spendtime * project.hourlyrate 
                    stripecharge = stripe.Charge.create(
                    amount = timesheet.payment+1000,
                    currency="usd",
                    customer = customer.stripetoken,
                    source = card.card_token, # obtained with Stripe.js
                    description="Project Payment"
                    )
                    timesheet.save()
                    try:
                        session = smtplib.SMTP('smtp.gmail.com',587)
                        session.ehlo()
                        session.starttls()
                        session.ehlo()
                        session.login('pradeeppatidar2018@gmail.com','ppatidar2018')
                        session.sendmail('pradeeppatidar2018@gmail.com', customer.email, 'amount deducted from your account is :')         
                        session.quit()
                        print "Successfully sent email"
                    except SMTPException:
                        print "Error: unable to send email"
                    
         except ObjectDoesNotExist :
            print "nothing" 
         project.save()
         t = TimeSheet.objects.filter(employee_id=employee_id,project_id=project_id)
         for t in t :
            print t.status , t.reject_comment,t.month,t.year,t.day,project_id,t.approvaldate
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


#this a completed timesheet view for clients 
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
             


#this a timesheet view for manager which is filled by employees
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
             
#this a timesheet view for payment by client on aproved timesheets
class ClientPaymentPageView(View):

    def get(self, request, employee_id, project_id, client_id, day, month, year, period):
         period = int(period)
         day = int(day)
         project = Project.objects.get(id= project_id)
         stripe.api_key = "sk_test_6NXzQP1ksrl4ApeJn5TdJ9SW"
         card = Card.objects.get(client_id=client_id,primary=True)
         customer = User.objects.get(id=client_id)
         if period == 1 :
            try:
                timesheet = TimeSheet.objects.get(month=month, day=day, employee_id=employee_id, project_id=project_id, year=year,status="aprove")
                if timesheet : 
                    timesheet.payment = timesheet.spendtime * project.hourlyrate 
                    stripecharge = stripe.Charge.create(
                    amount = timesheet.payment+1000,
                    currency="usd",
                    customer = customer.stripetoken,
                    source = card.card_token, # obtained with Stripe.js
                    description="Project Payment"
                     )
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
                        stripecharge = stripe.Charge.create(
                        amount = timesheet.payment+1000,
                        currency="usd",
                        customer = customer.stripetoken,
                        source = card.card_token, # obtained with Stripe.js
                        description="Project Payment"
                         )
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
                        stripecharge = stripe.Charge.create(
                        amount = timesheet.payment+1000,
                        currency="usd",
                        customer = customer.stripetoken,
                        source = card.card_token, # obtained with Stripe.js
                        description="Project Payment"
                        )
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

    
