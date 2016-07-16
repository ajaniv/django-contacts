"""
.. module::  django_core_models.social_media.tests.test_views
   :synopsis: social_media models application views unit test module.

*social_media*  application views unit test module.
"""
from __future__ import absolute_import, print_function
from django_core_utils.tests.api_test_utils import (
    NamedModelApiTestCase,
    VersionedModelApiTestCase)
from django_core_models.core.tests.factories import (
    AnnotationModelFactory,
    CategoryModelFactory)
from django_core_models.images.tests.factories import (
    ImageReferenceModelFactory)
from django_core_models.locations.tests.factories import (
    USAddressModelFactory,
    AddressTypeModelFactory,
    GeographicLocationModelFactory,
    GeographicLocationTypeModelFactory,
    LanguageModelFactory,
    LanguageTypeModelFactory,
    TimezoneModelFactory,
    TimezoneTypeModelFactory)
from django_core_models.organizations.tests.factories import (
    OrganizationModelFactory,
    OrganizationUnitModelFactory,
    RoleModelFactory,
    TitleModelFactory)
from django_core_models.social_media.tests.factories import (
    EmailModelFactory,
    EmailTypeModelFactory,
    FormattedNameModelFactory,
    GroupModelFactory,
    InstantMessagingModelFactory,
    InstantMessagingTypeModelFactory,
    LogoTypeModelFactory,
    NameModelFactory,
    NicknameModelFactory,
    NicknameTypeModelFactory,
    PhoneModelFactory,
    PhoneTypeModelFactory,
    PhotoTypeModelFactory,
    UrlModelFactory,
    UrlTypeModelFactory)


from . import factories
from .. import models
from .. import serializers


class ConctactTypeApiTestCase(NamedModelApiTestCase):
    """ContactType API unit test class."""
    factory_class = factories.ContactTypeModelFactory
    model_class = models.ContactType
    serializer_class = serializers.ContactTypeSerializer

    url_detail = "contact-type-detail"
    url_list = "contact-type-list"

    name = factories.ContactTypeModelFactory.name

    def test_create_contact_type(self):
        self.verify_create_defaults()

    def test_create_contact_type_partial(self):
        self.verify_create_defaults_partial()

    def test_get_contact_type(self):
        self.verify_get_defaults()

    def test_put_contact_type_partial(self):
        instance = self.create_instance_default()
        data = dict(id=instance.id, name=self.name)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_type(self):
        self.verify_delete_default()


class ConctactRelationshipTypeApiTestCase(NamedModelApiTestCase):
    """Contact  API unit test class."""
    factory_class = factories.ContactRelationshipTypeModelFactory
    model_class = models.ContactRelationshipType
    serializer_class = serializers.ContactRelationshipTypeSerializer

    url_detail = "contact-relationship-type-detail"
    url_list = "contact-relationship-type-list"

    name = factories.ContactRelationshipTypeModelFactory.name

    def test_create_contact_relationship_type(self):
        self.verify_create_defaults()

    def test_create_contact_relationship_type_partial(self):
        self.verify_create_defaults_partial()

    def test_get_contact_relationship_type(self):
        self.verify_get_defaults()

    def test_put_contact_relationship_type_partial(self):
        instance = self.create_instance_default()
        data = dict(id=instance.id, name=self.name)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_relationship_type(self):
        self.verify_delete_default()


