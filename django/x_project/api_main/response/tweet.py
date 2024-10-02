from typing import Dict, Any

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
