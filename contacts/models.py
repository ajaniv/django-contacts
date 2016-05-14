"""
.. module::  contacts.models
   :synopsis:  Contact models module.

Contact models module.  A primary design decision was to be inspired by key
abstractions from rfc6350 "vCard Format Specification".  In addition to design
reuse, the objective is to be able to import and export data in compliance
with rfc6350.

This lead to a more complex business object model.  The intention is
to hide the complexity  in the client application.

VCard import/export per VCard spec version issues have to be handled
by the import/export process logic.  There may be cases were
an import->export process will not yield an exact "equal" VCard instance.

One of the design principles adhered to was allowing the grouping, tagging,
or organization of instances using the definition of an associated 'Type' class
(i.e. Phone->PhoneType, Email->EmailType)
"""
#
# Note: Adding db table name naming convention control to allow flexible
#    integration of the application in target db environments.
#    Have not found a way to have a class decorator simplify the
#    implementation with Django 1.9.  A db table is named using the following
#    substrings, each separated by an '_':
#    a) Site label (i.e. 'sl')
#    b) Application name (i.e. contacts)
#    c) Class name in lower case with underscores (i.e. contact_name)
#    Based on the above, for a class named ContactName, the db table name
#    would be:
#        'sl_contacts_contact_name'
#

# @TODO: add missing rfc6350 fields (i.e. Contact Key, audio, Media
#        see https://github.com/areski/django-audiofield)
# @TODO: For image, review approach to have bundled
#        thumbnail/compressed version
# @TODO: check implementation of related contact when uri is used,not contact
#        defined in model
# @TODO: contact accesss requires quite a few joins, look at optimization
# @TODO: str methods
# @TODO: review on_delete=CASCADE for reference data types
#        in many-2-many relationships
# @TODO: review manager add/remove method implementation; too many methods
from __future__ import absolute_import

# @TODO: review class field layout
# @TODO: review each of the types, determine which should be optional
import logging
from inflection import humanize, pluralize, underscore

from django.conf import settings
import django.contrib.auth.models
from django.db.models import Model
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _

from guardian.models import UserObjectPermissionBase
from guardian.models import GroupObjectPermissionBase


from python_core_utils.core import class_name
from django_core_utils import fields

from django_core_models.core.models import Annotation, Category
from django_core_models.demographics.models import Gender
from django_core_models.images.models import ImageReference
from django_core_models.locations.models import (Address, AddressType,
                                                 GeographicLocation,
                                                 GeographicLocationType,
                                                 Language, LanguageType,
                                                 Timezone, TimezoneType)
from django_core_models.organizations.models import (Organization,
                                                     OrganizationUnit, Role,
                                                     Title)
from django_core_models.social_media.models import (Email, EmailType,
                                                    FormattedName, Group,
                                                    InstantMessaging,
                                                    InstantMessagingType,
                                                    LogoType, Name, Nickname,
                                                    NicknameType, Phone,
                                                    PhoneType, PhotoType, Url,
                                                    UrlType)

from django_core_utils.models import (NamedModel, PrioritizedModel,
                                      VersionedModelManager,
                                      db_table, related_name_base)


from . import validation

logger = logging.getLogger(__name__)
_app_label = 'contacts'


def create_fields(instance, **kwargs):
    """Return dict of fields to be used as create params."""
    site = kwargs.pop("site", instance.site)
    creation_user = kwargs.pop("creation_user", instance.creation_user)
    effective_user = kwargs.pop("effective_user", instance.effective_user)
    update_user = kwargs.pop("update_user", instance.update_user)
    params = dict(
        creation_user=creation_user, effective_user=effective_user,
        site=site, update_user=update_user)
    params.update(kwargs)
    return params


def delete_association(association_class, **kwargs):
    """Remove an association.

    Requires deletion when using 'through'.
    """

    try:
        instance = association_class.objects.get(**kwargs)
    except association_class.DoesNotExist:
        logger.exception(
            "%s instance with kwargs %s not found",
            class_name(association_class), kwargs)
        raise

    return instance.delete()


