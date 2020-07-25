"""
Django Docker settings for MemberManagement project.
Reads all relevant setting from the environment
"""
from .settings import *

# No Debugging
DEBUG = False

# we want to allow all hosts
ALLOWED_HOSTS = os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "").split(",")

# all our sessions be safe
SECRET_KEY = os.environ.setdefault("DJANGO_SECRET_KEY", "")

DJANGO_INCLUDE_TRACKING = os.environ.setdefault("DJANGO_INCLUDE_TRACKING", "")

# Passwords
DATABASES = {
    'default': {
        'ENGINE': os.environ.setdefault("DJANGO_DB_ENGINE", ""),
        'NAME': os.environ.setdefault("DJANGO_DB_NAME", ""),
        'USER': os.environ.setdefault("DJANGO_DB_USER", ""),
        'PASSWORD': os.environ.setdefault("DJANGO_DB_PASSWORD", ""),
        'HOST': os.environ.setdefault("DJANGO_DB_HOST", ""),
        'PORT': os.environ.setdefault("DJANGO_DB_PORT", ""),
    }
}

# staticfiles
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# add the static file root
STATIC_ROOT = "/var/www/static/"
