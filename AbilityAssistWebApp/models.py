
from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Volunteers(models.Model):
    phone = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)

    def __str__(self):
        return self.email

class TravelHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    location = models.CharField(max_length=100)
    # Add additional fields for travel history (if needed)

    def __str__(self):
        return f"{self.user.username} - {self.location}"
