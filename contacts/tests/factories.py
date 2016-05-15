"""
.. module::  django_core_models.contats.tests.factories
   :synopsis: contats application unit test factories module.

*contats* application unit test factories module.
"""
from __future__ import absolute_import, print_function

import factory

from django_core_models.core.tests.factories import (
    AnnotationModelFactory, CategoryModelFactory)
from django_core_models.images.tests.factories import (
    ImageReferenceModelFactory)
from django_core_models.locations.tests.factories import (
    GeographicLocationModelFactory, LanguageModelFactory,
    TimezoneModelFactory, USAddressModelFactory)
from django_core_models.organizations.tests.factories import (
    OrganizationModelFactory, RoleModelFactory,
    TitleModelFactory)
from django_core_models.social_media.tests.factories import (
    EmailModelFactory, FormattedNameModelFactory,
    GroupModelFactory, InstantMessagingModelFactory,
    NameModelFactory, NicknameModelFactory,
    PhoneModelFactory, UrlModelFactory)
from django_core_utils.tests.factories import (
    NamedModelFactory, VersionedModelFactory, UserFactory)

from .. import models


class ContactTypeModelFactory(NamedModelFactory):
    """ContactType model factory class.
    """
    name = "Personal"

    class Meta(object):
        """Model meta class."""
        model = models.ContactType


class ContactRelationshipTypeModelFactory(NamedModelFactory):
    """ContactRelationshipType model factory class.
    """
    name = "Colleague"

    class Meta(object):
        """Model meta class."""
        model = models.ContactRelationshipType


class ContactsModelFactory(VersionedModelFactory):
    """Contact association model factory class."""
    class Meta(object):
        """Model meta class."""
        abstract = True
        model = models.ContactsModel


class ContactModelFactory(ContactsModelFactory):
    """Contact model factory class.
    """
    name = factory.SubFactory(NameModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.Contact


class ContactAddressModelFactory(ContactsModelFactory):
    """ContactAddress association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    address = factory.SubFactory(USAddressModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactAddress


class ContactAnnotationModelFactory(ContactsModelFactory):
    """ContactAnnotation association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    annotation = factory.SubFactory(AnnotationModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactAnnotation


class ContactCategoryModelFactory(ContactsModelFactory):
    """ContactCategory association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    category = factory.SubFactory(CategoryModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactCategory


class ContactEmailModelFactory(ContactsModelFactory):
    """ContactEmail association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    email = factory.SubFactory(EmailModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactEmail


class ContactFormattedNameModelFactory(ContactsModelFactory):
    """ContactFormattedName association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    name = factory.SubFactory(FormattedNameModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactFormattedName


class ContactGeographicLocationModelFactory(ContactsModelFactory):
    """ContactGroup association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    geographic_location = factory.SubFactory(GeographicLocationModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactGeographicLocation


class ContactGroupModelFactory(ContactsModelFactory):
    """ContactGroup association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    group = factory.SubFactory(GroupModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactGroup


class ContactInstantMessagingModelFactory(ContactsModelFactory):
    """ContactInstantMessaging association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    instant_messaging = factory.SubFactory(InstantMessagingModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactInstantMessaging


class ContactLanguageModelFactory(ContactsModelFactory):
    """ContactLanguage association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    language = factory.SubFactory(LanguageModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactLanguage


class ContactLogoModelFactory(ContactsModelFactory):
    """ContactLogo association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    image_reference = factory.SubFactory(ImageReferenceModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactLogo


class ContactNameModelFactory(ContactsModelFactory):
    """ContactName association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    name = factory.SubFactory(NameModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactName


class ContactNicknameModelFactory(ContactsModelFactory):
    """ContactNickname association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    name = factory.SubFactory(NicknameModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactNickname


class ContactOrganizationModelFactory(ContactsModelFactory):
    """ContactOrganization association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    organization = factory.SubFactory(OrganizationModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactOrganization


class ContactPhoneModelFactory(ContactsModelFactory):
    """ContactPhone association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    phone = factory.SubFactory(PhoneModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactPhone


class ContactPhotoModelFactory(ContactsModelFactory):
    """ContactPhoto association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    image_reference = factory.SubFactory(ImageReferenceModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactPhoto


class RelatedContactModelFactory(ContactsModelFactory):
    """RelatedContact association model factory class.
    """
    from_contact = factory.SubFactory(ContactModelFactory)
    to_contact = factory.SubFactory(ContactModelFactory)
    contact_relationship_type = factory.SubFactory(
        ContactRelationshipTypeModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.RelatedContact


class ContactRoleModelFactory(ContactsModelFactory):
    """ContactRole association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    role = factory.SubFactory(RoleModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactRole


class ContactTimezoneModelFactory(ContactsModelFactory):
    """ContactTimezone association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    timezone = factory.SubFactory(TimezoneModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactTimezone


class ContactTitleModelFactory(ContactsModelFactory):
    """ContactTitle association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    title = factory.SubFactory(TitleModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactTitle


class ContactUrlModelFactory(ContactsModelFactory):
    """ContactUrl association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory)
    url = factory.SubFactory(UrlModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactUrl


class UserProfileModelFactory(factory.DjangoModelFactory):
    """UserProfile  model factory class.
    """
    user = factory.SubFactory(UserFactory)

    class Meta(object):
        """Model meta class."""
        model = models.UserProfile
