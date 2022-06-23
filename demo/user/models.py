from django.db import models
from django.contrib.auth.models import User
# Create your models here.
GENDER_CHOICE = (
    (1, 'male'),
    (2, 'female'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    country = models.CharField(null=True, max_length=50)
    town = models.CharField(null=True, max_length=20)
    mobile_phone = models.CharField(null=True,max_length=20)
    address = models.CharField(null=True,max_length=100)
    created_datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_datetime = models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'user'

    def __str__(self):
        return str(self.user)