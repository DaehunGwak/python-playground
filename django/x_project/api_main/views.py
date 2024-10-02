import json

from django.shortcuts import render

from api_main.response.tweet import to_tweet_response
from data_tweets.models import Tweet


def template_tweets_view(request):
    tweets = Tweet.objects.order_by('-created_at').all()
    tweet_responses = list(
        map(lambda tweet: to_tweet_response(tweet), tweets)
    )
    return render(
        request,
        template_name='tweets.html',
        context={
            'tweets': json.dumps(tweet_responses, indent=4, ensure_ascii=False),
        },
    )
