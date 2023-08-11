from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .validations import *
from django.contrib.auth.hashers import make_password


from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response
from .models import AppUser
import random

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Password must be at least 5 characters long.')
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)
        return user

    def send_otp(self, email):
        subject = "Dine Eazy - Account verification email"
        otp=random.randint(1000,9999) # Retrieve the OTP from the session
        message = f'Dear Customer, your OTP is {otp}.'
        email_from = settings.EMAIL_HOST
        send_mail(subject, message, email_from, [email])

        # Save the OTP in the user object
        user = self.instance
        user.otp = otp
        user.save()

    class Meta:
        model = AppUser
        fields = ('id', 'email', 'password', 'name', 'mobile', 'is_active')

        
class VerifyAccountSerializer(serializers.Serializer):
    email=serializers.EmailField()
    print("email otpp..........",email)
    otp=serializers.CharField()
    
    
    
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id','email','name','mobile','is_user','is_active']    



class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email','name','mobile','password']

    def create(self, validated_data):
        user_obj = UserModel.objects.create_user(email=validated_data['email'],
                                               password=validated_data['password'])
        user_obj.name = validated_data['name']
        user_obj.mobile = validated_data['mobile']
        user_obj.save()
        return user_obj
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, validated_data):
        email = UserModel.objects.get('email')
        password = UserModel.objects.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise ValidationError('Invalid email or password.')
        return user


    






