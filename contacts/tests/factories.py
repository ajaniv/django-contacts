"""
.. module::  django_core_models.contats.tests.factories
   :synopsis: contats application unit test factories module.

*contats* application unit test factories module.
"""
from __future__ import absolute_import, print_function

import factory.fuzzy

from django_core_utils.tests.factories import (NamedModelFactory,
                                               VersionedModelFactory)

from django_core_models.social_media.tests.factories import (EmailModelFactory,
                                                             GroupModelFactory,
                                                             NameModelFactory,
                                                             FormattedNameModelFactory,
                                                             InstantMessagingModelFactory,
                                                             NicknameModelFactory)
from django_core_models.locations.tests.factories import (
    USAddressModelFactory)
from django_core_models.core.tests.factories import (
    AnnotationModelFactory, CategoryModelFactory)
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
    class Meta(object):
        """Model meta class."""
        model = models.Contact


class ContactAddressModelFactory(ContactsModelFactory):
    """ContactAddress association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory, name=NameModelFactory())
    address = factory.SubFactory(USAddressModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactAddress


class ContactAnnotationModelFactory(ContactsModelFactory):
    """ContactAnnotation association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory, name=NameModelFactory())
    annotation = factory.SubFactory(AnnotationModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactAnnotation


class ContactCategoryModelFactory(ContactsModelFactory):
    """ContactCategory association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory, name=NameModelFactory())
    category = factory.SubFactory(CategoryModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactCategory


class ContactEmailModelFactory(ContactsModelFactory):
    """ContactEmail association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory, name=NameModelFactory())
    email = factory.SubFactory(EmailModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactEmail


class ContactFormattedNameModelFactory(ContactsModelFactory):
    """ContactFormattedName association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory, name=NameModelFactory())
    name = factory.SubFactory(FormattedNameModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactFormattedName


class ContactGroupModelFactory(ContactsModelFactory):
    """ContactGroup association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory, name=NameModelFactory())
    group = factory.SubFactory(GroupModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactGroup


class ContactInstantMessagingModelFactory(ContactsModelFactory):
    """ContactInstantMessaging association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory, name=NameModelFactory())
    instant_messaging = factory.SubFactory(InstantMessagingModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactInstantMessaging


class ContactNameModelFactory(ContactsModelFactory):
    """ContactName association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory, name=NameModelFactory())
    name = factory.SubFactory(NameModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactName


class ContactNicknameModelFactory(ContactsModelFactory):
    """ContactNickname association model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory, name=NameModelFactory())
    name = factory.SubFactory(NicknameModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactNickname
