from django.core.mail import send_mail
import random
from django.conf import settings
from .models import AppUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from  restaurant_api.models import Booking





def send_otp_via_email(email):
    subject="Dine Eazy- Account verification email"
    otp=random.randint(1000,9999)
    message=f'Dear Customer Your OTP is {otp} '
    email_from=settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    user_obj=AppUser.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()
    
 
 