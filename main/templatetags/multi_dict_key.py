from django.template.defaultfilters import register

@register.filter(name='multi_dict_key')
def multi_dict_key(d: dict, k: str):
    '''Returns the given key from a dictionary.'''
    return d.get(k)
