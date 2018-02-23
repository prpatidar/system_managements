from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser

from users.models import User
        

class Project(models.Model):
    title = models.CharField(max_length=30)
    discription = models.TextField(max_length=100)
    status = models.CharField(max_length=30, default="Pending", blank=True)
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True) #auto_now_add=False,
    createdby = models.CharField(blank=True, max_length=2) #Need To Do

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