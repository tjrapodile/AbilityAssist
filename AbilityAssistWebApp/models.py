
from django.db import models
from django.contrib.auth.models import User



class Trip(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    start_point = models.CharField(max_length = 100)
    destination = models.ForeignKey('Geolocation',on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.start_point} to {self.destination}'

class Geolocation(models.Model):
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length = 50)
    destination_name = models.CharField(max_length = 100)





