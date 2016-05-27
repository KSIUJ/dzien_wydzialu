from django.db import models
from registration.signals import user_registered
from django.contrib.auth.models import User


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

    class Meta:
        verbose_name_plural = "Activities"


class Group(models.Model):

    def __str__(self):
        return str(self.id)


class Event(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity = models.ForeignKey(Activity, null=True, blank=True)
    group = models.ForeignKey(Group)


class School(models.Model):
    name = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    Teacher = 'T'
    Coordinator = 'C'
    Roles = ((Teacher, 'Nauczyciel'),
             (Coordinator, 'Koordynator'))
    user = models.ForeignKey(User)
    school = models.ForeignKey(School)
    role = models.CharField(max_length=50, choices=Roles, default=Teacher)


class Image(models.Model):
    image_file=models.ImageField(upload_to='dzien_wydzialu/home/static/images')


def user_registered_callback(sender, user, request, **kwargs):
    profile = Profile(user=user)
    school_id = request.POST.get('school')
    profile.school = School.objects.get(pk=school_id)
    profile.save()

user_registered.connect(user_registered_callback)



