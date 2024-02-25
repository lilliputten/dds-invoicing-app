"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import posixpath, re
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Determine dev mode...

RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')
RUNNING_MANAGE_PY = (len(sys.argv) > 0 and sys.argv[0] == 'manage.py')
RUNNING_MOD_WSGI = (len(sys.argv) > 0 and sys.argv[0] == 'mod_wsgi')
LOCAL_RUN = RUNNING_MANAGE_PY and not RUNNING_MOD_WSGI
LOCAL = LOCAL_RUN and RUNNING_DEVSERVER
DEV = LOCAL
DEBUG = True  # LOCAL

print('RUNNING_DEVSERVER', RUNNING_DEVSERVER)
print('RUNNING_MANAGE_PY', RUNNING_MANAGE_PY)
print('RUNNING_MOD_WSGI', RUNNING_MOD_WSGI)
print('LOCAL', LOCAL)
print('DEV', DEV)

DEV_MAKET_MODE = LOCAL and False  # Try to compile js & css resources on-the-fly, alternatively it's possible to use `livereload-assets-server` (see below)
BLOCKS_FILES_SCAN = DEV_MAKET_MODE
SHOW_DJANGO_TOOLBAR = True
COMPRESS_ENABLED = not LOCAL # not DEV_MAKET_MODE
USE_PRECOMPILERS = False
USE_FAKE_DB = False

BEAUTIFY_HTML = not LOCAL # COMPRESS_ENABLED
BEAUTIFY_HTML_OPTIONS = {
    'REPLACE_BEGINNING_SPACES': False,
    'REMOVE_FOLDS': True,
}

# Basic app properties...

APP_NAME = 'main'  # Root app name

# Aux folders...

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_FOLDER = posixpath.join('static', '')
STATIC_ROOT = posixpath.join(BASE_DIR, STATIC_FOLDER, '')
STATIC_URL = posixpath.join('/', STATIC_FOLDER, '')

ASSETS_FOLDER = posixpath.join('assets-src', '')
ASSETS_ROOT = posixpath.join(BASE_DIR, ASSETS_FOLDER, '')
ASSETS_URL = posixpath.join('/', ASSETS_FOLDER, '')

MEDIA_FOLDER = posixpath.join('media', '')
MEDIA_ROOT = posixpath.join(BASE_DIR, MEDIA_FOLDER, '')
MEDIA_URL = posixpath.join('/', MEDIA_FOLDER, '')

BLOCKS_FOLDER = posixpath.join('blocks', '')
BLOCKS_ROOT = posixpath.join(STATIC_ROOT, BLOCKS_FOLDER, '' )

#  TEMPLATES_PATH = STATIC_FOLDER # posixpath.join(STATIC_FOLDER, 'templates', '')  # TODO?

# Additional locations of static files
STATICFILES_DIRS = (

    # Put strings here, like '/home/html/static' or 'C:/www/django/static'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #  STATIC_ROOT,
    #  ASSETS_ROOT,  ## Debug only
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j!v87tv!k=v7@79h&hydkr3og41uq@z=)euo@+)rbw0a*dpvx@'

ALLOWED_HOSTS = [
    'dds-invoicing-server.lilliputten.ru',
    'dds-invoicing-server.lilliputten.com',
    #  # TODO: Add other actual domains
]
if DEV:
    ALLOWED_HOSTS.insert(0, 'localhost');

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Extra apps...
    #  'social.apps.django_app.default',
    #  'bootstrapform',
    'compressor',

    # Local apps...
    'main.apps.MainConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add livereload app...
INSTALLED_APPS.insert(0, 'livereload');
if False or DEV:
    MIDDLEWARE.append('livereload.middleware.LiveReloadScript');

ROOT_URLCONF = 'django_project.urls'

# Extra templates folders...
TEMPLATES_DIRS = [STATIC_ROOT]
if DEV:
    TEMPLATES_DIRS.append(ASSETS_ROOT);

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                APP_NAME+'.context_processors.common_values',  # Pass local context to the templates. @see `main/context_processors.py`
            ],
        },
        'DIRS': TEMPLATES_DIRS,
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Site config

SITE_NAME = u'DDS Invoicing'
SITE_TITLE = SITE_NAME
SITE_DESCRIPTION = u'DDS Invoicing'
SITE_KEYWORDS = u'''
DDS
Invoicing
application
'''
SITE_KEYWORDS = re.sub(r'\s*[\n\r]+\s*', ', ', SITE_KEYWORDS.strip())
#  print(u'keywords: %s ' % SITE_KEYWORDS)

if DEV: SITE_TITLE += ' (DEV)'


# pass settings to context
PASS_VARIABLES = {
    # DEBUG: Debug only!
    'RUNNING_DEVSERVER': RUNNING_DEVSERVER,
    'RUNNING_MOD_WSGI': RUNNING_MOD_WSGI,
    'RUNNING_MANAGE_PY': RUNNING_MANAGE_PY,
    'ARGV': sys.argv,

    'DEBUG': DEBUG,
    'DEV': DEV,
    'LOCAL_RUN': LOCAL_RUN,
    'LOCAL': LOCAL,
    'DEV_MAKET_MODE': DEV_MAKET_MODE,
    'COMPRESS_ENABLED': COMPRESS_ENABLED,
    'SITE_NAME': SITE_NAME,
    'SITE_TITLE': SITE_TITLE,
    'BEAUTIFY_HTML': BEAUTIFY_HTML,
    'BEAUTIFY_HTML_OPTIONS': BEAUTIFY_HTML_OPTIONS,
    'BLOCKS_FOLDER': BLOCKS_FOLDER,
    'STATIC_ROOT': STATIC_ROOT,
    'BLOCKS_ROOT': BLOCKS_ROOT,
    'STATIC_URL': STATIC_URL,
    'SITE_DESCRIPTION': SITE_DESCRIPTION,
    'SITE_KEYWORDS': SITE_KEYWORDS,
    #  'ITEM_PER_USER_LIMIT': 20,
    #  'SITEMAP_LIMIT': 1000,
    #  'RSS_LIMIT': 100,
    #  'RELATED_LIMIT': 6,
    #  'ITEM_PER_PAGE': 10,
    #  'LOGIN_TO_CONTACT': True,
}
