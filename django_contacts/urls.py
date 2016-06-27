"""django_core_models URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns

from django_core_utils.views import UserList, UserDetail
from contacts import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='/admin')),

]


urlpatterns_api_base = [
    url(r'^api/root/end-points/$', views.api_root, name='api-list'),
    url(r'^api/root/users/$', UserList.as_view(), name='user-list'),
    url(r'^api/root/users/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(), name='user-detail'),
]


urlpatterns_api_core_models = [
    # url(r'^api/root/', include('django_core_models.urls')),
    url(r'^api/core-models/', include('django_core_models.core.urls')),
    url(r'^api/demographics/',
        include('django_core_models.demographics.urls')),
    url(r'^api/images/',
        include('django_core_models.images.urls')),
    url(r'^api/locations/',
        include('django_core_models.locations.urls')),
    url(r'^api/organizations/',
        include('django_core_models.organizations.urls')),
    url(r'^api/social-media/',
        include('django_core_models.social_media.urls')),
]

urlpatterns_api_contacts = [
    url(r'^api/contacts/', include('contacts.urls')),
]

urlpatterns_api = (urlpatterns_api_core_models +
                   urlpatterns_api_contacts +
                   urlpatterns_api_base)

urlpatterns_rest_framework = [
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
    ]

urlpatterns = (format_suffix_patterns(urlpatterns_api) +
               urlpatterns +
               urlpatterns_rest_framework)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
