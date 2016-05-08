"""
.. module::  django_core_models.settings_test
   :synopsis:  django_core_models test settings module.

django_core_models test settings module.
"""
from .settings import *  # @UnusedWildImport

# Uncomment FORCE_DEBUG to see db statements;
# It also requires change to django.db log level to debug
# FORCE_DEBUG = True
# disable throttling during unit tests
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = tuple()
