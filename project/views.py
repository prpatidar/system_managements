import calendar,datetime
from collections import OrderedDict

from django import forms
from django.conf import settings
from django.template import loader
from django.http import JsonResponse
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
from project.forms import ProjectForm, TaskForm, UpdateProjectForm, UpdateTaskForm 

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
        response['clients']=User.objects.filter(role="client", createdby=manager_id)
        response['form'] = ProjectForm()
        response['form'].fields['status'].widget = forms.HiddenInput()
        response['projects'] = Project.objects.filter(createdby=manager_id)
        return render(request, 'project/project.html', response)

#view is used to update project 
class UpdateProjectPageView(View):

    def get(self, request, project_id,manager_id):
        response = {'project_id':project_id,'manager_id':manager_id}
        data=Project.objects.get(id=project_id,createdby=manager_id)
        response['form'] = UpdateProjectForm(instance=data)
        if data.status=='Started':
            response['form'].fields['title'].widget = forms.HiddenInput()
            response['form'].fields['startdate'].widget = forms.HiddenInput()
            response['form'].fields['hourlyrate'].widget = forms.HiddenInput()
            response['form'].fields['payment_type'].widget = forms.HiddenInput()
        return render(request,'project/updateproject.html' , response)

    def post(self, request, project_id,manager_id):
        response = {'project_id':project_id,'manager_id':manager_id}
        print request.POST
        form = UpdateProjectForm(request.POST)
        project=Project.objects.get(id=project_id,createdby=manager_id)
        print project.title
        if form.is_valid():
            if form.cleaned_data['title']:
                project.title = form.cleaned_data['title']
            if form.cleaned_data['discription']:
                project.discription = form.cleaned_data['discription']
            if form.cleaned_data['status']:
                project.status = form.cleaned_data['status']
            if form.cleaned_data['startdate']:
                project.startdate = form.cleaned_data['startdate']
            if form.cleaned_data['enddate']:
                project.enddate = form.cleaned_data['enddate']
            if form.cleaned_data['hourlyrate']:
                project.hourlyrate = form.cleaned_data['hourlyrate']
            if form.cleaned_data['payment_type']:
                project.payment_type = form.cleaned_data['payment_type']
            project.save()
            return render(request,'project/updateproject.html')
        else :
            print form.errors
            response['form'] = form
            return render(request,'project/updateproject.html',response) 


# view to delete a project by manager 
class DeleteProjectPageView(View):

    def get(self, request, project_id, manager_id):
        project_id = request.GET.get('project_id')
        Project.objects.filter(id=project_id).delete()
        Task.objects.filter(project_id=project_id).delete()
        return redirect(reverse('project' ,kwargs ={'manager_id': manager_id}))


#view is used to update task progress 
class UpdateTaskPageView(View):

    def get(self, request, task_id):
        response = {'task_id':task_id}
        data = Task.objects.get(id=task_id)
        response['form'] = UpdateTaskForm(instance=data)
        response['data']= data
        return render(request,'project/updatetask.html' , response)

    def post(self, request, task_id):
        task=Task.objects.get(id=task_id)
        task.status=request.POST.get('status')
        estimatetime =request.POST.get('estimatetime')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        if estimatetime:
            task.estimatetime = estimatetime
        if startdate :
            task.startdate = startdate
        if enddate :
            task.enddate = enddate
        task.save()
        return render(request,'project/updatetask.html')


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
        return redirect(reverse('clientprojects'))


# task view for manager
class TaskPageView(View):
    
    def get(self, request, project_id, manager_id):
        response = {'project_id': project_id, 'manager_id': manager_id }
        response['employees']=User.objects.filter(role="employee", createdby=manager_id)
        response['form'] = TaskForm()
        response['form'].fields['project'].widget = forms.HiddenInput()
        response['tasks'] = Task.objects.filter(project_id = project_id)
        return render(request,'project/task.html', response)

class DeleteTaskPageView(View):

    def get(self, request, project_id, manager_id,task_id):
        task_id = request.GET.get('task_id')
        Task.objects.filter(id=task_id).delete()
        return redirect(reverse('task' ,kwargs ={'manager_id': manager_id,'project_id':project_id}))

# create project view for manager
class CreateProjectPageView(View):
   
    def post(self, request, manager_id):
        response = {'manager_id': manager_id }
        response['clients']=User.objects.filter(role="client", createdby=manager_id)
        form = ProjectForm(request.POST)
        print form.errors
        if form.is_valid():
            f=form.save(commit=False)
            f.createdby=manager_id 
            f.client_id= request.POST.get('client_id')
            f.save()
            return render(request,'project/createproject.html')
        else:
            response['form'] = form
            return render(request,'project/createproject.html', response)

#create task view for manager
class CreateTaskPageView(View):
  
    def post(self, request, project_id, manager_id):

        response = {'project_id': project_id, 'manager_id': manager_id}
        form = TaskForm(request.POST)
        if form.is_valid():
            task=form.save(commit=False)
            task.project_id=project_id
            task.employee_id = request.POST.get('employee_id')
            task.save()
            return render(request,'project/createtask.html')
        else:
            response['form'] = form
            return render(request,'project/createtask.html', response)