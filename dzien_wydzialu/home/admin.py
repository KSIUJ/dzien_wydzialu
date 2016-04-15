from django.contrib import admin
from dzien_wydzialu.home.models import Room, Lecturer, Activity, Event, Group


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    fields = ('number', 'projector', 'board', 'computers', 'info', 'seats')


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    fields = ('name', 'surname', 'degree')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fields = ('title', 'is_lecture', 'lecturer', 'room')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('start_time', 'end_time', 'activity')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass
