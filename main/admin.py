from django import forms
from django.contrib import admin

from .models import Application


class CustomApplicationForm(forms.ModelForm):
    #  created_at = forms.DateTimeField()
    #  secret_code = forms.UUIDField()

    class Meta:
        model = Application
        #  fields = ('secret_code', 'created_at')
        readonly_fields = ('secret_code', 'created_at')
        exclude = ('id',)


class ApplicationAdmin(admin.ModelAdmin):
    # NOTE: Trying to show non-editable fields (this approach doesn't work)
    fields = ('secret_code', 'created_at')
    readonly_fields = ('secret_code', 'created_at')
    form = CustomApplicationForm


admin.site.register(Application)
