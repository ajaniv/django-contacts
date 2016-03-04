"""
.. module::  contact.models
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
# @TODO: how to model organization contact vs person contact
# @TODO: define the rules between specifying the fomratted name and contact name
# @TODO: how to handle multiple addresses per contact (i.e preferred)
# @TODO: how to best model Role, Title within context of organization.
#    Should organization have attributes of Role, Title?
# @TODO: review approach to common types, whether separate ref data application is required
# @TODO: model contact group; allow a contact to be associated with multiple groups
# @TODO: add contact audio (see https://github.com/areski/django-audiofield)
# @TODO: add missing rfc6350 fields (i.e. Contact Key)
from django.utils.translation import gettext as _

from core.models import VersionedObject, NamedObject
from core.models import app_table_name, db_table_name
from core.models_image import Image
from core.models_demographics import Gender
from core.models_organization import Role, Title
from core.models_location import Country, Language, Province, State, Timezone
from core import fields

_app_label = 'contacts'


class GeographicLocation(VersionedObject):
    """Geographic location model class.

    Captures geographic location data.
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("GeographicLocation"))
    latitude = fields.latitude_field()
    longitude = fields.longitude_field()


class Name(VersionedObject):
    """Contact name model class.

    Defines the contact name components.
    A contact may be associated with at most one Name instance:
        Contact(1) --------> Name(0..1)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Name"))

    family_name = fields.char_field(max_length=1024)
    given_name = fields.char_field(max_length=1024)
    additional_name = fields.char_field(max_length=1024)
    honorific_prefix = fields.char_field(max_length=1024)
    honorific_suffix = fields.char_field(max_length=1024)

    @property
    def full_name(self):
        return '%s %s' % (self.given_name, self.family_name)


class ContactType(NamedObject):
    """Contact type model class.

    Allows the organization of contacts into categories.
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("ContactType"))


class Contact(VersionedObject):
    """Contact model class.

    Capture contact attributes.  Designed to allow having multiple contact
    instances per person, organization, etc.
    """

    class Meta(VersionedObject.Meta):
        abstract = True
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Contact"))
    contact_type = fields.foreign_key_field(ContactType)

    contact_name = fields.one_to_one_field(Name, blank=True, null=True)
    gender = fields.foreign_key_field(Gender, blank=True, null=True)

    birth_date = fields.date_field(blank=True, null=True)
    anniversary = fields.date_field(blank=True, null=True)


class FormattedName(VersionedObject):
    """Contact formatted name model class.

    Specifies the formatted contact name.
    A Contact must be associated with at least one FormatedName instance:
        Contact(1) ------> FormattedName(1..*)
    """
    # @TODO: handle multiple formatted names (i.e. concept of preferred)

    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("FormattedName"))

    contact = fields.foreign_key_field(Contact)
    name = fields.char_field(max_length=1024)

    def __str__(self):
        return self.name


class NicknameType(NamedObject):
    """Contact nickname type model class.

    Allow contact nickname classification.
    Sample values may include 'work, 'home', 'unknown'.
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("NicknameType"))


class Nickname(VersionedObject):
    """Contact nickname model class.

    Allow a association of contact with a nickname.
    A Contact may be associated with 0 or more Nickname instances:
        Contact(1) ------> Nickname(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Nickname"))
    contact = fields.foreign_key_field(Contact)
    nickname_type = fields.foreign_key_field(NicknameType)
    name = fields.char_field(max_length=1024)


class PhotoType(NamedObject):
    """Contact photo type model class.

    Allow contact photo classification.
    Sample values may include 'unknown'.
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("PhotoType"))


class ContactImage(VersionedObject):
    """Contact image abstract model base class.

    Capture contact  photograph information.
    A contact may be associated with 0 or more photos:
        Contact(1) -------> Photo(0..*).
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        abstract = True
        db_table = app_table_name(_app_label, db_table_name("ContactPhoto"))

    contact = fields.foreign_key_field(Contact)

    image = fields.foreign_key_field(Image, null=True, blank=True)
    url = fields.url_field(null=True, blank=True)


class Photo(ContactImage):
    """Contact photo class.

    Capture contact photo information.
    A contact may be associated with 0 or more photos:
        Contact(1) -------> Photo(0..*).
    """
    class Meta(VersionedObject.Meta):
        db_table = app_table_name(_app_label, db_table_name("Photo"))
    photo_type = fields.foreign_key_field(PhotoType)


class LogoType(NamedObject):
    """Contact logo type model class.

    Allow contact logo classification.
    Sample values may include 'unknown'.
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("PhotoType"))


class Logo(ContactImage):
    """Contact logo class.

    Capture contact logo information.
    A contact may be associated with 0 or more logos:
        Contact(1) -------> Logo(0..*).
    """
    class Meta(VersionedObject.Meta):
        db_table = app_table_name(_app_label, db_table_name("Logo"))


class UrlType(NamedObject):
    """Contact url type model class.

    Sample values may include 'unknown'.
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("UrlType"))


