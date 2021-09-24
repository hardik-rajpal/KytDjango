from django.db import models

# Create your models here.
class MainRow(models.Model):
    dayIndex = models.FloatField()
    monthIndex = models.FloatField()
    title = models.CharField(max_length=300)
    channel = models.CharField(max_length=100)
    titleLink = models.URLField(max_length=1000)
    channelLink = models.URLField(max_length=1000)
    moment = models.CharField(max_length=100)
    def __str__(self):
        return self.moment    