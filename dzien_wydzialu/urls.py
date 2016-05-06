from django.conf.urls import url, include
from django.contrib import admin
from dzien_wydzialu.home import views
from registration.backends.default.views import RegistrationView
from dzien_wydzialu.home.forms import ExRegistrationForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^program/$', views.program),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class = ExRegistrationForm), name = 'registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
]
