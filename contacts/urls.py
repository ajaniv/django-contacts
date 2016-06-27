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

    url(r'^contacts/$',
        views.ContactList.as_view(),
        name='contact-list'),
    url(r'^contacts/(?P<pk>[0-9]+)/$',
        views.ContactDetail.as_view(),
        name='contact-detail'),

]
