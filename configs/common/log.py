"""
.. module::  configs.common.log
   :synopsis:  Django log settings file.

Django log settings file.

"""
import os
from .root import CURRENT_ENV, LOCAL_ENV, DEV_ENV, LOG_DIR
from python_core_utils.core import mkdir


LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_ERROR = 'ERROR'
LOG_LEVEL_DEBUG = 'DEBUG'


LOG_LEVEL = (LOG_LEVEL_DEBUG
             if CURRENT_ENV == DEV_ENV or CURRENT_ENV == LOCAL_ENV
             else LOG_LEVEL_INFO)


mkdir(LOG_DIR)

_verbose_format = ('%(levelname)s %(asctime)s' +
                   ' %(module)s %(process)d' +
                   ' %(thread)d %(message)s')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': _verbose_format
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'null': {
            'level': LOG_LEVEL_DEBUG,
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': LOG_LEVEL_DEBUG,
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'log_file': {
            'level': LOG_LEVEL_DEBUG,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'maxBytes': 16777216,  # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': LOG_LEVEL_ERROR,
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        }
    },
    'loggers': {
        'django.db': {
            'handlers': ['console', 'log_file'],
            'level': LOG_LEVEL_INFO,
            'propagate': True
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'django_core_models': {
            'handlers': ['log_file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'django_core_utils': {
            'handlers': ['log_file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'python_core_utils': {
            'handlers': ['log_file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True
        }
    }
}
