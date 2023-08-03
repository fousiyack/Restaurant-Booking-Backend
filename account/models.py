from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager

class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('An email field  is required.')
        
        user = self.create_user(email=self.normalize_email(email), password=password, **extra_fields)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user
class AppUser(AbstractBaseUser):
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
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
class UserProfile(models.Model):
    user = models.OneToOneField( AppUser , on_delete=models.CASCADE)
    address = models.CharField(blank=True, max_length=100)
    profile_img = models.ImageField(default='default.jpg', upload_to='userprofile')
    city = models.CharField(blank=True, max_length=50)
    state = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.user.first_name    