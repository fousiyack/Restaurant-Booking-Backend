from rest_framework import serializers
from .models import Restaurant,Booking,Payment,Complaint

from admin_api.models import Table,Times
from user_api.models import AppUser
from user_api.serializers import UsersSerializer
from admin_api.serializers import TableSerializer,TimeSlotSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    user=UsersSerializer()
    class Meta:
        model = Restaurant
        fields = '__all__'

class BookingHistorySerializer(serializers.ModelSerializer):
    restaurantId=RestaurantSerializer()
    user=UsersSerializer()
    tableId=TableSerializer()
    timeId=TimeSlotSerializer()


    class Meta:
        model = Booking
        fields ='__all__'
        #  'time_start', 'time_end', 
class RestBookingHistorySerializer(serializers.ModelSerializer):
    
    user=UsersSerializer()
    tableId=TableSerializer()
    timeId=TimeSlotSerializer()


    class Meta:
        model = Booking
        fields ='__all__'
        #  'time_start', 'time_end',         




class BookingSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Booking
        fields = '__all__'
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'        
        
class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'           
        