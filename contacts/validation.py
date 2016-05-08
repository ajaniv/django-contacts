"""
.. module::  contacts.validation
   :synopsis:  locations validation module

*contacts* application validation module.

"""
from __future__ import absolute_import
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


def name_validation(name, formatted_name):
    """Validate name and formatted name.
    """
    if name is None and formatted_name is None:
        raise ValidationError(_("Name and formatted_name are none."))
