from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt import views as jwt_views




urlpatterns = [
	path('register/', views.UserRegister.as_view()),
    path('restaurantRegister/', views.RestaurantRegister.as_view()),
    path('verify/', views.VerifyOTP.as_view(), name='verify'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout/', views.UserLogout.as_view(), name='logout'),
    path('edit/<int:pk>/', UserDetails.as_view(), name='User-edit'),
    path('details/<int:pk>/', UserDetails.as_view(), name='details'),
    path('delete/<int:pk>/', UserDelete.as_view(), name='delete'),
    path('userList/', views.UserListView.as_view(), name='userList'),
    path('verify-mobile', views.UserListView.as_view(), name='verify-mobile'),
    path('block/<int:user_id>/', BlockUser.as_view(), name='block_user'),
    path('unblock/<int:user_id>/', UnblockUser.as_view(), name='unblock_user'),
    path('create-checkout-session/', StripeCheckoutView.as_view(), name='checkout'),
    path('webhook-test/' , WebHook,name="stripe_webhook"), 
    
    
      
]

