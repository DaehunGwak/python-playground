from typing import Dict, Any

from rest_framework import serializers

from data_tweets.models import Tweet


def to_tweet_response(tweet: Tweet) -> Dict[str, Any]:
    return {
        'user': {
            'username': tweet.user.username,
        },
        'payload': tweet.payload,
        'created_at': str(tweet.created_at),
        'updated_at': str(tweet.updated_at),
    }


class TweetUserResponse(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)


class TweetResponse(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = TweetUserResponse(read_only=True, many=False)
    payload = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

