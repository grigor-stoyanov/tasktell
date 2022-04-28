import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-rlvnw&h5cs=zx5qwtw#nu%)^a&apsmii=oh*9*c58)+xd@y$6k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',
    '0.0.0.0',
    'tasktell.herokuapp.com',
]

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
TASKTELL_APPS = [
    'tasktell.main',
    'tasktell.auth_app',
    'tasktell.chat'
]
OTHER_APPS = [
    'cloudinary'
]
INSTALLED_APPS = DJANGO_APPS + TASKTELL_APPS + OTHER_APPS

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tasktell.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'tasktell.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'tasktell_db',
#         'USER': 'postgres',
#         'PASSWORD': '1123QwER',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd7i0s6bicf5g9i',
        'USER': 'hnjoocwzadxmdd',
        'PASSWORD': '2eb1d739da4154ad197810a9df0e2043957320541a7b32e25fe9330037c5fc8a',
        'HOST': 'ec2-99-80-170-190.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
BASE_DIR2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR2, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR2, 'static'),)
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_URL = 'media/'

AUTH_USER_MODEL = "auth_app.TasktellUser"
cloudinary.config(
    cloud_name="hagtn3ld8",
    api_key="134141593643571",
    api_secret="ftAP5HOwIJlAvxuArA4wptPu6xo"
)
EMAIL_BACKEND = 'django.core.mail.backends.s    mtp.EmailBackend'

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'grigorg25@gmail.com'
EMAIL_HOST_PASSWORD = 'jivotno2'
