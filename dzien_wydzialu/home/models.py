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

    def __str__(self):
        return str(self.number)


class Lecturer(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    degree = models.CharField(max_length=250)

    def __str__(self):
        return self.name + ' ' + self.surname


class Activity(models.Model):
    title = models.CharField(max_length=250)
    is_lecture = models.BooleanField()
    lecturer = models.ManyToManyField(Lecturer)
    room = models.ForeignKey(Room)
    description = models.TextField(max_length=3000)

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School)
    role = models.CharField(max_length=50, choices=Roles, default=Teacher)
    phone_number = models.CharField(max_length=15)


class Image(models.Model):
    name = models.CharField(max_length=25, blank=True)
    image_file = models.ImageField(upload_to='images')


def user_registered_callback(sender, user, request, **kwargs):
    profile = Profile(user=user)
    school_id = request.POST.get('school')
    profile.school = School.objects.get(pk=school_id)
    phone_number = request.POST.get('phone_number')
    profile.phone_number = phone_number
    profile.save()
    first_name = request.POST.get('first_name')
    user.first_name = first_name
    last_name = request.POST.get('last_name')
    user.last_name = last_name
    user.save()

user_registered.connect(user_registered_callback)


class VisitorGroup(models.Model):
    profile = models.CharField(max_length=100)
    info = models.TextField(max_length=3000, blank=True)
    caretaker = models.ForeignKey(User)
    assigned_group = models.OneToOneField(Group,
                                          on_delete=models.CASCADE,
                                          null=True,
                                          related_name='assigned_group')

    def __str__(self):
        return str(self.id)


class SurveyCode(models.Model):
    group = models.ForeignKey(Group)
    code = models.CharField(max_length=8)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class SurveyAnswer(models.Model):
    activity = models.ForeignKey(Activity)
    group = models.ForeignKey(Group)
    answer = models.TextField(max_length=3000)

    def __str__(self):
        return self.activity.title + "_" + str(self.group)
