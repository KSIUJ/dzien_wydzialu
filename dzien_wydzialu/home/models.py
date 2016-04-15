from django.db import models


class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    projector = models.BooleanField()
    board = models.BooleanField()
    computers = models.PositiveSmallIntegerField()
    info = models.TextField(max_length=3000, blank=True)
    seats = models.PositiveSmallIntegerField()


class Lecturer(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    degree = models.CharField(max_length=250)


class Activity(models.Model):
    title = models.CharField(max_length=250)
    is_lecture = models.BooleanField()
    lecturer = models.ManyToManyField(Lecturer)
    room = models.ForeignKey(Room)
    description = models.TextField(max_length=3000)


class Group(models.Model):
    pass


class Event(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity = models.ForeignKey(Activity, null=True, blank=True)
    group = models.ForeignKey(Group)


class School(models.Model):
    name = models.CharField(max_length=250)
    postal_code=models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField()