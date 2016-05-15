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
    """ContactType model admin form class.
    """
    class Meta(forms.NamedModelAdminForm.Meta):
        """Form meta class."""
        model = models.ContactType


class ContactRelationshipTypeAdminForm(forms.NamedModelAdminForm):
    """ContactRelationshipType model admin form class.
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
    """ContactAddress model admin form class.
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
    """ContactAnnotation model admin form class.
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


class ContactCategoryAdminForm(ContactAssociationAdminForm):
    """ContactCategory model admin form class.
    """
    class Meta(ContactAssociationAdminForm.Meta):
        """Form meta class."""
        model = models.ContactCategory
        labels = dict_merge(
            ContactAssociationAdminForm.Meta.labels,
            text.contact_category_labels)

        help_texts = dict_merge(
            ContactAssociationAdminForm.Meta.help_texts,
            text.contact_category_help_texts)


class ContactEmailAdminForm(ContactAssociationAdminForm):
    """ContactEmail model admin form class.
    """
    class Meta(ContactAssociationAdminForm.Meta):
        """Form meta class."""
        model = models.ContactEmail
        labels = dict_merge(
            ContactAssociationAdminForm.Meta.labels,
            text.contact_email_labels)

        help_texts = dict_merge(
            ContactAssociationAdminForm.Meta.help_texts,
            text.contact_email_help_texts)


class ContactFormattedNameAdminForm(ContactAssociationAdminForm):
    """ContactFormattedName model admin form class.
    """
    class Meta(ContactAssociationAdminForm.Meta):
        """Form meta class."""
        model = models.ContactFormattedName
        labels = dict_merge(
            ContactAssociationAdminForm.Meta.labels,
            text.contact_formatted_name_labels)

        help_texts = dict_merge(
            ContactAssociationAdminForm.Meta.help_texts,
            text.contact_formatted_name_help_texts)


class ContactGeographicLocationAdminForm(ContactAssociationAdminForm):
    """ContactGeographicLocation model admin form class.
    """
    class Meta(ContactAssociationAdminForm.Meta):
        """Form meta class."""
        model = models.ContactGeographicLocation
        labels = dict_merge(
            ContactAssociationAdminForm.Meta.labels,
            text.contact_geographic_location_labels)

        help_texts = dict_merge(
            ContactAssociationAdminForm.Meta.help_texts,
            text.contact_geographic_location_help_texts)


class ContactGroupAdminForm(ContactAssociationAdminForm):
    """ContactGroup model admin form class.
    """
    class Meta(ContactAssociationAdminForm.Meta):
        """Form meta class."""
        model = models.ContactGroup
        labels = dict_merge(
            ContactAssociationAdminForm.Meta.labels,
            text.contact_group_labels)

        help_texts = dict_merge(
            ContactAssociationAdminForm.Meta.help_texts,
            text.contact_group_help_texts)


class ContactInstantMessagingAdminForm(ContactAssociationAdminForm):
    """ContactInstantMessaging model admin form class.
    """
    class Meta(ContactAssociationAdminForm.Meta):
        """Form meta class."""
        model = models.ContactInstantMessaging
        labels = dict_merge(
            ContactAssociationAdminForm.Meta.labels,
            text.contact_instant_messaging_labels)

        help_texts = dict_merge(
            ContactAssociationAdminForm.Meta.help_texts,
            text.contact_instant_messaging_help_texts)


class ContactLanguageAdminForm(ContactAssociationAdminForm):
    """ContactLanguage model admin form class.
    """
    class Meta(ContactAssociationAdminForm.Meta):
        """Form meta class."""
        model = models.ContactLanguage
        labels = dict_merge(
            ContactAssociationAdminForm.Meta.labels,
            text.contact_language_labels)

        help_texts = dict_merge(
            ContactAssociationAdminForm.Meta.help_texts,
            text.contact_language_help_texts)


class ContactLogoAdminForm(ContactAssociationAdminForm):
    """ContactLogo model admin form class.
    """
    class Meta(ContactAssociationAdminForm.Meta):
        """Form meta class."""
        model = models.ContactLogo
        labels = dict_merge(
            ContactAssociationAdminForm.Meta.labels,
            text.contact_logo_labels)

        help_texts = dict_merge(
            ContactAssociationAdminForm.Meta.help_texts,
            text.contact_logo_help_texts)


class ContactNameAdminForm(ContactAssociationAdminForm):
    """ContactName model admin form class.
    """
    class Meta(ContactAssociationAdminForm.Meta):
        """Form meta class."""
        model = models.ContactName
        labels = dict_merge(
            ContactAssociationAdminForm.Meta.labels,
            text.contact_name_labels)

        help_texts = dict_merge(
            ContactAssociationAdminForm.Meta.help_texts,
            text.contact_name_help_texts)
