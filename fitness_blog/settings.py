"""
Django settings for fitness_blog project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variable or generate a random key
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
# Set DEBUG = False for production
# Temporarily set to True to troubleshoot login issues
DEBUG = True  # Change back to False after fixing login issues

# Setări de securitate pentru producție
# Add 'localhost' and '127.0.0.1' for local development
ALLOWED_HOSTS = ['ghidulfit365.ro', 'www.ghidulfit365.ro', 'localhost', '127.0.0.1', '69.62.119.15']

# Add CSRF trusted origins for HTTPS
CSRF_TRUSTED_ORIGINS = [
    "https://ghidulfit365.ro",
    "https://www.ghidulfit365.ro",
    "http://69.62.119.15",
]

# Cookie settings
# DO NOT set cookie domains - this causes login issues with IP addresses
# SESSION_COOKIE_DOMAIN = None
# CSRF_COOKIE_DOMAIN = None

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Setări SSL/HTTPS pentru producție
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    # În modul de dezvoltare, dezactivează setările de securitate stricte
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# Always set the proxy header regardless of DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Application definition

INSTALLED_APPS = [
    # 'jazzmin',  # Comentează sau elimină această linie
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'blog',
    'ckeditor',
]

# Elimină sau comentează setările Jazzmin
# JAZZMIN_SETTINGS = {
#     "site_title": "Fitness Blog Admin",
#     "site_header": "Fitness Blog",
#     "welcome_sign": "Bine ai venit în panoul de administrare",
#     "copyright": "Fitness Blog",
# }

# Jazzmin UI Tweaks removed

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blog.middleware.SitemapContentTypeMiddleware',
]

ROOT_URLCONF = 'fitness_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'fitness_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ghidulfit365',
        'USER': 'ghidulfit365_user',
        'PASSWORD': 'adrianvilea2025',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ro'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/ghidulfit365/staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/ghidulfit365/media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SEO Settings
SITE_ID = 1
SITE_NAME = "GhidulFit365"
SITE_DOMAIN = "ghidulfit365.ro"

# Robots.txt și Sitemap settings
ROBOTS_TXT_PATH = os.path.join(BASE_DIR, 'robots.txt')

# Login and authentication settings
LOGIN_REDIRECT_URL = '/admin/'
LOGIN_URL = '/admin/login/'
LOGOUT_REDIRECT_URL = '/admin/login/'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False  # Set to False for development

# CSRF settings
CSRF_COOKIE_HTTPONLY = False  # Set to False to allow JavaScript access
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = False  # Set to False for development
