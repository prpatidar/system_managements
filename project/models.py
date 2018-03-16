from __future__ import unicode_literals

from django.db import models

from users.models import User
        

# this model is used to deal with project related operations
class Project(models.Model):
    title = models.CharField(max_length=30)
    discription = models.TextField(max_length=100)
    status = models.CharField(max_length=30, default="Pending", blank=True)
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True) #auto_now_add=False,
    createdby = models.CharField(blank=True,max_length=100) #Need To Do
    client = models.ForeignKey(User, blank=True ) 
    hourlyrate = models.IntegerField(blank=True,null=True)
    payment_type = models.CharField(max_length=10, blank=True,null=True) 

# this model is used to deal with task for a project 
class Task(models.Model):
    project= models.ForeignKey(Project, blank=True)
    title = models.CharField(max_length=30)
    discription = models.TextField(max_length=100)
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    employee = models.ForeignKey(User, blank=True)
    status = models.CharField(max_length=30, default="Pending")
    estimatetime =models.CharField(max_length=10, null=True, blank=True)
    spendtime = models.CharField(max_length=10, null=True, blank=True)
