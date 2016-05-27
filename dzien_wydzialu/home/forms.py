from registration.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import authenticate
from django import forms
from dzien_wydzialu.home.models import School

 
class ExRegistrationForm(RegistrationForm):
    school = forms.ModelChoiceField(queryset = School.objects.all())



    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['school'].label = 'Szkoła'
        self.fields['school'].error_messages = {'required': 'To pole jest wymagane!'}
        self.fields['school'].help_text = 'Wybierz swoją szkołę z listy.'
        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['username'].help_text = 'Maksymalnie 30 znaków. Dozwolone litery, cyfry oraz @/./+/-/_ .'
        self.fields['username'].error_messages = {'unique': 'Podana nazwa jest już w systemie!',
                                                  'invalid': 'Podana nazwa zawiera niedozwolone znaki!',
                                                  'required': 'To pole jest wymagane!'}
        self.fields['email'].error_messages = {'required': 'To pole jest wymagane!'}
        self.fields['password1'].label = 'Hasło'
        self.fields['password1'].help_text = 'Wprowadzone hasło powinno mieć miniumum 8 znaków!'
        self.fields['password1'].error_messages = {'required': 'To pole jest wymagane!'}
        self.fields['password2'].label = 'Potwierdzenie hasła'
        self.fields['password2'].help_text = 'Wprowadź ponownie hasło.'
        self.fields['password2'].error_messages = {'required': 'To pole jest wymagane!'}
        self.error_messages = {'password_mismatch': 'Podane hasła są różne, wprowadź ponownie.',
                               'password_too_short': 'To nie dziła bez tego importa co go nie moge znalezc'}



