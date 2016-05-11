"""
.. module::  runtests
   :synopsis:  Enable python setup.py test to work

"""

import os
import sys

import django
from django.test.utils import get_runner
from django.conf import settings

DJANGO_SETTINGS_MODULE = 'DJANGO_SETTINGS_MODULE'
os.environ[DJANGO_SETTINGS_MODULE] = os.environ.get(
    DJANGO_SETTINGS_MODULE, 'django_contacts.settings_test')

test_dir = os.path.join(os.path.dirname(__file__), 'contacts')
sys.path.insert(0, test_dir)


def runtests():

    TestRunner = get_runner(settings)

    test_runner = TestRunner(verbosity=1, interactive=True)

    if hasattr(django, 'setup'):
        django.setup()

    failures = test_runner.run_tests([test_dir])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()
