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

import re

from core.helpers.debug_helpers import get_object_props

from .ApplicationForm import ApplicationForm, ApplicationClientForm
from .models import ApplicationModel

"""
Save form:
    formset = ApplicationFormSet(request.POST)
"""


class DetailView(generic.DetailView):
    model = ApplicationModel
    template_name = "detail.html"


def components_demo(request: HttpRequest):
    return render(request, "components-demo.django")


def detail(request: HttpRequest, application_id: str):
    # Find application by id...
    application = get_object_or_404(ApplicationModel, pk=application_id)
    form = ApplicationForm(instance=application)
    context = {"application": application, "form": form}
    return render(request, "detail.html.django", context)


def new_application(request: HttpRequest):
    # Empty application...
    application = ApplicationModel()
    application.name = 'Test'
    form = ApplicationClientForm(instance=application)
    form.is_valid()
    fields = form.fields
    context = {
        "application": application,
        "form": form,
        "form_data": form.data,
        "fields": fields,
        "field_types": {id: fields[id].widget.__class__.__name__ for id in fields},
        "select_choices": {id: fields[id].choices if fields[id].widget.__class__.__name__ == 'Select' else None
            for id in fields},
    }
    #  list = tuple((id, fields[id].widget.__class__.__name__) for id in fields)
    print('YYY', get_object_props(form))
    #  print('XXX', fields['status'].choices)
    #  name: TextInput
    #  email: EmailInput
    #  text: TextInput
    #  payment_method: Select
    #  status: Select
    #  payment_status: Select
    #  option_hackaton: CheckboxInput
    #  option_tshirt: CheckboxInput

    return render(request, "new-application-form.html.django", context)


def index(request: HttpRequest):
    #  return HttpResponse("Hello, world. You're at the main index.")  # pyright: ignore [reportArgumentType]
    latest_application_list = ApplicationModel.objects.order_by(  # pyright: ignore [reportAttributeAccessIssue]
        "-created_at")[:5]
    #  output = ", ".join([q.email for q in latest_application_list])
    #  return HttpResponse(output)
    context = {
        "latest_application_list": latest_application_list,
    }
    template = loader.get_template("index.html.django")
    return HttpResponse(template.render(context, request))
