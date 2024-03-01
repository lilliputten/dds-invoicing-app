from django import forms
from django.contrib import admin
from preferences.admin import PreferencesAdmin

from .models import Event, Application, EventOption,  SitePreferences


# @see:
# - https://realpython.com/customize-django-admin-python/#adding-search-to-the-list-screen


class ApplicationAdminForm(forms.ModelForm):
    #  created_at = forms.DateTimeField()
    #  secret_code = forms.UUIDField()

    class Meta:
        model = Application
        #  fields = ('secret_code', 'created_at', )
        #  readonly_fields = ('secret_code', 'created_at', )
        exclude = ('id',)


class ApplicationAdmin(admin.ModelAdmin):
    # NOTE: Trying to show non-editable fields (this approach doesn't work)
    #  fields = ('secret_code', 'created_at', )
    readonly_fields = ('id', 'secret_code', 'created_at', 'updated_at')
    search_fields = ('name__startswith', 'email')
    form = ApplicationAdminForm

    list_display = ('id', 'status', 'name', 'email', 'created_at', 'updated_at')


#  class AllowedEmailsAdmin(admin.ModelAdmin):
#     search_fields = ('email', )
#     list_display = ('email', 'allow_participation', 'free_participation')


class EventsAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')
    list_display = ('name', 'status', 'options_list', 'id')

    def options_list(self, obj):
        return "\n".join([p.name for p in obj.options.all()])


class EventOptionsAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'active')


#  admin.site.register(AllowedEmail, AllowedEmailsAdmin)

admin.site.register(EventOption, EventOptionsAdmin)
admin.site.register(Event, EventsAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(SitePreferences, PreferencesAdmin)
