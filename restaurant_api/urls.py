from django.urls import path

# from . import views
from .views import *

urlpatterns = [
    # path('',login.as_view(), name='login-restaurant'),
    path('addrest/',AddRestaurantView.as_view(), name='add-restaurant'),
    path('restList/',RestaurantListView.as_view(), name='restaurant-list'),
    path('restListall/',RestaurantListViewall.as_view(), name='restaurant-list'),
    path('edit/<int:pk>/', RestaurantDetail.as_view(), name='restaurant-detail'),
    path('details/<int:pk>/', RestaurantDetail.as_view(), name='details'),
    path('Approve/<int:rest_id>/', ApproveRestaurant.as_view(), name='Approve'),
    path('NotApprove/<int:rest_id>/', NotApproveRestaurant.as_view(), name='NotApprove'),
    path('delete/<int:pk>/', RestaurantDelete.as_view(), name='delete'),
    path('RestListCity/<int:city>/', RestaurantListCity.as_view(), name='RestListCity'),
    path('RestListCuisine/<int:cuisine_type>/', RestaurantListCuisine.as_view(), name='RestListCuisine'),
    path('has-entry/<int:user_id>/', check_restaurant_entry, name='check_restaurant_entry'),
    path('booking/', create_booking, name='table-booking'),
    path('check-table-availability/', check_table_availability, name='check_table_availability'),
    path('complaint/', create_complaint, name='create-complaint'),
    path('complaints/', Complaints, name='complaints'),
    path('updateCompltStatus/<int:complaintId>/', updateCompltStatus, name='updateCompltStatus'),
    path('UserComplaints/<str:userEmail>/', UserComplaints, name='UserComplaints'),

    path('payment/', create_checkout_session,name='payment'),   
    
    path('RestListOwner/<int:userId>/', RestaurantListOwner.as_view(), name='RestListOwner'),
    
    path('booking-history/', BookingHistory.as_view(), name='booking_history'), 
    path('restBooking-history/<int:restaurantId>/', RestBookingHistory, name='booking_history'), 
    path('UserBooking/<int:userId>/', UserBookingHistory, name='UserBooking'),
    path('bookingCancel/<int:bookingId>/', cancel_booking, name='cancel_booking'),
    path('total-bookings/', TotalBookingsCount.as_view(), name='total-bookings'),
    
]