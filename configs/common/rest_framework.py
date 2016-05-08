"""
.. module::  configs.common.rest_framework
   :synopsis:  Django rest framework settings file.

Django rest framework settings file.

"""
API_DEFAULT_VERSION = '1.0'
API_ALLOWED_VERSIONS = (API_DEFAULT_VERSION,)
REST_FRAMEWORK = {
    "FORMAT_SUFFIX_KWARG": "content_format",
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # @TODO: review permission settings
    'DEFAULT_PERMISSION_CLASSES': [
       'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_VERSIONING_CLASS':
        'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': API_DEFAULT_VERSION,
    'ALLOWED_VERSIONS': (API_ALLOWED_VERSIONS,),
    # @TODO: review page size settings
    'PAGE_SIZE': 10,
    # @TODO: review throttling settings
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',
        'user': '100/minute'
    }
}