class ContactApiTestCase(VersionedModelApiTestCase):
    """Contact  API unit test class."""
    factory_class = factories.ContactModelFactory
    model_class = models.Contact
    serializer_class = serializers.ContactSerializer

    url_detail = "contact-detail"
    url_list = "contact-list"

    simple_attrs = ("anniversary", "birth_date")
    foreign_keys = ("contact_type", "formatted_name", "gender", "name")
    non_assoc_attrs = simple_attrs + foreign_keys

    def contact_data(self, instance):
        """return contact data"""
        instance = instance or self.factory_class()
        data = dict()

        for attr in self.non_assoc_attrs:
            value = getattr(instance, attr, None)
            if value:
                data[attr] = value.id if attr in self.foreign_keys else value

        return data

    def post_required_data(self, ref_instance, user=None, site=None):
        """Return named model post request required data."""
        data = super(
            ContactApiTestCase, self).post_required_data(user, site)
        data.update(self.contact_data(ref_instance))
        return data

    def verify_create_contact(
            self, ref_instance=None,
            data=None, extra_attrs=None):
        """Generate post request for contact creation."""
        data = data or self.post_required_data(ref_instance)

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        base_attrs = [attr for attr in self.non_assoc_attrs
                      if getattr(instance, attr, None)]

        attrs = base_attrs + extra_attrs if extra_attrs else base_attrs
        if ref_instance:
            self.assert_instance_equal(ref_instance, instance, attrs)

        return response, instance

    def test_create_contact(self):
        instance = self.create_instance_default()
        self.verify_create_contact(
            ref_instance=instance)

    def test_create_contact_partial(self):
        instance = self.create_instance_default()
        data = self.contact_data(instance)
        self.verify_create_contact(
            ref_instance=instance,
            data=data)

    def test_get_contact(self):
        self.verify_get_defaults()

    def test_put_contact_partial(self):
        instance = self.create_instance_default()
        contact_type = factories.ContactTypeModelFactory()
        data = dict(id=instance.id,
                    name=instance.name.id,
                    contact_type=contact_type.id)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact(self):
        self.verify_delete_default()


class ContactAssociationApiTestCase(VersionedModelApiTestCase):
    """Base class for contact association test cases."""
    def setUp(self):
        super(ContactAssociationApiTestCase, self).setUp()
        self.contact = factories.ContactModelFactory()

    def verify_contact_association(self, instance, data):
        for key, value in data.items():
            attr = getattr(instance, key)
            self.assertEqual(value, attr.id, "unexpected attr value")


