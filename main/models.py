import uuid
from django.db import models
from core.constants import dateTimeFormat


# TODO:
# Emails list:
# - For free applying
# - To limit people allowed to apply

# See https://docs.djangoproject.com/en/5.0/intro/tutorial04/

class Application(models.Model):

    # Generated:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    secret_code = models.UUIDField(default=uuid.uuid4)  #, editable=False)
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


# TODO: Use choices as options
class Choice(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)  # pyright: ignore [reportArgumentType]
