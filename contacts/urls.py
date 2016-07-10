"""
.. module::  contacts.urls
   :synopsis:  contacts application urls module

*contacts* application urls module.

"""
from __future__ import absolute_import
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^contact-relationship-types/$',
        views.ContactRelationshipTypeList.as_view(),
        name="contact-relationship-type-list"),
    url(r'^contact-relationship-types/(?P<pk>[0-9]+)/$',
        views.ContactRelationshipTypeDetail.as_view(),
        name='contact-relationship-type-detail'),

    url(r'^contact-types/$',
        views.ContactTypeList.as_view(),
        name="contact-type-list"),
    url(r'^contact-types/(?P<pk>[0-9]+)/$',
        views.ContactTypeDetail.as_view(),
        name='contact-type-detail'),

    # @TODO: revisit contacts name, results in contacts repeated twice in url
    url(r'^contacts/$',
        views.ContactList.as_view(),
        name='contact-list'),
    url(r'^contacts/(?P<pk>[0-9]+)/$',
        views.ContactDetail.as_view(),
        name='contact-detail'),

    url(r'^contact-addresses/$',
        views.ContactAddressList.as_view(),
        name='contact-address-list'),
    url(r'^contact-addresses/(?P<pk>[0-9]+)/$',
        views.ContactAddressDetail.as_view(),
        name='contact-address-detail'),

    url(r'^contact-annotations/$',
        views.ContactAnnotationList.as_view(),
        name='contact-annotation-list'),
    url(r'^contact-annotations/(?P<pk>[0-9]+)/$',
        views.ContactAnnotationDetail.as_view(),
        name='contact-annotation-detail'),

    url(r'^contact-categories/$',
        views.ContactCategoryList.as_view(),
        name='contact-category-list'),
    url(r'^contact-categories/(?P<pk>[0-9]+)/$',
        views.ContactCategoryDetail.as_view(),
        name='contact-category-detail'),

    url(r'^contact-emails/$',
        views.ContactEmailList.as_view(),
        name='contact-email-list'),
    url(r'^contact-emails/(?P<pk>[0-9]+)/$',
        views.ContactEmailDetail.as_view(),
        name='contact-email-detail'),

    url(r'^contact-formatted-names/$',
        views.ContactFormattedNameList.as_view(),
        name='contact-formatted-name-list'),
    url(r'^contact-formatted-names/(?P<pk>[0-9]+)/$',
        views.ContactFormattedNameDetail.as_view(),
        name='contact-formatted-name-detail'),

    url(r'^contact-geographic-locations/$',
        views.ContactGeographicLocationList.as_view(),
        name='contact-geographic-location-list'),
    url(r'^contact-geographic-locations/(?P<pk>[0-9]+)/$',
        views.ContactGeographicLocationDetail.as_view(),
        name='contact-geographic-location-detail'),

    url(r'^contact-groups/$',
        views.ContactGroupList.as_view(),
        name='contact-group-list'),
    url(r'^contact-groups/(?P<pk>[0-9]+)/$',
        views.ContactGroupDetail.as_view(),
        name='contact-group-detail'),

    url(r'^contact-instant-messaging/$',
        views.ContactInstantMessagingList.as_view(),
        name='contact-instant-messaging-list'),
    url(r'^contact-instant-messaging/(?P<pk>[0-9]+)/$',
        views.ContactInstantMessagingDetail.as_view(),
        name='contact-instant-messaging-detail'),

    url(r'^contact-languages/$',
        views.ContactLanguageList.as_view(),
        name='contact-language-list'),
    url(r'^contact-languages/(?P<pk>[0-9]+)/$',
        views.ContactLanguageDetail.as_view(),
        name='contact-language-detail'),

    url(r'^contact-logos/$',
        views.ContactLogoList.as_view(),
        name='contact-logo-list'),
    url(r'^contact-logos/(?P<pk>[0-9]+)/$',
        views.ContactLogoDetail.as_view(),
        name='contact-logo-detail'),

    url(r'^contact-names/$',
        views.ContactNameList.as_view(),
        name='contact-name-list'),
    url(r'^contact-names/(?P<pk>[0-9]+)/$',
        views.ContactNameDetail.as_view(),
        name='contact-name-detail'),

    url(r'^contact-nicknames/$',
        views.ContactNicknameList.as_view(),
        name='contact-nickname-list'),
    url(r'^contact-nicknames/(?P<pk>[0-9]+)/$',
        views.ContactNicknameDetail.as_view(),
        name='contact-nickname-detail'),

    url(r'^contact-organizations/$',
        views.ContactOrganizationList.as_view(),
        name='contact-organization-list'),
    url(r'^contact-organizations/(?P<pk>[0-9]+)/$',
        views.ContactOrganizationDetail.as_view(),
        name='contact-organization-detail'),

    url(r'^contact-phones/$',
        views.ContactPhoneList.as_view(),
        name='contact-phone-list'),
    url(r'^contact-phones/(?P<pk>[0-9]+)/$',
        views.ContactPhoneDetail.as_view(),
        name='contact-phone-detail'),

    url(r'^contact-photos/$',
        views.ContactPhotoList.as_view(),
        name='contact-photo-list'),
    url(r'^contact-photos/(?P<pk>[0-9]+)/$',
        views.ContactPhotoDetail.as_view(),
        name='contact-photo-detail'),

    url(r'^contact-roles/$',
        views.ContactRoleList.as_view(),
        name='contact-role-list'),
    url(r'^contact-roles/(?P<pk>[0-9]+)/$',
        views.ContactRoleDetail.as_view(),
        name='contact-role-detail'),

    url(r'^contact-timezones/$',
        views.ContactTimezoneList.as_view(),
        name='contact-timezone-list'),
    url(r'^contact-timezones/(?P<pk>[0-9]+)/$',
        views.ContactTimezoneDetail.as_view(),
        name='contact-timezone-detail'),

    url(r'^contact-titles/$',
        views.ContactTitleList.as_view(),
        name='contact-title-list'),
    url(r'^contact-titles/(?P<pk>[0-9]+)/$',
        views.ContactTitleDetail.as_view(),
        name='contact-title-detail'),

    url(r'^contact-urls/$',
        views.ContactUrlList.as_view(),
        name='contact-url-list'),
    url(r'^contact-urls/(?P<pk>[0-9]+)/$',
        views.ContactUrlDetail.as_view(),
        name='contact-url-detail'),

    url(r'^related-contacts/$',
        views.RelatedContactList.as_view(),
        name='contact-url-list'),
    url(r'^related-contacts/(?P<pk>[0-9]+)/$',
        views.RelatedContactDetail.as_view(),
        name='contact-url-detail'),

]
