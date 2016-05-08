"""
.. module::  configs.common.mysql
   :synopsis:  Django mysql settings file.

Django mysql settings file.

"""
from __future__ import unicode_literals
import os
ENV_MYSQL_NAME = 'MYSQL_NAME'
ENV_MYSQL_USER = 'MYSQL_USER'
ENV_MYSQL_PASSWORD = 'MYSQL_PASSWORD'
ENV_MYSQL_HOST = 'MYSQL_HOST'
ENV_MYSQL_PORT = 'MYSQL_PORT'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ[ENV_MYSQL_NAME],
        'USER': os.environ[ENV_MYSQL_USER],
        'PASSWORD': os.environ[ENV_MYSQL_PASSWORD],
        'HOST': os.environ[ENV_MYSQL_HOST],
        'PORT': os.environ[ENV_MYSQL_PORT],
    }
}
