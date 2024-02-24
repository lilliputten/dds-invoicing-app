from django import forms
from django.forms import ModelForm
from .models import Application


class ApplicationForm(ModelForm):
    class Meta:
        model = Application

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
