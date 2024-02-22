from django.shortcuts import render
from django.http import HttpResponse


def detail(request, application_id):
    return HttpResponse(b"You're looking at item %s." % application_id)


def index(request):
    return HttpResponse(b"Hello, world. You're at the main index.")
