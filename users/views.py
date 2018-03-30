import stripe
import calendar,datetime
from collections import OrderedDict

from django import forms
from django.conf import settings
from django.template import loader
from django.http import JsonResponse
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import render , redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from users.models import User
from users.forms import EmployeeForm
from timesheet.models import TimeSheet
from project.models import Project, Task 
from timesheet.forms import TimeSheetForm
from project.forms import ProjectForm ,TaskForm


# this class is used to render index page
class IndexPageView(View):

    def get(self, request):
        response = {}
        return render(request,'index1.html', response)
  

# this class is used to render on home page for all users
@login_required
def HomePageView(request) :
    response = {}
    return render(request,'users/home.html', response )


# this class is used to render on all employee list under a login manager
class EmployeePageView(View) :

    def get(self, request, manager_id):
        response = {'manager_id':manager_id}
        User = get_user_model()
        form = EmployeeForm()
        response['form'] = form
        response['users'] = User.objects.filter(role='employee',createdby=manager_id)
        return render(request,'users/employee.html', response )


# this class is used to render on all client list under a login manager
class ClientPageView(View) :

    def get(self, request, manager_id):
        response = {'manager_id':manager_id}
        response['users'] = User.objects.filter(role='client',createdby=manager_id)
        form = EmployeeForm()
        form.fields['role'].widget = forms.HiddenInput()
        response['form'] = form
        return render(request,'users/client.html', response )


# this class is used to delete users profile (non-client)
class DeleteProfilePageView(View):

    def get(self, request, employee_id, manager_id):
        employee_id = request.GET.get('employee_id')
        User.objects.filter(id=employee_id).delete()
        return redirect(reverse('employee' ,kwargs ={'manager_id': manager_id}))


# this class is used to delete a client profile as well as thier stripe profile 
class DeleteClientPageView(View):

    def get(self, request, employee_id, manager_id):
        employee_id = request.GET.get('employee_id')
        user = User.objects.get(id=employee_id)
        stripe.api_key = "sk_test_6NXzQP1ksrl4ApeJn5TdJ9SW"
        cu = stripe.Customer.retrieve(user.stripetoken)
        print user.stripetoken
        cu.delete()
        user.save()
        User.objects.filter(id=employee_id).delete()
        return redirect(reverse('client' ,kwargs ={'manager_id': manager_id}))


# this class is used to create a employee under login manager
class CreateEmployeePageView(View):

    def post(self, request, manager_id):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            print "hii"
            employee=form.save(commit=False)
            employee.role="employee"
            employee.createdby=manager_id
            employee.save()
            return render(request,'users/createemployee.html')
        else :
            response = {'form':form,'manager_id':manager_id}
            return render(request,'users/createemployee.html', response)


# this class is used to create client under a login manager
class CreateClientPageView(View):

    def post(self, request, manager_id):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee=form.save(commit=False)
            employee.role="client"
            employee.createdby=manager_id
            stripe.api_key = "sk_test_6NXzQP1ksrl4ApeJn5TdJ9SW"
            stripetoken = stripe.Customer.create(description=employee.email)
            employee.stripetoken=stripetoken['id']
            print employee.stripetoken
            employee.save()
            return render(request,'users/createclient.html')
        else :
            response = {'form':form,'manager_id':manager_id}
            return render(request,'users/createclient.html', response)



# this class is used to update user profile
class UpdateProfilePageView(View):

    def get(self, request, employee_id):
        data = User.objects.get(id=employee_id)
        form = EmployeeForm(instance=data)
        form.fields['role'].widget = forms.HiddenInput()
        response = {'form':form,'employee_id':employee_id}
        return render(request,'users/updateprofile.html' , response)

    def post(self, request, employee_id):
        data = User.objects.get(id=employee_id)
        form = EmployeeForm(instance=data)
        form.fields['role'].widget = forms.HiddenInput()
        response = {'form':form,'employee_id':employee_id}
        user=User.objects.get(id=employee_id)
        employee=EmployeeForm(request.POST)
        response['formerror']= employee
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
            return render(request,'users/updateprofile.html')
        else :
            return render(request,'users/updateprofile.html' , response)