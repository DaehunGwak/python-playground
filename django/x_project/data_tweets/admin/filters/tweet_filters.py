from django.contrib import admin

_ELON_MUSK_STR = 'Elon Musk'


class TweetElonMuskFilter(admin.SimpleListFilter):
    title = "payload: Elon Musk"
    parameter_name = 'pyload-elon'  # URL query paramter

    def lookups(self, request, model_admin):
        return [
            ('contain', 'contain `Elon Musk`'),
            ('not_contain', 'not contain `Elon Musk`'),
        ]

    def queryset(self, request, tweets):
        if self.value() == 'contain':
            return tweets.filter(payload__contains=_ELON_MUSK_STR)
        elif self.value() == 'not_contain':
            return tweets.exclude(payload__contains=_ELON_MUSK_STR)
        return tweets
