"""
.. module::  contacts.tests.test_permissions
   :synopsis: contacts application permissions unit test module.

*contacts* application permissions unit test module.
"""

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from guardian.shortcuts import assign_perm
from django.shortcuts import get_object_or_404
from django_core_utils.tests.test_utils import BaseModelTestCase
from django_core_utils.tests.factories import GroupFactory
from . import factories
from . import test_models
from .. import models


class PermissionsTestCase(BaseModelTestCase):
    """Permission  unit test class.
    """
    def create_contact(self, **kwargs):

        instance = factories.ContactModelFactory(**kwargs)
        instance.clean()
        return instance


class VerifyObjectPermissionTestCase(test_models.PermissionsMixin,
                                     PermissionsTestCase):
    """Object permission functional verification unit test class."""

    def setUp(self):
        test_models.PermissionsMixin.setUp(self)
        PermissionsTestCase.setUp(self)

    def tearDown(self):
        PermissionsTestCase.tearDown(self)
        test_models.PermissionsMixin.tearDown(self)

    def test_contact_function_default_permission(self):
        for permission in models.PERMISSIONS_CONTACT_FUNCTIONAL:
            self.assertFalse(self.user.has_perm(permission))

    def test_contact_functional_permission_set(self):
        self.assertFalse(self.user.has_perm(models.PERMISSION_ADD))
        content_type = ContentType.objects.get_for_model(models.Contact)
        permission = Permission.objects.get(
            codename="add_contact",
            content_type=content_type)
        self.user.user_permissions.set([permission])
        # need to bypass cache
        user = get_object_or_404(User, pk=self.user.id)
        self.assertTrue(user.has_perm(models.PERMISSION_ADD))

    def test_contact_object_default_no_permission(self):
        contact = self.create_contact()
        for permission in models.PERMISSIONS_CONTACT_OBJECT:
            self.assertFalse(self.user.has_perm(permission, contact))

    def test_contact_object_set_permission_user(self):
        contact = self.create_contact()
        self.assertFalse(self.user.has_perm(models.PERMISSION_READ, contact))
        assign_perm(models.PERMISSION_READ, self.user, contact)
        self.assertTrue(self.user.has_perm(models.PERMISSION_READ, contact))

    def test_contact_object_set_permission_group(self):
        contact = self.create_contact()
        group = GroupFactory()
        assign_perm(models.PERMISSION_READ, group, contact)
        self.assertFalse(self.user.has_perm(models.PERMISSION_READ, contact))
        self.user.groups.add(group)
        self.assertTrue(self.user.has_perm(models.PERMISSION_READ, contact))


class ContactPermissionTestCase(PermissionsTestCase):
    """Contact permission unit test class."""
    def setUp(self):
        # Before creation of test user and  super user
        self.assertEqual(models.UserProfile.objects.count(), 0)
        super(ContactPermissionTestCase, self).setUp()
        # After creation of test user and  super user
        self.assertEqual(models.UserProfile.objects.count(), 2)

    def test_contact_permission_signal_simple_profile(self):
        self.assertEqual(models.ContactObjectPermission.objects.count(), 0)
        contact = self.create_contact()
        for permission in models.PERMISSIONS_CONTACT_OBJECT:
            self.assertTrue(self.user.has_perm(permission, contact))
        self.assertEqual(models.ContactObjectPermission.objects.count(),
                         len(models.PERMISSIONS_CONTACT_OBJECT))
        contact.delete()
        self.assertEqual(models.ContactObjectPermission.objects.count(), 0)

    def test_contact_permission_signal_complex_profile(self):
        # set up profile with group data, from which
        # the permissions are derived
        self.assertEqual(models.ContactObjectPermission.objects.count(), 0)
        profile = models.UserProfile.objects.get(user=self.user)
        user = factories.UserFactory()
        group = GroupFactory()
        user.groups.add(group)

        profile.groups_read.add(group)
        profile.groups_write.add(group)
        contact = self.create_contact()
        # based on the profile setup, following contact creation would
        # expect to have two for the user, and two for the group
        self.assertEqual(
            models.ContactObjectPermission.objects.count(), 2)
        self.assertEqual(
            models.ContactGroupObjectPermission.objects.count(), 2)

        for permission in models.PERMISSIONS_CONTACT_OBJECT:
            self.assertTrue(user.has_perm(permission, contact))

        contact.delete()
        self.assertEqual(models.ContactObjectPermission.objects.count(), 0)
