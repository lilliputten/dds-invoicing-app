from django.apps import AppConfig
from django.conf import settings

from core.helpers.logger import DEBUG
from core.helpers.utils import getTrace


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # pyright: ignore [reportAssignmentType]
    name = 'main'
