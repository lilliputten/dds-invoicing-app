from django.db import models
from preferences.models import Preferences
from django.conf import settings

from .Application import Application


# See:
# https://docs.djangoproject.com/en/5.0/intro/tutorial04/
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
# https://realpython.com/customize-django-admin-python/#modifying-a-change-list-using-list_display


class AllowedEmail(models.Model):
    email = models.EmailField(primary_key=True, max_length=80, null=False, blank=False)
    allow_participation = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]
    free_participation = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]

    def __str__(self):
        """
        Human-readable representation of the object
        """
        info = ', '.join(list(filter(None, [
            str(self.email) if self.email else None,
        ])))
        return info


class SitePreferences(Preferences):
    # @see https://github.com/praekelt/django-preferences
    # Site title
    site_title = models.CharField(max_length=80, default=settings.SITE_TITLE)  # pyright: ignore [reportArgumentType]

    # NOTE: To use `AllowedEmail` to restrict applicants by listed emails only
    allow_only_listed_emails = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]

    # TODO: Add other essential parameters...


__all__ = [
    'Application'
]
