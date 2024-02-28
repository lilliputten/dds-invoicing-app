from django.template.defaultfilters import register
from django.forms import ModelForm


@register.filter(name='form_all_field_types')
def form_all_field_types(form: ModelForm):
    '''Return all form field types'''
    fields = form.fields
    return {id: fields[id].widget.__class__.__name__ for id in fields}
