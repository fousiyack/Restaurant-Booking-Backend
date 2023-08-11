from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Restaurant
from .serializers import *
from rest_framework import status
from user_api.models import *
from user_api.serializers import UserLoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import  login, logout
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView
from django.views.decorators.http import require_http_methods

from django.core.mail import send_mail
from django.conf import settings
from  restaurant_api.models import Booking,Complaint
from rest_framework.parsers import MultiPartParser


from rest_framework import generics



from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.decorators import login_required
import stripe






class AddRestaurantView(APIView):
    def post(self, request):
        
        data = request.data
        
        print("dataaaaaaaaaa",data)
        
        serializer = RestaurantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)       
           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class restaurant_login(APIView):
    def post(self, request):
     data = request.data
     serializer = UserLoginSerializer(data=data)
     serializer.is_valid(raise_exception=True)
    # Authenticate the restaurant
     user = authenticate(request, email=serializer.validated_data['email'],
            password=serializer.validated_data['password'])
     if user is not None:
        # Generate JWT token
        login(request, user)
        access_token = AccessToken.for_user(user)
        access_token['email'] = user.email
        access_token['is_active'] = user.is_active
        access_token['is_superuser'] = user.is_superuser
        access_token['is_res_admin'] = user.is_res_admin
        access_token['id'] = user.is_res_admin
     else:
        return Response({'message': 'Invalid email or password'}, status=401)
   
class RestaurantListView(APIView):
    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.filter(is_approved=True)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
    
class RestaurantListViewall(APIView):
    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.filter().select_related('user')
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)    
    
class RestaurantListCity(APIView):
    def get(self, request, city):
        restaurants = Restaurant.objects.filter(city=city)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)    

class RestaurantListCuisine(APIView):
    def get(self, request, cuisine_type):
        restaurants = Restaurant.objects.filter(cuisine_type=cuisine_type)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)   
    
class RestaurantListOwner(APIView):
    def get(self, request, userId):
        restaurants = Restaurant.objects.filter(user=userId)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)            
    


