"""
.. module::  config.dev
   :synopsis:  Django dev environment settings file.

Django  dev environment settings file.

"""
import os
from configs.common.root import *  # @UnusedWildImport
from configs.common.django import *  # @UnusedWildImport
from configs.common.log import *  # @UnusedWildImport
from configs.common.database import *  # @UnusedWildImport
from configs.common.rest_framework import *  # @UnusedWildImport

# @TODO: revisit usage of django_extensions only in dev
#  and not in the context of tox testing
ENV_TOX_CONTEXT = 'TOX_CONTEXT'
if not os.getenv(ENV_TOX_CONTEXT, False):
    INSTALLED_APPS += ["django_extensions"]
