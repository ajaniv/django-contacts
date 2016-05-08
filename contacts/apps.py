"""
.. module::  django_contacts.apps
   :synopsis:  Django contacts application configuration  module.

Django demographics application configuration  module.

"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ContactsConfig(AppConfig):
    """Django's  contacts application configuration class."""
    name = __package__
    verbose_name = _("Contacts")
