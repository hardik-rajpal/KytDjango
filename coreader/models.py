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
    title = models.CharField(max_length=300,default='')
    coverLink = models.CharField(max_length=2000,default=common['coverPlaceholder'])
    numPages = models.IntegerField(default=1)
    bookmark = models.IntegerField(default=1)
    uiColor = models.IntegerField(default=4283215696)
    pdfPath = models.CharField(max_length=1000,default='')
    archived = models.BooleanField(default=False)
class Note(models.Model):
    title = models.CharField(max_length=300,blank=False)
    content = models.TextField(max_length=20000,default='')
    book = models.ForeignKey('coreader.Book',on_delete=models.CASCADE)
class Glossary(models.Model):
    title = models.CharField(max_length=300,blank=False)
    ownerType = models.CharField(max_length=20,choices=[('user','user')
    ,('book','book')
    ],
    default='book'
    )
    ownerID = models.IntegerField(default=0)
class UserProfile(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300,default='')
    accountType = models.CharField(max_length=20,default='google')
    profilePicLink = models.CharField(max_length=1000,default='https://i.imgur.com/vxP6SFl.png')
    identifier = models.CharField(max_length=300,default='')
    token = models.UUIDField(default = uuid.uuid4,editable = True)
    favouriteWords = models.OneToOneField(Glossary,on_delete=models.CASCADE)
