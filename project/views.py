import calendar,datetime
from collections import OrderedDict

from django import forms
from django.conf import settings
from django.template import loader
from django.views.generic import View
from project.models import Project, Task 
from django.core.urlresolvers import reverse
from django.shortcuts import render , redirect
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from users.forms import EmployeeForm
from timesheet.models import TimeSheet
from timesheet.forms import TimeSheetForm
from project.forms import ProjectForm ,TaskForm

#Task list view for employees
class EmployeeTaskPageView(View):

    def get(self, request, project_id, employee_id):
        response = {}
        response['tasks'] = Task.objects.filter(project_id=project_id, employee_id=employee_id)
        return render(request, 'project/employeetask.html', response)


#this a project list view for employees
class EmployeeProjectPageView(View):

    def get(self, request, employee_id):
        response = {'employee_id': employee_id}
        date = datetime.datetime.now()
        response['month'] = date.month
        response['year'] = date.year
        project_ids = Task.objects.filter(employee_id=employee_id).values_list('project_id', flat=True)
        response['projects'] = Project.objects.filter(pk__in=project_ids)
        return render(request, 'project/employeeprojects.html', response)


#this a project list view for client
class ClientProjectPageView(View):

    def get(self, request, client_id):
        response = {'client_id': client_id}
        date = datetime.datetime.now()
        response['month'] = date.month
        response['year'] = date.year
        response['projects'] = Project.objects.filter(client_id=client_id)
        return render(request, 'project/clientprojects.html', response)


# project list view for manager
class ProjectPageView(View):

    def get(self, request, manager_id):
        response = {'manager_id': manager_id}
        date = datetime.datetime.now()
        response['month'] = date.month
        response['year'] = date.year
        response['projects'] = Project.objects.filter(createdby=manager_id)
        return render(request, 'project/project.html', response)


# view to delete a project by manager 
class DeleteProjectPageView(View):

    def get(self, request, project_id, manager_id):
        Project.objects.filter(id=project_id).delete()
        Task.objects.filter(project_id=project_id).delete()
        return redirect(reverse('project' ,kwargs ={'manager_id': manager_id}))


#view is used to update task progress 
class UpdateTaskPageView(View):

    def get(self, request, task_id):
        response = {'task_id':task_id}
        return render(request,'project/updatetask.html' , response)

    def post(self, request, task_id):
        task=Task.objects.get(id=task_id)
        task.status=request.POST.get('status')
        estimatetime =request.POST.get('estimatetime')
        if estimatetime:
            task.estimatetime = estimatetime
        spendtime = request.POST.get('spendtime')
        if spendtime:
            task.spendtime = spendtime
        task.save()
        return redirect(reverse('home'))


# view to update hourlyrate and payment type for project by client
class ProjectFormPageView(View):

    def post(self, request):
        project_id=request.POST.get('project_id')
        print request.POST
        project=Project.objects.get(id=int(project_id))
        payment_type =request.POST.get('payment_type')
        if payment_type:
            project.payment_type = payment_type
        hourlyrate = request.POST.get('hourlyrate')
        if hourlyrate:
            project.hourlyrate = hourlyrate
        project.save()
        return redirect(reverse('home'))


#view to update the task starting and end dates
class UpdateDatePageView(View):

    def get(self, request, task_id):
        response = {'task_id':task_id}
        return render(request, 'project/updatedate.html' , response)

    def post(self, request, task_id):
        task=Task.objects.get(id=task_id)
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        if startdate :
            task.startdate = startdate
        if enddate :
            task.enddate = enddate
        task.save()
        return redirect(reverse('home'))


# task view for manager
class TaskPageView(View):
    
    def get(self, request, project_id, manager_id):
        response = {'project_id': project_id, 'manager_id': manager_id }
        response['tasks'] = Task.objects.filter(project_id = project_id)
        return render(request,'project/task.html', response)

 
# create project view for manager
class CreateProjectPageView(View):
    
    def get(self, request, manager_id):
        response = {'manager_id': manager_id }
        response['clients']=User.objects.filter(role="client", createdby=manager_id)
        response['form'] = ProjectForm()
        return render(request, 'project/createproject.html', response)
    
    def post(self, request, manager_id):
        response = {'manager_id': manager_id }

        response['form'] = ProjectForm()
        form = ProjectForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.createdby=manager_id 
            f.client_id= request.POST.get('client_id')
            f.save()
            return redirect(reverse('project' ,kwargs ={'manager_id': manager_id}))
        else:
            return render(request, 'project/createproject.html', response)


#create task view for manager
class CreateTaskPageView(View):
   
    def get(self, request, project_id, manager_id):
        response = {'project_id': project_id, 'manager_id':manager_id}
        response['employees']=User.objects.filter(role="employee", createdby=manager_id)
        response['form'] = TaskForm()
        response['form'].fields['project'].widget = forms.HiddenInput()
        return render(request,'project/createtask.html', response)
    def post(self, request, project_id, manager_id):
        response = {'project_id': project_id, 'manager_id': manager_id}
        form = TaskForm(request.POST)
        response['form'] = form
        if form.is_valid():
            task=form.save(commit=False)
            task.project_id=project_id
            task.employee_id = request.POST.get('employee_id')
            task.save()
            return redirect(reverse('project' ,kwargs ={'manager_id': manager_id}))
        else:
            print form.errors
            return render(request, 'project/createtask.html', response )

