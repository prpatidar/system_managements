from django.shortcuts import render , redirect
from django.views.generic import View
from django.conf import settings
from django.template import loader
from django.contrib.auth import get_user_model
from .forms import EmployeeForm



class HomePageView(View) :
   def get(self, request):
       return render(request,'system/home.html',{})

class EmployeePageView(View) :
   def get(self, request):
       User = get_user_model()
       users = User.objects.all()
       return render(request,'system/employee.html',{"users":users})

class CreateEmployeePageView(View):
   def get(self, request):
       form = EmployeeForm()
       return render(request,'system/createemployee.html',{'form':form})
   def post(self,request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
          form.save()
          return redirect('/system/employee')
        else :
          return render(request,'system/createemployee.html',{'form':form})
        

