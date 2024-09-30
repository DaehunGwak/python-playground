from django.db import models

from data_auth.models import User


class Tweet(models.Model):
    payload = models.TextField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return (f"Tweet(payload={self.payload}, "
                f"user.id={self.user.id}, "  # TODO: N+1
                f"created_at={self.created_at}, "
                f"updated_at={self.updated_at})")

    class Meta:
        db_table = 'tweet'
