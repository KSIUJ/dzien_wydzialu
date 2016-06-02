from django.contrib import admin
from dzien_wydzialu.home.models import Room, Lecturer, Activity, Event, Group, School, Profile, Image


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'projector', 'board', 'computers', 'seats')


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'degree')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_lecture', 'room')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'activity')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Profile)
class ProfilelAdmin(admin.ModelAdmin):
    list_display = ('user','role', 'school')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')