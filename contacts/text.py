"""
..  module:: contacts.text
    :synopsis: Django contacts application text  module.

Django contacts application text  module.
"""
from django.utils.translation import ugettext_lazy as _

# flake8: noqa
# required because of pep8 regression in ignoring disable of E123
contact_labels = {
    "addresses": _("Addresses"),
    "anniversary": _("Anniversary"),
    "annotations": _("Annotations"),
    "birth_date": _("Birth date"),
    "categories": _("Categories"),
    "contact_type": _("Contact type"),
    "emails": _("Emails"),
    "formatted_name": _("Formatted name"),
    "formatted_names": _("Formatted names"),
    "gender": _("Gender"),
    "geographic_locations": _("Geographic locations"),
    "groups": _("Groups"),
    "instant_messaging": _("Instant messaging"),
    "languages": _("Languages"),
    "logos": _("Logos"),
    "name": _("Name"),
    "names": _("Names"),
    "nicknames": _("Nicknames"),
    "organizations": _("Organizations"),
    "phones": _("Phones"),
    "photos": _("Photos"),
    "related_contacts": _("Related contacts"),
    "roles": _("Roles"),
    "timezones": _("Timezones"),
    "titles": _("Titles"),
    "urls": _("Urls"),

    }

contact_help_texts = {
    "addresses": _("Addresses."),
    "anniversary": _("Anniversary."),
    "annotations": _("Annotations."),
    "birth_date": _("Birth date."),
    "categories": _("Categories."),
    "contact_type": _("Contact type."),
    "emails": _("Emails."),
    "formatted_name": _("Formatted name."),
    "formatted_names": _("Additional formatted names."),
    "gender": _("Gender."),
    "geographic_locations": _("Geographic locations."),
    "groups": _("Groups."),
    "instant_messaging": _("Instant messaging."),
    "languages": _("Languages."),
    "logos": _("Logos."),
    "name": _("Name."),
    "names": _("Additional names."),
    "nicknames": _("Nicknames."),
    "organizations": _("Organizations."),
    "phones": _("Phones."),
    "photos": _("Photos."),
    "related_contacts": _("Related contacts."),
    "roles": _("Roles."),
    "timezones": _("Timezones."),
    "titles": _("Titles."),
    "urls": _("Urls."),
    }

contact_address_labels = {
    "address": _("Address"),
    "address_type": _("Address type"),
    }

contact_address_help_texts = {
    "address": _("Address."),
    "address_type": _("Address type."),
    }

contact_annotation_labels = {
    "annotation": _("Annotation"),
    }

contact_annotation_help_texts = {
    "annotation": _("Annotation."),
    }
