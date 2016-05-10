"""
.. module::  contacts.tests.test_models
   :synopsis: contacts application models unit test module.

*contacts* application models unit test module.
"""
from __future__ import absolute_import, print_function

from django.utils import timezone
from python_core_utils.core import class_name
from django_core_utils.tests.test_utils import (NamedModelTestCase,
                                                VersionedModelTestCase)
from django_core_models.social_media.tests.factories import (
    EmailModelFactory, GroupModelFactory, FormattedNameModelFactory,
    InstantMessagingModelFactory, InstantMessagingTypeModelFactory,
    NameModelFactory,  NicknameTypeModelFactory,
    NicknameModelFactory)
from django_core_models.demographics.tests.factories import (
    GenderModelFactory)
from django_core_models.locations.tests.factories import (
    AddressTypeModelFactory)

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
    def create_contact(self, **kwargs):
        name = kwargs.pop("name", None)
        formatted_name = kwargs.pop("formatted_name", None)
        if not (name or formatted_name):
            name = NameModelFactory()
        instance = factories.ContactModelFactory(
            name=name, formatted_name=formatted_name, **kwargs)
        instance.clean()
        return instance

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
        contact = self.create_contact()
        address = factories.USAddressModelFactory()
        contact_address = models.Contact.objects.address_add(
            contact, address, address_type=AddressTypeModelFactory())
        self.assertTrue(contact_address, "ContactAddress creation error")
        self.assertEqual(contact.addresses.count(), 1)
        ret = models.Contact.objects.address_remove(contact, address)
        self.assertEqual(ret[0], 1)

    def test_contact_annotation_add_remove(self):
        contact = self.create_contact()
        annotation = factories.AnnotationModelFactory()
        contact_annotation = models.Contact.objects.annotation_add(
            contact, annotation)
        self.assertTrue(contact_annotation, "ContactAnnotation creation error")
        self.assertEqual(contact.annotations.count(), 1)
        ret = models.Contact.objects.annotation_remove(contact, annotation)
        self.assertEqual(ret[0], 1)

    def test_contact_category_add_remove(self):
        contact = self.create_contact()
        category = factories.CategoryModelFactory()
        contact_category = models.Contact.objects.category_add(
            contact, category)
        self.assertTrue(contact_category, "ContactCategory creation error")
        self.assertEqual(contact.categories.count(), 1)
        ret = models.Contact.objects.category_remove(contact, category)
        self.assertEqual(ret[0], 1)

    def test_contact_email_add_remove(self):
        contact = self.create_contact()
        email = EmailModelFactory()
        contact_email = models.Contact.objects.email_add(
            contact, email)
        self.assertTrue(contact_email,
                        "ContactEmail creation error")
        self.assertEqual(contact.emails.count(), 1)
        ret = models.Contact.objects.email_remove(contact, email)
        self.assertEqual(ret[0], 1)

    def test_contact_formatted_name_add_remove(self):
        contact = self.create_contact()
        name = FormattedNameModelFactory()
        contact_formatted_name = models.Contact.objects.formatted_name_add(
            contact, name)
        self.assertTrue(contact_formatted_name,
                        "ContactFormattedName creation error")
        self.assertEqual(contact.formatted_names.count(), 1)
        ret = models.Contact.objects.formatted_name_remove(contact, name)
        self.assertEqual(ret[0], 1)

    def test_contact_group_add_remove(self):
        contact = self.create_contact()
        group = GroupModelFactory()
        contact_group = models.Contact.objects.group_add(contact, group)
        self.assertTrue(contact_group,
                        "ContactGroup creation error")
        self.assertEqual(contact.groups.count(), 1)
        ret = models.Contact.objects.group_remove(contact, group)
        self.assertEqual(ret[0], 1)

    def test_contact_instant_messaging_add_remove(self):
        contact = self.create_contact()
        instant_messaging = InstantMessagingModelFactory()
        manager = models.Contact.objects
        contact_instant_messaging = manager.instant_messaging_add(
            contact, instant_messaging,
            instant_messaging_type=InstantMessagingTypeModelFactory())
        self.assertTrue(contact_instant_messaging,
                        "ContactInstantMessaging creation error")
        self.assertEqual(contact.instant_messaging.count(), 1)
        ret = manager.instant_messaging_remove(
            contact, instant_messaging)
        self.assertEqual(ret[0], 1)

    def test_contact_name_add_remove(self):
        contact = self.create_contact()
        name = NameModelFactory()
        contact_name = models.Contact.objects.name_add(contact, name)
        self.assertTrue(contact_name, "ContactName creation error")
        self.assertEqual(contact.names.count(), 1)
        ret = models.Contact.objects.name_remove(contact, name)
        self.assertEqual(ret[0], 1)

    def test_contact_nickname_add_remove(self):
        contact = self.create_contact()
        name = NicknameModelFactory()
        contact_nickname = models.Contact.objects.nickname_add(
            contact, name, nickname_type=NicknameTypeModelFactory())
        self.assertTrue(contact_nickname,
                        "ContactNickname creation error")
        self.assertEqual(contact.nicknames.count(), 1)
        ret = models.Contact.objects.nickname_remove(contact, name)
        self.assertEqual(ret[0], 1)


