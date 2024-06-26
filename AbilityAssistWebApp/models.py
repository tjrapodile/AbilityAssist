
from django.db import models
from django.contrib.auth.models import User



class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_point = models.ForeignKey('InitialGeolocation', on_delete=models.CASCADE)
    end_point = models.ForeignKey('FinalGeolocation', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)
    distance = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    completed = models.BooleanField(default=False)


    def __str__(self):
        return f'Mobile No/Username:{self.user.username} on a trip from {self.start_point} to {self.end_point}'

class LocationUpdate(models.Model):
    trip = models.ForeignKey('Trip', related_name='location_updates', on_delete=models.CASCADE)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Location update for {self.trip} at {self.timestamp}'

class InitialGeolocation(models.Model):
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.longitude + '' + self.latitude

class FinalGeolocation(models.Model):
    value = models.CharField(max_length=50)
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


class AboutImage(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url







