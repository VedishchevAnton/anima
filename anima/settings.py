import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-anima-change-me-in-production'

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    # 'django.contrib.sessions',
    # 'django.contrib.contenttypes',
    'landing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'anima.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR, 'landing', 'jtemplates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'anima.jinja.env_class.JinjaEnvironment',
            'extensions': [
                'jinja2.ext.i18n',
                'jinja2.ext.loopcontrols',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'anima.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Google reCAPTCHA v2
GOOGLE_RECAPTCHA_SITE_KEY = '6LehOaAUAAAAANp_PYW4BgXVZNiP3VcQ3oVH8y52'
GOOGLE_RECAPTCHA_SECRET_KEY = '6LehOaAUAAAAABWClXRh45yBegULSytqthRQLruR'

# Email
# Для Mail.ru: EMAIL_HOST = 'smtp.mail.ru', EMAIL_PORT = 465, EMAIL_USE_TLS = False, EMAIL_USE_SSL = True
# Для Yandex:  EMAIL_HOST = 'smtp.yandex.ru', EMAIL_PORT = 465, EMAIL_USE_TLS = False, EMAIL_USE_SSL = True
# Для Gmail:   EMAIL_HOST = 'smtp.gmail.com', EMAIL_PORT = 587, EMAIL_USE_TLS = True, EMAIL_USE_SSL = False
# EMAIL_HOST_USER — ваш email (например anima.market@mail.ru)
# EMAIL_HOST_PASSWORD — пароль приложения (не пароль от почты!)
#   Mail.ru: Настройки → Безопасность → Пароли для внешних приложений
#   Yandex:  id.yandex.ru → Безопасность → Пароли приложений
#   Gmail:   myaccount.google.com → Безопасность → Пароли приложений
# Рекомендуется указывать в anima/local.py, чтобы не пушить пароли в git
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
FEEDBACK_EMAIL = 'anima.market@mail.ru'
DEFAULT_FROM_EMAIL = 'anima.market@mail.ru'

# Local settings override
try:
    from .local import *
except ImportError:
    pass
