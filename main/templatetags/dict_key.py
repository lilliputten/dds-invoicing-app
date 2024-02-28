from django.template.defaultfilters import register


@register.filter(name='dict_key')
def dict_key(d: dict, k: str):
    '''Returns the given key from a dictionary.'''
    return d[k]
