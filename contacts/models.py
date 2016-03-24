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
# @TODO: how to model organization contact vs person contact; via contact type?
# @TODO: define the rules between specifying the fomratted name and contact name
# @TODO: how to handle multiple addresses per contact (i.e preferred)
# @TODO: add contact Media
# @TODO: add missing rfc6350 fields (i.e. Contact Key, audio see https://github.com/areski/django-audiofield)
# @TODO: add manager classes
# @TODO: For image, review approach to have bundled thumbnail/compressed version
# @TODO: check implementation of related contact when uri is used,not contact
# defined in model


from core.models import VersionedModel, NamedModel, PrioritizedModel
from core.models import app_table_name, db_table_name
from core_models.models import Image
from core_models.models import Gender
from core_models.models import Role, Title
from core_models.models import Organization, OrganizationUnit
from core_models.models import Annotation, Category
from core_models.models import EmailType, FormattedName, Group, Name
from core_models.models import InstantMessagingType, LogoType
from core_models.models import NicknameType, PhoneType
from core_models.models import PhotoType, UrlType
from core_models.models import Address, AddressType, Language, LanguageType
from core_models.models import GeographicLocation, GeographicLocationType
from core_models.models import Timezone, TimezoneType
from core import fields

_app_label = 'contacts'


class ContactType(NamedModel):
    """Contact type model class.

    Allows the organization of contacts into categories.
    """
    class Meta(NamedModel.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name("ContactType"))


class BaseModel(VersionedModel, PrioritizedModel):
    class Meta(VersionedModel.Meta):
        app_label = _app_label
        abstract = True


class Contact(BaseModel):
    """Contact model class.

    Capture contact attributes.  Designed to allow having multiple contact
    instances per person, organization, etc.
    """

    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("Contact"))

    contact_type = fields.foreign_key_field(ContactType)
    gender = fields.foreign_key_field(Gender, blank=True, null=True)

    address = fields.many_to_many_field(
        Address, through="ContactAddress", blank=True, null=True)
    annotations = fields.many_to_many_field(
        Annotation, through="ContactAnnotation", blank=True, null=True)
    categories = fields.many_to_many_field(
        Category, through="ContactCategory", blank=True, null=True)
    emails = fields.many_to_many_field(
        EmailType, through="ContactEmail",
        blank=True, null=True)
    formatted_names = fields.many_to_many_field(
        FormattedName, through="ContactFormattedName",
        blank=True, null=True)
    groups = fields.many_to_many_field(
        Group, through="ContactGroup",
        blank=True, null=True)
    instant_messaging = fields.many_to_many_field(
        InstantMessagingType, through="ContactInstanceMessaging",
        blank=True, null=True)
    languages = fields.many_to_many_field(
        Language, through="ContactLanguage",
        blank=True, null=True)
    locations = fields.many_to_many_field(
        GeographicLocation, through="ContactGeographicLocation",
        blank=True, null=True)
    logos = fields.many_to_many_field(
        Image, through="ContactLogo",
        blank=True, null=True)
    names = fields.many_to_many_field(
        Name, through="ContactName",
        blank=True, null=True)
    nicknames = fields.many_to_many_field(
        NicknameType, through="ContactNickname",
        blank=True, null=True)
    organizations = fields.many_to_many_field(
        Organization, through="ContactOrganization",
        blank=True, null=True)
    phones = fields.many_to_many_field(
        PhoneType, through="ContactPhone",
        blank=True, null=True)
    photos = fields.many_to_many_field(
        Image, through="ContactPhoto",
        blank=True, null=True)
    related_contacts = fields.many_to_many_field(
        "self", through="RelatedContacts", symmetrical=False,
        blank=True, null=True)
    roles = fields.many_to_many_field(
        Role, through="ContactRole", blank=True, null=True)
    timezones = fields.many_to_many_field(
        Timezone, through="ContactTimezone", blank=True, null=True)
    urls = fields.many_to_many_field(
        UrlType, through="ContactUrl", blank=True, null=True)

    birth_date = fields.date_field(blank=True, null=True)
    anniversary = fields.date_field(blank=True, null=True)


