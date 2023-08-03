from django.db import models

# Create your models here.



class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class CuisineType(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cuisine_images',blank=True)
    def __str__(self):
        return self.name
    
class Times(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    

    def __str__(self):
        return f'{self.start_time}- {self.end_time}'
    # 


class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'Table {self.table_number}'    
        
    
    




