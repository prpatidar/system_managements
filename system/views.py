from django.shortcuts import render , redirect
from django.views.generic import View
from django.conf import settings
from django.template import loader
from django.contrib.auth import get_user_model
from .forms import EmployeeForm , ProjectForm ,TaskForm
from .models import Project, Task ,User
from django import forms


class HomePageView(View) :
   def get(self, request):
       return render(request,'system/home.html',{})

class EmployeePageView(View) :
   def get(self, request):
       User = get_user_model()
       users = User.objects.all()
       return render(request,'system/employee.html',{"users":users})

class EmployeeTaskPageView(View) :
   def get(self, request):
       tasks = Task.objects.all()
       return render(request,'system/employeetask.html',{"tasks":tasks})


class ProjectPageView(View) :
   def get(self, request):
       projects = Project.objects.all()
       return render(request,'system/project.html',{"projects":projects})

class TaskPageView(View) :
   def get(self, request,projectid):
       tasks = Task.objects.filter(project_id = projectid)
       return render(request,'system/task.html',{"tasks":tasks ,'projectid':projectid})


class CreateEmployeePageView(View):
   def get(self, request):
        form = EmployeeForm()
        form.fields['role'].widget = forms.HiddenInput()
        return render(request,'system/createemployee.html',{'form':form})
   def post(self,request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
          employee=form.save(commit=False)
          employee.role="employee"
          employee.save()
          return redirect('/system/employee')
        else :
          return render(request,'system/createemployee.html',{'form':form})

class CreateProjectPageView(View):
   def get(self, request):
        form = ProjectForm()
        return render(request,'system/createproject.html',{'form' : form})
   def post(self,request):
        form = ProjectForm(request.POST)
        if form.is_valid():
          form.save()
          return redirect('/system/project')
        else :
          return render(request,'system/createproject.html',{'form':form})

class CreateTaskPageView(View):
   def get(self, request,projectid):
        employees=User.objects.filter(role="employee")
        form = TaskForm()
        form.fields['project_id'].widget = forms.HiddenInput()
        return render(request,'system/createtask.html',{'form' : form,'projectid': projectid ,'employees':employees})
   def post(self,request,projectid):
        form = TaskForm(request.POST)
        if form.is_valid():
          print projectid
          task=form.save(commit=False)
          task.project_id_id=projectid
          task.save()
          return redirect('/system/project')
        else :
          print form.errors
          return render(request,'system/createtask.html',{'form':form ,'projectid' : projectid})

