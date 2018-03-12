from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# this is django's user model which is overrided to store more fileds for users
class User(AbstractBaseUser, PermissionsMixin):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    username =models.CharField(('username'),max_length=30)
    email = models.EmailField( ('email'), unique=True)
    first_name = models.CharField(('first_name'), max_length=30, blank=True)
    last_name = models.CharField(('last_name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(('date_joined'), auto_now_add=True)
    is_active = models.BooleanField(('is_active'), default=True)
    role= models.CharField( ('role'),max_length=30,default='manager')
    createdby = models.CharField(max_length=2,default=0)
    stripetoken = models.CharField(max_length=100, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    def is_staff(self):
         return False
 