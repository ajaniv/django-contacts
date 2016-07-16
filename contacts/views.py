"""
..  module:: contacts.views
    :synopsis: contacts application views  module.

*contacts*  application views  module.
"""
from __future__ import absolute_import
import collections
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from django_core_utils.views import ObjectListView, ObjectDetailView
import django_core_models.views as core_model_views
from . import models
from . import serializers


class ContactRelationshipTypeMixin(object):
    """ContactRelationshipType mixin class."""
    queryset = models.ContactRelationshipType.objects.all()
    serializer_class = serializers.ContactRelationshipTypeSerializer


class ContactRelationshipTypeList(ContactRelationshipTypeMixin,
                                  ObjectListView):
    """Class to list all ContactRelationshipType instances,
     or create  new ContactRelationshipType instance."""
    pass


class ContactRelationshipTypeDetail(ContactRelationshipTypeMixin,
                                    ObjectDetailView):
    """
    Class to retrieve, update or delete ContactRelationshipType instance.
    """
    pass


class ContactTypeMixin(object):
    """ContactType mixin class."""
    queryset = models.ContactType.objects.all()
    serializer_class = serializers.ContactTypeSerializer


class ContactTypeList(ContactTypeMixin, ObjectListView):
    """Class to list all ContactType instances,
    or create new ContactType instance."""
    pass


class ContactTypeDetail(ContactTypeMixin, ObjectDetailView):
    """
    Class to retrieve, update or delete ContactType instance.
    """
    pass


class ContactMixin(object):
    """Contact mixin class."""
    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializer


class ContactList(ContactMixin, ObjectListView):
    """Class to list all Contact instances,
    or create new Contact instance."""
    pass


class ContactDetail(ContactMixin, ObjectDetailView):
    """
    Class to retrieve, update or delete Contact instance.
    """
    pass


class ContactAddressMixin(object):
    """ContactAddress mixin class."""
    queryset = models.ContactAddress.objects.all()
    serializer_class = serializers.ContactAddressSerializer


class ContactAddressList(ContactAddressMixin, ObjectListView):
    """Class to list all ContactAddress instances,
    or create new ContactAddress instance."""
    pass


class ContactAddressDetail(ContactAddressMixin, ObjectDetailView):
    """
    Class to retrieve, update or delete ContactAddress instance.
    """
    pass


class ContactAnnotationMixin(object):
    """ContactAnnotation mixin class."""
    queryset = models.ContactAnnotation.objects.all()
    serializer_class = serializers.ContactAnnotationSerializer


class ContactAnnotationList(ContactAnnotationMixin, ObjectListView):
    """Class to list all ContactAnnotation instances,
    or create new ContactAnnotation instance."""
    pass


class ContactAnnotationDetail(ContactAnnotationMixin, ObjectDetailView):
    """
    Class to retrieve, update or delete ContactAnnotation instance.
    """
    pass


class ContactCategoryMixin(object):
    """ContactCategory mixin class."""
    queryset = models.ContactCategory.objects.all()
    serializer_class = serializers.ContactCategorySerializer


class ContactCategoryList(ContactCategoryMixin, ObjectListView):
    """Class to list all ContactCategory instances,
    or create new ContactCategory instance."""
    pass


class ContactCategoryDetail(ContactCategoryMixin, ObjectDetailView):
    """
    Class to retrieve, update or delete ContactCategory instance.
    """
    pass


class ContactEmailMixin(object):
    """ContactEmail mixin class."""
    queryset = models.ContactEmail.objects.all()
    serializer_class = serializers.ContactEmailSerializer


class ContactEmailList(ContactEmailMixin, ObjectListView):
    """Class to list all ContactEmail instances,
    or create new ContactEmail instance."""
    pass


class ContactEmailDetail(ContactEmailMixin, ObjectDetailView):
    """
    Class to retrieve, update or delete ContactEmail instance.
    """
    pass


class ContactFormattedNameMixin(object):
    """ContactFormattedName mixin class."""
    queryset = models.ContactFormattedName.objects.all()
    serializer_class = serializers.ContactFormattedNameSerializer


class ContactFormattedNameList(ContactFormattedNameMixin, ObjectListView):
    """Class to list all ContactFormattedName instances,
    or create new ContactFormattedName instance."""
    pass


class ContactFormattedNameDetail(ContactFormattedNameMixin, ObjectDetailView):
    """
    Class to retrieve, update or delete ContactFormattedName instance.
    """
    pass


class ContactGeographicLocationMixin(object):
    """ContactGeographicLocation mixin class."""
    queryset = models.ContactGeographicLocation.objects.all()
    serializer_class = serializers.ContactGeographicLocationSerializer


class ContactGeographicLocationList(ContactGeographicLocationMixin,
                                    ObjectListView):
    """Class to list all ContactGeographicLocation instances,
    or create new ContactGeographicLocation instance."""
    pass


class ContactGeographicLocationDetail(ContactGeographicLocationMixin,
                                      ObjectDetailView):
    """
    Class to retrieve, update or delete ContactGeographicLocation instance.
    """
    pass


