"""
.. module::  contacts.forms
   :synopsis:  Django contacts application forms module.

Django contacts application forms  module.

"""
from __future__ import absolute_import
from django_core_utils import forms
from python_core_utils.core import dict_merge

from . import models
from . import text


class ContactAdminForm(forms.PrioritizedModelAdminForm):
    """Contact model admin form  class.
    """
    class Meta(forms.PrioritizedModelAdminForm.Meta):
        """Form meta class."""
        model = models.Contact
        labels = dict_merge(
            forms.PrioritizedModelAdminForm.Meta.labels,
            text.contact_labels)

        help_texts = dict_merge(
            forms.PrioritizedModelAdminForm.Meta.help_texts,
            text.contact_help_texts)


class ContactTypeAdminForm(forms.NamedModelAdminForm):
    """ContactType  model admin form class.
    """
    class Meta(forms.NamedModelAdminForm.Meta):
        """Form meta class."""
        model = models.ContactType


class ContactRelationshipTypeAdminForm(forms.NamedModelAdminForm):
    """ContactRelationshipType  model admin form class.
    """
    class Meta(forms.NamedModelAdminForm.Meta):
        """Form meta class."""
        model = models.ContactRelationshipType


class ContactAssociationAdminForm(forms.PrioritizedModelAdminForm):
    """Base class for contact association model form.
    """
    class Meta(forms.PrioritizedModelAdminForm.Meta):
        """Form meta class."""
        models.ContactAssociation
        fields = '__all__'


class ContactAddressAdminForm(ContactAssociationAdminForm):
    """ContactAddress  model admin form class.
    """
    class Meta(ContactAssociationAdminForm.Meta):
        """Form meta class."""
        model = models.ContactAddress
        labels = dict_merge(
            ContactAssociationAdminForm.Meta.labels,
            text.contact_address_labels)

        help_texts = dict_merge(
            ContactAssociationAdminForm.Meta.help_texts,
            text.contact_address_help_texts)


class ContactAnnotationAdminForm(ContactAssociationAdminForm):
    """ContactAnnotation  model admin form class.
    """
    class Meta(ContactAssociationAdminForm.Meta):
        """Form meta class."""
        model = models.ContactAnnotation
        labels = dict_merge(
            ContactAssociationAdminForm.Meta.labels,
            text.contact_annotation_labels)

        help_texts = dict_merge(
            ContactAssociationAdminForm.Meta.help_texts,
            text.contact_annotation_help_texts)
