"""
.. module::  contacts.tests.test_models
   :synopsis: contacts application models unit test module.

*contacts* application models unit test module.
"""
from __future__ import absolute_import, print_function

from django.utils import timezone
from django.conf import settings

from python_core_utils.core import class_name
from django_core_utils.tests.factories import GroupFactory
from django_core_utils.tests.test_utils import (BaseModelTestCase,
                                                NamedModelTestCase,
                                                VersionedModelTestCase)

from django_core_models.demographics.tests.factories import GenderModelFactory
from django_core_models.images.tests.factories import (
    ImageModelFactory, ImageReferenceModelFactory)
from django_core_models.locations.tests.factories import (
    AddressTypeModelFactory, GeographicLocationModelFactory,
    LanguageModelFactory, TimezoneModelFactory,
    TimezoneTypeModelFactory)
from django_core_models.organizations.tests.factories import (
    OrganizationModelFactory, OrganizationUnitModelFactory,
    RoleModelFactory, TitleModelFactory)
from django_core_models.social_media.tests.factories import (
    EmailModelFactory, FormattedNameModelFactory,
    GroupModelFactory, InstantMessagingModelFactory,
    InstantMessagingTypeModelFactory, LogoTypeModelFactory,
    NameModelFactory, NicknameModelFactory,
    NicknameTypeModelFactory, PhoneModelFactory,
    PhoneTypeModelFactory, PhotoTypeModelFactory,
    UrlModelFactory, UrlTypeModelFactory)


from . import factories

from .. import models


class PermissionsMixin(object):
    """Permission unit test mixin class."""
    def setUp(self):
        self.saved_setting = settings.USE_OBJECT_PERMISSIONS
        settings.USE_OBJECT_PERMISSIONS = False

    def tearDown(self):
        settings.USE_OBJECT_PERMISSIONS = self.saved_setting


class ContactsNamedModelTestCase(PermissionsMixin, NamedModelTestCase):
    """Named model helper unit test class."""
    def setUp(self):
        PermissionsMixin.setUp(self)
        NamedModelTestCase.setUp(self)

    def tearDown(self):
        NamedModelTestCase.tearDown(self)
        PermissionsMixin.tearDown(self)


class ContactsVersionedModelTestCase(PermissionsMixin, VersionedModelTestCase):
    """Versioned model helper unit test class."""

    def setUp(self):
        PermissionsMixin.setUp(self)
        VersionedModelTestCase.setUp(self)

    def tearDown(self):
        VersionedModelTestCase.tearDown(self)
        PermissionsMixin.tearDown(self)


class ContactTypeTestCase(ContactsNamedModelTestCase):
    """ContactType model unit test class.
    """
    def test_contact_type_crud(self):
        self.verify_named_model_crud(
            names=("name_1", "name_2"),
            factory_class=factories.ContactTypeModelFactory,
            get_by_name="name_1")


class ContactRelationshipTypeTestCase(ContactsNamedModelTestCase):
    """ContactRelationship model unit test class.
    """
    def test_contact_relationship_type_crud(self):
        self.verify_named_model_crud(
            names=("name_1", "name_2"),
            factory_class=factories.ContactRelationshipTypeModelFactory,
            get_by_name="name_1")


class ContactTestCase(ContactsVersionedModelTestCase):
    """Contact model unit test class.
    """
    def test_contact_crud_name(self):
        self.verify_versioned_model_crud(
            factory_class=factories.ContactModelFactory)

    def test_contact_crud_formatted_name(self):
        self.verify_versioned_model_crud(
            factory_class=factories.ContactModelFactory,
            name=None,
            formatted_name=FormattedNameModelFactory())

    def test_contact_optional_fields(self):
        instance = factories.ContactModelFactory(
            contact_type=factories.ContactTypeModelFactory(),
            gender=GenderModelFactory(),
            name=NameModelFactory(),
            birth_date=timezone.now(),
            anniversary=timezone.now())
        instance.clean()