class ContactName(BaseModel):
    """Contact name model class.

    Defines the contact name components.
    While the RFC specifies that a contact may be associated with at most one
    Name instance, this implementation supports many such instances:
        Contact(1) --------> Name(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("Name"))
        unique_together = ('contact', 'name')

    contact = fields.foreign_key_field(Contact)
    name = fields.foreign_key_field(Name)


class FormattedName(BaseModel):
    """Contact formatted name model class.

    Specifies the formatted contact name.
    A Contact must be associated with at least one FormatedName instance:
        Contact(1) ------> FormattedName(1..*)
    """
    # @TODO: handle multiple formatted names (i.e. concept of preferred)

    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("FormattedName"))
        unique_together = ('contact', 'name')

    contact = fields.foreign_key_field(Contact)
    name = fields.foreign_key_field(FormattedName)

    def __str__(self):
        return self.name


class ContactNickname(BaseModel):
    """Contact nickname model class.

    Allow a association of contact with a nickname.
    A Contact may be associated with 0 or more Nickname instances:
        Contact(1) ------> Nickname(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("Nickname"))
        unique_together = ('contact', 'nickname_type', 'name')

    contact = fields.foreign_key_field(Contact)
    nickname_type = fields.foreign_key_field(NicknameType)
    name = fields.char_field()


class ContactImage(BaseModel):
    """Contact image abstract model base class.

    Capture contact  photograph information.
    A contact may be associated with 0 or more images:
        Contact(1) -------> Image(0..*).

    An image may be associated with one or more contacts.
    """
    # @TODO: need to validate that image or url have been configured
    class Meta(BaseModel.Meta):
        abstract = True

    contact = fields.foreign_key_field(Contact)
    image = fields.foreign_key_field(Image, null=True, blank=True)
    # url of image if one is not defined
    url = fields.url_field(null=True, blank=True)


class ContactPhoto(ContactImage):
    """Contact photo class.

    Capture contact photo information.
    A contact may be associated with 0 or more photos:
        Contact(1) -------> Photo(0..*).
    """
    class Meta(ContactImage.Meta):
        db_table = app_table_name(_app_label, db_table_name("ContactPhoto"))
        unique_together = ('contact', 'image', 'url', 'photo_type')

    photo_type = fields.foreign_key_field(PhotoType)


class ContactLogo(ContactImage):
    """Contact logo class.

    Capture contact logo information.
    A contact may be associated with 0 or more logos:
        Contact(1) -------> Logo(0..*).
    """
    class Meta(ContactImage.Meta):
        db_table = app_table_name(_app_label, db_table_name("ContactLogo"))
        unique_together = ('contact', 'image', 'url', 'logo_type')

    logo_type = fields.foreign_key_field(LogoType)


class ContactUrl(BaseModel):
    """Contact url model class.

    A contact may be associated with 0:* urls.  These may include
    social media urls including Linkedln, Facebook, Twitter.
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("ContactUrl"))
        unique_together = ('contact', 'url_type', 'url')

    contact = fields.foreign_key_field(Contact)
    url_type = fields.foreign_key_field(UrlType)
    url = fields.url_field()


class ContactAddress(BaseModel):
    """Contact address model class.

    Capture the attributes of contact address(s).
    A contact may be associated with 0 or more addresses as follows:
    Contact(1)  -------> ContactAddress(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("ContactAddress"))
        unique_together = ('contact', 'address', 'address_type')

    contact = fields.foreign_key_field(Contact)
    address = fields.foreign_key_field(Address)
    address_type = fields.foreign_key_field(AddressType)


class ContactPhone(BaseModel):
    """Contact phone model class.

    Capture contact telephone(s) attributes.
    A contact may be associated with 0 or more  telephones:
        Contact(1) ------> Phone(0:*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("ContactPhone"))
        unique_together = ('contact', 'phone_type', 'phone_number')
    contact = fields.foreign_key_field(Contact)
    phone_type = fields.foreign_key_field(PhoneType)
    phone_number = fields.phone_number_field()


class ContactEmail(BaseModel):
    """Contact email address model class.

    Captures contact email address(s).  Contact may be associated with
    0 or more email addresses:
        Contact (1) ------> Email(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("ContactEmail"))
        unique_together = ('contact', 'email_type', 'email')
    contact = fields.foreign_key_field(Contact)
    email_type = fields.foreign_key_field(EmailType)
    email = fields.email_field()


class ContactInstantMessaging(BaseModel):
    """Contact instant messaging model class.

    Capture the URI(s) for contact instant messaging.
    A contact may be associated with  0 or more instance messaging uri's:
        Contact(1) -------> InstantMessaging(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label,
                                  db_table_name("ContactInstantMessaging"))
        unique_together = ('contact',
                           'instance_messaging_type', 'instance_messaging')
    contact = fields.foreign_key_field(Contact)
    instance_messaging_type = fields.foreign_key_field(InstantMessagingType)
    instance_messaging = fields.instance_messaging_field()


class ContactLanguage(BaseModel):
    """Contact language model class.

    Specify the language(s) that may be used for communicating with
    a contact.  A contact may be associated 0 or more languages:
        Contact(1) -------> ContactLanguage(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("ContactLanguage"))
        unique_together = ('contact',
                           'language', 'language_type')
    contact = fields.foreign_key_field(Contact)
    language = fields.foreign_key_field(Language)
    language_type = fields.foreign_key_field(
        LanguageType, blank=True, null=True)