class ContactAddressApiTestCase(ContactAssociationApiTestCase):
    """ContactAddress  API unit test class."""
    factory_class = factories.ContactAddressModelFactory
    model_class = models.ContactAddress
    serializer_class = serializers.ContactAddressSerializer

    url_detail = "contact-address-detail"
    url_list = "contact-address-list"

    def setUp(self):
        super(ContactAddressApiTestCase, self).setUp()
        self.address = USAddressModelFactory()
        self.address_type = AddressTypeModelFactory()

    def contact_address_data(
            self, contact=None, address=None, address_type=None):
        """return contact address data"""
        contact = contact or self.contact
        address = address or self.address
        address_type = address_type or self.address_type
        data = dict(contact=self.contact.id,
                    address=address.id,
                    address_type=address_type.id)

        return data

    def post_required_data(self, contact=None, address=None,
                           address_type=None, user=None, site=None):
        """Return named model post request required data."""
        data = super(
            ContactAddressApiTestCase, self).post_required_data(user, site)
        data.update(self.contact_address_data(contact, address, address_type))
        return data

    def verify_create_contact_address(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact address creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_address(self):
        self.verify_create_contact_address()

    def test_create_contact__address_partial(self):
        data = self.contact_address_data()
        self.verify_create_contact_address(data=data)

    def test_get_contact_address(self):
        self.verify_get_defaults()

    def test_put_contact_address_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id,
                    priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_address(self):
        self.verify_delete_default()


class ContactAnnotationApiTestCase(ContactAssociationApiTestCase):
    """ContactAnnotation  API unit test class."""
    factory_class = factories.ContactAnnotationModelFactory
    model_class = models.ContactAnnotation
    serializer_class = serializers.ContactAnnotationSerializer

    url_detail = "contact-annotation-detail"
    url_list = "contact-annotation-list"

    def setUp(self):
        super(ContactAnnotationApiTestCase, self).setUp()
        self.annotation = AnnotationModelFactory()

    def contact_annotation_data(self, contact=None, annotation=None):
        """return contact address data"""
        contact = contact or self.contact
        annotation = annotation or self.annotation
        data = dict(contact=self.contact.id,
                    annotation=annotation.id)

        return data

    def post_required_data(self, contact=None, annotation=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactAnnotationApiTestCase, self).post_required_data(user, site)
        data.update(self.contact_annotation_data(contact, annotation))
        return data

    def verify_create_contact_annotation(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact annotation creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_annotation(self):
        self.verify_create_contact_annotation()

    def test_create_contact_annotation_partial(self):
        data = self.contact_annotation_data()
        self.verify_create_contact_annotation(data=data)

    def test_get_contact_annotation(self):
        self.verify_get_defaults()

    def test_put_contact_annotation_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_annotation(self):
        self.verify_delete_default()


class ContactCategoryApiTestCase(ContactAssociationApiTestCase):
    """ContactCategory  API unit test class."""
    factory_class = factories.ContactCategoryModelFactory
    model_class = models.ContactCategory
    serializer_class = serializers.ContactCategorySerializer

    url_detail = "contact-category-detail"
    url_list = "contact-category-list"

    def setUp(self):
        super(ContactCategoryApiTestCase, self).setUp()
        self.category = CategoryModelFactory()

    def contact_category_data(self, contact=None, category=None):
        """return contact category data"""
        contact = contact or self.contact
        category = category or self.category
        data = dict(contact=self.contact.id,
                    category=category.id)

        return data

    def post_required_data(self, contact=None, category=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactCategoryApiTestCase, self).post_required_data(user, site)
        data.update(self.contact_category_data(contact, category))
        return data

    def verify_create_contact_category(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact category creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_category(self):
        self.verify_create_contact_category()

    def test_create_contact_category_partial(self):
        data = self.contact_category_data()
        self.verify_create_contact_category(data=data)

    def test_get_contact_category(self):
        self.verify_get_defaults()

    def test_put_contact_category_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_category(self):
        self.verify_delete_default()


class ContactEmailApiTestCase(ContactAssociationApiTestCase):
    """ContactEmail  API unit test class."""
    factory_class = factories.ContactEmailModelFactory
    model_class = models.ContactEmail
    serializer_class = serializers.ContactEmailSerializer

    url_detail = "contact-email-detail"
    url_list = "contact-email-list"

    def setUp(self):
        super(ContactEmailApiTestCase, self).setUp()
        self.email = EmailModelFactory()
        self.email_type = EmailTypeModelFactory()

    def contact_email_data(self, contact=None, email=None, email_type=None):
        """return contact email data"""
        contact = contact or self.contact
        email = email or self.email
        email_type = email_type or self.email_type
        data = dict(contact=self.contact.id,
                    email=email.id,
                    email_type=email_type.id)

        return data

    def post_required_data(self, contact=None, email=None, email_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactEmailApiTestCase, self).post_required_data(user, site)
        data.update(self.contact_email_data(contact, email, email_type))
        return data

    def verify_create_contact_email(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact email creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_email(self):
        self.verify_create_contact_email()

    def test_create_contact_email_partial(self):
        data = self.contact_email_data()
        self.verify_create_contact_email(data=data)

    def test_get_contact_email(self):
        self.verify_get_defaults()

    def test_put_contact_email_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_email(self):
        self.verify_delete_default()


class ContactFormattedNameApiTestCase(ContactAssociationApiTestCase):
    """ContactFormattedName  API unit test class."""
    factory_class = factories.ContactFormattedNameModelFactory
    model_class = models.ContactFormattedName
    serializer_class = serializers.ContactFormattedNameSerializer

    url_detail = "contact-formatted-name-detail"
    url_list = "contact-formatted-name-list"

    def setUp(self):
        super(ContactFormattedNameApiTestCase, self).setUp()
        self.name = FormattedNameModelFactory()

    def contact_formatted_name_data(self, contact=None, name=None):
        """return contact formatted name  data"""
        contact = contact or self.contact
        name = name or self.name

        data = dict(contact=self.contact.id, name=name.id)

        return data

    def post_required_data(self, contact=None, name=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactFormattedNameApiTestCase, self).post_required_data(user,
                                                                      site)
        data.update(self.contact_formatted_name_data(contact, name))
        return data

    def verify_create_contact_formatted_name(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact formatted name creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_formatted_name(self):
        self.verify_create_contact_formatted_name()

    def test_create_contact_formatted_name_partial(self):
        data = self.contact_formatted_name_data()
        self.verify_create_contact_formatted_name(data=data)

    def test_get_contact_formatted_name(self):
        self.verify_get_defaults()

    def test_put_contact_formatted_name_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_formatted_name(self):
        self.verify_delete_default()


class ContactGeographicLocationApiTestCase(ContactAssociationApiTestCase):
    """ContactGeographicLocation  API unit test class."""
    factory_class = factories.ContactGeographicLocationModelFactory
    model_class = models.ContactGeographicLocation
    serializer_class = serializers.ContactGeographicLocationSerializer

    url_detail = "contact-geographic-location-detail"
    url_list = "contact-geographic-location-list"

    def setUp(self):
        super(ContactGeographicLocationApiTestCase, self).setUp()
        self.geographic_location = GeographicLocationModelFactory()
        self.geographic_location_type = GeographicLocationTypeModelFactory()

    def contact_geographic_location_data(self, contact=None,
                                         geographic_location=None,
                                         geographic_location_type=None):
        """return contact geographic location data"""
        contact = contact or self.contact
        geographic_location = geographic_location or self.geographic_location
        geographic_location_type = (geographic_location_type or
                                    self.geographic_location_type)

        data = dict(contact=self.contact.id,
                    geographic_location=geographic_location.id,
                    geographic_location_type=geographic_location_type.id)

        return data

    def post_required_data(self, contact=None, geographic_location=None,
                           geographic_location_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactGeographicLocationApiTestCase, self).post_required_data(
                user, site)
        data.update(
            self.contact_geographic_location_data(contact,
                                                  geographic_location,
                                                  geographic_location_type))
        return data

    def verify_create_contact_geographic_location(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact geographic location creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_geographic_location(self):
        self.verify_create_contact_geographic_location()

    def test_create_contact_geographic_location_partial(self):
        data = self.contact_geographic_location_data()
        self.verify_create_contact_geographic_location(data=data)

    def test_get_contact_geographic_location(self):
        self.verify_get_defaults()

    def test_put_contact_geographic_location_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_geographic_location(self):
        self.verify_delete_default()


class ContactGroupApiTestCase(ContactAssociationApiTestCase):
    """ContactGroup API unit test class."""
    factory_class = factories.ContactGroupModelFactory
    model_class = models.ContactGroup
    serializer_class = serializers.ContactGroupSerializer

    url_detail = "contact-group-detail"
    url_list = "contact-group-list"

    def setUp(self):
        super(ContactGroupApiTestCase, self).setUp()
        self.group = GroupModelFactory()

    def contact_group_data(self, contact=None, group=None):
        """return contact geographic location data"""
        contact = contact or self.contact
        group = group or self.group

        data = dict(contact=self.contact.id, group=group.id)

        return data

    def post_required_data(self, contact=None, group=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactGroupApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_group_data(contact, group))
        return data

    def verify_create_contact_group(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact group creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_group(self):
        self.verify_create_contact_group()

    def test_create_contact_group_partial(self):
        data = self.contact_group_data()
        self.verify_create_contact_group(data=data)

    def test_get_contact_group(self):
        self.verify_get_defaults()

    def test_put_contact_group_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_group(self):
        self.verify_delete_default()


class ContactImageApiTestCase(ContactAssociationApiTestCase):
    """ContactImage API unit test class."""

    def setUp(self):
        super(ContactImageApiTestCase, self).setUp()
        self.image_reference = ImageReferenceModelFactory()

    def contact_image_data(self, contact=None, image_reference=None):
        """return contact geographic location data"""
        contact = contact or self.contact
        image_reference = image_reference or self.image_reference

        data = dict(contact=self.contact.id,
                    image_reference=image_reference.id)

        return data

    def post_required_data(self, contact=None, image_reference=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactImageApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_image_data(contact, image_reference))
        return data

    def verify_create_contact_image_reference(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact image reference creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance


class ContactLogoApiTestCase(ContactImageApiTestCase):
    """ContactLogo API unit test class."""
    factory_class = factories.ContactLogoModelFactory
    model_class = models.ContactLogo
    serializer_class = serializers.ContactLogoSerializer

    url_detail = "contact-logo-detail"
    url_list = "contact-logo-list"

    def setUp(self):
        super(ContactLogoApiTestCase, self).setUp()
        self.logo_type = LogoTypeModelFactory()

    def contact_logo_data(self, logo_type=None):
        """return contact logo data"""
        logo_type = logo_type or self.logo_type
        data = dict(logo_type=self.logo_type.id)
        return data

    def post_required_data(self, contact=None, image_reference=None,
                           logo_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactLogoApiTestCase, self).post_required_data(
                user, site, contact, image_reference)
        data.update(self.contact_logo_data(logo_type))
        return data

    def test_create_contact_logo(self):
        self.verify_create_contact_image_reference()

    def test_create_contact_logo_partial(self):
        data = self.contact_image_data()
        data.update(self.contact_logo_data())
        self.verify_create_contact_image_reference(data=data)

    def test_get_contact_logo(self):
        self.verify_get_defaults()

    def test_put_contact_logo_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_logo(self):
        self.verify_delete_default()


class ContactPhotoApiTestCase(ContactImageApiTestCase):
    """ContactPhoto API unit test class."""
    factory_class = factories.ContactPhotoModelFactory
    model_class = models.ContactPhoto
    serializer_class = serializers.ContactPhotoSerializer

    url_detail = "contact-photo-detail"
    url_list = "contact-photo-list"

    def setUp(self):
        super(ContactPhotoApiTestCase, self).setUp()
        self.photo_type = PhotoTypeModelFactory()

    def contact_photo_data(self, photo_type=None):
        """return contact photo data"""
        photo_type = photo_type or self.photo_type
        data = dict(photo_type=self.photo_type.id)
        return data

    def post_required_data(self, contact=None, image_reference=None,
                           photo_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactPhotoApiTestCase, self).post_required_data(
                user, site, contact, image_reference)
        data.update(self.contact_photo_data(photo_type))
        return data

    def test_create_contact_photo(self):
        self.verify_create_contact_image_reference()

    def test_create_contact_photo_partial(self):
        data = self.contact_image_data()
        data.update(self.contact_photo_data())
        self.verify_create_contact_image_reference(data=data)

    def test_get_contact_photo(self):
        self.verify_get_defaults()

    def test_put_contact_photo_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_photo(self):
        self.verify_delete_default()


class ContactInstantMessagingApiTestCase(ContactAssociationApiTestCase):
    """ContactInstantMessaging API unit test class."""
    factory_class = factories.ContactInstantMessagingModelFactory
    model_class = models.ContactInstantMessaging
    serializer_class = serializers.ContactInstantMessagingSerializer

    url_detail = "contact-instant-messaging-detail"
    url_list = "contact-instant-messaging-list"

    def setUp(self):
        super(ContactInstantMessagingApiTestCase, self).setUp()
        self.instant_messaging = InstantMessagingModelFactory()
        self.instant_messaging_type = InstantMessagingTypeModelFactory()

    def contact_instant_messaging_data(self, contact=None,
                                       instant_messaging=None,
                                       instant_messaging_type=None):
        """return contact instant_messaging data"""
        contact = contact or self.contact
        instant_messaging = instant_messaging or self.instant_messaging
        instant_messaging_type = (instant_messaging_type or
                                  self.instant_messaging_type)

        data = dict(contact=self.contact.id,
                    instant_messaging=instant_messaging.id,
                    instant_messaging_type=instant_messaging_type.id)

        return data

    def post_required_data(self, contact=None, instant_messaging=None,
                           instant_messaging_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactInstantMessagingApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_instant_messaging_data(
            contact,
            instant_messaging,
            instant_messaging_type))
        return data

    def verify_create_contact_instant_messaging(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact instant messaging creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_instant_messaging(self):
        self.verify_create_contact_instant_messaging()

    def test_create_contact_instant_messaging_partial(self):
        data = self.contact_instant_messaging_data()
        self.verify_create_contact_instant_messaging(data=data)

    def test_get_contact_instant_messaging(self):
        self.verify_get_defaults()

    def test_put_contact_instant_messaging_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_instant_messaging(self):
        self.verify_delete_default()


class ContactLanguageApiTestCase(ContactAssociationApiTestCase):
    """ContactLanguage API unit test class."""
    factory_class = factories.ContactLanguageModelFactory
    model_class = models.ContactLanguage
    serializer_class = serializers.ContactLanguageSerializer

    url_detail = "contact-language-detail"
    url_list = "contact-language-list"

    def setUp(self):
        super(ContactLanguageApiTestCase, self).setUp()
        self.language = LanguageModelFactory()
        self.language_type = LanguageTypeModelFactory()

    def contact_language_data(self, contact=None,
                              language=None, language_type=None):
        """return contact language data"""
        contact = contact or self.contact
        language = language or self.language
        language_type = (language_type or self.language_type)

        data = dict(contact=self.contact.id,
                    language=language.id,
                    language_type=language_type.id)

        return data

    def post_required_data(self, contact=None, language=None,
                           language_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactLanguageApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_language_data(
            contact,
            language,
            language_type))
        return data

    def verify_create_contact_language(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact language creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_language(self):
        self.verify_create_contact_language()

    def test_create_contact_language_partial(self):
        data = self.contact_language_data()
        self.verify_create_contact_language(data=data)

    def test_get_contact_language(self):
        self.verify_get_defaults()

    def test_put_contact_language_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_language(self):
        self.verify_delete_default()


class ContactNameApiTestCase(ContactAssociationApiTestCase):
    """ContactName API unit test class."""
    factory_class = factories.ContactNameModelFactory
    model_class = models.ContactName
    serializer_class = serializers.ContactNameSerializer

    url_detail = "contact-name-detail"
    url_list = "contact-name-list"

    def setUp(self):
        super(ContactNameApiTestCase, self).setUp()
        self.name = NameModelFactory()

    def contact_name_data(self, contact=None, name=None):
        """return contact name data"""
        contact = contact or self.contact
        name = name or self.name

        data = dict(contact=self.contact.id,
                    name=name.id)

        return data

    def post_required_data(self, contact=None, name=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactNameApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_name_data(
            contact,
            name))
        return data

    def verify_create_contact_name(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact name creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_name(self):
        self.verify_create_contact_name()

    def test_create_contact_name_partial(self):
        data = self.contact_name_data()
        self.verify_create_contact_name(data=data)

    def test_get_contact_name(self):
        self.verify_get_defaults()

    def test_put_contact_name_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_name(self):
        self.verify_delete_default()


class ContactNicknameApiTestCase(ContactAssociationApiTestCase):
    """ContactNickname API unit test class."""
    factory_class = factories.ContactNicknameModelFactory
    model_class = models.ContactNickname
    serializer_class = serializers.ContactNicknameSerializer

    url_detail = "contact-nickname-detail"
    url_list = "contact-nickname-list"

    def setUp(self):
        super(ContactNicknameApiTestCase, self).setUp()
        self.name = NicknameModelFactory()
        self.nickname_type = NicknameTypeModelFactory()

    def contact_nickname_data(self, contact=None,
                              name=None, nickname_type=None):
        """return contact nickname data"""
        contact = contact or self.contact
        name = name or self.name
        nickname_type = nickname_type or self.nickname_type

        data = dict(contact=self.contact.id,
                    name=name.id,
                    nickname_type=nickname_type.id)

        return data

    def post_required_data(self, contact=None, name=None,
                           nickname_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactNicknameApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_nickname_data(
            contact,
            name,
            nickname_type))
        return data

    def verify_create_contact_nickname(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact nickname creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_nickname(self):
        self.verify_create_contact_nickname()

    def test_create_contact_nickname_partial(self):
        data = self.contact_nickname_data()
        self.verify_create_contact_nickname(data=data)

    def test_get_contact_nickname(self):
        self.verify_get_defaults()

    def test_put_contact_nickname_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_nickname(self):
        self.verify_delete_default()


class ContactOrganizationApiTestCase(ContactAssociationApiTestCase):
    """ContactOrganization API unit test class."""
    factory_class = factories.ContactOrganizationModelFactory
    model_class = models.ContactOrganization
    serializer_class = serializers.ContactOrganizationSerializer

    url_detail = "contact-organization-detail"
    url_list = "contact-organization-list"

    def setUp(self):
        super(ContactOrganizationApiTestCase, self).setUp()
        self.organization = OrganizationModelFactory()
        self.unit = OrganizationUnitModelFactory()

    def contact_organization_data(self, contact=None,
                                  organization=None,
                                  unit=None):
        """return contact organization data"""
        contact = contact or self.contact
        organization = organization or self.organization
        unit = unit or self.unit

        data = dict(contact=self.contact.id,
                    organization=organization.id,
                    unit=unit.id)

        return data

    def post_required_data(self, contact=None, organization=None,
                           unit=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactOrganizationApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_organization_data(
            contact,
            organization,
            unit))
        return data

    def verify_create_contact_organization(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact organization creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_organization(self):
        self.verify_create_contact_organization()

    def test_create_contact_organization_partial(self):
        data = self.contact_organization_data()
        self.verify_create_contact_organization(data=data)

    def test_get_contact_organization(self):
        self.verify_get_defaults()

    def test_put_contact_organization_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_organization(self):
        self.verify_delete_default()


class ContactPhoneApiTestCase(ContactAssociationApiTestCase):
    """ContactPhone API unit test class."""
    factory_class = factories.ContactPhoneModelFactory
    model_class = models.ContactPhone
    serializer_class = serializers.ContactPhoneSerializer

    url_detail = "contact-phone-detail"
    url_list = "contact-phone-list"

    def setUp(self):
        super(ContactPhoneApiTestCase, self).setUp()
        self.phone = PhoneModelFactory()
        self.phone_type = PhoneTypeModelFactory()

    def contact_phone_data(self, contact=None,
                           phone=None, phone_type=None):
        """return contact organization data"""
        contact = contact or self.contact
        phone = phone or self.phone
        phone_type = phone_type or self.phone_type

        data = dict(contact=self.contact.id,
                    phone=phone.id,
                    phone_type=phone_type.id)

        return data

    def post_required_data(self, contact=None, phone=None,
                           phone_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactPhoneApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_phone_data(
            contact,
            phone,
            phone_type))
        return data

    def verify_create_contact_phone(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact phone creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_phone(self):
        self.verify_create_contact_phone()

    def test_create_contact_phone_partial(self):
        data = self.contact_phone_data()
        self.verify_create_contact_phone(data=data)

    def test_get_contact_phone(self):
        self.verify_get_defaults()

    def test_put_contact_phone_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_phone(self):
        self.verify_delete_default()


class ContactRoleApiTestCase(ContactAssociationApiTestCase):
    """ContactRole API unit test class."""
    factory_class = factories.ContactRoleModelFactory
    model_class = models.ContactRole
    serializer_class = serializers.ContactRoleSerializer

    url_detail = "contact-role-detail"
    url_list = "contact-role-list"

    def setUp(self):
        super(ContactRoleApiTestCase, self).setUp()
        self.role = RoleModelFactory()
        self.organization = OrganizationModelFactory()

    def contact_role_data(self, contact=None,
                          role=None, organization=None):
        """return contact role data"""
        contact = contact or self.contact
        role = role or self.role
        organization = organization or self.organization

        data = dict(contact=self.contact.id,
                    role=role.id,
                    organization=organization.id)

        return data

    def post_required_data(self, contact=None, role=None,
                           organization=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactRoleApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_role_data(
            contact,
            role,
            organization))
        return data

    def verify_create_contact_role(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact role creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_role(self):
        self.verify_create_contact_role()

    def test_create_contact_role_partial(self):
        data = self.contact_role_data()
        self.verify_create_contact_role(data=data)

    def test_get_contact_role(self):
        self.verify_get_defaults()

    def test_put_contact_role_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_role(self):
        self.verify_delete_default()


class ContactTimezoneApiTestCase(ContactAssociationApiTestCase):
    """ContactTimezone API unit test class."""
    factory_class = factories.ContactTimezoneModelFactory
    model_class = models.ContactTimezone
    serializer_class = serializers.ContactTimezoneSerializer

    url_detail = "contact-timezone-detail"
    url_list = "contact-timezone-list"

    def setUp(self):
        super(ContactTimezoneApiTestCase, self).setUp()
        self.timezone = TimezoneModelFactory()
        self.timezone_type = TimezoneTypeModelFactory()

    def contact_timezone_data(self, contact=None,
                              timezone=None, timezone_type=None):
        """return contact timezone data"""
        contact = contact or self.contact
        timezone = timezone or self.timezone
        timezone_type = timezone_type or self.timezone_type

        data = dict(contact=self.contact.id,
                    timezone=timezone.id,
                    timezone_type=timezone_type.id)

        return data

    def post_required_data(self, contact=None, timezone=None,
                           timezone_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactTimezoneApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_timezone_data(
            contact,
            timezone,
            timezone_type))
        return data

    def verify_create_contact_timezone(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact timezone creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_timezone(self):
        self.verify_create_contact_timezone()

    def test_create_contact_timezone_partial(self):
        data = self.contact_timezone_data()
        self.verify_create_contact_timezone(data=data)

    def test_get_contact_timezone(self):
        self.verify_get_defaults()

    def test_put_contact_timezone_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_timezone(self):
        self.verify_delete_default()


class ContactTitleApiTestCase(ContactAssociationApiTestCase):
    """ContactTitle API unit test class."""
    factory_class = factories.ContactTitleModelFactory
    model_class = models.ContactTitle
    serializer_class = serializers.ContactTitleSerializer

    url_detail = "contact-title-detail"
    url_list = "contact-title-list"

    def setUp(self):
        super(ContactTitleApiTestCase, self).setUp()
        self.title = TitleModelFactory()
        self.organization = OrganizationModelFactory()

    def contact_title_data(self, contact=None,
                           title=None, organization=None):
        """return contact title data"""
        contact = contact or self.contact
        title = title or self.title
        organization = organization or self.organization

        data = dict(contact=self.contact.id,
                    title=title.id,
                    organization=organization.id)

        return data

    def post_required_data(self, contact=None, title=None,
                           title_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactTitleApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_title_data(
            contact,
            title,
            title_type))
        return data

    def verify_create_contact_title(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact title creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_title(self):
        self.verify_create_contact_title()

    def test_create_contact_title_partial(self):
        data = self.contact_title_data()
        self.verify_create_contact_title(data=data)

    def test_get_contact_title(self):
        self.verify_get_defaults()

    def test_put_contact_title_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_title(self):
        self.verify_delete_default()


class ContactUrlApiTestCase(ContactAssociationApiTestCase):
    """ContactUrl API unit test class."""
    factory_class = factories.ContactUrlModelFactory
    model_class = models.ContactUrl
    serializer_class = serializers.ContactUrlSerializer

    url_detail = "contact-url-detail"
    url_list = "contact-url-list"

    def setUp(self):
        super(ContactUrlApiTestCase, self).setUp()
        self.url = UrlModelFactory()
        self.url_type = UrlTypeModelFactory()

    def contact_url_data(self, contact=None,
                         url=None, url_type=None):
        """return contact url data"""
        contact = contact or self.contact
        url = url or self.url
        url_type = url_type or self.url_type

        data = dict(contact=self.contact.id,
                    url=url.id,
                    url_type=url_type.id)

        return data

    def post_required_data(self, contact=None, url=None,
                           url_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactUrlApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_url_data(
            contact,
            url,
            url_type))
        return data

    def verify_create_contact_url(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact url creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_contact_url(self):
        self.verify_create_contact_url()

    def test_create_contact_url_partial(self):
        data = self.contact_url_data()
        self.verify_create_contact_url(data=data)

    def test_get_contact_url(self):
        self.verify_get_defaults()

    def test_put_contact_url_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_contact_url(self):
        self.verify_delete_default()


class RelatedContactApiTestCase(ContactAssociationApiTestCase):
    """RelatedContact API unit test class."""
    factory_class = factories.RelatedContactModelFactory
    model_class = models.RelatedContact
    serializer_class = serializers.RelatedContactSerializer

    url_detail = "related-contact-detail"
    url_list = "related-contact-list"

    def setUp(self):
        super(RelatedContactApiTestCase, self).setUp()
        self.to_contact = factories.ContactModelFactory()
        self.contact_relationship_type = (
            factories.ContactRelationshipTypeModelFactory())

    def related_contact_data(self, from_contact=None,
                             to_contact=None,
                             contact_relationship_type=None):
        """return related contact data"""
        from_contact = from_contact or self.contact
        to_contact = to_contact or self.to_contact
        contact_relationship_type = (contact_relationship_type or
                                     self.contact_relationship_type)

        data = dict(from_contact=from_contact.id,
                    to_contact=to_contact.id,
                    contact_relationship_type=contact_relationship_type.id)

        return data

    def post_required_data(self, contact=None, to_contact=None,
                           contact_relationship_type=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            RelatedContactApiTestCase, self).post_required_data(
                user, site)
        data.update(self.related_contact_data(
            contact,
            to_contact,
            contact_relationship_type))
        return data

    def verify_create_related_contact(
            self,
            data=None, extra_attrs=None):
        """Generate post request for contact url creation."""
        data = data or self.post_required_data()

        response, instance = self.verify_create(
            url_name=self.url_list,
            data=data,
            model_class=self.model_class)

        self.verify_contact_association(instance, data)
        return response, instance

    def test_create_related_contact(self):
        self.verify_create_related_contact()

    def test_create_related_contact_partial(self):
        data = self.related_contact_data()
        self.verify_create_related_contact(data=data)

    def test_get_related_contact(self):
        self.verify_get_defaults()

    def test_put_related_contact_partial(self):
        instance = self.create_instance_default()

        # @TODO: need to limit what can be updated
        data = dict(id=instance.id, priority=5)
        self.verify_put(self.url_detail, instance, data, self.serializer_class)

    def test_delete_related_contact(self):
        self.verify_delete_default()
