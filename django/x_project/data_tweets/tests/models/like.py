from django.test import TestCase
from django.db import connection, IntegrityError

from data_auth.models import User
from data_tweets.models import Like
from data_tweets.models.tweet import Tweet


class LikeTestCase(TestCase):
    def setUp(self):
        connection.force_debug_cursor = True
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
            password='password',
        )
        self.tweet = Tweet.objects.create(
            payload='test_tweet',
            user=self.user,
        )

    def test_create_and_read_like(self):
        Like.objects.create(
            user=self.user,
            tweet=self.tweet,
        )

        results = Like.objects.filter(user=self.user, tweet=self.tweet)
        print(results)
        self.assertEqual(len(results), 1)

    def test_create_duplicated_exception(self):
        try:
            Like.objects.create(
                user=self.user,
                tweet=self.tweet,
            )
            Like.objects.create(
                user=self.user,
                tweet=self.tweet,
            )
        except Exception as e:
            print(e)
            self.assertIsInstance(e, IntegrityError)
