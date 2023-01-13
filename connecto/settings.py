"""
Django settings for connecto project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

import cloudinary
import cloudinary.api
import cloudinary.uploader
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['connecto.cleverapps.io', '127.0.0.1', '10.2.194.209']

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'booking.apps.BookingConfig',
]

THIRD_PARTY_APPS = [
    'jazzmin',
    'drf_yasg',
    'rest_framework',
    'corsheaders',
    # 'debug_toolbar',
    'background_task',
    'anymail',
    'cloudinary',
]

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DJANGO_APPS

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:5173',
    'http://localhost:1111',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:5173',
    'http://localhost:1111',
]

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'accept-encoding',
    'x-csrftoken',
    'access-control-allow-origin',
    'content-disposition'
)
CORS_ALLOW_CREDENTIALS = False

CORS_ALLOW_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'booking.middleware.AuthorizedOriginMiddleware'
]

# INTERNAL_IPS = [
#     # ...
#     "127.0.0.1",
#     # ...
# ]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

ROOT_URLCONF = 'connecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'connecto.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': config('DATABASE_DBNAME'),
#         'HOST': 'localhost',
#         'USER': config('DATABASE_USER'),
#         'PASSWORD': config('DATABASE_PASS'),
#     }
# }

# Online DB

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("POSTGRESQL_ADDON_DB"),
        'USER': config("POSTGRESQL_ADDON_USER"),
        'PASSWORD': config("POSTGRESQL_ADDON_PASSWORD"),
        'HOST': config("POSTGRESQL_ADDON_HOST"),
        'PORT': config("POSTGRESQL_ADDON_PORT"),
        'CONN_MAX_AGE': 500,
    }
}

SILENCED_SYSTEM_CHECKS = ['mysql.E001']

JAZZMIN_SETTINGS = {
    "site_title": "Connecto Admin",
    "site_header": "Connecto",
    "site_brand": "Connecto",
    "copyright": "Connecto Transfers Ltd",
    "site_logo": "books/img/connecto.jpg",
    "login_icon": "books/img/connecto.jpg",
    "welcome_sign": "Welcome to Connecto",
    "show_ui_builder": False,

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth.user": "fas fa-users",
        "auth.group": "fas fa-user-cog",
        "background_task.task": "fas fa-clipboard-list",
        "background_task.completedtask": "fas fa-check-double",
        "booking.country": "fas fa-globe",
        "booking.booking": "fas fa-book",
        "booking.place": "fas fa-location-arrow",
        "booking.vehicle": "fas fa-car",
        "booking.placereview": "fas fa-star",
        "booking.vehiclereview": "fas fa-star",
        "booking.equipmenttype": "fas fa-screwdriver",
        "booking.equipmentchoice": "fas fa-fill",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

}

JAZZMIN_UI_TWEAKS = {
    "theme": "minty",
    "body_small_text": True,
    # "dark_mode_theme": "darkly",
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# CLOUDINARY
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET')
)

# STRIPE CONFIG
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
STRIPE_ENDPOINT_SECRET = config('STRIPE_ENDPOINT_SECRET')

BACKGROUND_TASK_RUN_ASYNC = True

EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"

# ANYMAIL = {
#     "SENDINBLUE_API_KEY": config('SENDINBLUE_API_KEY'),
# }

ANYMAIL_SENDINBLUE_API_KEY = config("SENDINBLUE_API_KEY")

ANYMAIL = {
    "IGNORE_UNSUPPORTED_FEATURES": True,
}

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

CSRF_COOKIE_SECURE = True

# SESSION_COOKIE_SECURE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]

STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# For deployment
STATIC_URL_PREFIX = config("STATIC_URL_PREFIX")

STATIC_FILES_PATH = config("STATIC_FILES_PATH")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
