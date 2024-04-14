
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class TravelHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    location = models.CharField(max_length=100)
    # Add additional fields for travel history (if needed)

    def __str__(self):
        return f"{self.user.username} - {self.location}"
