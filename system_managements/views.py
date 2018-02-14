from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
from django.template import loader

class IndexPageView(View):
   def get(self, request):
       return render(request,'index.html',{})
  

