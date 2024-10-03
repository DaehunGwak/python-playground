import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view

from api_main.response.tweet import to_tweet_response, TweetResponse
from data_auth.models import User
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


@api_view(['GET'])
def tweets_v1_view(request):
    tweets = (Tweet.objects
              .order_by('-created_at')
              .select_related('user')
              .all())
    responses = list(
        map(lambda t: TweetResponse(t).data, tweets)
    )
    return JsonResponse({
        'results': responses
    })


@api_view(['GET'])
def user_tweets_v1_view(requests, user_id):
    user = get_object_or_404(User, username=user_id)
    tweets = (Tweet.objects
              .filter(user=user)
              .order_by('-created_at')
              .select_related('user')
              .all())
    responses = list(
        map(lambda t: TweetResponse(t).data, tweets)
    )
    return JsonResponse({
        'results': responses
    })
