from django.db import models

class ChatSnippet(models.Model):
    snippet = models.TextField()
    published = models.BooleanField(default=True)
    def __str__(self):
        return self.snippet.split('H#')[1]
class Quote(models.Model):
    text = models.CharField(max_length=600)
    author = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    likedBy = models.TextField(blank=True,default='')
    def __str__(self):
        return (self.author + ': '+self.text)[:30]