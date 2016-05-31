"""
.. module::  location.admin
   :synopsis:  Django location application admin  module.

Django location application admin  module.

"""
from __future__ import absolute_import
from django.forms.models import BaseInlineFormSet
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from guardian.admin import GuardedModelAdminMixin, GroupManage, UserManage
from guardian.shortcuts import get_objects_for_user
from guardian.compat import OrderedDict, get_user_model, get_model_name
from guardian.shortcuts import get_users_with_perms
from guardian.shortcuts import get_groups_with_perms

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


_contacts_inline_fields = ("id", "priority")


class ContactsInline(admin.TabularInline):
    """Base  contacts admin inline class."""
    readonly_fields = (
        "id", "creation_time", "creation_user", "deleted",
        "site", "update_time", "update_user", "effective_user",
        "uuid", "version")
    formset = OrderedFormSet
    extra = 1

_address_fields = (
    _contacts_inline_fields + ("address", "address_type", ),)


class AddressInline(ContactsInline):
    """Address inline class."""
    model = models.ContactAddress
    form = forms.ContactAddressAdminForm
    fieldsets = (
        ("Contact address",
         {"fields": _address_fields}),
    )

_annotation_fields = (
    _contacts_inline_fields + ("annotation", ),)


class AnnotationInline(ContactsInline):
    """Annotation inline class."""
    model = models.ContactAnnotation
    form = forms.ContactAnnotationAdminForm
    fieldsets = (
        ("Contact annotation",
         {"fields": _annotation_fields}),
    )

_category_fields = (
    _contacts_inline_fields + ("category", ),)


class CategoryInline(ContactsInline):
    """Category inline class."""
    model = models.ContactCategory
    form = forms.ContactCategoryAdminForm
    fieldsets = (
        ("Contact category",
         {"fields": _category_fields}),
    )

_email_fields = (
    _contacts_inline_fields + ("email", "email_type"),)


class EmailInline(ContactsInline):
    """Email inline class."""
    model = models.ContactEmail
    form = forms.ContactEmailAdminForm
    fieldsets = (
        ("Contact email",
         {"fields": _email_fields}),
    )

_formatted_name_fields = (
    _contacts_inline_fields + ("name",),)


class FormattedNameInline(ContactsInline):
    """FormattedName inline class."""
    model = models.ContactFormattedName
    form = forms.ContactFormattedNameAdminForm
    fieldsets = (
        ("Contact formatted name",
         {"fields": _formatted_name_fields}),
    )

_geographic_location_fields = (
    _contacts_inline_fields + ("geographic_location",
                               "geographic_location_type"),)


class GeographicLocationInline(ContactsInline):
    """GeographicLocation inline class."""
    model = models.ContactGeographicLocation
    form = forms.ContactGeographicLocationAdminForm
    fieldsets = (
        ("Contact geographic location",
         {"fields": _geographic_location_fields}),
    )

_group_fields = (
    _contacts_inline_fields + ("group",),)


class GroupInline(ContactsInline):
    """Group inline class."""
    model = models.ContactGroup
    form = forms.ContactGroupAdminForm
    fieldsets = (
        ("Contact group",
         {"fields": _group_fields}),
    )

_instant_messaging_fields = (
    _contacts_inline_fields + ("instant_messaging", "instant_messaging_type"),)


class InstantMessagingInline(ContactsInline):
    model = models.ContactInstantMessaging
    form = forms.ContactInstantMessagingAdminForm
    fieldsets = (
        ("Contact instant messaging",
         {"fields": _instant_messaging_fields}),
    )

_language_fields = (
    _contacts_inline_fields + ("language", "language_type"),)


class LanguageInline(ContactsInline):
    model = models.ContactLanguage
    form = forms.ContactLanguageAdminForm
    fieldsets = (
        ("Contact language",
         {"fields": _language_fields}),
    )

_logo_fields = (
    _contacts_inline_fields + ("image_reference", "logo_type"),)


class LogoInline(ContactsInline):
    model = models.ContactLogo
    form = forms.ContactLogoAdminForm
    fieldsets = (
        ("Contact logo",
         {"fields": _logo_fields}),
    )

_name_fields = (
    _contacts_inline_fields + ("name",),)


