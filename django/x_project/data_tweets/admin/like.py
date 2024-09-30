from django.contrib import admin

from data_tweets.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Data",
            {
                "fields": (
                    "id",
                    "user",
                    "tweet",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("wide",),
            },
        ),
    )

    list_display = ("id", "user", "tweet", "created_at")
    readonly_fields = ("id", "created_at", "updated_at")
