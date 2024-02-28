from django import forms
from django.forms import ModelForm
from .models import ApplicationModel


# TODO: Check redundancy, see ApplicationForm.py

class ApplicationForm(ModelForm):
    class Meta:
        model = ApplicationModel

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
