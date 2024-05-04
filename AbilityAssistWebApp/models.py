
from django.db import models
from django.contrib.auth.models import User



class Trip(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    start_point = models.ForeignKey('InitialGeolocation',on_delete = models.CASCADE)
    end_point = models.ForeignKey('FinalGeolocation',on_delete = models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'{self.start_point} to {self.end_point}'

class FinalGeolocation(models.Model):
    value = models.CharField(max_length=50)
    name = models.CharField(max_length = 100)

class InitialGeolocation(models.Model):
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)





