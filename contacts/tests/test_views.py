"""
.. module::  django_core_models.social_media.tests.test_views
   :synopsis: social_media models application views unit test module.

*social_media*  application views unit test module.
"""
from __future__ import absolute_import, print_function
from django_core_utils.tests.api_test_utils import (NamedModelApiTestCase,
                                                    VersionedModelApiTestCase)

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
    factory_class = factories.ContactModelFactory
    model_class = models.Contact
    serializer_class = serializers.ContactSerializer

    url_detail = "contact-detail"
    url_list = "contact-list"

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

    url_detail = "contacts-detail"
    url_list = "contacts-list"

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
