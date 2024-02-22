from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django import template
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Application


def detail(request: HttpRequest, application_id: str):
    #  return HttpResponse("You're looking at application %s." % application_id)  # pyright: ignore [reportArgumentType]
    #  try:
    #      application = Application.objects.get(pk=application_id)
    #  except Application.DoesNotExist:
    #      raise Http404("Application does not exist")
    application = get_object_or_404(Application, pk=application_id)
    return render(request, "detail.html", {"application": application})

def index(request: HttpRequest):
    #  return HttpResponse("Hello, world. You're at the main index.")  # pyright: ignore [reportArgumentType]
    latest_application_list = Application.objects.order_by("-created_at")[:5]  # pyright: ignore [reportAttributeAccessIssue]
    #  output = ", ".join([q.email for q in latest_application_list])
    #  return HttpResponse(output)
    context = {
        "latest_application_list": latest_application_list,
    }
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context, request))