class ContactGroupMixin(object):
    """ContactGroup mixin class."""
    queryset = models.ContactGroup.objects.all()
    serializer_class = serializers.ContactGroupSerializer


class ContactGroupList(ContactGroupMixin, ObjectListView):
    """Class to list all ContactGroup instances,
    or create new ContactGroup instance."""
    pass


class ContactGroupDetail(ContactGroupMixin, ObjectDetailView):
    """
    Class to retrieve, update or delete ContactGroup instance.
    """
    pass


class ContactLogoMixin(object):
    """ContactLogo mixin class."""
    queryset = models.ContactLogo.objects.all()
    serializer_class = serializers.ContactLogoSerializer


class ContactLogoList(ContactLogoMixin, ObjectListView):
    """Class to list all ContactLogo instances,
    or create new ContactLogo instance."""
    pass


class ContactLogoDetail(ContactLogoMixin, ObjectDetailView):
    """
    Class to retrieve, update or delete ContactLogo instance.
    """
    pass


class ContactPhotoMixin(object):
    """ContactPhoto mixin class."""
    queryset = models.ContactPhoto.objects.all()
    serializer_class = serializers.ContactPhotoSerializer


class ContactPhotoList(ContactPhotoMixin, ObjectListView):
    """Class to list all ContactPhoto instances,
    or create new ContactPhoto instance."""
    pass


class ContactPhotoDetail(ContactPhotoMixin, ObjectDetailView):
    """
    Class to retrieve, update or delete ContactPhoto instance.
    """
    pass


class ContactInstantMessagingMixin(object):
    """ContactInstantMessaging mixin class."""
    queryset = models.ContactInstantMessaging.objects.all()
    serializer_class = serializers.ContactInstantMessagingSerializer


class ContactInstantMessagingList(ContactInstantMessagingMixin,
                                  ObjectListView):
    """Class to list all ContactInstantMessaging instances,
    or create new ContactInstantMessaging instance."""
    pass


class ContactInstantMessagingDetail(ContactInstantMessagingMixin,
                                    ObjectDetailView):
    """
    Class to retrieve, update or delete ContactInstantMessaging instance.
    """
    pass


class ContactLanguageMixin(object):
    """ContactLanguage mixin class."""
    queryset = models.ContactLanguage.objects.all()
    serializer_class = serializers.ContactLanguageSerializer


class ContactLanguageList(ContactLanguageMixin,
                          ObjectListView):
    """Class to list all ContactLanguageinstances,
    or create new ContactLanguage instance."""
    pass


class ContactLanguageDetail(ContactLanguageMixin,
                            ObjectDetailView):
    """
    Class to retrieve, update or delete ContactLanguage instance.
    """
    pass


class ContactNameMixin(object):
    """ContactName mixin class."""
    queryset = models.ContactName.objects.all()
    serializer_class = serializers.ContactNameSerializer


class ContactNameList(ContactNameMixin,
                      ObjectListView):
    """Class to list all ContactNameinstances,
    or create new ContactName instance."""
    pass


class ContactNameDetail(ContactNameMixin,
                        ObjectDetailView):
    """
    Class to retrieve, update or delete ContactName instance.
    """
    pass


class ContactNicknameMixin(object):
    """ContactNickname mixin class."""
    queryset = models.ContactNickname.objects.all()
    serializer_class = serializers.ContactNicknameSerializer


class ContactNicknameList(ContactNicknameMixin,
                          ObjectListView):
    """Class to list all ContactNickname instances,
    or create new ContactNickname instance."""
    pass


class ContactNicknameDetail(ContactNicknameMixin,
                            ObjectDetailView):
    """
    Class to retrieve, update or delete ContactNickname instance.
    """
    pass


class ContactOrganizationMixin(object):
    """ContactOrganization mixin class."""
    queryset = models.ContactOrganization.objects.all()
    serializer_class = serializers.ContactOrganizationSerializer


class ContactOrganizationList(ContactOrganizationMixin,
                              ObjectListView):
    """Class to list all ContactOrganization instances,
    or create new ContactOrganization instance."""
    pass


class ContactOrganizationDetail(ContactOrganizationMixin,
                                ObjectDetailView):
    """
    Class to retrieve, update or delete ContactOrganization instance.
    """
    pass


class ContactPhoneMixin(object):
    """ContactPhone mixin class."""
    queryset = models.ContactPhone.objects.all()
    serializer_class = serializers.ContactPhoneSerializer


class ContactPhoneList(ContactPhoneMixin,
                       ObjectListView):
    """Class to list all ContactPhone instances,
    or create new ContactPhone instance."""
    pass


class ContactPhoneDetail(ContactPhoneMixin,
                         ObjectDetailView):
    """
    Class to retrieve, update or delete ContactPhone instance.
    """
    pass


class ContactRoleMixin(object):
    """ContactRole mixin class."""
    queryset = models.ContactRole.objects.all()
    serializer_class = serializers.ContactRoleSerializer


class ContactRoleList(ContactRoleMixin,
                      ObjectListView):
    """Class to list all ContactRole instances,
    or create new ContactRole instance."""
    pass


