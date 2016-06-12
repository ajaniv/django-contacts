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
        fields = PrioritizedModelSerializer.Meta.fields + (
            "name",)


class ContactSerializer(ContactsModelSerializer):
    """Contact model serializer class."""

    class Meta(ContactsModelSerializer.Meta):
        """Meta class definition."""
        model = models.Contact
        fields = ContactsModelSerializer.Meta.fields + (
            "formatted_name", "name", "anniversary",
            "birth_date", "contact_type", "gender")
