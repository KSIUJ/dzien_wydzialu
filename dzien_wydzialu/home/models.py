from django.db import models

# Create your models here.
class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    projector = models.BooleanField()
    board = models.BooleanField()
    computers = models.PositiveSmallIntegerField()
    info = models.TextField(max_length=3000)
    seats = models.PositiveSmallIntegerField()

