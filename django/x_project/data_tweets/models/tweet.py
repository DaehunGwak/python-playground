from django.db import models

from data_auth.models import User


class Tweet(models.Model):
    payload = models.TextField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