def create_association(association_class, **kwargs):
    """Create association instance."""
    return association_class.objects.create(**kwargs)

_contact_type = "ContactType"
_contact_type_vebose = humanize(underscore(_contact_type))


class ContactType(NamedModel):
    """Contact type model class.

    Allows the organization of contacts into logical types.
    Values may include individual, organization, unknown.
    """
    # @TODO: is this duplicate of category?
    class Meta(NamedModel.Meta):
        """Model meta class declaration."""
        app_label = _app_label
        db_table = db_table(_app_label, _contact_type)
        verbose_name = _(_contact_type_vebose)
        verbose_name_plural = _(pluralize(_contact_type_vebose))


_related_contact_type = "ContactRelationshipType"
_related_contact_type_verbose = humanize(underscore(_related_contact_type))


class ContactRelationshipType(NamedModel):
    """Related contact type model class.

    Allows classification of contact relationships.
    Sample values may include "unknown",
    "acquaintance", "parent", "child", "co-worker",  "friend"
    """
    class Meta(NamedModel.Meta):
        app_label = _app_label
        db_table = db_table(_app_label, _related_contact_type)
        verbose_name = _(_related_contact_type_verbose)
        verbose_name_plural = _(pluralize(_related_contact_type_verbose))


class ContactsModel(PrioritizedModel):
    """Base contacts class."""
    class Meta(PrioritizedModel.Meta):
        """Model meta class declaration."""
        app_label = _app_label
        abstract = True


