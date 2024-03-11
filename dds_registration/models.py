import string
import random
from functools import partial
from datetime import date

from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.models import (
    Group,
    User,
    # BaseUserManager,
    # AbstractBaseUser,
)

from django.db.models.signals import post_save

from core.constants.date_time_formats import dateTimeFormat


alphabet = string.ascii_lowercase + string.digits


random_code_length = 8


def random_code(length=random_code_length):
    return ''.join(random.choices(alphabet, k=length))


class Event(models.Model):
    code = models.TextField(unique=True, default=random_code)   # TODO: Show as an input
    title = models.TextField(unique=True, null=False, blank=False)  # TODO: Show as an input
    description = models.TextField(blank=True)
    registration_open = models.DateField(auto_now=True, help_text='Date registration opens')
    registration_close = models.DateField(blank=True, null=True, help_text='Date registration closes')
    max_participants = models.PositiveIntegerField(
        default=0,  # pyright: ignore [reportArgumentType]
        help_text='Maximum number of participants to this event (0 = no limit)',
    )
    currency = models.TextField(null=True, blank=True)  # TODO: Show as an input

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_active_registrations(self):
        """
        Return the active registrations
        """
        return self.registrations.all()  # filter(cancelledOn__isnull=True)

    def __unicode__(self):
        return self.name

    def clean(self):
        super(Event, self).clean()
        if self.registration_close and self.registration_open >= self.registration_close:
            raise ValidationError('Registration must open before it closes')

    def in_registration_window(self):
        today = date.today()
        return (today >= self.registration_open) and (not self.registration_close or today <= self.registration_close)

    def url(self):
        reverse('event_view', args=(self.unique_code,))

    def __str__(self):
        # fmt: off
        info = ', '.join(filter(None, map(str, [
            ' '.join(filter(None, map(str, [
                self.title,
                '({})'.format(self.code) if self.code else None,
            ]))),
            self.created_at.strftime(dateTimeFormat) if self.created_at else None,
        ])))
        # fmt: on
        return info


class RegistrationOption(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    item = models.TextField(null=False, blank=False)  # TODO: Show as an input
    price = models.FloatField(default=0, null=False)
    add_on = models.BooleanField(default=False)

    def __str__(self):
        # fmt: off
        info = ' '.join(filter(None, map(str, [
            self.item,
            '({})'.format(self.price) if self.price else None,
        ])))
        # fmt: on
        return info


class Registration(models.Model):
    """
    Ex `Booking` class in OneEvent
    """

    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='registrations', on_delete=models.CASCADE)
    options = models.ManyToManyField(RegistrationOption)
    paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['event', 'user'], name='Single registration')]

    def __str__(self):
        # fmt: off
        info = ', '.join(filter(None, map(str, [
            self.user.get_full_name(),
            self.user.email,
            self.created_at.strftime(dateTimeFormat) if self.created_at else None,
        ])))
        # fmt: on
        return info


class Message(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    message = models.TextField()
    emailed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # fmt: off
        info = ', '.join(filter(None, map(str, [
            self.event,
            self.created_at.strftime(dateTimeFormat) if self.created_at else None,
            'emailed' if self.emailed else None,
        ])))
        # fmt: on
        return info


class DiscountCode(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    code = models.TextField(default=partial(random_code, length=4))  # TODO: Show as an input
    # pyright: ignore [reportArgumentType]
    only_registration = models.BooleanField(default=True)
    percentage = models.IntegerField(help_text='Value as a percentage, like 10', blank=True, null=True)
    absolute = models.FloatField(help_text='Absolute amount of discount', blank=True, null=True)

    def __str__(self):
        # fmt: off
        info = ', '.join(filter(None, map(str, [
            self.event,
            self.created_at.strftime(dateTimeFormat) if self.created_at else None,
        ])))
        # fmt: on
        return info


class GroupDiscount(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    only_registration = models.BooleanField(default=True)
    percentage = models.IntegerField(help_text='Value as a percentage, like 10', blank=True, null=True)
    absolute = models.FloatField(help_text='Absolute amount of discount', blank=True, null=True)

    def __str__(self):
        # fmt: off
        info = ', '.join(filter(None, map(str, [
            self.event,
            'registration only' if self.only_registration else None,
            self.percentage,
            self.absolution,
        ])))
        # fmt: on
        return info