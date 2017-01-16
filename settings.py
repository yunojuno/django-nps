# -*- coding: utf-8 -*-
from distutils.version import StrictVersion

import django

DJANGO_VERSION = StrictVersion(django.get_version())

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'nps.db',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'net_promoter_score',
)

_MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

if DJANGO_VERSION < StrictVersion('1.10.0'):
    MIDDLEWARE_CLASSES = _MIDDLEWARE_CLASSES
else:
    MIDDLEWARE = _MIDDLEWARE_CLASSES

SECRET_KEY = "NPS"

ROOT_URLCONF = 'urls'

APPEND_SLASH = True

STATIC_URL = '/static/'

assert DEBUG is True, "This project is only intended to be used for testing."
