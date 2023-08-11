from django.contrib.auth import get_user_model, login, logout
import jwt
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from restaurant_api.models import Payment
from restaurant_api.serializers import PaymentSerializer
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .validations import custom_validation, validate_email, validate_password
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import AppUser
from restaurant_api.models import Booking
from .validations import *
from twilio.rest import Client
from django.conf import settings
import random
import re
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponse

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt






import stripe

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

class RestaurantRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Update the is_user field to True
        user.is_res_admin = True
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
            
            # return HttpResponseRedirect('https://dine-eazy.vercel.app/user/')  
            return HttpResponseRedirect('http://localhost:8000/user/')  
            
        
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
         
            
            
            
class UserLogin(APIView):
    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user is None or not user.is_verified or not user.is_active:
            raise AuthenticationFailed('Invalid credentials')

        # User authentication successful
        login(request, user)
        
        payload = {
            'name': user.name,
            'email':user.email,
            'user_id': user.id, 
            'mobile':user.mobile,
            'is_active': user.is_active,
            'is_verified': user.is_verified,
            'is_res_admin': user.is_res_admin,
            'is_superuser': user.is_superuser,
            'exp': datetime.utcnow() + timedelta(minutes=15),

                }  
        print(payload,"payload heree")
        
        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])

        
        return Response({
            "access_token": access_token,
            # "refresh_token": refresh_token,
            "email": user.email,
            "is_res_admin": user.is_res_admin,
            "id":user.id,
            "is_superuser":user.is_superuser,
            
            
        })            




class UserLogout(APIView):  
    def post(self,request):
        try:
            logout(request)
            return Response({'message': 'User logged out'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

import os

stripe.api_key = settings.STRIPE_SECRET_KEY


# YOUR_DOMAIN = 'http://localhost:3000'  

YOUR_DOMAIN = 'https://dine-eazy.vercel.app/' 



class StripeCheckoutView(APIView):
    def post(self, request, *args, **kwargs):
      
        try:
            booking_id = request.GET.get('booking_id')  # Retrieve booking_id from query parameters
            user_id = request.POST.get('userId')  # Retrieve userId from query parameters             email = request.POST.get('email') 
            product=stripe.Product.create(name='Restaurant Menu')
            booking=Booking.objects.get(pk=booking_id)
            user=AppUser.objects.get(pk=user_id)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data': {
                            'currency':'INR',
                             'unit_amount':int(request.POST.get('price')) * 100, 
                             'product_data':{
                                 'name':product.name,
                                

                             }
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "product_id":product.id
                },
                mode='payment',
                payment_method_types=['card'],
                 success_url=YOUR_DOMAIN + '/success',
                 cancel_url=YOUR_DOMAIN + '/?canceled=true',
            )
            payment = Payment.objects.create(
                 booking=booking,
                 amount=int(request.POST.get('price')),  # Store amount in cents
                 user=user,
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response({'msg':'something went wrong while creating stripe session','error':str(e)}, status=500)
        




        
        
@csrf_exempt
@api_view(["POST"])      
class WebHook(APIView):
    def post(self, request):
        
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = "whsec_5cc0040e9f1e0201b9d997be65fffc49f2066bddcd8b9bee1e6d496b51d300f1"  
          
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
          
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
           
            return JsonResponse({'error': 'Invalid signature'}, status=400)

        
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            print("--------payment_intent ---------->", payment_intent)
            

        elif event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            print("--------checkout_session ---------->", session)
            

        elif event['type'] == 'payment_method.attached':
            payment_method = event['data']['object']
            print("--------payment_method ---------->", payment_method)
            

        return JsonResponse({'success': True})
def send_booking_email(email,booking):
        subject = 'Dine Eazy-Booking'
        message = f'Your booking for {booking.date} at {booking.time} in {booking.restaurantId.restaurant_name} has been booked.'
        email_from=settings.EMAIL_HOST
        recipient_list = [email]
        send_mail(subject,message,email_from,recipient_list)    
        
class BlockUser(APIView):
    def put(self, request, user_id):
        user = AppUser.objects.get(id=user_id)

        user.is_active = False
        user.save()
        print(user)
        return Response({'message': 'User blocked successfully'}, status=status.HTTP_200_OK)


class UnblockUser(APIView):
    def put(self, request, user_id):
        user =  AppUser.objects.get(id=user_id)
      
        user.is_active = True
        user.save()
        return Response({'message': 'User unblocked successfully'}, status=status.HTTP_200_OK)

class UserView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (JWTAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class UserListView(APIView):
    def get(self, request, *args, **kwargs):
        users = AppUser.objects.filter(is_user=True)
  
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)
    

class HomeView(APIView):
    # permission_classes=(IsAuthenticated, )
    
    def get(self,request):
        content={'message' :'Welcome to JWT Authentication using React and Django'}
        return Response(content) 
    

                
class UserDetails(APIView):
    def get(self, request, pk):
        try:
            user = AppUser.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AppUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try:
            user = AppUser.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AppUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
class UserDelete(APIView):
    def delete(self, request, pk):
        try:
            user_obj = AppUser.objects.get(id=pk)
            user_obj.delete()
            return Response({'status': 200, 'message': 'User deleted'})
        except AppUser.DoesNotExist:
            return Response({'status': 404, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 500, 'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    