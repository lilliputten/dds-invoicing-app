from django.template.defaultfilters import register
from django.forms import ModelForm


@register.filter(name='form_field_type')
def form_field_type(form: ModelForm, id: str):
    '''Return form field types'''
    fields = form.fields
    return fields[id].widget.__class__.__name__
    #  field_types = {id: fields[id].widget.__class__.__name__ for id in fields}
    #  return getattr(field_types, id, )
