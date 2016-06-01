from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from dzien_wydzialu.home.models import School, VisitorGroup
from registration.forms import RegistrationForm


def validate_password_strength(value2):
    # here we can do everythin connected with validate password, we can change minimum lenght
    # number of digits in password , whatever we want
    min_length = 8

    if len(value2) < min_length:
        raise ValidationError(_('Hasło jest za krótkie.').format(min_length))
    return value2


class ExAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Nazwa użytkownika"),max_length=254, error_messages={'required': 'To pole jest wymagane.'})
    password = forms.CharField(label=_("Hasło"), strip=False, widget=forms.PasswordInput, error_messages={'required': 'To pole jest wymagane.'})

    error_messages = {
        'invalid_login': _("Proszę wprowadzić prawidłową nazwę użytkownika i hasło."),
        'inactive': _("To konto jest nieaktywne."),
        'required': _("to jest wymagane")
    }

class ExRegistrationForm(RegistrationForm):
    school = forms.ModelChoiceField(queryset = School.objects.all())
    #overwrited method for password check
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return validate_password_strength(self.cleaned_data['password2'])

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


class VisitorGroupForm(forms.ModelForm):
    class Meta:
        model = VisitorGroup
        fields = ['profile', 'info']

    def __init__(self, *args, **kwargs):
        super(VisitorGroupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'newVisitorGroupForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))
