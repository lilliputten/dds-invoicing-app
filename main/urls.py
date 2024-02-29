from django.urls import path
#  from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
from django.conf import settings

from . import views

app_name = "application"

cache_timeout = 15 * 60  # in seconds: {min}*60
if settings.LOCAL or settings.DEBUG:
    cache_timeout = 0

urlpatterns = [
    # see: https://docs.djangoproject.com/en/5.0/intro/tutorial03/

    path("", views.create_new_application, name="create_application"),
    #  path("application/<str:pk>/", views.DetailView.as_view(), name="detail"),
    path("application/review/<str:application_id>/", views.review_application, name="review_application"),
    path("components-demo", views.components_demo, name="components_demo"),

    # service pages
    path('robots.txt', cache_page(cache_timeout)(views.RobotsView.as_view()), name='robots'),
    #  url(r'^robots\.txt$', cache_page(cache_timeout)(views.RobotsView.as_view()), name='robots'),
    #  url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap.sitemaps_dict}, name='sitemap'),
]
