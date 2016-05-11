"""
.. module::  contacts.validation
   :synopsis:  locations validation module

*contacts* application validation module.

"""
from __future__ import absolute_import

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def name_validation(name, formatted_name):
    """Validate Contact name and formatted name.
    """
    if name is None and formatted_name is None:
        raise ValidationError(_("Name and formatted_name are none."))


def image_validation(image, url):
    """Validate ContactImage association image and url.
    """
    if not (image or url):
        raise ValidationError(_("Image and url are none."))
