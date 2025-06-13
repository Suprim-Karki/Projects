from django.db import models
from datetime import datetime

# Create your models here.
class Room(models.Model):
    name=models.CharField(max_length=100)

class Message(models.Model):
    value=models.CharField(max_length=1000000)
    date=models.CharField(default=datetime.now,blank=True)
    user=models.CharField(max_length=1000000)
    name=models.CharField(max_length=1000000)