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
    """Class to list all ContactGeographicLocationName instances,
    or create new ContactGeographicLocation instance."""
    pass


class ContactGeographicLocationDetail(ContactGeographicLocationMixin,
                                      ObjectDetailView):
    """
    Class to retrieve, update or delete ContactGeographicLocation instance.
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
        'contact-types': reverse(
            'contact-type-list',
            request=request,
            format=content_format),
        'contact-relationship-types': reverse(
            'contact-relationship-type-list',
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
