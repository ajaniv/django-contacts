"""
.. module::  configs.common.permissions
   :synopsis:  Django permissions settings file.

Django permissions settings file.

"""
from __future__ import unicode_literals

# custom authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
]
USE_OBJECT_PERMISSIONS = True
ANONYMOUS_USER_NAME = "AnonymousUser"
