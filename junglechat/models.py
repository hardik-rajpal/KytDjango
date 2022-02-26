
from django.db import models
from django.utils import timezone
class UserToken(models.Model):
    dateMade=models.DateField(auto_created=True,default=timezone.now)
    def __str__(self):
        return str(self.dateMade)
class Tag(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return self.title
class ChatSnippet(models.Model):
    snippet = models.TextField()
    published = models.BooleanField(default=True)
    def __str__(self):
        return self.snippet.split('H#')[1]
class Quote(models.Model):
    text = models.CharField(max_length=600)
    author = models.CharField(max_length=100)
    date = models.DateField(auto_created=True)
    tags = models.ManyToManyField(Tag,related_name='tag+')
    likedBy = models.TextField(blank=True,default='')
    published = models.BooleanField(default=True)
    def __str__(self):
        return (self.author + ': '+self.text)[:30]