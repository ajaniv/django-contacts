"""
.. module::  contact.models
   :synopsis:  Contact models module.

Contact models module.
"""

# @TODO: how to model organization contact vs person contact
# @TODO: model telephone
# @TODO: model email
# @TODO: model social links
# @TODO: model contact photo
# @TODO: contact as separate app
# @TODO: libs as separate repository - how to manage

from core import models
from core import fields

_app_label = 'contact'


@models.meta(models.BusinessObject.Meta, _app_label)
class Country(models.BusinessObject):
    """
    Class definition for country.
    Uses 2 character ISO 3166.
    """
    iso_code = fields.char_field(max_length=2)
    name = fields.char_field()

    def __str__(self):
        return self.name


@models.meta(models.BusinessObject.Meta, _app_label)
class StateProvince(models.BusinessObject):
    """
    Class definition for states and provinces.
    Uses 3 character ISO 3166-2.
    """
    iso_code = fields.char_field(max_length=3)
    name = fields.char_field()
    country = fields.foreign_key_field(Country)

    def __str__(self):
        return self.name


class ContactName(models.BusinessObject.Meta, _app_label):
    """
    Contact name details class.
    """
    family_name = fields.char_field(max_length=1024)
    given_name = fields.char_field(max_length=1024)
    additional_name = fields.char_field(max_length=1024)
    honorific_prefix = fields.char_field(max_length=1024)
    honorific_suffix = fields.char_field(max_length=1024)

    @property
    def full_name(self):
        return '%s %s' % (self.given_name, self.family_name)


@models.meta(models.BusinessObject.Meta, _app_label, abstract=True)
class Contact(models.BusinessObject):
    """
    Contact definition class.
    """
    # If defined, overrides ContactName data
    formatted_named = fields.char_field(max_length=1024, blank=True, null=True)
    contact_name = fields.one_to_one_field(ContactName)
    birth_date = fields.date_field(blank=True, null=True)
    gender = fields.char_field(max_length=1024, blank=True, null=True)


@models.meta(models.BusinessObject.Meta, _app_label, abstract=True)
class ContactNickname(models.BusinessObject):
    """
    Contact nickname class.
    """
    contact = fields.foreign_key_field(Contact)
    nickname_type = fields.char_field(max_length=1024, blank=True, null=True)


@models.meta(models.BusinessObject.Meta, _app_label, abstract=True)
class ContactPhoto(models.BusinessObject):
    """
    Contact photo class.
    """
    contact = fields.foreign_key_field(Contact)


@models.meta(models.BusinessObject.Meta,
             _app_label,
             unique_together=("address_line1", "address_line2",
                              "postal_code", "city",
                              "state_province", "country")
             )
class Address(models.BusinessObject):
    """
    Class definition for address.
    """
    contact = fields.foreign_key_field(Contact)
    state_province = fields.foreign_key_field(StateProvince, blank=True)
    country = fields.foreign_key_field(Country, blank=False)

    address_line1 = fields.char_field(max_length=45)
    address_line2 = fields.char_field(max_length=45, blank=True)
    postal_code = fields.char_field(max_length=10)
    city = fields.char_field(max_length=50, blank=False)
    tz = fields.char_field(max_length=100)

    latitude = fields.latitude_field()
    longitude = fields.longitude_field()

    def __str__(self):
        return "%s, %s %s" % (self.city, self.state_province,
                              str(self.country))

    #@TODO: missing time zone


@models.meta(models.BusinessObject.Meta, _app_label)
class Organization(models.BusinessObject):
    """
    Organization the contact is affiliated with.
    """
    contact = fields.foreign_key_field(Contact)
    name = fields.char_field(max_length=1024)
    unit = fields.char_field(max_length=1024, blank=True)

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
