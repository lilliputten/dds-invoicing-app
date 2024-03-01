from django.db import models
from preferences.models import Preferences
from django.db import models
from django.conf import settings
#  from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
#  from django.contrib.contenttypes.models import ContentType
import uuid

from core.constants.date_time_formats import dateTimeFormat


# See:
# https://docs.djangoproject.com/en/5.0/intro/tutorial04/
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
# https://realpython.com/customize-django-admin-python/#modifying-a-change-list-using-list_display


class EventOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80, null=False, blank=False)
    active = models.BooleanField(default=True)  # pyright: ignore [reportArgumentType]

    def __str__(self):
        return str(self.name)


class Event(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=80, null=False, blank=False)
    description = models.TextField(max_length=600, blank=True)

    options = models.ManyToManyField(
        EventOption,
        related_name="event",
    )

    STATUSES = (
        ("WAITING", "Waiting"),
        ("ACTIVE", "Active"),
        ("CLOSED", "Closed"),
    )
    status = models.CharField(max_length=15, choices=STATUSES, default="WAITING")

    allowed_emails = models.TextField(max_length=600, default='', blank=True)
    no_payment_emails = models.TextField(max_length=600, default='', blank=True)

    def __str__(self):
        return str(self.name)


#  class AllowedEmail(models.Model):
#      email = models.EmailField(primary_key=True, max_length=80, null=False, blank=False)
#      allow_participation = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]
#      free_participation = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]
#
#      def __str__(self):
#          return str(self.email)


class Application(models.Model):

    # Generated:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    secret_code = models.UUIDField(default=uuid.uuid4)  # , editable=False)
    #  secret_code = models.CharField(max_length=100)  # (generated)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Application to event
    event = models.ForeignKey(
        Event,
        on_delete=models.deletion.CASCADE,  # pyright: ignore [reportAttributeAccessIssue]
        related_name="application",
        null=True,
        blank=False,
    )

    # User data:
    name = models.CharField(max_length=80, null=False, blank=False)
    email = models.EmailField(max_length=80, null=False, blank=False)
    comment = models.TextField(max_length=400, blank=True)  # Comment

    # Payment method:
    PAYMENT_METHODS = (
        ("STRIPE", "Stripe"),
        ("INVOICE", "Invoice"),
    )
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHODS, default="STRIPE")  # (stripe, invoice)

    # Status:
    STATUSES = (
        ("WAITING", "Waiting"),
        ("FINISHED", "Finished"),
    )
    status = models.CharField(max_length=15, choices=STATUSES, default="WAITING")  # (waiting, finished)
    PAYMENT_STATUSES = (
        # TODO: Not required?
        ("WAITING", "Waiting"),
        ("FINISHED", "Finished"),
    )
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUSES, default="WAITING")  # (waiting, finished)
    # TODO: Update neccessary status values

    options = models.ManyToManyField(
        EventOption,
        related_name="application",
    )

    #  # Application options:
    #  option_hackaton = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]
    #  option_tshirt = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]

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


class SitePreferences(Preferences):
    # @see https://github.com/praekelt/django-preferences
    # Site title
    site_title = models.CharField(max_length=80, default=settings.SITE_TITLE)  # pyright: ignore [reportArgumentType]

    # NOTE: To use `AllowedEmail` to restrict applicants by listed emails only
    allow_only_listed_emails = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]

    # TODO: Add other essential parameters...
