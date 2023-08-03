from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .validations import *
from django.contrib.auth.hashers import check_password
from .models import *

UserModel = get_user_model()

# class AdminLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()
#     print("password",password)

#     def check_admin(self, validated_data):
        
#         user = authenticate(email=validated_data['email'], password=validated_data['password'])
        
#         print("userrr..........",user)
#         if not user:
#             raise ValidationError('Invalid credentials')
#         if not check_password(validated_data['password'], user.password):
#             raise ValidationError('Invalid credentials')
#         if not user.is_active or not user.is_staff or not user.is_superuser:
#             raise ValidationError('Access denied')
#         return user
    
    
class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_admin(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise ValidationError('Invalid email or password.')
        return user

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email',)

        
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'    
        
class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model =CuisineType
        fields = '__all__'       

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Times
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'            
     

