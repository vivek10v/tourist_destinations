from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)    
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
class Destination(models.Model):
    place_name = models.CharField(max_length=100)
    weather = models.CharField(max_length=100)
    location_state = models.CharField(max_length=100)
    location_district = models.CharField(max_length=100)
    google_map_link = models.URLField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.place_name
