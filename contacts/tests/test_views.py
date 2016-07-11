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
    GeographicLocationTypeModelFactory)
from django_core_models.social_media.tests.factories import (
    EmailModelFactory,
    EmailTypeModelFactory,
    FormattedNameModelFactory,
    GroupModelFactory,
    InstantMessagingModelFactory,
    InstantMessagingTypeModelFactory,
    LogoTypeModelFactory,
    PhotoTypeModelFactory)


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
        """Generate post request for contact group creation."""
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
