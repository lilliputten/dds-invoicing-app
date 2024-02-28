from django.urls import path

from . import views

app_name = "application"

urlpatterns = [
    # see: https://docs.djangoproject.com/en/5.0/intro/tutorial03/

    path("", views.create_new_application, name="create_application"),
    #  path("application/<str:pk>/", views.DetailView.as_view(), name="detail"),
    path("application/review/<str:application_id>/", views.review_application, name="review_application"),
    path("components-demo", views.components_demo, name="components_demo"),
]
