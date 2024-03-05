from django.db import models
from preferences.models import Preferences
from django.db import models
from django.conf import settings
import uuid
from uuid import UUID
#  import datetime

from core.constants.date_time_formats import dateTimeFormat


#  now = datetime.datetime.now()


# See:
# https://docs.djangoproject.com/en/5.0/intro/tutorial04/
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
# https://realpython.com/customize-django-admin-python/#modifying-a-change-list-using-list_display


class EventOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80, null=False, blank=False)
    active = models.BooleanField(default=True)  # pyright: ignore [reportArgumentType]

    # TODO: Store active (and default) values in the vent object?

    # TODO: Add default value?

    def __str__(self):
        return str(self.name)


class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=80, null=False, blank=False)
    description = models.TextField(max_length=600, blank=True)

    options = models.ManyToManyField(
        EventOption,
        related_name="event",
    )

    # TODO: Add check for correct event status!
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
        # TODO: Other statuses?
        ("WAITING", "Waiting for activation"),
        ("PAYMENT", "Waiting for payment"),
        ("ACTIVE", "Active"),
        ("CLOSED", "Closed"),
    )
    status = models.CharField(max_length=15, choices=STATUSES, default="WAITING")  # (waiting, finished)
    PAYMENT_STATUSES = (
        # TODO: Not required?
        ("WAITING", "Waiting"),
        ("OK", "Ok"),
    )
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUSES, default="WAITING")  # (waiting, finished)

    options = models.ManyToManyField(
        EventOption,
        related_name="application",
    )

    #  # Hardcoded options aren't used anymore: used many-to-many relation with `EventOption` (see above)
    #  # Application options:
    #  option_hackaton = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]
    #  option_tshirt = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if event_id:
        #     self.event = Event.objects.get(pk=event_id)  # pyright: ignore [reportAttributeAccessIssue]

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

    #  # NOTE: To use `AllowedEmail` to restrict applicants by listed emails only (UNUSED)
    #  allow_only_listed_emails = models.BooleanField(default=False)  # pyright: ignore [reportArgumentType]

    # TODO: Add other essential parameters...
