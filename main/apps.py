from django.apps import AppConfig
from django.conf import settings

from core.helpers.logger import DEBUG
from core.helpers.utils import getTrace

DEBUG(getTrace('App start'), {
    'RUNNING_DEVSERVER': settings.RUNNING_DEVSERVER,
    'RUNNING_MANAGE_PY': settings.RUNNING_MANAGE_PY,
    'RUNNING_MOD_WSGI': settings.RUNNING_MOD_WSGI,
    'LOCAL': settings.LOCAL,
    'DEV': settings.DEV,
})


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # pyright: ignore [reportAssignmentType]
    name = 'main'
