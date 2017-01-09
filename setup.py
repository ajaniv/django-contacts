"""
.. module::  setup
   :synopsis: A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

_git_url_root = 'git+ssh://git@github.com/ajaniv/'
setup(
    name='django-contacts',
    version='0.2.0',
    include_package_data=True,
    license='BSD License',  # example license
    description='Django contacts application',
    long_description=README,
    url='http://www.ondalear.com/',
    author='Amnon Janiv',
    author_email='amnon.janiv@ondalear.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'python-core-utils',
        'django-core-utils',
        'django-core-models',
        'Django>=1.9.0'
    ],
    dependency_links=[
        _git_url_root + 'python-core-utils@v0.2.0#egg=python-core-utils',
        _git_url_root + 'django-core-utils@v0.2.0#egg=django-core-utils',
        _git_url_root + 'django-core-models@v0.2.0#egg=django-core-models'
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    test_suite='runtests.runtests',
)
