from django.conf.urls import url
from django.contrib import admin
from dzien_wydzialu.home import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
]
