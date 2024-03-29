"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config
import sys
import logging


class DefaultFilter(logging.Filter):
    def filter(self, record):
        # Add level so generic tools like Cloud Logs can understand our log levels
        record.level = record.levelname
        return True


class SimpleLogFormatter(logging.Formatter):
    simple_fmt = "[%(asctime)s] %(levelname)s %(name)s %(message)s"

    def __init__(self):
        super(self.__class__, self).__init__(fmt=self.__class__.simple_fmt)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k^^#3vataz^a8^rswh5+qf3bjn60h^#$zd3bfm*^6ro9#02@b7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'apps.FOMS',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'crispy_forms',

]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'apps/FOMS/templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "db",
        "PORT": 5432,
        "PASSWORD": "postgres",
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = False
DATE_FORMAT = 'd-m-Y'
DATETIME_FORMAT = 'd-m-Y H:i'

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'apps/FOMS/static')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/FOMS/'

REDIS_HOST = config("REDIS_HOST", default="redis")
REDIS_PORT = config("REDIS_PORT", default="6379")

REDIS_URL = "redis://{host}:{port}".format(
    host=REDIS_HOST,
    port=REDIS_PORT,
)

RABBIT_URL = config("RABBIT_URL", default="amqp://guest:guest@rabbit:5672/")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"default_filter": {"()": DefaultFilter}},
    "formatters": {"configured": {"()": SimpleLogFormatter}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "configured",
            "filters": ["default_filter"],
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "apps.pricing": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django": {"level": "INFO", "handlers": ["console"]},
        "root": {"level": "INFO", "handlers": ["console"]},
    },
}

EMAIL_USER = config("EMAIL_USER", default="")
EMAIL_PASSWORD = config("EMAIL_PASSWORD", default="")
