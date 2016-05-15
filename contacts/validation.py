"""
.. module::  contacts.validation
   :synopsis:  locations validation module

*contacts* application validation module.

"""
from __future__ import absolute_import

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def contact_validation(contact):
    """Validate Contact name and formatted name.
    """
    if contact.name is None and contact.formatted_name is None:
        raise ValidationError(_("Name and formatted_name are none."))

    if contact.pk is None:
        return

    if (contact.name and
            contact.names.filter(
                id=contact.name.id).exists()):
        raise ValidationError(_("Name is already associated with contact."))

    if (contact.formatted_name and
            contact.formatted_names.filter(
                id=contact.formatted_name.id).exists()):

        msg = "Formatted name is already associated with contact."
        raise ValidationError(_(msg))


def image_validation(image, url):
    """Validate ContactImage association image and url.
    """
    if not (image or url):
        raise ValidationError(_("Image and url are none."))


def contact_formatted_name_validation(association):
    """Validate ContactFormattedName."""
    if association.name == association.contact.formatted_name:
        msg = "Contact has foreign key association to formatted name."
        raise ValidationError(_(msg))


def contact_name_validation(association):
    """Validate ContactName."""
    if association.name == association.contact.name:
        msg = "Contact has foreign key association to name."
        raise ValidationError(_(msg))


def related_contact_validation(association):
    """Validate RelatedConct."""
    if association.from_contact == association.to_contact:
        msg = "Contact cannot be associated to itself."
        raise ValidationError(_(msg))
