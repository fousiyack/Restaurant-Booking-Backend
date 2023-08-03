from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('An email field number is required.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('An email field  is required.')
        
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user
   


class AppUser(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    address = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_res_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False,null=True,blank=True)
    is_user= models.BooleanField(default=False)
    otp=models.CharField( max_length=6,null=True,blank=True)
    USERNAME_FIELD = 'email'


    objects = AppUserManager()

    def __str__(self):
        return self.email
