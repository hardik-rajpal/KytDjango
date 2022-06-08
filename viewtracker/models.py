from django.db import models
from django.db.models.fields import CharField, DateField, GenericIPAddressField, IntegerField

# Create your models here.
class KYTVisitor(models.Model):
    freq = IntegerField(default=0)
    loc = CharField(max_length = 300)
    dates = CharField(max_length=1000, default="")
    def __str__(self):
        return self.loc
class JCVisitor(models.Model):
    freq = IntegerField(default=0)
    loc = CharField(max_length = 300)
    dates = CharField(max_length=1000, default="")
    def __str__(self):
        return self.loc