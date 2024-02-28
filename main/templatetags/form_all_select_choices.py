from django.template.defaultfilters import register
from django.forms import ModelForm


@register.filter(name='form_all_select_choices')
def form_all_select_choices(form: ModelForm):
    '''Return form fields choices'''
    fields = form.fields
    return {id: fields[id].choices if fields[id].widget.__class__.__name__ == 'Select' else None
            for id in fields}
