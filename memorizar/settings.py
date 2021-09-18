"""
Django settings for memorizar project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env('.env')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = env('SECRET_KEY')
HOST_NAME = env('HOST_NAME')
ALLOWED_HOSTS = ['*']
STAGE = env('STAGE')
DEBUG = (STAGE == 'local')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django_extensions',
    'import_export',
    'social_django',
    'whitenoise.runserver_nostatic',
    'cloudinary_storage',
    'cloudinary',
    'django_celery_results',

    'memorizar',
    'users',
    'workbooks',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'memorizar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'memorizar/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'libraries': {
                'memorizar': 'memorizar.templatetags.memorizar_extras'
            }
        },
    },
]

WSGI_APPLICATION = 'memorizar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

# Auth0

SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
SOCIAL_AUTH_AUTH0_DOMAIN = env('AUTH0_DOMAIN')
SOCIAL_AUTH_AUTH0_KEY = env('AUTH0_ID')
SOCIAL_AUTH_AUTH0_SECRET = env('AUTH0_SECRET')
SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email',
]
SOCIAL_AUTH_URL_NAMESPACE = "users:social"

AUTHENTICATION_BACKENDS = {
    'lib.backend.Auth0',
    'django.contrib.auth.backends.ModelBackend'
}

LOGIN_URL = '/users/login/auth0'
LOGIN_REDIRECT_URL = '/workbooks'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators


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


SUPERUSER_EMAIL = env('SUPERUSER_EMAIL')
SUPERUSER_PASSWORD = env('SUPERUSER_PASSWORD')


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ja-jp'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'memorizar.storage.WhiteNoiseStaticFilesStorage'

from urllib.parse import urlparse
o = urlparse(env('CLOUDINARY_URL'))
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': o.hostname,
    'API_KEY': o.username,
    'API_SECRET': o.password
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'

# Media files
# https://docs.djangoproject.com/en/3.0/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Email service
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = env('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = env('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Background task
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = env('REDIS_URL')
# Celery Configuration Options
CELERY_TIMEZONE = "Asia/Tokyo"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# 本番環境かどうか
IS_PRODUCTION = (STAGE == 'master')

# heroku
if env('STAGE') != 'local':
    import django_heroku
    django_heroku.settings(locals())