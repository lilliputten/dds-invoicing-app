from django.template.defaultfilters import register
from django.forms import ModelForm


@register.filter(name='form_select_choices')
def form_select_choices(form: ModelForm, id: str):
    '''Return form field choices'''
    fields = form.fields
    return fields[id].choices \
        if fields[id].widget.__class__.__name__ == 'SelectMultiple' \
        or fields[id].widget.__class__.__name__ == 'Select' \
        else None
