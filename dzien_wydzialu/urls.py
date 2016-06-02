from django.conf.urls import url, include
from django.contrib import admin
from dzien_wydzialu.home import views
from registration.backends.default.views import RegistrationView
from dzien_wydzialu.home.forms import ExRegistrationForm
from dzien_wydzialu.home.forms import ExAuthenticationForm
from django.views.generic import TemplateView



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='homepage'),
    url(r'^program/$', views.program, name='program'),
    url(r'^program/group/(?P<group_id>\d+)', views.get_group_pdf, name='group_pdf'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=ExRegistrationForm), name='registration_register'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'authentication_form': ExAuthenticationForm},
        name='auth_login'),
    url(r'^accounts/', include('registration.backends.default.urls')),
 ]
