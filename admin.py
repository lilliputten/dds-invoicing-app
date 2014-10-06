'''
Created on 5 Jun 2014

@author: germs
'''
from django.contrib import admin
from models import (Event, EventChoice, EventChoiceOption, ParticipantBooking,
                    ParticipantOption)
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class EditLinkToInlineObjectMixin(object):
    '''
    Mixin to allow having a link to the admin page of another Model
    From http://stackoverflow.com/a/22113967
    '''
    def edit_link(self, instance):
        url = reverse(
            'admin:%s_%s_change' % (instance._meta.app_label, instance._meta.module_name),
            args=[instance.pk]
        )
        if instance.pk:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''


class LimitedAdminInlineMixin(object):
    """
    InlineAdmin mixin limiting the selection of related items according to
    criteria which can depend on the current parent object being edited.

    A typical use case would be selecting a subset of related items from
    other inlines, ie. images, to have some relation to other inlines.

    Use as follows::

        class MyInline(LimitedAdminInlineMixin, admin.TabularInline):
            def get_filters(self, obj):
                return (('<field_name>', dict(<filters>)),)

    From https://gist.github.com/dokterbob/828117
    """

    @staticmethod
    def limit_inline_choices(formset, field, empty=False, **filters):
        """
        This function fetches the queryset with available choices for a given
        `field` and filters it based on the criteria specified in filters,
        unless `empty=True`. In this case, no choices will be made available.
        """
        assert field in formset.form.base_fields

        qs = formset.form.base_fields[field].queryset
        if empty:
            formset.form.base_fields[field].queryset = qs.none()
        else:
            qs = qs.filter(**filters)

            formset.form.base_fields[field].queryset = qs

    def get_formset(self, request, obj=None, **kwargs):
        """
        Make sure we can only select variations that relate to the current
        item.
        """
        formset = \
            super(LimitedAdminInlineMixin, self).get_formset(request,
                                                             obj,
                                                             **kwargs)

        for (field, filters) in self.get_filters(obj):
            if obj:
                self.limit_inline_choices(formset, field, **filters)
            else:
                self.limit_inline_choices(formset, field, empty=True)

        return formset

    def get_filters(self, _):
        """
        Return filters for the specified fields. Filters should be in the
        following format::

            (('field_name', {'categories': obj}), ...)

        For this to work, we should either override `get_filters` in a
        subclass or define a `filters` property with the same syntax as this
        one.
        """
        return getattr(self, 'filters', ())


class EventChoiceOptionInline(admin.TabularInline):
    model = EventChoiceOption
    fields = ('title', 'default',)


class EventChoiceAdmin(admin.ModelAdmin):
    fields = ('event', 'title', )
    readonly_fields = ('event',)
    inlines = [EventChoiceOptionInline]
    list_display = ('event', 'title')


class EventChoiceInline(admin.TabularInline, EditLinkToInlineObjectMixin):
    model = EventChoice
    fields = ('title', 'edit_link',)
    readonly_fields = ('edit_link',)


class EventAdmin(admin.ModelAdmin):
    fields = (
        'title',
        ('start', 'end'),
        ('location_name', 'location_address'),
        'organisers',
        ('booking_close', 'choices_close'),
        ('price_for_employees', 'price_for_contractors', 'price_currency'),
        ('employees_groups', 'contractors_groups'),
    )
    inlines = (EventChoiceInline,)
    list_display = ('title', 'start', 'end')


class ParticipantOptionInline(LimitedAdminInlineMixin, admin.TabularInline):
    model = ParticipantOption

    def get_filters(self, obj):
        return (('option', {'choice__event': obj.event}),)


class ParticipantBookingAdmin(admin.ModelAdmin):
    inlines = (ParticipantOptionInline,)
    list_display = ('event', 'person', 'cancelled')


admin.site.register(Event, EventAdmin)
admin.site.register(EventChoice, EventChoiceAdmin)
admin.site.register(ParticipantBooking, ParticipantBookingAdmin)
