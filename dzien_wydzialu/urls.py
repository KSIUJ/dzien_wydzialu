from django.conf.urls import url, include
from django.contrib import admin
from dzien_wydzialu.home import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^program/$', views.program),
    url(r'^accounts/', include('registration.backends.default.urls')),
]
