from registration.forms import RegistrationForm
from django import forms
from dzien_wydzialu.home.models import School
 
class ExRegistrationForm(RegistrationForm):
    school = forms.ModelChoiceField(queryset = School.objects.all())