class RestaurantDetail(APIView):
    def get(self, request, pk):
        try:
         
            restaurant = Restaurant.objects.get(pk=pk)
            serializer = RestaurantSerializer(restaurant)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response({'message': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        parser_classes=[MultiPartParser]
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            serializer = RestaurantSerializer(restaurant, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Restaurant.DoesNotExist:
            return Response({'message': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        
     
class ApproveRestaurant(APIView):
    def put(self, request, rest_id):
        resturant = Restaurant.objects.get(id=rest_id)
        print(resturant)
        resturant.is_approved = True
        resturant.save()
        return Response({'message': 'Restaurant approved successfully'}, status=status.HTTP_200_OK)


class NotApproveRestaurant(APIView):
    def put(self, request, rest_id):
        resturant =  Restaurant.objects.get(id=rest_id)
        resturant.is_approved = False
        resturant.save()
        return Response({'message': 'Restaurant not approved '}, status=status.HTTP_200_OK)     
    
class RestaurantDelete(APIView):
    def delete(self, request, pk):
        try:
            rest_obj = Restaurant.objects.get(id=pk)
            rest_obj.delete()
            return Response({'status': 200, 'message': 'deleted'})
        except Restaurant.DoesNotExist:
            return Response({'status': 404, 'message': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 500, 'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       
    
    
# def add_or_edit_restaurant(request):
#     # Get the logged-in user
#     user = request.user
    
#     try:
#         # Try to retrieve the restaurant entry for the logged-in user
#         restaurant = Restaurant.objects.get(user=user)
        
#         # If a restaurant entry exists, redirect to the edit page
#         return redirect('edit_restaurant', restaurant_id=restaurant.id)
#     except Restaurant.DoesNotExist:
#         # If a restaurant entry doesn't exist, proceed to add the restaurant details
#         return redirect('add_restaurant')   
    
def check_restaurant_entry(request, user_id):
    try:
        user_restaurant =Restaurant.objects.get(user=user_id)
        has_entry = True
        restaurant_id = user_restaurant.id
        restaurant_name = user_restaurant.restaurant_name
    except Restaurant.DoesNotExist:
        has_entry = False
        restaurant_id = None

    response_data = {
        'hasEntry': has_entry,
        'restaurantId': restaurant_id
        # 'restaurantName': restaurant_name,
        
    }

    return JsonResponse(response_data)    


# @authentication_classes([])
# @permission_classes([])
@api_view(['POST'])
# @login_required(login_url='user/login')  
def create_booking(request):
    print("...............inside view",request.data)
    serializer = BookingSerializer(data=request.data)
    print("serializer.......",serializer)
    
    if serializer.is_valid():
        
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @login_required(login_url='user/login') 
@api_view(['POST']) 
def create_complaint(request):
    
    serializer = ComplaintSerializer(data=request.data)
    print("complaintssssssssssssssss",serializer)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def Complaints(request):
    if request.method == 'GET':
        complaints = Complaint.objects.all()
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# class updateCompltStatus(APIView):
#     def put(self, request, complaint_id):
#         print(request.data,"dataaaaaaaaaaaaaaaaaaaaaaaaaa")
#         complaint =  Complaint.objects.get(id=complaint_id)
#         # complaint.status = False
#         # complaint.save()
#         return Response({'message': 'Restaurant not approved '}, status=status.HTTP_200_OK)    
@api_view(['PUT'])
def updateCompltStatus(request, complaintId):
    try:
        complaint = Complaint.objects.get(id=complaintId)
    except Complaint.DoesNotExist:
        return JsonResponse({"error": "Complaint not found"}, status=404)

    if request.method == 'PUT':
        new_status = request.data.get('status')

        if new_status not in ['Pending', 'In Progress', 'Resolved']:
            return JsonResponse({"error": "Invalid status"}, status=400)

        complaint.status = new_status
        complaint.save()

        return JsonResponse({"message": "Status updated successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)    
      


def check_table_availability(request):
    if request.method == 'GET':
        restaurantId = request.GET.get('restaurantId')
        tableId = request.GET.get('tableId')
        date = request.GET.get('date')
        timeId = request.GET.get('timeId')
      
        try:
    # Check if any booking already exists for the given table, date, and time
            booking = Booking.objects.filter(restaurantId=restaurantId, tableId=tableId, date=date, timeId=timeId)
            if booking.exists():
              return JsonResponse({'available': False})  # Table is not available
            else:
              return JsonResponse({'available': True})  # Table is available
        except Booking.DoesNotExist:
            return JsonResponse({'available': True})  # Table is available

    return JsonResponse({'error': 'Invalid request'}, status=400)


class BookingHistory(APIView):
    def get(self, request):
        bookings = Booking.objects.select_related('restaurantId', 'tableId', 'timeId', 'user').order_by('-created_at')
        serializer = BookingHistorySerializer(bookings, many=True)
        print(serializer.data)
        return Response(serializer.data)
@api_view(['GET']) 
def UserComplaints(request,userEmail):
        print(userEmail,'user_id..complaintssssssssssss........................')
        complaints = Complaint.objects.filter(email=userEmail)
        print(complaints,"complaints.................................")
        serializer = ComplaintSerializer(complaints, many=True)
        print(serializer.data)
        return Response(serializer.data)    


@api_view(['GET']) 
def UserBookingHistory(request,userId):
        print(userId,'user_id..........................')
        bookings = Booking.objects.filter(user=userId).select_related('restaurantId', 'tableId', 'timeId', 'user').order_by('-created_at')
        serializer = BookingHistorySerializer(bookings, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
def send_booking_canceled_email(email,instance):
    if instance.status == 'canceled':
        subject = 'Dine Eazy-Booking Canceled'
        message = f'Your booking for {instance.date} at {instance.restaurantId.restaurant_name} has been canceled.'
        email_from=settings.EMAIL_HOST
        recipient_list = [instance.user.email]
        send_mail(subject,message,email_from,recipient_list)   
        
       
    
@api_view(['PUT']) 
def cancel_booking(request, bookingId):
    try:
        booking = Booking.objects.get(pk=bookingId)
       
        booking.status = 'canceled'
        booking.save()
        
        #DO REFUND....................................
     
        send_booking_canceled_email(booking.user.email,booking)
        
        return JsonResponse({'message': 'Booking canceled successfully.'}, status=200)
        # else:
        #     return JsonResponse({'message': 'Booking cannot be canceled.'}, status=400)

    except Booking.DoesNotExist:
        return JsonResponse({'message': 'Booking not found.'}, status=404)   
    
class TotalBookingsCount(APIView):
    def get(self, request, format=None):
        total_bookings_count = Booking.objects.count()
        return Response({"total_bookings": total_bookings_count})    
    
@api_view(['GET'])  
def RestBookingHistory(request,restaurantId):
        bookings = Booking.objects.filter(restaurantId=restaurantId).select_related( 'tableId', 'timeId', 'user').order_by('-created_at')
       
        print(bookings)
        print('-----------------------------------------')
        serializer = RestBookingHistorySerializer(bookings, many=True)
        print(serializer.data)
        print('-------------------------------------')
        return Response(serializer.data)    

    
    
    # employee = Employee.objects.select_related('department').get(email=email)
    #         department_name = employee.department.name 


# class BookingHistory(generics.ListAPIView):
#     queryset = Booking.objects.select_related('restaurantId', 'tableId', 'timeId', 'user')
#     serializer_class = BookingSerializer

stripe.api_key = 'sk_test_tR3PYbcVNZZ796tH88S4VQ2u'

YOUR_DOMAIN = 'http://localhost:8000'  

def create_checkout_session(request):
    if request.method == 'POST':
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': 1000,  # Replace with your actual Price ID
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/payment/?success=true',
                cancel_url=YOUR_DOMAIN + '/payment/?canceled=true',
            )
            return redirect(session.url, code=303)
        except Exception as e:
            # Handle the error
            pass

    return render(request, 'payment.html')







