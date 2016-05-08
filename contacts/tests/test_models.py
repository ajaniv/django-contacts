"""
.. module::  contacts.tests.test_models
   :synopsis: contacts application models unit test module.

*contacts* application models unit test module.
"""
from __future__ import absolute_import, print_function

from django.utils import timezone
from django_core_utils.tests.test_utils import (NamedModelTestCase,
                                                VersionedModelTestCase)
from django_core_models.social_media.tests.factories import (
    NameModelFactory, FormattedNameModelFactory)
from django_core_models.demographics.tests.factories import (
    GenderModelFactory)
from django_core_models.locations.tests.factories import (
    USAddressModelFactory)
from . import factories
from .. import models


class ContactTypeTestCase(NamedModelTestCase):
    """ContactType model unit test class.
    """
    def test_contact_type_crud(self):
        self.verify_named_model_crud(
            names=("name_1", "name_2"),
            factory_class=factories.ContactTypeModelFactory,
            get_by_name="name_1")


class ContactRelationshipTypeTestCase(NamedModelTestCase):
    """ContactRelationship model unit test class.
    """
    def test_contract_relationship_type_crud(self):
        self.verify_named_model_crud(
            names=("name_1", "name_2"),
            factory_class=factories.ContactRelationshipTypeModelFactory,
            get_by_name="name_1")


class ContactTestCase(VersionedModelTestCase):
    """Contact model unit test class.
    """
    def test_contact_crud_name(self):
        self.verify_versioned_model_crud(
            factory_class=factories.ContactModelFactory,
            name=NameModelFactory())

    def test_contact_crud_formatted_name(self):
        self.verify_versioned_model_crud(
            factory_class=factories.ContactModelFactory,
            formatted_name=FormattedNameModelFactory())

    def test_contact_optional_fields(self):
        instance = factories.ContactModelFactory(
            contact_type=factories.ContactTypeModelFactory(),
            gender=GenderModelFactory(),
            name=NameModelFactory(),
            birth_date=timezone.now(),
            anniversary=timezone.now())
        instance.clean()

    def test_contact_address_add_remove(self):
        contact = factories.ContactModelFactory()
        address = USAddressModelFactory()
        contact_address = models.Contact.objects.address_add(contact, address)
        self.assertTrue(contact_address, "contact_address creation error")
        self.assertEqual(contact.addresses.count(), 1)
        ret = models.Contact.objects.address_remove(contact, address)
        self.assertEqual(ret[0], 1)

    def test_contact_name_add_remove(self):
        contact = factories.ContactModelFactory()
        name = NameModelFactory()
        contact_name = models.Contact.objects.name_add(contact, name)
        self.assertTrue(contact_name, "contact_name creation error")
        self.assertEqual(contact.names.count(), 1)
        ret = models.Contact.objects.name_remove(contact, name)
        self.assertEqual(ret[0], 1)


class ContactNameTestCase(VersionedModelTestCase):
    """ContactName model unit test class.
    """
    def test_contact_name_crud(self):
        self.verify_versioned_model_crud(
            factory_class=factories.ContactNameModelFactory)

    def test_contact_name_access(self):
        instance = factories.ContactNameModelFactory()
        self.assertEqual(models.ContactName.objects.count(), 1,
                         "ContactName creation error")
        self.assertEqual(instance.contact.names.count(), 1)
        names = instance.contact.names.all()
        self.assertEqual(list(names)[0], instance.name,
                         "Unexpected name instance")

    def test_contact_name_clear(self):
        # verify underlying object state following clear
        instance = factories.ContactNameModelFactory()
        self.assertEqual(models.ContactName.objects.count(), 1,
                         "ContactName creation error")
        instance.contact.names.clear()
        self.assertEqual(instance.contact.names.count(), 0)
        self.assertEqual(models.ContactName.objects.count(), 0,
                         "unexpected ContactName instances")
        self.assertEqual(models.Contact.objects.count(), 1,
                         "unexpected Contact instances")
        self.assertEqual(models.Name.objects.count(), 1,
                         "unexpected Name instances")

    def test_contact_delete(self):
        # verify delete propagation
        instance = factories.ContactNameModelFactory()
        self.assertEqual(models.ContactName.objects.count(), 1,
                         "ContactName creation error")
        instance.contact.delete()
        self.assertEqual(
            models.ContactName.objects.count(), 0,
            "ContactName instance mismatch following contact delete")

    def test_name_delete(self):
        # verify delete propagation
        instance = factories.ContactNameModelFactory()
        self.assertEqual(models.ContactName.objects.count(), 1,
                         "ContactName creation error")
        instance.name.delete()
        self.assertEqual(
            models.ContactName.objects.count(), 0,
            "ContactName instance mismatch following name delete")
