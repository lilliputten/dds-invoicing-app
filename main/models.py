from django.db import models
from preferences.models import Preferences
from django.db import models
from django.conf import settings
import uuid
from core.constants.date_time_formats import dateTimeFormat


# See:
# https://docs.djangoproject.com/en/5.0/intro/tutorial04/
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
# https://realpython.com/customize-django-admin-python/#modifying-a-change-list-using-list_display


class Application(models.Model):

    # Generated:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    secret_code = models.UUIDField(default=uuid.uuid4)  # , editable=False)
    #  secret_code = models.CharField(max_length=100)  # (generated)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # User data:
    name = models.CharField(max_length=80, null=False, blank=False)
    email = models.EmailField(max_length=80, null=False, blank=False)
    text = models.CharField(max_length=200, blank=True)  # Comment

    # Options:
    PAYMENT_METHODS = (
        ("STRIPE", "Stripe"),
        ("INVOICE", "Invoice"),
    )
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHODS, default="STRIPE")  # (stripe, invoice)

    # State:
    STATUSES = (
        ("WAITING", "Waiting"),
        ("FINISHED", "Finished"),
    )
    status = models.CharField(max_length=15, choices=STATUSES, default="WAITING")  # (waiting, finished)
    PAYMENT_STATUSES = (
        ("WAITING", "Waiting"),
        ("FINISHED", "Finished"),
    )
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUSES, default="WAITING")  # (waiting, finished)
    # TODO: Update neccessary status values

    # Application options:
    option_hackaton = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]
    option_tshirt = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]

    def __str__(self):
        """
        Human-readable representation of the object
        """
        info = ", ".join(list(filter(None, [
            str(self.email) if self.email else None,
            str(self.name) if self.name else None,
            #  str(self.created_at) if self.created_at else "",
            self.created_at.strftime(dateTimeFormat)  # pyright: ignore [reportAttributeAccessIssue]
            if self.created_at else None,
        ])))
        info = " (" + info + ")" if info else None
        info = " ".join(list(filter(None, [
            str(self.id),
            info,
        ])))
        return info


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