class ContactAssociationTestCase(VersionedModelTestCase):
    """Base class for contact association test cases."""

    def create_instance(self, factory_class, **kwargs):
        """Create instance of the designated class."""
        return self.verify_create(factory_class, **kwargs)

    def verify_access(self, factory_class, association_name,
                      attr_name,  **kwargs):
        """Verify association access"""
        instance = self.create_instance(factory_class, **kwargs)
        association = getattr(instance.contact, association_name)
        self.assertEqual(association.count(), 1)
        self.assertEqual(list(association.all())[0],
                         getattr(instance, attr_name),
                         "Unexpected association instance")

    def verify_clear(self, factory_class, association_name,
                     other_class, **kwargs):
        """Verify underlying object state following clear"""
        instance = self.create_instance(factory_class, **kwargs)
        association = getattr(instance.contact, association_name)
        association.clear()
        self.assertEqual(association.count(), 0,
                         "Unexpected association entries")
        model_class = factory_class.model_class()
        self.assertEqual(model_class.objects.count(), 0,
                         "unexpected %s  instances" % class_name(model_class))
        self.assertEqual(models.Contact.objects.count(), 1,
                         "unexpected Contact instances")
        if other_class:
            self.assertEqual(
                other_class.objects.count(), 1,
                "unexpected %s  instances" % class_name(other_class))

    def verify_contact_delete(self, factory_class, **kwargs):
        """Verify contact delete propagation."""
        instance = self.create_instance(factory_class, **kwargs)
        instance.contact.delete()
        model_class = factory_class.model_class()
        self.assertEqual(
            model_class.objects.count(), 0,
            "%s instance mismatch following contact delete" %
            class_name(model_class))

    def verify_other_delete(self, factory_class, attr_name, **kwargs):
        """Verify delete propagation through other model."""
        instance = self.create_instance(factory_class, **kwargs)
        value = getattr(instance, attr_name)
        value.delete()
        model_class = factory_class.model_class()
        self.assertEqual(
            model_class.objects.count(), 0,
            "%s instance mismatch following contact delete" %
            class_name(model_class))


class ContactAddressTestCase(ContactAssociationTestCase):
    """ContactAddress association model unit test class.
    """
    factory_class = factories.ContactAddressModelFactory
    association_name = "addresses"
    other_class = models.Address
    attr_name = "address"

    def test_contact_address_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_address_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_address_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_address_delete(self):
        self.verify_other_delete(
            factory_class=self.factory_class,
            attr_name=self.attr_name)


class ContactAnnotationTestCase(ContactAssociationTestCase):
    """ContactAnnotation association model unit test class.
    """
    factory_class = factories.ContactAnnotationModelFactory
    association_name = "annotations"
    other_class = models.Annotation
    attr_name = "annotation"

    def test_contact_annotation_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_annotation_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_annotation_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_annotation_delete(self):
        self.verify_other_delete(
            factory_class=self.factory_class,
            attr_name=self.attr_name)


class ContactCategoryTestCase(ContactAssociationTestCase):
    """ContactCategory association model unit test class.
    """
    factory_class = factories.ContactCategoryModelFactory
    association_name = "categories"
    other_class = models.Category
    attr_name = "category"

    def test_contact_category_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_category_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_category_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)


class ContactEmailTestCase(ContactAssociationTestCase):
    """ContactEmail association model unit test class.
    """
    factory_class = factories.ContactEmailModelFactory
    association_name = "emails"
    other_class = models.Email
    attr_name = "email"

    def test_contact_email_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_email_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_email_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_email_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)


class ContactGroupTestCase(ContactAssociationTestCase):
    """ContactGroup association model unit test class.
    """
    factory_class = factories.ContactGroupModelFactory
    association_name = "groups"
    other_class = models.Group
    attr_name = "group"

    def test_contact_group_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_group_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_group_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_group_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)


class ContactFormattedNameTestCase(ContactAssociationTestCase):
    """ContactFormattedName association model unit test class.
    """
    factory_class = factories.ContactFormattedNameModelFactory
    association_name = "formatted_names"
    other_class = models.FormattedName
    attr_name = "name"

    def test_contact_name_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_name_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_name_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_name_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)


class ContactInstantMessagingTestCase(ContactAssociationTestCase):
    """ContactInstantMessaging association model unit test class.
    """
    factory_class = factories.ContactInstantMessagingModelFactory
    association_name = "instant_messaging"
    other_class = models.InstantMessaging
    attr_name = "instant_messaging"

    def test_contact_instant_messaging_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_instant_messaging_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_instant_messaging_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_instant_messaging_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)


class ContactNameTestCase(ContactAssociationTestCase):
    """ContactName association model unit test class.
    """
    factory_class = factories.ContactNameModelFactory
    association_name = "names"
    other_class = models.Name
    attr_name = "name"

    def test_contact_name_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_name_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_name_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_name_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)


class ContactNicknameTestCase(ContactAssociationTestCase):
    """ContactNickname association model unit test class.
    """
    factory_class = factories.ContactNicknameModelFactory
    association_name = "nicknames"
    other_class = models.Nickname
    attr_name = "name"

    def test_contact_name_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_nickname_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_nickname_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)