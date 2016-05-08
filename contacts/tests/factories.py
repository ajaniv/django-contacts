"""
.. module::  django_core_models.contats.tests.factories
   :synopsis: contats application unit test factories module.

*contats* application unit test factories module.
"""
from __future__ import absolute_import, print_function

import factory.fuzzy

from django_core_utils.tests.factories import (NamedModelFactory,
                                               VersionedModelFactory)

from django_core_models.social_media.tests.factories import NameModelFactory
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


class ContactModelFactory(VersionedModelFactory):
    """Contact model factory class.
    """
    class Meta(object):
        """Model meta class."""
        model = models.Contact


class ContactNameModelFactory(VersionedModelFactory):
    """ContactName model factory class.
    """
    contact = factory.SubFactory(ContactModelFactory, name=NameModelFactory())
    name = factory.SubFactory(NameModelFactory)

    class Meta(object):
        """Model meta class."""
        model = models.ContactName
