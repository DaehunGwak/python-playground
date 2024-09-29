from django.contrib import admin

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
                    "created_at",
                    "updated_at",
                ),
                "classes": ("wide",),
            },
        ),
    )

    list_display = ('id', 'user', 'created_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
