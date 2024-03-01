from django.forms import ModelForm

from .models import Application


class ApplicationClientForm(ModelForm):
    class Meta:
        model = Application
        exclude = ('id', 'secret_code', 'status', 'payment_status')
        fields = '__all__'


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ('id', 'secret_code')
        fields = '__all__'


__all__ = [
    'ApplicationClientForm',
    'ApplicationForm'
]
