import uuid
from django.db import models
from django.contrib.auth.models import User
from kyt1.constants import common
# Create your models here.
#TODO: reading stats 
class WordBlock(models.Model):
    glossary = models.ForeignKey('coreader.Glossary',on_delete=models.CASCADE)
    word = models.CharField(max_length=50,null=False,blank=False)
    isKnown = models.BooleanField(default=False)
    comment = models.TextField()
class Book(models.Model):
    user = models.ForeignKey('coreader.UserProfile',on_delete=models.CASCADE)
    coverLink = models.CharField(max_length=2000,default=common['coverPlaceholder'])
    numPages = models.IntegerField()
    bookmark = models.IntegerField()
    color = models.CharField(max_length=10)
    archived = models.BooleanField(default=False)
class Note(models.Model):
    title = models.CharField(max_length=300,blank=False)
    book = models.ForeignKey('coreader.Book',on_delete=models.CASCADE)
class Glossary(models.Model):
    title = models.CharField(max_length=300,blank=False)
    book = models.ForeignKey('coreader.Book',on_delete=models.CASCADE)
class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = True)
    favouriteWords = models.OneToOneField(Glossary,on_delete=models.CASCADE)