class ContactManager(VersionedModelManager):
    """Contact manager class."""

    def address_add(self, contact, address, **kwargs):
        """Add contact and address association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactAddress, contact=contact,
            address=address, **params)

    def address_remove(self, contact, address, **kwargs):
        """Remove contact and address association."""
        return delete_association(
            ContactAddress, contact=contact, address=address)

    def annotation_add(self, contact, annotation, **kwargs):
        """Add contact and annotation association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactAnnotation, contact=contact,
            annotation=annotation, **params)

    def annotation_remove(self, contact, annotation, **kwargs):
        """Remove contact and annotation association."""
        return delete_association(
            ContactAnnotation, contact=contact, annotation=annotation)

    def category_add(self, contact, category, **kwargs):
        """Add contact and categry association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactCategory, contact=contact,
            category=category, **params)

    def category_remove(self, contact, category):
        """Remove contact and category association."""
        return delete_association(
            ContactCategory, contact=contact, category=category)

    def email_add(self, contact, email, **kwargs):
        """Add contact and email association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactEmail, contact=contact,
            email=email, **params)

    def email_remove(self, contact, email):
        """Remove contact and email association."""
        return delete_association(
            ContactEmail, contact=contact, email=email)

    def formatted_name_add(self, contact, name, **kwargs):
        """Add contact and formatted name association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactFormattedName, contact=contact,
            name=name, **params)

    def formatted_name_remove(self, contact, name):
        """Remove contact and formatted name association."""
        return delete_association(
            ContactFormattedName, contact=contact, name=name)

    def geographic_location_add(self, contact, geographic_location, **kwargs):
        """Add contact and geographic location association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactGeographicLocation, contact=contact,
            geographic_location=geographic_location, **params)

    def geographic_location_remove(self, contact, geographic_location):
        """Remove contact and geographic location association."""
        return delete_association(
            ContactGeographicLocation, contact=contact,
            geographic_location=geographic_location)

    def group_add(self, contact, group, **kwargs):
        """Add contact and group association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactGroup, contact=contact,
            group=group, **params)

    def group_remove(self, contact, group):
        """Remove contact and group association."""
        return delete_association(
            ContactGroup, contact=contact, group=group)

    def instant_messaging_add(self, contact, instant_messaging, **kwargs):
        """Add contact and instant messaging association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactInstantMessaging, contact=contact,
            instant_messaging=instant_messaging, **params)

    def instant_messaging_remove(self, contact, instant_messaging):
        """Remove contact and instant_messaging association."""
        return delete_association(
            ContactInstantMessaging, contact=contact,
            instant_messaging=instant_messaging)

    def language_add(self, contact, language, **kwargs):
        """Add contact and language association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactLanguage, contact=contact,
            language=language, **params)

    def language_remove(self, contact, language):
        """Remove contact and language association."""
        return delete_association(
            ContactLanguage, contact=contact,
            language=language)

    def logo_add(self, contact, image_reference, **kwargs):
        """Add contact and logo  association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactLogo, contact=contact,
            image_reference=image_reference, **params)

    def logo_remove(self, contact, image_reference):
        """Remove contact and logo association."""
        return delete_association(
            ContactLogo, contact=contact,
            image_reference=image_reference)

    def name_add(self, contact, name, **kwargs):
        """Add contact and name association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactName, contact=contact,
            name=name, **params)

    def name_remove(self, contact, name):
        """Remove contact and name association."""
        return delete_association(ContactName, contact=contact, name=name)

    def nickname_add(self, contact, name, **kwargs):
        """Add contact and nickname association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactNickname, contact=contact,
            name=name, **params)

    def nickname_remove(self, contact, name):
        """Remove contact and nickname association."""
        return delete_association(ContactNickname, contact=contact, name=name)

    def organization_add(self, contact, organization, **kwargs):
        """Add contact and organization association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactOrganization, contact=contact,
            organization=organization, **params)

    def organization_remove(self, contact, organization):
        """Remove contact and organization association."""
        return delete_association(
            ContactOrganization, contact=contact, organization=organization)

    def phone_add(self, contact, phone, **kwargs):
        """Add contact and phone association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactPhone, contact=contact,
            phone=phone, **params)

    def phone_remove(self, contact, phone):
        """Remove contact and phone association."""
        return delete_association(
            ContactPhone, contact=contact, phone=phone)

    def photo_add(self, contact, image_reference, **kwargs):
        """Add contact and photo association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactPhoto, contact=contact,
            image_reference=image_reference, **params)

    def photo_remove(self, contact, image_reference):
        """Remove contact and photo association."""
        return delete_association(
            ContactPhoto, contact=contact, image_reference=image_reference)

    def related_contact_add(self, from_contact, to_contact, **kwargs):
        """Add contact and photo association."""
        params = create_fields(from_contact, **kwargs)
        return create_association(
            RelatedContact, from_contact=from_contact,
            to_contact=to_contact, **params)

    def related_contact_remove(self, from_contact, to_contact):
        """Remove contact and photo association."""
        return delete_association(
            RelatedContact, from_contact=from_contact, to_contact=to_contact)

    def role_add(self, contact, role, **kwargs):
        """Add contact and role association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactRole, contact=contact,
            role=role, **params)

    def role_remove(self, contact, role):
        """Remove contact and role association."""
        return delete_association(
            ContactRole, contact=contact, role=role)

    def timezone_add(self, contact, timezone, **kwargs):
        """Add contact and timezone association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactTimezone, contact=contact,
            timezone=timezone, **params)

    def timezone_remove(self, contact, timezone):
        """Remove contact and timezone association."""
        return delete_association(
            ContactTimezone, contact=contact, timezone=timezone)

    def title_add(self, contact, title, **kwargs):
        """Add contact and title association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactTitle, contact=contact,
            title=title, **params)

    def title_remove(self, contact, title):
        """Remove contact and title association."""
        return delete_association(
            ContactTitle, contact=contact, title=title)

    def url_add(self, contact, url, **kwargs):
        """Add contact and url association."""
        params = create_fields(contact, **kwargs)
        return create_association(
            ContactUrl, contact=contact,
            url=url, **params)

    def url_remove(self, contact, url):
        """Remove contact and url association."""
        return delete_association(
            ContactUrl, contact=contact, url=url)

_contact = "Contact"
_contact_verbose = humanize(underscore(_contact))


