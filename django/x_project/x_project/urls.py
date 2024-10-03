from django.contrib import admin
from django.urls import path

from api_main.views import template_tweets_view, tweets_v1_view, user_tweets_v1_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', template_tweets_view, name='template-tweets'),
    path('api/v1/tweets', tweets_v1_view, name='api-v1-tweets'),
    path('api/v1/users/<str:user_id>/tweets', user_tweets_v1_view, name='api-v1-user-tweets'),
]
