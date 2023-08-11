from django.conf import settings
from django.db import models
from admin_api.models import *
from user_api . models import *
from .models import *



# Create your models here.
from django.db import models

class Restaurant(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)
    executive_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_images',blank=True)
    restaurant_address = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
  
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    image1 = models.ImageField(upload_to='restaurant_images', blank=True, null=True)
    image2 = models.ImageField(upload_to='restaurant_images', blank=True, null=True)
    image3 = models.ImageField(upload_to='restaurant_images', blank=True, null=True)
    image4 = models.ImageField(upload_to='restaurant_images', blank=True, null=True)
    cuisine_type = models.CharField(max_length=255, null=True, blank=True)
    
    

    def __str__(self):
        return self.restaurant_name
    

class Booking(models.Model):
    restaurantId = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user=models.ForeignKey(AppUser, on_delete=models.CASCADE)
    tableId= models.ForeignKey(Table, on_delete=models.CASCADE)
    guestCount = models.PositiveIntegerField()
    date = models.DateField()
    timeId = models.ForeignKey(Times, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # payment = models.OneToOneField(Payment, null=True, blank=True, on_delete=models.SET_NULL)
  
   
    created_at = models.DateTimeField(auto_now_add=True)
    
    class meta:
        ordering=['-created_at']

    def __str__(self):
        return f'{self.restaurantId} - Table {self.tableId} - {self.date} {self.timeId}'
    
class Payment(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Payment for {self.booking}'
    
class Complaint(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    restaurantId =  models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    complaint = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Resolved', 'Resolved'),
        ],
        default='Pending', 
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class meta:
        ordering=['-created_at']
    
    def __str__(self):
        return f"Complaint from {self.name} at {self.restaurantId} - Status: {self.status}"
    

    
    
















