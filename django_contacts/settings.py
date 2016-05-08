"""
Django settings for ad_server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from configs.common.root import (CURRENT_ENV, DEV_ENV,
                                 LOCAL_ENV, STAGING_ENV, PROD_ENV)


if CURRENT_ENV in (DEV_ENV, LOCAL_ENV):
    from configs.dev import *  # @UnusedWildImport
elif CURRENT_ENV == STAGING_ENV:
    # @TODO define staging env
    pass
elif CURRENT_ENV == PROD_ENV:
    # @TODO define prod env
    pass
else:
    raise ValueError('Invalid environment %s' % CURRENT_ENV)

try:
    from .settings_local import *
except ImportError:
    pass
