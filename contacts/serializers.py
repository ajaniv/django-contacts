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


class ContactAssociationSerializer(ContactsModelSerializer):
    """ContactsModel serializer class."""
    class Meta(ContactsModelSerializer.Meta):
        """Meta class definition."""
        model = models.ContactsModel
        fields = PrioritizedModelSerializer.Meta.fields + (
            "contact",)


class ContactAddressSerializer(ContactAssociationSerializer):
    """ContactAddress model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactAddress
        fields = ContactAssociationSerializer.Meta.fields + (
            "address", "address_type")


class ContactAnnotationSerializer(ContactAssociationSerializer):
    """ContactAnnotation model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactAnnotation
        fields = ContactAssociationSerializer.Meta.fields + (
            "annotation",)


class ContactCategorySerializer(ContactAssociationSerializer):
    """ContactCategory model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactCategory
        fields = ContactAssociationSerializer.Meta.fields + (
            "category",)


class ContactEmailSerializer(ContactAssociationSerializer):
    """ContactEmail model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactEmail
        fields = ContactAssociationSerializer.Meta.fields + (
            "email", "email_type")


class ContactFormattedNameSerializer(ContactAssociationSerializer):
    """ContactFormattedName model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactFormattedName
        fields = ContactAssociationSerializer.Meta.fields + (
            "name",)


class ContactGeographicLocationSerializer(ContactAssociationSerializer):
    """ContactGeographicLocation model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactGeographicLocation
        fields = ContactAssociationSerializer.Meta.fields + (
            "geographic_location", "geographic_location_type")


class ContactGroupSerializer(ContactAssociationSerializer):
    """ContactGroup model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactGroup
        fields = ContactAssociationSerializer.Meta.fields + (
            "group",)


class ContactImageSerializer(ContactAssociationSerializer):
    """ContactImage model serializer class."""

    class Meta(ContactsModelSerializer.Meta):
        """Meta class definition."""
        model = models.ContactImage
        fields = ContactAssociationSerializer.Meta.fields + (
            "image_reference",)


class ContactLogoSerializer(ContactImageSerializer):
    """ContactLogo model serializer class."""

    class Meta(ContactImageSerializer.Meta):
        """Meta class definition."""
        model = models.ContactLogo
        fields = ContactImageSerializer.Meta.fields + (
            "logo_type",)


class ContactPhotoSerializer(ContactImageSerializer):
    """ContactPhoto model serializer class."""

    class Meta(ContactImageSerializer.Meta):
        """Meta class definition."""
        model = models.ContactPhoto
        fields = ContactImageSerializer.Meta.fields + (
            "photo_type",)


class ContactInstantMessagingSerializer(ContactAssociationSerializer):
    """ContactInstantMessaging model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactInstantMessaging
        fields = ContactAssociationSerializer.Meta.fields + (
            "instant_messaging", "instant_messaging_type")


class ContactLanguageSerializer(ContactAssociationSerializer):
    """ContactLanguage model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactLanguage
        fields = ContactAssociationSerializer.Meta.fields + (
            "language", "language_type")


class ContactNameSerializer(ContactAssociationSerializer):
    """ContactName model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactName
        fields = ContactAssociationSerializer.Meta.fields + (
            "name",)


class ContactNicknameSerializer(ContactAssociationSerializer):
    """ContactNickname model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactNickname
        fields = ContactAssociationSerializer.Meta.fields + (
            "name", "nickname_type")


class ContactOrganizationSerializer(ContactAssociationSerializer):
    """ContactOrganization model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactOrganization
        fields = ContactAssociationSerializer.Meta.fields + (
            "organization", "unit")


class ContactPhoneSerializer(ContactAssociationSerializer):
    """ContactPhone model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactPhone
        fields = ContactAssociationSerializer.Meta.fields + (
            "phone", "phone_type")


class ContactRoleSerializer(ContactAssociationSerializer):
    """ContactRole model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactRole
        fields = ContactAssociationSerializer.Meta.fields + (
            "role", "organization")


class ContactTimezoneSerializer(ContactAssociationSerializer):
    """ContactTimezone model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactTimezone
        fields = ContactAssociationSerializer.Meta.fields + (
            "timezone", "timezone_type")


class ContactTitleSerializer(ContactAssociationSerializer):
    """ContactTitle model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactTitle
        fields = ContactAssociationSerializer.Meta.fields + (
            "title", "organization")


class ContactUrlSerializer(ContactAssociationSerializer):
    """ContactUrl model serializer class."""

    class Meta(ContactAssociationSerializer.Meta):
        """Meta class definition."""
        model = models.ContactUrl
        fields = ContactAssociationSerializer.Meta.fields + (
            "url", "url_type")


class RelatedContactSerializer(PrioritizedModelSerializer):
    """ContactUrl model serializer class."""

    class Meta(PrioritizedModelSerializer.Meta):
        """Meta class definition."""
        model = models.RelatedContact
        fields = PrioritizedModelSerializer.Meta.fields + (
            "from_contact", "to_contact", "contact_relationship_type")
