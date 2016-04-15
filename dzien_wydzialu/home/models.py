from django.db import models


class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    projector = models.BooleanField()
    board = models.BooleanField()
    computers = models.PositiveSmallIntegerField()
    info = models.TextField(max_length=3000)
    seats = models.PositiveSmallIntegerField()


class Lecturer(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    dergee = models.CharField(max_length=250)


class Activity(models.Model):
    title = models.CharField(max_length=250)
    is_lecture = models.BooleanField()
    lecturer = models.ManyToManyField(Lecturer) #to check
    room = models.ForeignKey(Room)
    description = models.TextField(max_length=3000)


class Group(models.Model):
    pass


class Event(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity = models.ForeignKey(Activity)
    group = models.ForeignKey(Group)