class Url(VersionedObject):
    """Contact url model class.

    A contact may be associated with 0:* urls.  These may include
    social media urls including Linkedln, Facebook, Twitter.
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Url"))

    contact = fields.foreign_key_field(Contact)
    url_type = fields.foreign_key_field(UrlType)
    url = fields.url_field()


class AddressType(NamedObject):
    """Contract address type model class.

    Allow the categorization of contact address.
    Sample values may include 'unknown'.
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("AddressType"))


class Address(VersionedObject):
    """Contact address model class.

    Capture the attributes of contact address(s).
    A contact may be associated with 0 or more addresses as follows:
    Contact(1)  -------> ContactAddress(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Address"))

    contact = fields.foreign_key_field(Contact)
    address_type = fields.foreign_key_field(AddressType)

    # Labe:l allows to override  name specified in contact
    label = fields.char_field(max_length=1024, null=True, blank=True)
    post_office_box = fields.char_field(max_length=1024, null=True, blank=True)

    # street_address/address line 1: e.g.75 Carol St.
    street_address = fields.char_field(max_length=1024, null=True, blank=True)

    # extended_address/address line 2: e.g., apartment or suite number
    extended_address = fields.char_field(max_length=1024, null=True, blank=True)

    # region:  (e.g., state or province)
    state = fields.foreign_key_field(State, blank=True, null=True)
    province = fields.foreign_key_field(Province, blank=True, null=True)

    country = fields.foreign_key_field(Country, blank=False)
    postal_code = fields.char_field(max_length=10)

    # locality: (e.g., city)
    city = fields.char_field(max_length=1024)

    # time_zone: allow the capture of time zone per address
    time_zone = fields.foreign_key_field(Timezone, blank=True, null=True)

    # geographic_location: allow the capture of geo location per address
    geographic_location = fields.foreign_key_field(GeographicLocation, blank=True, null=True)

    def __str__(self):
        return "%s, %s %s" % (self.city, self.state_province,
                              str(self.country))


class PhoneType(NamedObject):
    """Phone type model class.

    Allow phone type specification.  Values may include "text",
    "fax", "cell", "unknown" """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("PhoneType"))


class Phone(VersionedObject):
    """Contact phone model class.

    Capture contact telephone(s) attributes.
    A contact may be associated with 0 or more  telephones:
        Contact(1) ------> Phone(0:*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Phone"))
    contact = fields.foreign_key_field(Contact)
    phone_type = fields.foreign_key_field(PhoneType)
    phone_number = fields.phone_number_field()


class EmailType(NamedObject):
    """Email type model class."""
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("EmailType"))


class Email(VersionedObject):
    """Contact email address model class.

    Captures contact email address(s).  Contact may be associated with
    0 or more email addresses:
        Contact (1) ------> Email(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Email"))
    contact = fields.foreign_key_field(Contact)
    email_type = fields.foreign_key_field(EmailType)
    email = fields.email_field()


class InstantMessagingType(NamedObject):
    """Instant messaging  type model class.

    Allows the definition of instant messaging type.

    Sample instant messaging type values include "unknown"
    """
    # @TODO: what are some of the possible instance messaging types?
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label,
                                  db_table_name("InstantMessagingType"))


class InstantMessaging(VersionedObject):
    """Contact instant messaging model class.

    Capture the URI(s) for contact instant messaging.
    A contact may be associated with  0 or more instance messaging uri's:
        Contact(1) -------> InstantMessaging(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("InstantMessaging"))
    contact = fields.foreign_key_field(Contact)
    instance_messaging_type = fields.foreign_key_field(InstantMessagingType)
    instance_messaging = fields.instance_messaging_field()


