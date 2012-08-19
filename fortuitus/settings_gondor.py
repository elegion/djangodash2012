import os
import urlparse

from .settings import *  # NOQA


DEBUG = False
TEMPLATE_DEBUG = DEBUG


if 'GONDOR_DATABASE_URL' in os.environ:
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['GONDOR_DATABASE_URL'])
    DATABASES = {
        'default': {
            'ENGINE': {
                'postgres': 'django.db.backends.postgresql_psycopg2'
            }[url.scheme],
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port
        }
    }

SITE_ID = 1

if 'GONDOR_DATA_DIR' in os.environ:
    MEDIA_ROOT = os.path.join(os.environ['GONDOR_DATA_DIR'],
                              'site_media', 'media')
    STATIC_ROOT = os.path.join(os.environ['GONDOR_DATA_DIR'],
                               'site_media', 'static')

MEDIA_URL = '/site_media/media/'
STATIC_URL = '/site_media/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

FILE_UPLOAD_PERMISSIONS = 0640

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'propagate': True,
        },
    }
}

COMPRESS_ENABLED = True