class ContactRoleDetail(ContactRoleMixin,
                        ObjectDetailView):
    """
    Class to retrieve, update or delete ContactRole instance.
    """
    pass


class ContactTimezoneMixin(object):
    """ContactTimezone mixin class."""
    queryset = models.ContactTimezone.objects.all()
    serializer_class = serializers.ContactTimezoneSerializer


class ContactTimezoneList(ContactTimezoneMixin,
                          ObjectListView):
    """Class to list all ContactTimezone instances,
    or create new ContactRole instance."""
    pass


class ContactTimezoneDetail(ContactTimezoneMixin,
                            ObjectDetailView):
    """
    Class to retrieve, update or delete ContactTimezone instance.
    """
    pass


class ContactTitleMixin(object):
    """ContactTitle mixin class."""
    queryset = models.ContactTitle.objects.all()
    serializer_class = serializers.ContactTitleSerializer


class ContactTitleList(ContactTitleMixin,
                       ObjectListView):
    """Class to list all ContactTitle instances,
    or create new ContactTitle instance."""
    pass


class ContactTitleDetail(ContactTitleMixin,
                         ObjectDetailView):
    """
    Class to retrieve, update or delete ContactTitle instance.
    """
    pass


class ContactUrlMixin(object):
    """ContactUrl mixin class."""
    queryset = models.ContactUrl.objects.all()
    serializer_class = serializers.ContactUrlSerializer


class ContactUrlList(ContactUrlMixin,
                     ObjectListView):
    """Class to list all ContactUrl instances,
    or create new ContactUrl instance."""
    pass


class ContactUrlDetail(ContactUrlMixin,
                       ObjectDetailView):
    """
    Class to retrieve, update or delete ContactUrl instance.
    """
    pass


class RelatedContactMixin(object):
    """RelatedContact mixin class."""
    queryset = models.RelatedContact.objects.all()
    serializer_class = serializers.RelatedContactSerializer


class RelatedContactList(RelatedContactMixin,
                         ObjectListView):
    """Class to list all RelatedContact instances,
    or create new ContactUrl instance."""
    pass


class RelatedContactDetail(RelatedContactMixin,
                           ObjectDetailView):
    """
    Class to retrieve, update or delete RelatedContact instance.
    """
    pass


def contacts_urls(request, content_format):
    """Return contacts application end points."""
    return {
        'contacts': reverse(
            'contact-list',
            request=request,
            format=content_format),
        'contact-addresses': reverse(
            'contact-address-list',
            request=request,
            format=content_format),
        'contact-annotations': reverse(
            'contact-annotation-list',
            request=request,
            format=content_format),
        'contact-categories': reverse(
            'contact-category-list',
            request=request,
            format=content_format),
        'contact-emails': reverse(
            'contact-email-list',
            request=request,
            format=content_format),
        'contact-formatted-names': reverse(
            'contact-formatted-name-list',
            request=request,
            format=content_format),
        'contact-geographic-locations': reverse(
            'contact-geographic-location-list',
            request=request,
            format=content_format),
        'contact-groups': reverse(
            'contact-group-list',
            request=request,
            format=content_format),
        'contact-instant-messaging': reverse(
            'contact-instant-messaging-list',
            request=request,
            format=content_format),
        'contact-languages': reverse(
            'contact-language-list',
            request=request,
            format=content_format),
        'contact-logos': reverse(
            'contact-logo-list',
            request=request,
            format=content_format),
        'contact-names': reverse(
            'contact-name-list',
            request=request,
            format=content_format),
        'contact-nicknames': reverse(
            'contact-nickname-list',
            request=request,
            format=content_format),
        'contact-organizations': reverse(
            'contact-organization-list',
            request=request,
            format=content_format),
        'contact-phones': reverse(
            'contact-phone-list',
            request=request,
            format=content_format),
        'contact-photos': reverse(
            'contact-photo-list',
            request=request,
            format=content_format),
        'contact-roles': reverse(
            'contact-role-list',
            request=request,
            format=content_format),
        'contact-timezones': reverse(
            'contact-timezone-list',
            request=request,
            format=content_format),
        'contact-titles': reverse(
            'contact-title-list',
            request=request,
            format=content_format),
        'contact-types': reverse(
            'contact-type-list',
            request=request,
            format=content_format),
        'contact-relationship-types': reverse(
            'contact-relationship-type-list',
            request=request,
            format=content_format),
        'contact-urls': reverse(
            'contact-url-list',
            request=request,
            format=content_format),
        'related-contacts': reverse(
            'related-contact-list',
            request=request,
            format=content_format),
    }


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_root(request, content_format=None):
    end_points = {}
    base_url_functions = (
        core_model_views.core_urls,
        core_model_views.demographics_urls,
        core_model_views.images_urls,
        core_model_views.locations_urls,
        core_model_views.organizations_urls,
        core_model_views.social_media_urls,
        core_model_views.root_urls)
    contacts_url_functions = (contacts_urls, )
    for url_function in base_url_functions + contacts_url_functions:
        end_points.update(url_function(request, content_format))
    return Response(collections.OrderedDict(sorted(end_points.items())))
