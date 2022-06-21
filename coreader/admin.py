from django.contrib import admin

from coreader.models import Book, Glossary, Note, UserProfile, WordBlock

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(WordBlock)
admin.site.register(Glossary)
admin.site.register(Note)