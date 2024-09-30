from django.db import models

from data_auth.models import User
from data_tweets.models import Tweet


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    tweet = models.ForeignKey(Tweet, on_delete=models.DO_NOTHING, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"Like(user.id={self.user.id}, "  # TODO: N+1
                f"tweet.id={self.tweet.id}, "  # TODO: N+1
                f"created_at={self.created_at}, "
                f"updated_at={self.updated_at})")

    class Meta:
        db_table = 'tweet_like'
        unique_together = ('user', 'tweet')
