"""
.. module::  contacts.signals
   :synopsis:  Django contacts application signals  module.

Django contacts application configuration  module.

"""
from __future__ import absolute_import
import logging
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django_core_utils.utils import current_site

from guardian.shortcuts import assign_perm

from . import models

logger = logging.getLogger(__name__)


def _create_params(user, **kwargs):
    """Return dict of fields to be used as create params."""
    site = kwargs.pop("site", current_site())
    creation_user = kwargs.pop("creation_user", user)
    effective_user = kwargs.pop("effective_user", user)
    update_user = kwargs.pop("update_user", user)
    params = dict(
        creation_user=creation_user, effective_user=effective_user,
        site=site, update_user=update_user)
    params.update(kwargs)
    return params


def _assign_permissions(contact, permission, targets):
    """Grant contact permission to collection of users or groups"""
    for target in targets:
        assign_perm(permission, target, contact)


@receiver(post_save, sender=models.Contact)
def contact_post_save(sender, **kwargs):
    """
    Create per contact instance access permissions.
    """
    contact, created = kwargs["instance"], kwargs["created"]
    if created:
        user = contact.creation_user
        if (user.username != settings.ANONYMOUS_USER_NAME and
                settings.USE_OBJECT_PERMISSIONS):
            # assign owner permissions
            for permission in models.PERMISSIONS_CONTACT_OBJECT:
                assign_perm(permission, user, contact)
            # assign permissions from user profile
            try:
                profile = models.UserProfile.objects.get(user=user)
            except models.UserProfile.DoesNotExist:
                logger.exception("expected profile for user %s missing", user)
                raise
            permissions = [models.PERMISSION_READ, models.PERMISSION_WRITE] * 2
            permission_targets = [
                profile.users_read.all(), profile.users_write.all(),
                profile.groups_read.all(), profile.groups_write.all()]
            for permission, target in zip(permissions, permission_targets):
                _assign_permissions(contact, permission, target)


@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
    """
    Create a ContactsUserProfile instance for all newly created User instances.
    """
    user, created = kwargs["instance"], kwargs["created"]
    if (created and user.username != settings.ANONYMOUS_USER_NAME and
            settings.USE_OBJECT_PERMISSIONS):
        models.UserProfile.objects.create(user=user)
