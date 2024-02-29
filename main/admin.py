from django import forms
from django.contrib import admin
from preferences.admin import PreferencesAdmin

from .models import Application, AllowedEmail, SitePreferences


# @see:
# - https://realpython.com/customize-django-admin-python/#adding-search-to-the-list-screen


class CustomApplicationForm(forms.ModelForm):
    #  created_at = forms.DateTimeField()
    #  secret_code = forms.UUIDField()

    class Meta:
        model = Application
        #  fields = ('secret_code', 'created_at', )
        readonly_fields = ('secret_code', 'created_at', )
        exclude = ('id',)


class ApplicationAdmin(admin.ModelAdmin):
    # NOTE: Trying to show non-editable fields (this approach doesn't work)
    #  fields = ('secret_code', 'created_at', )
    readonly_fields = ('secret_code', 'created_at', )
    search_fields = ('name__startswith', )
    form = CustomApplicationForm

    list_display = ('name', 'email', 'created_at')


class AllowedEmailsAdmin(admin.ModelAdmin):
    search_fields = ('email', )

    list_display = ('email', 'allow_participation', 'free_participation')


admin.site.register(Application, ApplicationAdmin)
admin.site.register(AllowedEmail, AllowedEmailsAdmin)
admin.site.register(SitePreferences, PreferencesAdmin)
