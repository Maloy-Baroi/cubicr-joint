from datetime import datetime

from django.db import models


# Create your models here.
from App_auth.models import CustomUser


class Room(models.Model):
    name = models.CharField(max_length=100)


class MessageModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
