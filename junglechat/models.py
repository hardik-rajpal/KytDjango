from django.db import models

class ChatSnippet(models.Model):
    snippet = models.TextField()
    def __str__(self):
        self.snippet