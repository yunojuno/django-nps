# -*- coding: utf-8 -*-
DEBUG = True

DATABASES= {
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

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

SECRET_KEY = "NPS"

ROOT_URLCONF = 'urls'

APPEND_SLASH = True

STATIC_URL = '/static/'

assert DEBUG is True, "This project is only intended to be used for testing."