class ContactAssociationTestCase(ContactsVersionedModelTestCase):
    """Base class for contact association test cases."""

    def create_contact(self, **kwargs):
        name = kwargs.pop("name", None)
        formatted_name = kwargs.pop("formatted_name", None)
        if not (name or formatted_name):
            name = NameModelFactory()
        instance = factories.ContactModelFactory(
            name=name, formatted_name=formatted_name, **kwargs)
        instance.clean()
        return instance

    def create_instance(self, factory_class, **kwargs):
        """Create instance of the designated class."""
        return self.verify_create(factory_class, **kwargs)

    def verify_access(self, factory_class, association_name,
                      attr_name, contact_attr_name=None,
                      **kwargs):
        """Verify association access"""
        instance = self.create_instance(factory_class, **kwargs)
        contact_attr_name = contact_attr_name or "contact"
        contact = getattr(instance, contact_attr_name)
        association = getattr(contact, association_name)
        self.assertEqual(association.count(), 1)
        self.assertEqual(list(association.all())[0],
                         getattr(instance, attr_name),
                         "Unexpected association instance")

    def verify_clear(self, factory_class, association_name,
                     other_class, contact_attr_name=None,
                     expected_contact_count=1,
                     expected_other_model_count=1,
                     **kwargs):
        """Verify underlying object state following clear"""
        instance = self.create_instance(factory_class, **kwargs)
        contact_attr_name = contact_attr_name or "contact"
        contact = getattr(instance, contact_attr_name)
        association = getattr(contact, association_name)
        association.clear()
        self.assertEqual(association.count(), 0,
                         "Unexpected association entries")
        model_class = factory_class.model_class()
        self.assertEqual(model_class.objects.count(), 0,
                         "unexpected %s  instances" % class_name(model_class))
        self.assertEqual(models.Contact.objects.count(),
                         expected_contact_count,
                         "unexpected Contact instances")
        if other_class:
            self.assertEqual(
                other_class.objects.count(), expected_other_model_count,
                "unexpected %s  instances" % class_name(other_class))

    def verify_contact_delete(self, factory_class,
                              contact_attr_name=None, **kwargs):
        """Verify contact delete propagation."""
        instance = self.create_instance(factory_class, **kwargs)
        contact_attr_name = contact_attr_name or "contact"
        contact = getattr(instance, contact_attr_name)
        contact.delete()
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

    def test_contact_address_add_remove(self):
        contact = self.create_contact()
        address = factories.USAddressModelFactory()
        contact_address = models.Contact.objects.address_add(
            contact, address, address_type=AddressTypeModelFactory())
        self.assertTrue(contact_address, "ContactAddress creation error")
        self.assertEqual(contact.addresses.count(), 1)
        ret = models.Contact.objects.address_remove(contact, address)
        self.assertEqual(ret[0], 1)


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

    def test_contact_annotation_add_remove(self):
        contact = self.create_contact()
        annotation = factories.AnnotationModelFactory()
        contact_annotation = models.Contact.objects.annotation_add(
            contact, annotation)
        self.assertTrue(contact_annotation, "ContactAnnotation creation error")
        self.assertEqual(contact.annotations.count(), 1)
        ret = models.Contact.objects.annotation_remove(contact, annotation)
        self.assertEqual(ret[0], 1)


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

    def test_category_delete(self):
        self.verify_other_delete(
            factory_class=self.factory_class,
            attr_name=self.attr_name)

    def test_contact_category_add_remove(self):
        contact = self.create_contact()
        category = factories.CategoryModelFactory()
        contact_category = models.Contact.objects.category_add(
            contact, category)
        self.assertTrue(contact_category, "ContactCategory creation error")
        self.assertEqual(contact.categories.count(), 1)
        ret = models.Contact.objects.category_remove(contact, category)
        self.assertEqual(ret[0], 1)


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


class ContactGeographicLocationTestCase(ContactAssociationTestCase):
    """ContactGeographicLocation association model unit test class.
    """
    factory_class = factories.ContactGeographicLocationModelFactory
    association_name = "geographic_locations"
    other_class = models.GeographicLocation
    attr_name = "geographic_location"

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

    def test_contact_geographic_location_add_remove(self):
        contact = self.create_contact()
        geographic_location = GeographicLocationModelFactory()
        manager = models.Contact.objects
        contact_geographic_location = manager.geographic_location_add(
            contact, geographic_location)
        self.assertTrue(contact_geographic_location,
                        "ContactGeographicLocation creation error")
        self.assertEqual(contact.geographic_locations.count(), 1)
        ret = manager.geographic_location_remove(contact, geographic_location)
        self.assertEqual(ret[0], 1)


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

    def test_contact_group_add_remove(self):
        contact = self.create_contact()
        group = GroupModelFactory()
        contact_group = models.Contact.objects.group_add(contact, group)
        self.assertTrue(contact_group,
                        "ContactGroup creation error")
        self.assertEqual(contact.groups.count(), 1)
        ret = models.Contact.objects.group_remove(contact, group)
        self.assertEqual(ret[0], 1)


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


