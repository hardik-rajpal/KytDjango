from .models import ChatSnippet, Quote, Tag, UserProfileToken
from django.contrib import admin

admin.site.register(ChatSnippet)
admin.site.register(Quote)
admin.site.register(Tag)
admin.site.register(UserProfileToken)