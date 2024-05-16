
from django.db import models
from django.contrib.auth.models import User



class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_point = models.ForeignKey('InitialGeolocation', on_delete=models.CASCADE)
    end_point = models.ForeignKey('FinalGeolocation', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    cancelled = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f'{self.start_point} to {self.end_point}'

class FinalGeolocation(models.Model):
    value = models.CharField(max_length=50)
    name = models.CharField(max_length = 100)

class InitialGeolocation(models.Model):
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)


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