class ContactLanguageTestCase(ContactAssociationTestCase):
    """ContactLanguage association model unit test class.
    """
    factory_class = factories.ContactLanguageModelFactory
    association_name = "languages"
    other_class = models.Language
    attr_name = "language"

    def test_contact_language_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_language_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_language_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_language_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

    def test_contact_language_add_remove(self):
        contact = self.create_contact()
        language = LanguageModelFactory()
        contact_language = models.Contact.objects.language_add(
            contact, language)
        self.assertTrue(contact_language, "ContactLanguage creation error")
        self.assertEqual(contact.languages.count(), 1)
        ret = models.Contact.objects.language_remove(contact, language)
        self.assertEqual(ret[0], 1)


class ContactLogoTestCase(ContactAssociationTestCase):
    """ContactLogo association model unit test class.
    """
    factory_class = factories.ContactLogoModelFactory
    association_name = "logos"
    other_class = models.ImageReference
    attr_name = "image_reference"

    def test_contact_logo_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_logo_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_logo_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_logo_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

    def test_contact_logo_add_remove(self):
        contact = self.create_contact()
        image_reference = ImageReferenceModelFactory(image=ImageModelFactory())
        # use image instance
        contact_logo = models.Contact.objects.logo_add(
            contact, image_reference=image_reference,
            logo_type=LogoTypeModelFactory())
        self.assertTrue(contact_logo, "ContactLogo creation error")
        self.assertEqual(contact.logos.count(), 1)
        ret = models.Contact.objects.logo_remove(
            contact, image_reference=image_reference)
        self.assertEqual(ret[0], 1)

        # use image url
        url = "http://www.example.com/image.gif"
        image_reference = ImageReferenceModelFactory(image=None, url=url)
        contact_logo = models.Contact.objects.logo_add(
            contact, image_reference=image_reference,
            logo_type=LogoTypeModelFactory())
        self.assertTrue(contact_logo, "ContactLogo creation error")
        self.assertEqual(contact.logos.count(), 1)
        ret = models.Contact.objects.logo_remove(
            contact, image_reference=image_reference)
        self.assertEqual(ret[0], 1)


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
        # an instance of name is created per contact factory use
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class,
            expected_other_model_count=2)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_name_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

    def test_contact_name_add_remove(self):
        contact = self.create_contact()
        name = NameModelFactory()
        contact_name = models.Contact.objects.name_add(contact, name)
        self.assertTrue(contact_name, "ContactName creation error")
        self.assertEqual(contact.names.count(), 1)
        ret = models.Contact.objects.name_remove(contact, name)
        self.assertEqual(ret[0], 1)


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

    def test_name_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

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


class ContactOrganizationTestCase(ContactAssociationTestCase):
    """ContactOrganization association model unit test class.
    """
    factory_class = factories.ContactOrganizationModelFactory
    association_name = "organizations"
    other_class = models.Organization
    attr_name = "organization"

    def test_contact_organization_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_organization_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_organization_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_organization_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

    def test_contact_organization_add_remove(self):
        contact = self.create_contact()
        organization = OrganizationModelFactory()
        unit = OrganizationUnitModelFactory(
            organization=organization)
        contact_organization = models.Contact.objects.organization_add(
            contact, organization,
            unit=unit)
        self.assertTrue(contact_organization,
                        "ContactOrganization creation error")
        self.assertEqual(contact.organizations.count(), 1)
        ret = models.Contact.objects.organization_remove(contact, organization)
        self.assertEqual(ret[0], 1)


class ContactPhoneTestCase(ContactAssociationTestCase):
    """ContactPhone association model unit test class.
    """
    factory_class = factories.ContactPhoneModelFactory
    association_name = "phones"
    other_class = models.Phone
    attr_name = "phone"

    def test_contact_phone_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_phone_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_phone_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_phone_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

    def test_contact_phone_add_remove(self):
        contact = self.create_contact()
        phone = PhoneModelFactory()
        phone_type = PhoneTypeModelFactory()
        contact_phone = models.Contact.objects.phone_add(
            contact, phone,
            phone_type=phone_type)
        self.assertTrue(contact_phone,
                        "ContactPhone creation error")
        self.assertEqual(contact.phones.count(), 1)
        ret = models.Contact.objects.phone_remove(contact, phone)
        self.assertEqual(ret[0], 1)


