import calendar,datetime
from collections import OrderedDict

from django import forms
from django.conf import settings
from django.template import loader
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import render , redirect
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from users.forms import EmployeeForm
from timesheet.models import TimeSheet
from project.models import Project, Task 
from timesheet.forms import TimeSheetForm
from project.forms import ProjectForm ,TaskForm



class IndexPageView(View):

    def get(self, request):
        response = {}
        return render(request,'index1.html', response)
  
index_page_view = IndexPageView.as_view()


class HomePageView(View) :

    def get(self, request):
        response = {}
        return render(request,'users/home.html', response )
   

home_page_view = HomePageView.as_view()


class EmployeePageView(View) :

    def get(self, request, manager_id):
        response = {'manager_id':manager_id}
        User = get_user_model()
        response['users'] = User.objects.filter(role='employee',createdby=manager_id)
        return render(request,'users/employee.html', response )

employee_page_view = EmployeePageView.as_view()


class DeleteProfilePageView(View):

    def get(self, request, employee_id, manager_id):
        User.objects.filter(id=employee_id).delete()
        return redirect(reverse('employee' ,kwargs ={'manager_id': manager_id}))

delete_profile_page_view = DeleteProfilePageView.as_view()


class CreateEmployeePageView(View):

    def get(self, request, manager_id):
        form = EmployeeForm()
        form.fields['role'].widget = forms.HiddenInput()
        response = {'form':form,'manager_id':manager_id}
        return render(request,'users/createemployee.html', response)

    def post(self, request, manager_id):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee=form.save(commit=False)
            employee.role="employee"
            employee.createdby=manager_id
            employee.save()
            return redirect(reverse('employee' ,kwargs ={'manager_id': manager_id}))
        else :
            response = {'form':form,'manager_id':manager_id}
            return render(request,'users/createemployee.html', response)

create_employee_page_view = CreateEmployeePageView.as_view()


class UpdateProfilePageView(View):

    def get(self, request, employee_id):
        form = EmployeeForm()
        form.fields['role'].widget = forms.HiddenInput()
        response = {'form':form,'employee_id':employee_id}
        return render(request,'users/updateprofile.html' , response)

    def post(self, request, employee_id):
        user=User.objects.get(id=employee_id)
        employee=EmployeeForm(request.POST)
        if employee.is_valid():
            if employee.cleaned_data['first_name']:
                user.first_name=employee.cleaned_data['first_name']
            if employee.cleaned_data['last_name']:
                user.last_name=employee.cleaned_data['last_name']
            if employee.cleaned_data['email'] :
                user.email=employee.cleaned_data['email']
            if employee.cleaned_data['username']:
                user.username=employee.cleaned_data['username']
        user.save()
        return redirect(reverse('home'))

update_profile_page_view = UpdateProfilePageView.as_view()