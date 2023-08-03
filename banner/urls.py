from django.urls import path
from . import views
from .views import *



urlpatterns = [
	
	path('', views.bannerView, name= 'banner'),
    path('add/', views.bannerAdd, name= 'bannerAdd'),
]