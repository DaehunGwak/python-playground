from django.test import TestCase
from django.db import connection

from data_auth.models import User
from data_tweets.models.tweet import Tweet


class TweetTest(TestCase):
    def setUp(self):
        connection.force_debug_cursor = True
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
            password='password',
        )

    def test_create_and_read_tweet(self):
        Tweet.objects.create(
            payload='test_tweet',
            user=self.user,
        )
        Tweet.objects.create(
            payload='test_tweet2',
            user=self.user,
        )

        results = Tweet.objects.filter(user=self.user)
        print(results)
        self.assertEqual(len(results), 2)