class ContactTimezone(BaseModel):
    """
    Contact time zone model class.

    Capture contact time zone(s) information.  A contact may be
    associated with 0 or more time zone:
        Contact ------> Timezone(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("ContactTimezone"))
        unique_together = ('contact',
                           'time_zone', 'time_zone_type')
    contact = fields.foreign_key_field(Contact)
    time_zone = fields.foreign_key_field(Timezone)
    time_zone_type = fields.foreign_key_field(
        TimezoneType, blank=True, null=True)


class ContactGeographicLocation(BaseModel):
    """
    Contact geographic location model class.

    Capture contact geographic location(s) information.  A contact may be
    associated with 0 or more geographic locations:
        Contact ------> GeographicLocation(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label,
                                  db_table_name("ContactGeographicLocation"))
        unique_together = ('contact',
                           'geographic_location',
                           'geographic_location_type')
    contact = fields.foreign_key_field(Contact)
    geographic_location = fields.foreign_key_field(GeographicLocation)
    geographic_location_type = fields.foreign_key_field(
        GeographicLocationType, blank=True, null=True)


class ContactTitle(BaseModel):
    """
    Contact title model class.

    Within the context of an organization, capture contact title attributes.
    A contact may be associated with multiple titles:
        Contact(1) -----> Title(0:*)

    The organization for which the title is in effect is optional.
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("ContactTitle"))
        unique_together = ('contact', 'title', 'organization')

    contact = fields.foreign_key_field(Contact)
    title = fields.foreign_key_field(Title)
    organization = fields.foreign_key_field(Organization,
                                            blank=True, null=True)


class ContactRole(BaseModel):
    """
    Contract role model class.

    Within the context of an organization, capture contact role attributes.
    A contact may be associated with multiple roles:
        Contact(1) -----> Role(0:*)

    The organization for which the role is in effect is optional.
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("ContacRole"))
        unique_together = ('contact', 'role', 'organization')

    contact = fields.foreign_key_field(Contact)
    role = fields.foreign_key_field(Role)
    organization = fields.foreign_key_field(Organization,
                                            blank=True, null=True)


class ContactOrganization(BaseModel):
    """Contact organization model class.
    A contact may be associated
    with 0 or more organizations:
        Contact(1) ------> Organization(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label,
                                  db_table_name("ContactOrganization"))
        unique_together = ('contact', 'organization')

    contact = fields.foreign_key_field(Contact)
    organization = fields.foreign_key_field(Organization)
    unit = fields.foreign_key_field(OrganizationUnit, blank=True, null=True)


class RelatedContactType(NamedModel):
    """Related contact type model class.

    Allows classification of contact relationships.
    Sample values may include "unknown",
    "acquaintance", "parent", "child", "co-worker",  "friend"
    """
    # @TODO: what are some of the possible instance messaging types?
    class Meta(NamedModel.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label,
                                  db_table_name("RelatedContactType"))


class RelatedContact(BaseModel):
    """Related contact model class.

    Capture related contact attributes.  A contact may be associated
    with 0 or more contact instances:
        Contact(1) ------> Contact(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("RelatedContact"))
        unique_together = ('from_contact', 'to_contact', 'uri',
                           'related_contact_type')

    from_contact = fields.foreign_key_field(Contact)
    to_contact = fields.foreign_key_field(Contact, null=True, blank=True)
    uri = fields.uri_field(blank=True, null=True)
    related_contact_type = fields.foreign_key_field(RelatedContactType)


class ContactCategory(BaseModel):
    """Contact category model class.

    Capture contact category attributes.  A contact may be associated
    with 0 or more contact categories:
        Contact(1) ------> Category(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label, db_table_name("ContactCategory"))
        unique_together = ('contact', 'category')

    contact = fields.foreign_key_field(Contact)
    category = fields.foreign_key_field(Category)


class ContactAnnotation(BaseModel):
    """Contact annotation model class.

    Capture contact annotation/notes attributes.  A contact may be associated
    with 0 or more  annotations:
        Contact(1) ------> Annotation(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label,
                                  db_table_name("ContactAnnotation"))
        unique_together = ('contact', 'annotation')

    contact = fields.foreign_key_field(Contact)
    annotation = fields.foreign_key_field(Annotation)


class ContactGroup(BaseModel):
    """Contact group model class.

    Capture contact group attributes.  A contact may be associated
    with 0 or more groups :
        Contact(1) ------> Group(0..*)
    """
    class Meta(BaseModel.Meta):
        db_table = app_table_name(_app_label,
                                  db_table_name("ContactGroup"))
        unique_together = ('contact', 'group')

    contact = fields.foreign_key_field(Contact)
    group = fields.foreign_key_field(Group)

