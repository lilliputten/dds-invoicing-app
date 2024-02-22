#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python:
# @module index.wsgi
# @desc Django wsgi start script
# @since 2024.02.21, 18:25
# @changed 2024.02.21, 18:45

"""
Django wsgi start script
"""

from django.core.wsgi import get_wsgi_application
import django
import os  # noqa
import sys  # noqa
import time  # noqa
import traceback  # noqa
import signal  # noqa
from pathlib import Path  # noqa

# App root path
rootPath = os.path.dirname(os.path.abspath(__file__))

# Detect home path...
home = str(Path.home())

# TODO: To load actual venv name from the external config file?
venv = '.venv-py3.10-django-5'  # Python 3.10, Django 5.0
#  venv = '.venv-py3.10-flask'  # Python 3.10, Flask 2.0.3
#  venv = '.virtualenv'  # Default

# Activate venv...
activate_this = os.path.join(home, venv, 'bin/activate_this.py')
# TODO: Check venv folder existency?
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

# Inject application path...
sys.path.insert(1, rootPath)  # noqa  # pylint: disable=wrong-import-position

# Start django app...

# This code is for modern django versions (>1.6)...
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'default_settings')
try:
    application = get_wsgi_application()
except RuntimeError:
    traceback.print_exc()
    os.kill(os.getpid(), signal.SIGINT)
    time.sleep(2.5)
    # TODO: To write error log to the file?

#  # UNUSED: Start flask application...
#  from src.server import app as application  # noqa

__all__ = [  # Exporting objects...
    'application',
]
