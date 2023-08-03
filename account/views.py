from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter

#from .serializers import UserSerializer, UserProfileSerializer
from account.models import User, UserProfile


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .serializers import *




@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/token',
        '/token/refresh'
    ]
    return Response(routes)
class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Update the is_user field to True
        user.is_user = True
        user.save()

        # Send OTP via email
        serializer.send_otp(user.email)

        return Response({
            'status': 200,
            'message': 'Registration successful, please check your email',
            'data': serializer.data,
        })


    
    
class VerifyOTP(APIView):
    def post(self, request):
        try:
            serializer = VerifyAccountSerializer(data=request.data)
            print('otp serilalizer', serializer)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            user = AppUser.objects.get(email=email)
            
            if user.otp != otp:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Something went wrong',
                    'data': 'Invalid OTP',
                })
            
            user.is_verified = True
            user.save()
            
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Account verified',
                'data': {},
            })
        
        except AppUser.DoesNotExist:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Something went wrong',
                'data': 'Invalid email',
            })
            
        except (KeyError, ValueError, ValidationError) as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Something went wrong',
                'data': str(e),
            })    
            
class ForgotPassword(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')

        if AppUser.objects.filter(email=email).exists:
            user = AppUser.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'msg':'Please Reset Password In The Link', 'user_id':user.id})
        
        return Response({'msg': 'No Account Registered With This Email'})
    
@api_view(['GET'])    
def reset_validate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid

        sessionid = request.session.get('uid')
        print(sessionid)

        return HttpResponseRedirect('http://localhost:3000/reset-password/')
    
    return Response({'msg': 'Link Expired or Invalid Token'})

       
class ResetPassword(APIView):
    def post(self, request, format=None):
        # print(request.data)
        str_user_id = request.data.get('user_id')
        user_id = int(str_user_id)
        password = request.data.get('password')
        
        print(user_id)
        if user_id :
            # print(type(user_id))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            print('saved')

            return Response({'msg': 'Password Updated Successfully'})
    
        return HttpResponseRedirect('http://localhost:3000/reset-password')          
