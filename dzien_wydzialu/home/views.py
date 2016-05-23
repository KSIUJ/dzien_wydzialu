from django.shortcuts import render
from dzien_wydzialu.home.models import Group


def index(request):
    return render(request, "home/index.html", {})


def program(request):
    groups = Group.objects.all()
    return render(request, "home/program.html", {
                  'groups': groups,
                  })