class ContactPhotoTestCase(ContactAssociationTestCase):
    """ContactPhoto association model unit test class.
    """
    factory_class = factories.ContactPhotoModelFactory
    association_name = "photos"
    other_class = models.ImageReference
    attr_name = "image_reference"

    def test_contact_photo_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_photo_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_photo_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_photo_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

    def test_contact_photo_add_remove(self):
        contact = self.create_contact()
        image_reference = ImageReferenceModelFactory(image=ImageModelFactory())
        # use image instance
        contact_photo = models.Contact.objects.photo_add(
            contact, image_reference=image_reference,
            photo_type=PhotoTypeModelFactory())
        self.assertTrue(contact_photo, "ContactPhoto creation error")
        self.assertEqual(contact.photos.count(), 1)
        ret = models.Contact.objects.photo_remove(
            contact, image_reference=image_reference)
        self.assertEqual(ret[0], 1)

        # use image url
        url = "http://www.example.com/image.gif"
        image_reference = ImageReferenceModelFactory(image=None, url=url)
        contact_photo = models.Contact.objects.photo_add(
            contact, image_reference=image_reference,
            photo_type=PhotoTypeModelFactory())
        self.assertTrue(contact_photo, "ContactPhoto creation error")
        self.assertEqual(contact.photos.count(), 1)
        ret = models.Contact.objects.photo_remove(
            contact, image_reference=image_reference)
        self.assertEqual(ret[0], 1)


class RelatedContactTestCase(ContactAssociationTestCase):
    """RelatedContact association model unit test class.
    """
    factory_class = factories.RelatedContactModelFactory
    association_name = "related_contacts"
    other_class = models.Contact
    attr_name = "to_contact"

    def test_contact_related_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_related_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name,
            contact_attr_name="from_contact")

    def test_contact_related_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class,
            contact_attr_name="from_contact",
            expected_contact_count=2,
            expected_other_model_count=2)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class,
                                   contact_attr_name="from_contact")

    def test_related_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

    def test_contact_related_add_remove(self):
        from_contact = self.create_contact()
        to_contract = self.create_contact()
        rel_type = factories.ContactRelationshipTypeModelFactory()
        related_contact = models.Contact.objects.related_contact_add(
            from_contact, to_contract,
            contact_relationship_type=rel_type)
        self.assertTrue(related_contact,
                        "RelatedContact creation error")
        self.assertEqual(from_contact.related_contacts.count(), 1)
        ret = models.Contact.objects.related_contact_remove(
            from_contact, to_contract)
        self.assertEqual(ret[0], 1)


class ContactRoleTestCase(ContactAssociationTestCase):
    """ContactRole association model unit test class.
    """
    factory_class = factories.ContactRoleModelFactory
    association_name = "roles"
    other_class = models.Role
    attr_name = "role"

    def test_contact_role_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_role_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_role_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_role_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

    def test_contact_role_add_remove(self):
        contact = self.create_contact()
        role = RoleModelFactory()
        organization = OrganizationModelFactory()
        contact_role = models.Contact.objects.role_add(
            contact, role,
            organization=organization)
        self.assertTrue(contact_role,
                        "ContactRole creation error")
        self.assertEqual(contact.roles.count(), 1)
        ret = models.Contact.objects.role_remove(contact, role)
        self.assertEqual(ret[0], 1)


class ContactTimezoneTestCase(ContactAssociationTestCase):
    """ContactTimezone association model unit test class.
    """
    factory_class = factories.ContactTimezoneModelFactory
    association_name = "timezones"
    other_class = models.Timezone
    attr_name = "timezone"

    def test_contact_timezone_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_timezone_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_timezone_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_timezone_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

    def test_contact_timezone_add_remove(self):
        contact = self.create_contact()
        timezone = TimezoneModelFactory()
        timezone_type = TimezoneTypeModelFactory()
        contact_timezone = models.Contact.objects.timezone_add(
            contact, timezone,
            timezone_type=timezone_type)
        self.assertTrue(contact_timezone,
                        "ContactTimezone creation error")
        self.assertEqual(contact.timezones.count(), 1)
        ret = models.Contact.objects.timezone_remove(contact, timezone)
        self.assertEqual(ret[0], 1)


