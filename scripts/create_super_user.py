#!/usr/bin/env python
"""
.. module::  create_super_user
   :synopsis:  crate default super user.

create default super user

"""
# @TODO: provide the ability to pass parameters on the command line
# of settings file, user name, email, password
from __future__ import print_function
import os
import sys
import getopt
from django.db.utils import IntegrityError

import django

DJANGO_SETTINGS_MODULE = "DJANGO_SETTINGS_MODULE"
os.environ[DJANGO_SETTINGS_MODULE] = os.environ.get(
    DJANGO_SETTINGS_MODULE, "django_core_models_settings.settings")

_username = 'admin'
_password = _username + '123'
_domain = 'example.com'


def _usage():
    tmpl = '%s -h -u <username> -p <password> -d <domain> -s <settings>'
    print(tmpl % sys.argv[0])


def _args_error(exit_code=1):
    _usage()
    sys.exit(exit_code)

try:
    opts, args = getopt.getopt(sys.argv[1:],
                               "hu:p:d:s:",
                               ["help", "username=", "password=",
                                "domain=", "settings="])
except getopt.GetoptError:
    _args_error()


for opt, arg in opts:
    if opt == "-h":
        _args_error(0)
    elif opt in ("-d", "--domain"):
        _domain = arg
    elif opt in ("-p", "--password"):
        _password = arg
    elif opt in ("-s", "--settings"):
        _settings = arg
        os.environ[DJANGO_SETTINGS_MODULE] = _settings
    elif opt in ("-u", "--username"):
        _username = arg

_email = '%s@%s' % (_username, _domain)


def _create_super_user(username, email, password):
    from django.contrib.auth.models import User
    try:
        User.objects.create_superuser(username=username,
                                      email=email,
                                      password=password)
        print("user '%s' created" % username)
    except IntegrityError:
        print("user '%s' already exists in the database" % username)


if __name__ == "__main__":
    if hasattr(django, 'setup'):
        django.setup()
    _create_super_user(_username, _email, _password)
