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
from django_core_models.locations.tests.factories import (
    USAddressModelFactory,
    AddressTypeModelFactory,
    GeographicLocationModelFactory,
    GeographicLocationTypeModelFactory)
from django_core_models.social_media.tests.factories import (
    EmailModelFactory,
    EmailTypeModelFactory,
    FormattedNameModelFactory)


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

    def post_required_data(self, contact=None, name=None,
                           user=None, site=None):
        """Return model post request required data."""
        data = super(
            ContactGeographicLocationApiTestCase, self).post_required_data(
                user, site)
        data.update(self.contact_geographic_location_data(contact, name))
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
