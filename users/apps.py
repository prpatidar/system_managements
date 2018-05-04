# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

# class HijackAdminConfig(AppConfig):
#     name = 'hijack_admin'
#     verbose_name = 'Hijack-Admin'

#     def ready(self):
#         from hijack_admin.checks import register_checks
#         register_checks()