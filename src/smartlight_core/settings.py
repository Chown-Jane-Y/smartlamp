import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jt8p_q65i9$)n965j%#4ybo2_ri3^@hl=l5#qvdhzvdq@$1zp)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '192.168.8.136']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
    'manage_lamps',
    'manage_hubs',
    'manage_groups',
    'manage_users'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',


)

ROOT_URLCONF = 'smartlight_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'smartlight_core.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
      # 'ENGINE': 'django.db.backends.mysql',
      # 'NAME': "conspace-core",

      # This is a development configuration
      # 'USER': 'root',
      # 'PASSWORD': 'de045e887d130aaf1054',
      # 'HOST': '192.10.11.60',

      # This is a test configuration
      #'USER': 'root',
      #'PASSWORD': 'packet',
      #'HOST': '127.0.0.1',
      #'PORT': '3306',
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'manage_users.Accounts'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'USE_SESSION_AUTH': True,
    'JSON_EDITOR': False,
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
}

# cross site
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '*'
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
    'x-token',
    'access-control-allow-origin'
)

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3000),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'conspace',
    'JWT_ALLOW_REFRESH': True
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.error_back.custom_exception.custom_exception_handler',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}



#  A logging configuration argument
'''
import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filename = os.path.join(BASE_DIR, 'conspace')
suffix = '.log'

#level = INFO
#hdlr = TimedRotatingFileHandler(filename,"midnight",1,5)
#fmt = Formatter(format)
#hdlr.setFormatter(fmt)
#root.addHandler(hdlr)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'handlers': {
        'django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': filename + '.django' + suffix,
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },

    'loggers': {
        'django.request': {
            'handlers': ["console"],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['django', "console"],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}'''
