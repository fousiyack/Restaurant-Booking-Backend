from django.db import models

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='Banner_images')
    
    def __str__(self):
        return self.title    