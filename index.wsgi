# -*- coding: utf-8 -*-
# vim: ft=python:
# @module index.wsgi
# @desc Django wsgi start script
# @since 2024.02.21, 18:25
# @changed 2024.02.24, 10:09

import os
import sys
import time
import traceback
import signal
from pathlib import Path  # noqa

# App root path
rootPath = os.path.dirname(os.path.abspath(__file__))

# Detect home path...
home = str(Path.home())

activate_this = '/home/g/goldenjeru/.virtualenv/bin/activate_this.py'
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

# Inject application path...
sys.path.insert(1, rootPath)  # noqa  # pylint: disable=wrong-import-position
# sys.path.insert(1,'/home/g/goldenjeru/lilliputten.ru/django-test/')

import django

if django.VERSION[1] <= 6 and django.VERSION[0] <= 1:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'default_settings'
    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "default_settings")
    from django.core.wsgi import get_wsgi_application
    try:
        application = get_wsgi_application()
    except RuntimeError:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)

__all__ = [  # Exporting objects...
    'application',
]
