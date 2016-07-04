"""
..  module:: contacts.serializers
    :synopsis: contacts application serializers module.

*contacts*  application serializers module.
"""
from __future__ import absolute_import

from django_core_utils.serializers import (NamedModelSerializer,
                                           PrioritizedModelSerializer)

from . import models


class ContactRelationshipTypeSerializer(NamedModelSerializer):
    """ContactRelationshipType model serializer class."""

    class Meta(NamedModelSerializer.Meta):
        """Meta class definition."""
        model = models.ContactRelationshipType


class ContactTypeSerializer(NamedModelSerializer):
    """ContactType model serializer class."""

    class Meta(NamedModelSerializer.Meta):
        """Meta class definition."""
        model = models.ContactType


class ContactsModelSerializer(PrioritizedModelSerializer):
    """ContactsModel serializer class."""
    class Meta(PrioritizedModelSerializer.Meta):
        """Meta class definition."""
        model = models.ContactsModel
        fields = PrioritizedModelSerializer.Meta.fields


class ContactSerializer(ContactsModelSerializer):
    """Contact model serializer class."""

    class Meta(ContactsModelSerializer.Meta):
        """Meta class definition."""
        model = models.Contact
        fields = ContactsModelSerializer.Meta.fields + (
            "formatted_name", "name", "anniversary",
            "birth_date", "contact_type", "gender")


class ContactAddressSerializer(ContactsModelSerializer):
    """ContactAddress model serializer class."""

    class Meta(ContactsModelSerializer.Meta):
        """Meta class definition."""
        model = models.ContactAddress
        fields = ContactsModelSerializer.Meta.fields + (
            "contact", "address", "address_type")


class ContactAnnotationSerializer(ContactsModelSerializer):
    """ContactAnnotation model serializer class."""

    class Meta(ContactsModelSerializer.Meta):
        """Meta class definition."""
        model = models.ContactAnnotation
        fields = ContactsModelSerializer.Meta.fields + (
            "contact", "annotation")


class ContactCategorySerializer(ContactsModelSerializer):
    """ContactCategory model serializer class."""

    class Meta(ContactsModelSerializer.Meta):
        """Meta class definition."""
        model = models.ContactCategory
        fields = ContactsModelSerializer.Meta.fields + (
            "contact", "category")


class ContactEmailSerializer(ContactsModelSerializer):
    """ContactEmail model serializer class."""

    class Meta(ContactsModelSerializer.Meta):
        """Meta class definition."""
        model = models.ContactEmail
        fields = ContactsModelSerializer.Meta.fields + (
            "contact", "email", "email_type")


class ContactFormattedNameSerializer(ContactsModelSerializer):
    """ContactFormattedName model serializer class."""

    class Meta(ContactsModelSerializer.Meta):
        """Meta class definition."""
        model = models.ContactFormattedName
        fields = ContactsModelSerializer.Meta.fields + (
            "contact", "name")


class ContactGeographicLocationSerializer(ContactsModelSerializer):
    """ContactGeographicLocation model serializer class."""

    class Meta(ContactsModelSerializer.Meta):
        """Meta class definition."""
        model = models.ContactGeographicLocation
        fields = ContactsModelSerializer.Meta.fields + (
            "contact", "geographic_location", "geographic_location_type")