class Contact(ContactsModel):
    """Contact model class.

    Capture contact attributes.  Designed to allow having multiple contact
    instances per person, organization, etc.

    Either name or formatted name have to be set on an instance.
    """
    formatted_name = fields.foreign_key_field(
        FormattedName, blank=True, null=True)
    name = fields.foreign_key_field(Name, blank=True, null=True)

    # 'simple fields'
    anniversary = fields.date_field(blank=True, null=True)
    birth_date = fields.date_field(blank=True, null=True)
    contact_type = fields.foreign_key_field(ContactType, blank=True, null=True)
    gender = fields.foreign_key_field(Gender, blank=True, null=True)

    # many-2-many fields
    addresses = fields.many_to_many_field(Address, through="ContactAddress")
    annotations = fields.many_to_many_field(Annotation,
                                            through="ContactAnnotation")
    categories = fields.many_to_many_field(Category,
                                           through="ContactCategory")
    emails = fields.many_to_many_field(Email,
                                       through="ContactEmail")
    formatted_names = fields.many_to_many_field(FormattedName,
                                                through="ContactFormattedName")
    geographic_locations = fields.many_to_many_field(
        GeographicLocation, through="ContactGeographicLocation")
    groups = fields.many_to_many_field(Group,
                                       through="ContactGroup")
    instant_messaging = fields.many_to_many_field(
        InstantMessaging, through="ContactInstantMessaging")
    languages = fields.many_to_many_field(Language, through="ContactLanguage")
    logos = fields.many_to_many_field(
        ImageReference, through="ContactLogo",
        related_name=related_name_base + "contact_logo")
    names = fields.many_to_many_field(Name, through="ContactName")
    nicknames = fields.many_to_many_field(Nickname,
                                          through="ContactNickname")
    organizations = fields.many_to_many_field(Organization,
                                              through="ContactOrganization")
    phones = fields.many_to_many_field(Phone,
                                       through="ContactPhone")
    photos = fields.many_to_many_field(
        ImageReference, through="ContactPhoto",
        related_name=related_name_base + "contact_photo")
    related_contacts = fields.many_to_many_field(
        "self", through="RelatedContact", symmetrical=False)
    roles = fields.many_to_many_field(Role, through="ContactRole")
    timezones = fields.many_to_many_field(Timezone, through="ContactTimezone")
    titles = fields.many_to_many_field(Title, through="ContactTitle")
    urls = fields.many_to_many_field(Url, through="ContactUrl")

    objects = ContactManager()

    class Meta(ContactsModel.Meta):
        db_table = db_table(_app_label, _contact)
        verbose_name = _(_contact_verbose)
        verbose_name_plural = _(pluralize(_contact_verbose))
        permissions = (
            ("read_contact", "Can read contacts"),
            ("write_contact", "Can write contacts"),
        )

    def clean(self):
        super(Contact, self).clean()
        validation.name_validation(self.name, self.formatted_name)

    @property
    def display_name(self):
        return self.name if self.name else self.formatted_name


class ContactAssociation(ContactsModel):
    """Base class for contact association."""
    class Meta(ContactsModel.Meta):
        abstract = True

_contact_address = "ContactAddress"
_contact_address_verbose = humanize(underscore(_contact_address))


class ContactAddress(ContactAssociation):
    """Contact address model class.

    Capture the attributes of contact address(s).
    A contact may be associated with 0 or more addresses as follows:
    Contact(1)  -------> ContactAddress(0..*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    address = fields.foreign_key_field(Address, on_delete=CASCADE)
    address_type = fields.foreign_key_field(AddressType, null=True, blank=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_address)
        verbose_name = _(_contact_address_verbose)
        verbose_name_plural = _(pluralize(_contact_address_verbose))
        unique_together = ("contact", "address", "address_type")


_contact_annotation = "ContactAnnotation"
_contact_annotation_verbose = humanize(underscore(_contact_annotation))


class ContactAnnotation(ContactAssociation):
    """Contact annotation model class.

    Capture contact annotation/notes attributes.  A contact may be associated
    with 0 or more  annotations:
        Contact(1) ------> Annotation(0..*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    annotation = fields.foreign_key_field(Annotation, on_delete=CASCADE)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_annotation)
        verbose_name = _(_contact_annotation_verbose)
        verbose_name_plural = _(pluralize(_contact_annotation_verbose))
        unique_together = ("contact", "annotation")

