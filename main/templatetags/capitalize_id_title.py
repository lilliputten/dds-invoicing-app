import re
from django.template.defaultfilters import register

from core.helpers.utils import capitalize_id


@register.filter(name='capitalize_id_title')
def capitalize_id_title(id):
    """ Get human-readable object title from id
    """
    return capitalize_id(id)
