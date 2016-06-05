from django.contrib import admin
from dzien_wydzialu.home.models import Room, Lecturer, Activity, Event, Group, School, Profile, Image, SurveyCode, SurveyAnswer


import string
import random


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


def generate_survey_codes(modeladmin, request, queryset):
    for group in queryset.all():
        for code in group.surveycode_set.all():
            code.delete()
    for group in queryset.all():
        for _ in range(20):
            code = SurveyCode()
            code.code = ''.join(
                random.SystemRandom()
                        .choice(string.ascii_uppercase +
                                string.digits) for _ in range(8))
            code.group = group
            code.save()


generate_survey_codes.short_description = "Generate survey codes for group"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id']
    actions = [generate_survey_codes]


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Profile)
class ProfilelAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'school')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(SurveyCode)
class SurveyCodeAdmin(admin.ModelAdmin):
    list_display = ('group', 'code', 'used')


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('activity', 'group', 'answer')
