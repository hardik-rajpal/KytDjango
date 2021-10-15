from django.db import models

class ChatSnippet(models.Model):
    snippet = models.TextField()
    published = models.BooleanField(default=True)
    def __str__(self):
        return self.snippet.split('H#')[1]