_contact_category = "ContactCategory"
_contact_category_verbose = humanize(underscore(_contact_category))


class ContactCategory(ContactAssociation):
    """Contact category model class.

    Capture contact category attributes.  A contact may be associated
    with 0 or more contact categories:
        Contact(1) ------> Category(0..*)
    """
    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_category)
        verbose_name = _(_contact_category_verbose)
        verbose_name_plural = _(pluralize(_contact_category_verbose))
        unique_together = ("contact", "category")

    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    category = fields.foreign_key_field(Category, on_delete=CASCADE)

_contact_email = "ContactEmail"
_contact_email_verbose = humanize(underscore(_contact_email))


class ContactEmail(ContactAssociation):
    """Contact email address model class.

    Captures contact email address(s).  Contact may be associated with
    0 or more email addresses:
        Contact (1) ------> Email(0..*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    email = fields.foreign_key_field(Email, on_delete=CASCADE)
    email_type = fields.foreign_key_field(EmailType, null=True, blank=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_email)
        verbose_name = _(_contact_email_verbose)
        verbose_name_plural = _(pluralize(_contact_email_verbose))
        unique_together = ("contact", "email", "email_type", )

_formatted_name = "FormattedName"
_formatted_name_verbose = humanize(underscore(_formatted_name))


class ContactFormattedName(ContactAssociation):
    """Contact formatted name model class.

    Specifies the formatted contact name.
    A Contact must be associated with at least one FormatedName instance:
        Contact(1) ------> FormattedName(1..*)
    """

    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    name = fields.foreign_key_field(FormattedName, on_delete=CASCADE)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _formatted_name)
        verbose_name = _(_formatted_name_verbose)
        verbose_name_plural = _(pluralize(_formatted_name_verbose))
        unique_together = ('contact', 'name')

_contact_geographic_location = "ContactGeographicLocation"
_contact_geographic_location_verbose = humanize(
    underscore(_contact_geographic_location))


class ContactGeographicLocation(ContactAssociation):
    """
    Contact geographic location model class.

    Capture contact geographic location(s) information.  A contact may be
    associated with 0 or more geographic locations:
        Contact ------> GeographicLocation(0..*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    geographic_location = fields.foreign_key_field(GeographicLocation,
                                                   on_delete=CASCADE)
    geographic_location_type = fields.foreign_key_field(
        GeographicLocationType, blank=True, null=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_geographic_location)
        verbose_name = _(_contact_geographic_location_verbose)
        verbose_name_plural = _(
            pluralize(_contact_geographic_location_verbose))
        unique_together = ("contact",
                           "geographic_location",
                           "geographic_location_type")

_contact_group = "ContactGroup"
_contact_group_verbose = humanize(underscore(_contact_group))


class ContactGroup(ContactAssociation):
    """ContactGroup model class.

    Capture contact group attributes.  A contact may be associated
    with 0 or more groups :
        Contact(1) ------> Group(0..*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    group = fields.foreign_key_field(Group, on_delete=CASCADE)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_group)
        verbose_name = _(_contact_group_verbose)
        verbose_name_plural = _(pluralize(_contact_group_verbose))
        unique_together = ("contact", "group")


class ContactImage(ContactAssociation):
    """Contact image abstract model base class.

    Capture contact  photograph information.
    A contact may be associated with 0 or more images:
        Contact(1) -------> Image(0..*).

    An image may be associated with one or more contacts.
    """
    contact = fields.foreign_key_field(
        Contact, on_delete=CASCADE,
        related_name="%(app_label)s_%(class)s_related_contact")
    image_reference = fields.foreign_key_field(ImageReference,
                                               on_delete=CASCADE)

    class Meta(ContactAssociation.Meta):
        abstract = True


_contact_instant_messaging = "ContactInstantMessaging"
_contact_instant_messaging_verbose = humanize(
    underscore(_contact_instant_messaging))


class ContactInstantMessaging(ContactAssociation):
    """Contact instant messaging model class.

    Capture the URI(s) for contact instant messaging.
    A contact may be associated with  0 or more instance messaging uri's:
        Contact(1) -------> InstantMessaging(0..*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    instant_messaging = fields.foreign_key_field(InstantMessaging,
                                                 on_delete=CASCADE)
    instant_messaging_type = fields.foreign_key_field(InstantMessagingType,
                                                      blank=True, null=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_instant_messaging)
        verbose_name = _(_contact_instant_messaging_verbose)
        verbose_name_plural = _(pluralize(_contact_instant_messaging_verbose))
        unique_together = ("contact",
                           "instant_messaging",
                           "instant_messaging_type", )


_contact_language = "ContactLanguage"
_contact_language_verbose = humanize(underscore(_contact_language))


class ContactLanguage(ContactAssociation):
    """Contact language model class.

    Specify the language(s) that may be used for communicating with
    a contact.  A contact may be associated 0 or more languages:
        Contact(1) -------> ContactLanguage(0..*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    language = fields.foreign_key_field(Language, on_delete=CASCADE)
    language_type = fields.foreign_key_field(
        LanguageType, blank=True, null=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_language)
        verbose_name = _(_contact_language_verbose)
        verbose_name_plural = _(pluralize(_contact_language_verbose))
        unique_together = ("contact", "language", "language_type")

_contact_logo = "ContactLogo"
_contact_logo_verbose = humanize(underscore(_contact_logo))


class ContactLogo(ContactImage):
    """Contact logo class.

    Capture contact logo information.
    A contact may be associated with 0 or more logos:
        Contact(1) -------> Logo(0..*).
    """
    logo_type = fields.foreign_key_field(LogoType, null=True, blank=True)

    class Meta(ContactImage.Meta):
        db_table = db_table(_app_label, _contact_logo)
        verbose_name = _(_contact_logo_verbose)
        verbose_name_plural = _(pluralize(_contact_logo_verbose))
        unique_together = ("contact", "image_reference", "logo_type")

_contact_name = "ContactName"
_contact_name_verbose = humanize(underscore(_contact_name))


class ContactName(ContactAssociation):
    """Contact name model class.

    Defines the contact name components.
    While the RFC specifies that a contact may be associated with at most one
    Name instance, this implementation supports many such instances:
        Contact(1) --------> Name(0..*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    name = fields.foreign_key_field(Name, on_delete=CASCADE)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_name)
        verbose_name = _(_contact_name_verbose)
        verbose_name_plural = _(pluralize(_contact_name_verbose))
        unique_together = ('contact', 'name')


_contact_nickname = "ContactNickname"
_contact_nickname_verbose = humanize(underscore(_contact_nickname))


class ContactNickname(ContactAssociation):
    """Contact nickname model class.

    Allow a association of contact with a nickname.
    A Contact may be associated with 0 or more Nickname instances:
        Contact(1) ------> Nickname(0..*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    name = fields.foreign_key_field(Nickname, on_delete=CASCADE)
    nickname_type = fields.foreign_key_field(
        NicknameType, null=True, blank=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_nickname)
        verbose_name = _(_contact_nickname_verbose)
        verbose_name_plural = _(pluralize(_contact_nickname_verbose))
        unique_together = ("contact", "name", "nickname_type")


_contact_organization = "ContactOrganization"
_contact_organization_verbose = humanize(underscore(_contact_organization))


class ContactOrganization(ContactAssociation):
    """Contact organization model class.
    A contact may be associated
    with 0 or more organizations:
        Contact(1) ------> Organization(0..*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    organization = fields.foreign_key_field(Organization, on_delete=CASCADE)
    unit = fields.foreign_key_field(OrganizationUnit, blank=True, null=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_organization)
        verbose_name = _(_contact_organization_verbose)
        verbose_name_plural = _(pluralize(_contact_organization_verbose))
        unique_together = ("contact", "organization")

_contact_phone = "ContactPhone"
_contact_phone_verbose = humanize(underscore(_contact_phone))


class ContactPhone(ContactAssociation):
    """Contact phone model class.

    Capture contact telephone(s) attributes.
    A contact may be associated with 0 or more  telephones:
        Contact(1) ------> Phone(0:*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    phone = fields.foreign_key_field(Phone, on_delete=CASCADE)
    phone_type = fields.foreign_key_field(PhoneType, blank=True, null=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_phone)
        verbose_name = _(_contact_phone_verbose)
        verbose_name_plural = _(pluralize(_contact_phone_verbose))
        unique_together = ("contact", "phone", "phone_type")

_contact_photo = "ContactPhoto"
_contact_photo_verbose = humanize(underscore(_contact_photo))


class ContactPhoto(ContactImage):
    """Contact photo class.

    Capture contact photo information.
    A contact may be associated with 0 or more photos:
        Contact(1) -------> Photo(0..*).
    """

    photo_type = fields.foreign_key_field(PhotoType, null=True, blank=True)

    class Meta(ContactImage.Meta):
        db_table = db_table(_app_label, _contact_photo)
        verbose_name = _(_contact_photo_verbose)
        verbose_name_plural = _(pluralize(_contact_photo_verbose))
        unique_together = ("contact", "image_reference", "photo_type")

_contact_role = "ContactRole"
_contact_role_verbose = humanize(underscore(_contact_role))


class ContactRole(ContactAssociation):
    """
    Contract role model class.

    Within the context of an organization, capture contact role attributes.
    A contact may be associated with multiple roles:
        Contact(1) -----> Role(0:*)

    The organization for which the role is in effect is optional.
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    role = fields.foreign_key_field(Role, on_delete=CASCADE)
    organization = fields.foreign_key_field(Organization,
                                            blank=True, null=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_role)
        verbose_name = _(_contact_role_verbose)
        verbose_name_plural = _(pluralize(_contact_role_verbose))
        unique_together = ("contact", "role", "organization")

_contact_timezone = "ContactTimezone"
_contact_timezone_verbose = humanize(underscore(_contact_timezone))


class ContactTimezone(ContactAssociation):
    """
    Contact time zone model class.

    Capture contact time zone(s) information.  A contact may be
    associated with 0 or more time zone:
        Contact ------> Timezone(0..*)
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    timezone = fields.foreign_key_field(Timezone, on_delete=CASCADE)
    timezone_type = fields.foreign_key_field(
        TimezoneType, blank=True, null=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_timezone)
        verbose_name = _(_contact_timezone_verbose)
        verbose_name_plural = _(pluralize(_contact_timezone_verbose))
        unique_together = (
            "contact", "timezone", "timezone_type")

_contact_title = "ContactTitle"
_contact_title_verbose = humanize(underscore(_contact_title))


class ContactTitle(ContactAssociation):
    """
    Contact title model class.

    Within the context of an organization, capture contact title attributes.
    A contact may be associated with multiple titles:
        Contact(1) -----> Title(0:*)

    The organization for which the title is in effect is optional.
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    title = fields.foreign_key_field(Title, on_delete=CASCADE)
    organization = fields.foreign_key_field(Organization,
                                            blank=True, null=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_title)
        verbose_name = _(_contact_title_verbose)
        verbose_name_plural = _(pluralize(_contact_title_verbose))
        unique_together = ("contact", "title", "organization")

_contact_url = "ContactUrl"
_contact_url_verbose = humanize(underscore(_contact_url))


class ContactUrl(ContactAssociation):
    """ContactUrl model class.

    A contact may be associated with 0:* urls.  These may include
    social media urls including Linkedln, Facebook, Twitter.
    """
    contact = fields.foreign_key_field(Contact, on_delete=CASCADE)
    url = fields.foreign_key_field(Url, on_delete=CASCADE)
    url_type = fields.foreign_key_field(UrlType, null=True, blank=True)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _contact_url)
        verbose_name = _(_contact_url_verbose)
        verbose_name_plural = _(pluralize(_contact_url_verbose))
        unique_together = ("contact", "url", "url_type",)


_related_contact = "RelatedContact"
_related_contact_verbose = humanize(underscore(_related_contact))


class RelatedContact(ContactAssociation):
    """Related contact model class.

    Capture related contact attributes.  A contact may be associated
    with 0 or more contact instances:
        Contact(1) ------> Contact(0..*)
    """
    from_contact = fields.foreign_key_field(
        Contact,
        on_delete=CASCADE,
        related_name="%(app_label)s_%(class)s_related_from_contact")
    to_contact = fields.foreign_key_field(
        Contact,
        on_delete=CASCADE,
        related_name="%(app_label)s_%(class)s_related_to_contact")
    contract_relationship_type = fields.foreign_key_field(
        ContactRelationshipType)

    class Meta(ContactAssociation.Meta):
        db_table = db_table(_app_label, _related_contact)
        verbose_name = _(_related_contact_verbose)
        verbose_name_plural = _(pluralize(_related_contact_verbose))
        unique_together = ("from_contact", "to_contact",
                           "contract_relationship_type")


PERMISSION_ADD = "contacts.add_contact"
PERMISSION_CHANGE = "contacts.change_contact"
PERMISSION_DELETE = "contacts.delete_contact"
PERMISSION_READ = "contacts.read_contact"
PERMISSION_WRITE = "contacts.write_contact"
PERMISSIONS_CONTACT_OBJECT = (PERMISSION_READ, PERMISSION_WRITE)
PERMISSIONS_CONTACT_FUNCTIONAL = (PERMISSION_ADD,
                                  PERMISSION_CHANGE,
                                  PERMISSION_DELETE)

# As per guardian documentation, defining these derived classes
# with physical foreign key definitions results in improved performance.
# The on_delete parameter is defined such that on contact instance deletion
# the associated object permissions are deleted as well.


class ContactObjectPermission(UserObjectPermissionBase):
    """User contact permission class."""
    content_object = fields.foreign_key_field(Contact, on_delete=CASCADE)


class ContactGroupObjectPermission(GroupObjectPermissionBase):
    """Group contact permission class."""
    content_object = fields.foreign_key_field(Contact, on_delete=CASCADE)

_contacts_user_profile = "UserProfile"
_contacts_user_profile_verbose = humanize(underscore(_contacts_user_profile))
_groups_read = "groups_read"
_groups_write = "groups_write"
_users_read = "users_read"
_users_write = "users_write"


def _field_helper(to_class, relation_type):
    return fields.many_to_many_field(
        to_class=to_class,
        db_table="{}_{}".format(
            db_table(_app_label, _contacts_user_profile), relation_type),
        related_name=related_name_base + relation_type)


class UserProfile(Model):
    """Contacts application user profile model class.

    Each user has an associated ContactsUserProfile instance which defines
    which users and groups are granted read/write access permissions
    for contacts created by the user.
    """
    user = fields.one_to_one_field(settings.AUTH_USER_MODEL,
                                   on_delete=CASCADE)
    groups_read = _field_helper(
        django.contrib.auth.models.Group, _groups_read)
    groups_write = _field_helper(
        django.contrib.auth.models.Group, _groups_write)
    users_read = _field_helper(
        django.contrib.auth.models.User, _users_read)
    users_write = _field_helper(
        django.contrib.auth.models.User, _users_write)

    class Meta(ContactsModel.Meta):
        db_table = db_table(_app_label, _contacts_user_profile)
        verbose_name = _(_contacts_user_profile_verbose)
        verbose_name_plural = _(pluralize(_contacts_user_profile_verbose))
