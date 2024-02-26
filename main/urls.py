from django.urls import path

from . import views

app_name = "application"

urlpatterns = [
    # see: https://docs.djangoproject.com/en/5.0/intro/tutorial03/
    path("", views.index, name="index"),
    #  path("application/<str:pk>/", views.DetailView.as_view(), name="detail"),
    path("application/<str:application_id>/", views.detail, name="detail"),
]