class ContactLanguageType(NamedObject):
    """Contact language type model class.

    Values may include "unknown".
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label,
                                  db_table_name("ContactLanguageType"))


class ContactLanguage(VersionedObject):
    """Contact language model class.

    Specify the language(s) that may be used for communicating with
    a contact.  A contact may be associated 0 or more languages:
        Contact(1) -------> ContactLanguage(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("ContactLanguage"))
    contact = fields.foreign_key_field(Contact)
    language_type = fields.foreign_key_field(ContactLanguageType)
    language = fields.foreign_key_field(Language)


class ContactTimezone(VersionedObject):
    """
    Contact time zone model class.

    Capture contact time zone(s) information.  A contact may be
    associated with 0 or more time zone:
        Contact ------> Timezone(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("ContactTimezone"))
    contact = fields.foreign_key_field(Contact)
    time_zone = fields.foreign_key_field(Timezone)


class ContactGeographicLocation(VersionedObject):
    """
    Contact geographic location model class.

    Capture contact geographic location(s) information.  A contact may be
    associated with 0 or more geographic locations:
        Contact ------> GeographicLocation(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("ContactGeographicLocation"))
    contact = fields.foreign_key_field(Contact)
    geographic_location = fields.foreign_key_field(GeographicLocation)


class ContactTitle(VersionedObject):
    """
    Contact title model class.

    Within the context of an organization, capture contact title attributes.
    A contact may be associated with multiple titles:
        Contact(1) -----> Title(0:*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("ContactTitle"))

    contact = fields.foreign_key_field(Contact)
    title = fields.foreign_key_field(Title)


class ContacRole(VersionedObject):
    """
    Contract role model class.

    Within the context of an organization, capture contact role attributes.
    A contact may be associated with multiple roles:
        Contact(1) -----> Role(0:*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("ContacRole"))

    contact = fields.foreign_key_field(Contact)
    role = fields.foreign_key_field(Role)


class OrganizationType(NamedObject):
    """Contact organization type model class.

    Allows classification of contact organization.
    Sample values may include "unknown"
    """
    # @TODO: what are some of the possible instance messaging types?
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label,
                                  db_table_name("InstantMessagingType"))


class Organization(VersionedObject):
    """Contact organization model class.

    Capture organization attributes.  A contact may be associated
    with 0 or more organizations:
        Contact(1) ------> Organization(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Organization"))

    contact = fields.foreign_key_field(Contact)
    name = fields.char_field(max_length=1024)
    unit = fields.char_field(max_length=1024, blank=True)
    organization_type = fields.foreign_key_field(OrganizationType)


class Member(VersionedObject):
    """Contact member model class.

    Capture membership attributes.  A contact may be associated
    with 0 or more member instances:
        Contact(1) ------> Member(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("Member"))

    contact = fields.foreign_key_field(Contact)
    uri = fields.uri_field()


class RelatedContactType(NamedObject):
    """Related contact type model class.

    Allows classification of contact relationships.
    Sample values may include "unknown",
    "acquaintance", "parent", "child", "co-worker",  "friend"
    """
    # @TODO: what are some of the possible instance messaging types?
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label,
                                  db_table_name("RelatedContactType"))


class RelatedContact(VersionedObject):
    """Related contact model class.

    Capture related contact attributes.  A contact may be associated
    with 0 or more contact instances:
        Contact(1) ------> Contact(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("RelatedContact"))

    contact = fields.foreign_key_field(Contact)
    uri = fields.uri_field(blank=True, null=True)
    related_contact_type = fields.foreign_key_field(RelatedContactType)


class Category(NamedObject):
    """Contact category model class.

    Allows classification of contacts.
    Sample values may include "industry", "travel", "unknown".
    """
    # @TODO: what are some of the possible instance messaging types?
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label,
                                  db_table_name("Category"))


class ContactCategory(VersionedObject):
    """Contact category model class.

    Capture contact category attributes.  A contact may be associated
    with 0 or more contact categories:
        Contact(1) ------> Category(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("ContactCategory"))

    contact = fields.foreign_key_field(Contact)
    category = fields.foreign_key_field(Category)


class ContactAnnotation(VersionedObject):
    """Contact annotation model class.

    Capture contact annotation/notes attributes.  A contact may be associated
    with 0 or more contact annotations:
        Contact(1) ------> Annotation(0..*)
    """
    class Meta(VersionedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("ContactAnnotation"))

    contact = fields.foreign_key_field(Contact)
    annotation = fields.annotation_field()
