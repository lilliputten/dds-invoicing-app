from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django import template
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm
from django.urls import reverse
from django.views import generic
from typing import TypedDict

from core.helpers.logger import DEBUG

from .ApplicationModel import ApplicationModel


DEBUG('Test', {'test': 1})

class ApplicationClientForm(ModelForm):
    asAdmin: bool

    # @see https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/
    def __init__(self, instance: ApplicationModel, asAdmin: bool = False):
        self.asAdmin = asAdmin
        super().__init__(instance=instance)

    class Meta:
        model = ApplicationModel
        exclude = ('id', 'secret_code')
        fields = '__all__'


class ApplicationForm(ModelForm):
    asAdmin: bool

    # @see https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/
    def __init__(self, instance: ApplicationModel, asAdmin: bool = False):
        self.asAdmin = asAdmin
        super().__init__(instance=instance)

    class Meta:
        model = ApplicationModel
        exclude = ('id', 'secret_code')
        fields = '__all__'