class NameInline(ContactsInline):
    model = models.ContactName
    form = forms.ContactNameAdminForm
    fieldsets = (
        ("Contact name",
         {"fields": _name_fields}),
    )

_nickname_fields = (
    _contacts_inline_fields + ("name", "nickname_type"),)


class NicknameInline(ContactsInline):
    model = models.ContactNickname
    form = forms.ContactNicknameAdminForm
    fieldsets = (
        ("Contact nickname",
         {"fields": _nickname_fields}),
    )

_organization_fields = (
    _contacts_inline_fields + ("organization", "unit"),)


class OrganizationInline(ContactsInline):
    model = models.ContactOrganization
    form = forms.ContactOrganizationAdminForm
    fieldsets = (
        ("Contact organization",
         {"fields": _organization_fields}),
    )

_phone_fields = (
    _contacts_inline_fields + ("phone", "phone_type"),)


class PhoneInline(ContactsInline):
    model = models.ContactPhone
    form = forms.ContactPhoneAdminForm
    fieldsets = (
        ("Contact phone",
         {"fields": _phone_fields}),
    )

_photo_fields = (
    _contacts_inline_fields + ("image_reference", "photo_type"),)


class PhotoInline(ContactsInline):
    model = models.ContactPhoto
    form = forms.ContactPhotoAdminForm
    fieldsets = (
        ("Contact photo",
         {"fields": _photo_fields}),
    )

_role_fields = (
    _contacts_inline_fields + ("role", "organization"),)


class RoleInline(ContactsInline):
    model = models.ContactRole
    form = forms.ContactRoleAdminForm
    fieldsets = (
        ("Contact role",
         {"fields": _role_fields}),
    )

_timezone_fields = (
    _contacts_inline_fields + ("timezone", "timezone_type"),)


class TimezoneInline(ContactsInline):
    model = models.ContactTimezone
    form = forms.ContactTimezoneAdminForm
    fieldsets = (
        ("Contact timezone",
         {"fields": _timezone_fields}),
    )

_title_fields = (
    _contacts_inline_fields + ("title", ),)


class TitleInline(ContactsInline):
    model = models.ContactTitle
    form = forms.ContactTitleAdminForm
    fieldsets = (
        ("Contact title",
         {"fields": _title_fields}),
    )

_url_fields = (
    _contacts_inline_fields + ("url", "url_type"),)


class UrlInline(ContactsInline):
    model = models.ContactUrl
    form = forms.ContactUrlAdminForm
    fieldsets = (
        ("Contact url",
         {"fields": _url_fields}),
    )


_related_contact_fields = (
    _contacts_inline_fields + (
        "from_contact", "to_contact", "contact_relationship_type"),)


