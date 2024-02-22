from django.urls import path

from . import views

urlpatterns = [
    # see: https://docs.djangoproject.com/en/5.0/intro/tutorial03/
    path("", views.index, name="index"),
    path("<int:application_id>/", views.detail, name="detail"),
]
