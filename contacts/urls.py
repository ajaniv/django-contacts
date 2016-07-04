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


]