class RelatedContactInline(ContactsInline):
    model = models.RelatedContact
    form = forms.RelatedContactAdminForm
    fk_name = "from_contact"
    fieldsets = (
        ("Related contact",
         {"fields": _related_contact_fields}),
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


class ContactAdmin(GuardedModelAdminMixin, PrioritizedModelAdmin):
    """
    Contact model admin class
    """
    user_owned_objects_field = 'creation_user'
    inlines = (
        AddressInline, AnnotationInline, CategoryInline, EmailInline,
        FormattedNameInline, GeographicLocationInline, GroupInline,
        InstantMessagingInline, LanguageInline, LogoInline,
        NameInline, NicknameInline, OrganizationInline,
        PhoneInline, PhotoInline, RoleInline,
        TimezoneInline, TitleInline,
        UrlInline, RelatedContactInline)

    form = forms.ContactAdminForm
    list_display = ("id", "name", "formatted_name", "priority", "contact_type",
                    "version", "update_time", "update_user")
    list_display_links = ("id", "name", "formatted_name")

    fieldsets = (
        ("Contact",
         {"fields": _contact_fields}),
    ) + PrioritizedModelAdmin.get_field_sets()

    def save_formset(self, request, form, formset, change):
        for form in formset.forms:
            obj = form.instance
            self.prepare(request, obj, form, change)

        super(ContactAdmin, self).save_formset(request, form, formset, change)

    def get_queryset(self, request):

        if (request.user.is_superuser or
                self.user_can_access_owned_objects_only):
            return super(ContactAdmin, self).get_queryset(request)

        contacts_qs = get_objects_for_user(
            request.user, 'contacts.read_contact', accept_global_perms=False)

        return contacts_qs

    def get_form(self, request, obj=None, **kwargs):
        form = super(ContactAdmin, self).get_form(request, obj, **kwargs)
        form.request_user = request.user
        return form

    def obj_perms_manage_view(self, request, object_pk):
        """
        Main object permissions view. Presents all users and groups with any
        object permissions for the current model *instance*. Users or groups
        without object permissions for related *instance* would **not** be
        shown. In order to add or manage user or group one should use links or
        forms presented within the page.
        """
        if not self.has_change_permission(request, None):
            post_url = reverse('admin:index', current_app=self.admin_site.name)
            return redirect(post_url)

        try:
            # django >= 1.7
            from django.contrib.admin.utils import unquote
        except ImportError:
            # django < 1.7
            from django.contrib.admin.util import unquote
        obj = get_object_or_404(self.get_queryset(
            request), pk=unquote(object_pk))
        owning_user = getattr(obj, self.user_owned_objects_field)

        if owning_user != request.user:
            post_url = reverse('admin:index', current_app=self.admin_site.name)
            return redirect(post_url)

        users_perms = OrderedDict(
            sorted(
                get_users_with_perms(obj, attach_perms=True,
                                     with_group_users=False).items(),
                key=lambda user: getattr(
                    user[0], get_user_model().USERNAME_FIELD)
            )
        )

        groups_perms = OrderedDict(
            sorted(
                get_groups_with_perms(obj, attach_perms=True).items(),
                key=lambda group: group[0].name
            )
        )

        if request.method == 'POST' and 'submit_manage_user' in request.POST:
            user_form = UserManage(request.POST)
            group_form = GroupManage()
            info = (
                self.admin_site.name,
                self.model._meta.app_label,
                get_model_name(self.model)
            )
            if user_form.is_valid():
                user_id = user_form.cleaned_data['user'].pk
                url = reverse(
                    '%s:%s_%s_permissions_manage_user' % info,
                    args=[obj.pk, user_id]
                )
                return redirect(url)
        elif (request.method == 'POST' and
              'submit_manage_group' in request.POST):
            user_form = UserManage()
            group_form = GroupManage(request.POST)
            info = (
                self.admin_site.name,
                self.model._meta.app_label,
                get_model_name(self.model)
            )
            if group_form.is_valid():
                group_id = group_form.cleaned_data['group'].id
                url = reverse(
                    '%s:%s_%s_permissions_manage_group' % info,
                    args=[obj.pk, group_id]
                )
                return redirect(url)
        else:
            user_form = UserManage()
            group_form = GroupManage()

        context = self.get_obj_perms_base_context(request, obj)
        context['users_perms'] = users_perms
        context['groups_perms'] = groups_perms
        context['user_form'] = user_form
        context['group_form'] = group_form

        # https://github.com/django/django/commit/cf1f36bb6eb34fafe6c224003ad585a647f6117b
        request.current_app = self.admin_site.name

        return render_to_response(
            self.get_obj_perms_manage_template(),
            context,
            RequestContext(request))


class UserProfileAdmin(GuardedModelAdminMixin, admin.ModelAdmin):
    """Versioned model admin class.
    """
    user_can_access_owned_objects_only = True
    user_owned_objects_field = "creation_user"
    form = forms.UserProfileAdminForm
    list_display = ("id", "get_username")
    list_filter = ("user__username",)

    ordering = ("id",)

    def get_username(self, instance):
        """return username ."""
        return instance.user.username
    get_username.short_description = "username"

_named_classes = (models.ContactType,
                  models.ContactRelationshipType,
                  )

for clasz in _named_classes:
    admin_site_register(
        clasz,
        (NamedModelAdmin,),
        named_model_admin_class_attrs(class_name(clasz)))

_other_model_classes = (models.Contact, models.UserProfile)
_other_admin_classes = (ContactAdmin, UserProfileAdmin)

for model_class, admin_class in zip(_other_model_classes,
                                    _other_admin_classes):
    admin.site.register(model_class, admin_class)
