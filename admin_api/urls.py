from django.urls import path
from . import views
from .views import *



urlpatterns = [
	
	path('login/', views.AdminLoginView.as_view(), name='login'),
    path('add_city/', views.CityAdd, name='add_city'),
    path('cities/', views.city.as_view(), name='cities'),
    path('update_city/<id>/', views.update_city, name='update_city'),
    path('get_city/<id>/', views.get_city, name='get_city'),
    path('delete_city/<id>/', views.delete_city, name='delete_city'),
    path('cuisines/', views.cuisines.as_view(), name='cuisines'),
    path('add_cuisine/', views.cuisineAdd, name='add_cuisine'),
    
    path('timeslots/', TimeSlotList.as_view(), name='timeslot-list'),
    # path('timeslots/<int:pk>/', TimeSlotEditDelete.as_view(), name='timeslot-retrieve-update-destroy'),
    path('tables/', TableListAdd.as_view(), name='table-list'),
    path('tables/<int:pk>/', TableEditDelete.as_view(), name='table-retrieve-update-destroy'),
    
]
