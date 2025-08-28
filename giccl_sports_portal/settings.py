import os
from pathlib import Path
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-8cvb3o27fy+icj*4oeph1*vp2*+78*_c3c!f=brp!!+dl+j7pn')

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'pwa',
    'widget_tweaks',
    'Sports_Users',
    'sports_base',
    'static_pages',
]

SITE_ID = 1
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'giccl_sports_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'giccl_sports_portal.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Keep in root
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'Sports_Users.CustomUser'
AUTHENTICATION_BACKENDS = [
    'Sports_Users.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

PWA_APP_NAME = 'GIGCCL Sports Portal'
PWA_APP_DESCRIPTION = "This is the Officially Sports Website for Islamia Government Graduate College, Civil Lines"
PWA_APP_THEME_COLOR = '#ffe1c0'
PWA_APP_BACKGROUND_COLOR = '#ffe1c0'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {'src': '/static/images/my_app_icon_160x160.png', 'sizes': '160x160'},
    {'src': '/static/images/my_app_icon_512x512.png', 'sizes': '512x512', 'type': 'image/png'},
    {'src': '/static/images/my_app_icon_144x144.png', 'sizes': '144x144', 'type': 'image/png'},
    {'src': '/static/images/my_app_icon_16x16.png', 'sizes': '16x16', 'type': 'image/png'},
    {'src': '/static/images/my_app_icon_32x32.png', 'sizes': '32x32', 'type': 'image/png'},
    {'src': '/static/images/my_app_icon_96x96.png', 'sizes': '96x96', 'type': 'image/png'},
    {'src': '/static/images/my_app_icon_512x512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
]
PWA_APP_ICONS_APPLE = [
    {'src': '/static/images/my_app_icon_160x160.png', 'sizes': '160x160'},
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    },
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
PWA_APP_SHORTCUTS = [
    {
        'name': 'GIGCCL',
        'url': '/',
        'description': 'Home page of GIGCCL Sports Portal',
        'icons': [{'src': '/static/images/my_app_icon_96x96.png', 'sizes': '96x96', 'type': 'image/png'}],
    },
]
PWA_APP_SCREENSHOTS = [
    {'src': '/static/images/screenshots/desktop_home.png', 'sizes': '1280x720', 'type': 'image/png', 'form_factor': 'wide'},
    {'src': '/static/images/screenshots/mobile_home.png', 'sizes': '750x1334', 'type': 'image/png', 'form_factor': 'narrow'},
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "gigccl.sspe@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'dbro evez isbd bbzo')
DEFAULT_FROM_EMAIL = "gigccl.sspe@gmail.com"
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = "[Sports Portal] "
PROTOCOL = os.environ.get('PROTOCOL', 'https')
DOMAIN = os.environ.get('DOMAIN', '127.0.0.1:8000')
PASSWORD_RESET_TIMEOUT = 3600

POPPLER_PATH = r"C:\poppler\Library\bin"