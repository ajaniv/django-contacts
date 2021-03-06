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

contact_category_labels = {
    "category": _("Category"),
    }

contact_category_help_texts = {
    "category": _("Category."),
    }

contact_email_labels = {
    "email": _("Email"),
    "email_type": _("Email type."),
    }

contact_email_help_texts = {
    "email": _("Email address."),
    "email_type": _("Email address type."),
    }

contact_formatted_name_labels = {
    "name": _("Name"),
    }

contact_formatted_name_help_texts = {
    "name": _("Name."),
    }

contact_geographic_location_labels = {
    "geographic_location": _("Geographic location"),
    "geographic_location_type": _("Geographic location type"),
    }

contact_geographic_location_help_texts = {
    "geographic_location": _("Geographic location."),
    "geographic_location_type": _("Geographic location type"),
    }

contact_group_labels = {
    "group": _("Group"),
    }

contact_group_help_texts = {
    "group": _("Group."),
    }


contact_instant_messaging_labels = {
    "instant_messaging": _("Instant messaging"),
    "instant_messaging_type": _("Instant messaging type"),
    }

contact_instant_messaging_help_texts = {
    "instant_messaging": _("Instant messaging address."),
    "instant_messaging_type": _("Instant messaging address type"),
    }

contact_language_labels = {
    "language": _("Language"),
    "language_type": _("Language type"),
    }

contact_language_help_texts = {
    "language": _("Language."),
    "language_type": _("Language type."),
    }

contact_logo_labels = {
    "image_reference": _("Image reference"),
    "logo_type": _("Logo type"),
    }

contact_logo_help_texts = {
    "image_reference": _("Image reference."),
    "logo_type": _("Logo type."),
    }

contact_name_labels = {
    "name": _("Name"),
    }

contact_name_help_texts = {
    "name": _("Name."),
    }

contact_nickname_labels = {
    "name": _("Name"),
    "nickname_type": _("Nickname type"),
    }

contact_nickname_help_texts = {
    "name": _("Name."),
    "nickname_type": _("Nickname type."),
    }

contact_organization_labels = {
    "organization": _("Organization"),
    "unit": _("Unit"),
    }

contact_organization_help_texts = {
    "organization": _("Organization."),
    "unit": _("Organization unit."),
    }

contact_phone_labels = {
    "phone": _("Phone"),
    "phone_type": _("Phone type"),
    }

contact_phone_help_texts = {
    "phone": _("Phone."),
    "phone type": _("Phone type."),
    }

contact_photo_labels = {
    "image_reference": _("Image reference"),
    "photo_type": _("Photo type"),
    }

contact_photo_help_texts = {
    "image_reference": _("Image reference."),
    "photo_type": _("Photo type."),
    }

contact_role_labels = {
    "role": _("Role"),
    "organization": _("Organization"),
    }

contact_role_help_texts = {
    "role": _("Role."),
    "organization": _("Organization."),
    }

contact_timezone_labels = {
    "timezone": _("Timezone"),
    "timezone_type": _("Timezone type"),
    }

contact_timezone_help_texts = {
    "timezone": _("Timezone."),
    "timezone_type": _("Timezone type."),
    }

contact_title_labels = {
    "title": _("Title"),
    "organization": _("Organization"),
    }

contact_title_help_texts = {
    "title": _("Title."),
    "organization": _("Organization."),
    }

contact_url_labels = {
    "url": _("Url"),
    "url_type": _("Url type"),
    }

contact_url_help_texts = {
    "url": _("Url."),
    "url_type": _("Url type."),
    }

related_contact_labels = {
    "from_contact": _("From contact"),
    "to_contact": _("To contact"),
    "contract_relationship_type": _("Relationship Type"),
    }

related_contact_help_texts = {
    "from_contact": _("From contact."),
    "to_contact": _("To contact."),
    "contact_relationship_type": _("Relationship Type."),
    }

user_profile_labels = {
    "user": _("User"),
    "groups_read": _("Groups read"),
    "groups_write": _("Groups write"),
    "users_read": _("Users read"),
    "users_write": _("Users write"),
    }

user_profile_help_texts = {
    "user": _("User."),
    "groups_read": _("Groups read."),
    "groups_write": _("Groups write."),
    "users_read": _("Users read."),
    "users_write": _("Users write."),
    }
