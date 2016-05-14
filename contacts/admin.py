"""
.. module::  location.admin
   :synopsis:  Django location application admin  module.

Django location application admin  module.

"""
from __future__ import absolute_import
from django.forms.models import BaseInlineFormSet
from django.contrib import admin

from django_core_utils.admin import (NamedModelAdmin,
                                     PrioritizedModelAdmin,
                                     admin_site_register,
                                     named_model_admin_class_attrs)
from python_core_utils.core import class_name

from . import forms
from . import models


class OrderedFormSet(BaseInlineFormSet):
    """Class to order inline objects."""
    order_clause = "-priority"

    def get_queryset(self):
        return super(OrderedFormSet,
                     self).get_queryset().order_by(self.order_clause)


class ContactsInline(admin.TabularInline):
    """Base  contacts admin inline class."""
    readonly_fields = (
        "id", "creation_time", "creation_user", "deleted",
        "site", "update_time", "update_user", "effective_user",
        "uuid", "version")
    formset = OrderedFormSet
    extra = 1

_address_fields = (
    ("id", "priority", "address", "address_type", ),)


class AddressInline(ContactsInline):
    model = models.ContactAddress
    form = forms.ContactAddressAdminForm
    fieldsets = (
        ('Contact address',
         {'fields': _address_fields}),
    )

_annotation_fields = (
    ("id", "priority", "annotation", ),)


class AnnotationInline(ContactsInline):
    model = models.ContactAnnotation
    form = forms.ContactAddressAdminForm
    fieldsets = (
        ('Contact annotation',
         {'fields': _annotation_fields}),
    )


CONTACT_NAME_SIZE = 60

_contact_fields = (
    ("name",),
    ("formatted_name",),
    ("contact_type"),
    ("priority"),
    ("anniversary"),
    ("birth_date",),
    ("gender",))


class ContactAdmin(PrioritizedModelAdmin):
    """
    Contact model admin class
    """
    inlines = (AddressInline, AnnotationInline)
    form = forms.ContactAdminForm
    list_display = ("id", "name", "formatted_name", "priority", "contact_type",
                    "version", "update_time", "update_user")
    list_display_links = ("id", "name", "formatted_name")

    fieldsets = (
        ('Contact',
         {'fields': _contact_fields}),
    ) + PrioritizedModelAdmin.get_field_sets()

    def save_formset(self, request, form, formset, change):
        for form in formset.forms:
            obj = form.instance
            self.prepare(request, obj, form, change)

        super(ContactAdmin, self).save_formset(request, form, formset, change)


_named_classes = (models.ContactType,
                  models.ContactRelationshipType,
                  )

for clasz in _named_classes:
    admin_site_register(
        clasz,
        (NamedModelAdmin,),
        named_model_admin_class_attrs(class_name(clasz)))

_other_model_classes = (models.Contact, )
_other_admin_classes = (ContactAdmin, )

for model_class, admin_class in zip(_other_model_classes,
                                    _other_admin_classes):
    admin.site.register(model_class, admin_class)
