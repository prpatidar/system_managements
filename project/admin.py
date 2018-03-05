# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from users.models import User
from timesheet.models import TimeSheet
from creditcard.models import Card

admin.site.register(User)
admin.site.register(TimeSheet)
admin.site.register(Card)
