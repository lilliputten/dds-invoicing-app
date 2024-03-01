from django import forms
from django.contrib import admin
from preferences.admin import PreferencesAdmin

from .models import Event, Application, EventOption, SitePreferences


# @see:
# - https://realpython.com/customize-django-admin-python/#adding-search-to-the-list-screen


class ApplicationAdminForm(forms.ModelForm):
    class Meta:
        model = Application
        #  readonly_fields = ('secret_code', 'created_at', )
        exclude = ['id']


class ApplicationAdmin(admin.ModelAdmin):
    # NOTE: Trying to show non-editable fields (this approach doesn't work)
    readonly_fields = ['id', 'secret_code', 'created_at', 'updated_at']
    search_fields = ['name__startswith', 'email']
    form = ApplicationAdminForm

    list_display = ('id', 'status', 'name', 'email', 'created_at', 'updated_at')


class EventsAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ['name', 'status', 'options_list', 'created_at', 'updated_at', 'id']
    search_fields = ['name__startswith']
    readonly_fields = ['id', 'created_at', 'updated_at']

    def options_list(self, obj):
        return ', '.join([p.name for p in obj.options.all()])


class EventOptionsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'active', 'id']


admin.site.register(EventOption, EventOptionsAdmin)
admin.site.register(Event, EventsAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(SitePreferences, PreferencesAdmin)
