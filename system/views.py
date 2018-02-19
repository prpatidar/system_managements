from django.shortcuts import render , redirect
from django.views.generic import View
from django.conf import settings
from django.template import loader
from django.contrib.auth import get_user_model
from .forms import EmployeeForm , ProjectForm ,TaskForm,TimeSheetForm
from .models import Project, Task ,User ,TimeSheet
from django import forms
import calendar,datetime
from collections import OrderedDict

class HomePageView(View) :
   def get(self, request):

       return render(request,'system/home.html',{})

class EmployeePageView(View) :
   def get(self, request,managerid):
       User = get_user_model()
       users = User.objects.filter(role='employee',createdby=managerid)
       return render(request,'system/employee.html',{"users":users,'managerid':managerid})

class EmployeeTaskPageView(View) :
   def get(self, request,projectid,employeeid):
       tasks = Task.objects.filter(project_id=projectid  , employee_id=employeeid)
       return render(request,'system/employeetask.html',{"tasks":tasks})

class EmployeeProjectPageView(View):
   def get(self, request,employeeid):
       tasks = Task.objects.filter(employee_id=employeeid)
       projectlist=[]
       for task in tasks:
            projectlist.append(task.project_id)
       projectlist=list(OrderedDict.fromkeys(projectlist))
       projects=Project.objects.filter(pk__in=projectlist) 
       return render(request,'system/employeeprojects.html',{"projects":projects,"employeeid":employeeid})

class ProjectPageView(View) :
   def get(self, request,managerid):
       projects = Project.objects.filter(createdby=managerid)
       return render(request,'system/project.html',{"projects":projects,'managerid':managerid})

class TimeSheetPageView(View):
   def get(self, request,employeeid):
       c=calendar.TextCalendar(calendar.MONDAY)
       date=datetime.datetime.now()
       days = []
       for i in c.itermonthdays(date.year,date.month):
           days.append(i)
       print employeeid
       timesheets=TimeSheet.objects.filter(month=date.month,employee_id=employeeid)
       print timesheets
       return render(request,'system/timesheet.html',{'timesheets':timesheets,'days' : days,'month':datetime.datetime.now().strftime('%B') , 'year' : date.year,'employeeid': employeeid } )

class TimeSheetFormPageView(View):
   def get(self, request,employeeid,day):
       tasks=Task.objects.filter(employee_id=employeeid)
       tasklist=[]
       for task in tasks :
           tasklist.append(task.title)
       return render(request,'system/timesheetform.html',{'employeeid': employeeid, 'day' : day,'tasklist' : tasklist })
   def post(self,request,employeeid,day):
       
       c=calendar.TextCalendar(calendar.MONDAY)
       date=datetime.datetime.now()
       timesheet=TimeSheet.objects.get(month=date.month,day=day,employee_id=employeeid)
       if timesheet :
         timesheet.taskname=request.POST.get('taskname')
         timesheet.spendtime=request.POST.get('spendtime')
         timesheet.save()
       else :
         form=TimeSheetForm()
         f=form.save(commit=False)
         f.day=day
         f.employee_id=employeeid
         f.month=date.month
         f.year=date.year
         f.spendtime=request.POST.get('spendtime')
         f.taskname =request.POST.get('taskname')
         f.save()
       print TimeSheet.objects.all()
       return redirect('/system/timesheet/'+employeeid+'/')



class DeleteProfilePageView(View):
   def get(self,request,employeeid,managerid):
       User.objects.filter(id=employeeid).delete()
       return redirect('/system/employee/'+managerid+'/')

class DeleteProjectPageView(View):
   def get(self,request,projectid,managerid):
       Project.objects.filter(id=projectid).delete()
       Task.objects.filter(project_id=projectid).delete()
       return redirect('/system/project/'+managerid+'/')


class UpdateTaskPageView(View):
   def get(self,request,taskid):
       return render(request,'system/updatetask.html' ,{'taskid':taskid})
   def post(self,request,taskid):
       task=Task.objects.get(id=taskid)
       task.status=request.POST.get('status')
       estimatetime =request.POST.get('estimatetime')
       if(estimatetime):
           task.estimatetime = estimatetime
       spendtime = request.POST.get('spendtime')
       if(spendtime):
          task.spendtime = spendtime
       task.save()
       return redirect('/system/home')


class TaskPageView(View) :
   def get(self, request,projectid,managerid):
       tasks = Task.objects.filter(project_id = projectid)
       return render(request,'system/task.html',{'tasks':tasks ,'projectid':projectid,'managerid':managerid})


class CreateEmployeePageView(View):
   def get(self, request,managerid):
        form = EmployeeForm()
        form.fields['role'].widget = forms.HiddenInput()
        return render(request,'system/createemployee.html',{'form':form,'managerid':managerid})
   def post(self,request,managerid):
        form = EmployeeForm(request.POST)
        if form.is_valid():
          employee=form.save(commit=False)
          employee.role="employee"
          employee.createdby=managerid
          employee.save()
          return redirect('/system/employee/'+managerid+'/')
        else :
          return render(request,'system/createemployee.html',{'form':form,'managerid':managerid})

class CreateProjectPageView(View):
   def get(self, request,managerid):
        form = ProjectForm()
        return render(request,'system/createproject.html',{'form' : form ,'managerid': managerid})
   def post(self,request,managerid):
        form = ProjectForm(request.POST)
        if form.is_valid():
          f=form.save(commit=False)
          f.createdby=managerid
          f.save()
          return redirect('/system/project/'+managerid+'/')
        else :
          return render(request,'system/createproject.html',{'form':form,'managerid': managerid})

class CreateTaskPageView(View):
   def get(self, request,projectid,managerid):
        employees=User.objects.filter(role="employee",createdby=managerid)
        form = TaskForm()
        form.fields['project'].widget = forms.HiddenInput()
        return render(request,'system/createtask.html',{'form' : form,'projectid': projectid ,'employees':employees,'managerid':managerid})
   def post(self,request,projectid,managerid):
        form = TaskForm(request.POST)
        if form.is_valid():
          print projectid
          task=form.save(commit=False)
          task.project_id=projectid
          task.employee_id = request.POST.get('employeeid')
          task.save()
          return redirect('/system/project/'+managerid+'/')
        else :
          print form.errors
          return render(request,'system/createtask.html',{'form':form ,'projectid' : projectid,'managerid':managerid})

class UpdateProfilePageView(View):
   def get(self,request,employeeid):
       form = EmployeeForm()
       form.fields['role'].widget = forms.HiddenInput()
       return render(request,'system/updateprofile.html' ,{'form':form,'employeeid':employeeid})
   def post(self,request,employeeid):
       user=User.objects.get(id=employeeid)
       employee=EmployeeForm(request.POST)
       if employee.is_valid():
        if(employee.cleaned_data['first_name']):
          user.first_name=employee.cleaned_data['first_name']
        if(employee.cleaned_data['last_name']):
          user.last_name=employee.cleaned_data['last_name']
        if(employee.cleaned_data['email']):
          user.email=employee.cleaned_data['email']
        if(employee.cleaned_data['username']):
          user.username=employee.cleaned_data['username']
        user.save()
       return redirect('/system/home')