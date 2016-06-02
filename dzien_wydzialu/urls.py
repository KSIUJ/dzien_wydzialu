from django.conf.urls import url, include
from django.contrib import admin
from dzien_wydzialu.home import views
from registration.backends.default.views import RegistrationView
from dzien_wydzialu.home.forms import ExRegistrationForm

accounts_patterns = [
    url(r'^register/$',
        RegistrationView.as_view(form_class=ExRegistrationForm),
        name='registration_register'),
    url(r'^', include('registration.backends.default.urls')),
]

urlpatterns = [
    url(r'^$',
        views.index,
        name='homepage'),
    url(r'^gallery/$',
        views.gallery,
        name='gallery'),
    url(r'^program/$',
        views.program,
        name='program'),
    url(r'^program/group/(?P<group_id>\d+)',
        views.get_group_pdf,
        name='group_pdf'),
    url(r'^visitorgroup/$',
        views.visitorgroup_index,
        name='visitorgroup_index'),
    url(r'^visitorgroup/new/$',
        views.visitorgroup_new,
        name='visitorgroup_new'),
    url(r'^visitorgroup/assign/$',
        views.visitorgroup_assign,
        name='visitorgroup_assign'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(accounts_patterns)),
]
