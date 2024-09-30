from django.test import TestCase
from django.db import connection

from data_auth.models import User
from data_tweets.models import Like
from data_tweets.models.tweet import Tweet


class TweetTest(TestCase):
    def setUp(self):
        connection.force_debug_cursor = True

    def test_create_and_read_tweet(self):
        # given
        user = User.objects.create(
            username='testuser',
            email='test@test.com',
            password='password',
        )
        Tweet.objects.create(payload='test_tweet', user=user)
        Tweet.objects.create(payload='test_tweet2', user=user)

        # when
        results = Tweet.objects.filter(user=user)
        print(results)

        # then
        self.assertEqual(len(results), 2)

    def test_likes_count(self):
        # given
        user1 = User.objects.create(
            username='testuser',
            email='test@test.com',
            password='password',
        )
        user2 = User.objects.create(
            username='testuser2',
            email='test2@test.com',
            password='password',
        )
        tweet = Tweet.objects.create(payload='test_tweet', user=user1)
        Like.objects.create(user=user1, tweet=tweet)
        Like.objects.create(user=user2, tweet=tweet)

        # when
        count = tweet.likes_count()

        # then
        self.assertEqual(count, 2)
