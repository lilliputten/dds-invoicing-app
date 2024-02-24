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

from .models import Application

"""
Save form:
    formset = ApplicationFormSet(request.POST)
"""


#  ApplicationForm = ModelForm

class ApplicationForm(ModelForm):
    # @see https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/
    class Meta:
        model = Application
        #  exclude = ('id',)
        fields = '__all__'


class DetailView(generic.DetailView):
    model = Application
    template_name = "detail.html"


def detail(request: HttpRequest, application_id: str):
    #  return HttpResponse("You're looking at application %s." % application_id)  # pyright: ignore [reportArgumentType]
    #  try:
    #      application = Application.objects.get(pk=application_id)
    #  except Application.DoesNotExist:
    #      raise Http404("Application does not exist")
    application = get_object_or_404(Application, pk=application_id)
    form = ApplicationForm(instance=application)
    return render(request, "detail.html", {"application": application, "form": form})


def index(request: HttpRequest):
    #  return HttpResponse("Hello, world. You're at the main index.")  # pyright: ignore [reportArgumentType]
    latest_application_list = Application.objects.order_by(  # pyright: ignore [reportAttributeAccessIssue]
        "-created_at")[:5]
    #  output = ", ".join([q.email for q in latest_application_list])
    #  return HttpResponse(output)
    context = {
        "latest_application_list": latest_application_list,
    }
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context, request))