class ContactTitleTestCase(ContactAssociationTestCase):
    """ContactTitle association model unit test class.
    """
    factory_class = factories.ContactTitleModelFactory
    association_name = "titles"
    other_class = models.Title
    attr_name = "title"

    def test_contact_title_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_title_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_title_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_title_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

    def test_contact_title_add_remove(self):
        contact = self.create_contact()
        title = TitleModelFactory()
        organization = OrganizationModelFactory()
        contact_title = models.Contact.objects.title_add(
            contact, title,
            organization=organization)
        self.assertTrue(contact_title,
                        "ContactTitle creation error")
        self.assertEqual(contact.titles.count(), 1)
        ret = models.Contact.objects.title_remove(contact, title)
        self.assertEqual(ret[0], 1)


class ContactUrlTestCase(ContactAssociationTestCase):
    """ContactUrl association model unit test class.
    """
    factory_class = factories.ContactUrlModelFactory
    association_name = "urls"
    other_class = models.Url
    attr_name = "url"

    def test_contact_url_crud(self):
        self.verify_versioned_model_crud(
            factory_class=self.factory_class)

    def test_contact_url_access(self):
        self.verify_access(
            factory_class=self.factory_class,
            association_name=self.association_name,
            attr_name=self.attr_name)

    def test_contact_url_clear(self):
        self.verify_clear(
            factory_class=self.factory_class,
            association_name=self.association_name,
            other_class=self.other_class)

    def test_contact_delete(self):
        self.verify_contact_delete(self.factory_class)

    def test_url_delete(self):
        self.verify_other_delete(
            self.factory_class, self.attr_name)

    def test_contact_url_add_remove(self):
        contact = self.create_contact()
        url = UrlModelFactory()
        url_type = UrlTypeModelFactory()
        contact_url = models.Contact.objects.url_add(
            contact, url,
            url_type=url_type)
        self.assertTrue(contact_url,
                        "ContactUrl creation error")
        self.assertEqual(contact.urls.count(), 1)
        ret = models.Contact.objects.url_remove(contact, url)
        self.assertEqual(ret[0], 1)


class UserProfileTestCase(PermissionsMixin, BaseModelTestCase):
    """UserProfile model unit test class.
    """
    def setUp(self):
        PermissionsMixin.setUp(self)
        BaseModelTestCase.setUp(self)

    def tearDown(self):
        BaseModelTestCase.tearDown(self)
        PermissionsMixin.tearDown(self)

    def create_user_profile(self, **kwargs):
        instance = factories.UserProfileModelFactory(**kwargs)
        instance.clean()
        return instance

    def verify_relation(self, attrs, other):
        profile = self.create_user_profile()
        for attr in attrs:
            relation = getattr(profile, attr)
            self.assertEqual(relation.count(), 0)
            relation.add(other)
            self.assertEqual(relation.count(), 1)
            relation.remove(other)
            self.assertEqual(relation.count(), 0)

    def test_user_profile_crud(self):
        instance = self.create_user_profile()
        self.assertEqual(models.UserProfile.objects.count(), 1)
        instance.full_clean()
        instance.save()
        saved = models.UserProfile.objects.get(pk=instance.id)
        self.assertEqual(instance, saved)
        saved.delete()
        self.assertEqual(models.UserProfile.objects.count(), 0)

    def test_user_profile_add_remove_user(self):
        self.verify_relation(("users_read", "users_write"),
                             factories.UserFactory())

    def test_user_profile_add_remove_groups(self):
        self.verify_relation(("groups_read", "groups_write"),
                             GroupFactory())

    def test_user_profile_delete_user(self):
        profile = self.create_user_profile()
        self.assertEqual(models.UserProfile.objects.count(), 1)
        self.assertEqual(profile.users_read.count(), 0)
        # 1. Verify when a user is deleted, the relationship is removed
        user = factories.UserFactory()
        profile.users_read.add(user)
        self.assertEqual(profile.users_read.count(), 1)
        user.delete()
        self.assertEqual(profile.users_read.count(), 0)
        # 2. Verify when a user is deleted associated profile is deleted
        profile.user.delete()
        self.assertEqual(models.UserProfile.objects.count(), 0)

    def test_user_profile_delete_group(self):
        profile = self.create_user_profile()
        self.assertEqual(models.UserProfile.objects.count(), 1)
        self.assertEqual(profile.groups_read.count(), 0)
        # Verify when a group is deleted, the relationship is removed
        group = GroupFactory()
        profile.groups_read.add(group)
        self.assertEqual(profile.groups_read.count(), 1)
        group.delete()
        self.assertEqual(profile.groups_read.count(), 0)
