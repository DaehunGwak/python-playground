from django.contrib import admin

from data_tweets.admin.filters.tweet_filters import TweetElonMuskFilter
from data_tweets.models import Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Data",
            {
                "fields": (
                    "id",
                    "payload",
                    "user",
                    "likes_count",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("wide",),
            },
        ),
    )

    list_filter = (
        "created_at",
        TweetElonMuskFilter,
    )

    search_fields = (
        "user__username",
    )

    list_display = ('id', 'user', 'payload', 'likes_count', 'created_at')
    readonly_fields = ('id', 'created_at', 'likes_count', 'updated_at')
