from __future__ import unicode_literals

from django.db import models


class TimeSheet(models.Model):
    project_id = models.IntegerField()
    taskname = models.CharField(max_length=30)
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    employee_id= models.IntegerField()
    spendtime = models.CharField(max_length=10,null=True,blank=True)
    status = models.CharField(max_length=10, default="pending")
    reject_comment = models.TextField(max_length=150,blank=True,null=True)