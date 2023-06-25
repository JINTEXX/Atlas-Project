from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.IntegerField(default=1)
    tokens_balance = models.IntegerField(default=0)
    subscription_expiry = models.DateTimeField(null=True, blank=True)
