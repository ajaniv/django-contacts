===============
django-contacts
===============

The *django-contacts* project objectives are to address the following primary use cases:

* Capture a contact definition inspired by `VCARD RFC6350  <https://tools.ietf.org/html/rfc6350/>`_.
* Organize contacts by groups (i.e builders, dentists) , contact type (i.e. individual, corporate), and category (i.e. friends, vendors, family).
* A contact may belong to one or more contact groups and contact categories.
* Defined relationships between contacts such as parent, child, co-worker.
* Contacts can be both private to an individual owner as well as shared by multiple users and groups.
* Changes to a contact can be made only by authorized user/users.
* Register interest to receive notifications when changes are made to contact/contacts.  
* Import/export from iPhone, Android, other sources using multiple formats including VCARD.
* Export/import to/from email.

It was developed using Django 1.9.4 for python 2.7, python 3.5, sqlite, MySql and Postgres.
*tox*, *Travis*, *Docker* and *coverage* are used for unit test execution.  The unit tests
are also executed under Django 1.8.

Detailed documentation may be found in the "docs" directory.

Contact ownership/permissions
-----------------------------
* Private contact is one that only its  creator can update and read.  Creator can designate users, user groups as being able to have read or read/write access
* Shared contact is one to which several user, user groups have read or read/write access
* Contact permission is a relationship:

	- contact ->user
	- contact->user group
	- contact->permissions(read/write)
	
The underlying implementation of permissions at the contact level is using `django-guardian`_.

Individual using shared site
----------------------------

* Registers to web site
* Uploads contacts
* Each contact that is uploaded has default permissions of private.
* Individual may grant others access to contact.
* User has default profile with default owner permissions

Corporate site
--------------

* As for individual using shared site except that each contract created by default has shared access to user, groups as per profile.

Connected contacts
------------------

* Further analysis is required to determine what it means to have 'connected-contacts'.


Build Status
------------

.. image:: https://travis-ci.org/ajaniv/django-contacts.svg?branch=master
    :target: https://travis-ci.org/ajaniv/django-contacts

Attributes
----------
Minimal attributes required to define a contact are either name or formatted_name.

* addresses
* anniversary
* annotations
* birth_date
* categories
* contact_type
* emails
* formatted_name
* formatted_names
* gender
* geographic_locations
* groups
* instant_messaging
* languages
* logos
* name
* names
* nicknames
* organizations
* phones
* photos
* related_contacts
* roles
* timezones
* titles
* urls



Quick start
-----------

1. Add the relevant applications to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        contacts.apps.ContactsConfig',
    
       
    ]
    
    
Dependencies
------------

Development/Runtime
^^^^^^^^^^^^^^^^^^^

* `djangorestframework`_.
* `django-core-models`_.
* `django-core-utils`_.
* `python-core-utils`_.


Testing
^^^^^^^

* `django-core-utils-tests  <https://github.com/ajaniv/django-core-utils-tests/>`_.


Development
^^^^^^^^^^^

* coverage
* flake8
* tox
* virtualenv

Command line scenarios
^^^^^^^^^^^^^^^^^^^^^^
These sample scenarios were executed using the `http <https://github.com/jkbrzt/httpie>`_ command line utility.
Replace ContactType with other resources such as ContactRelationshipType and Contact.

Create (ContactType)  with basic authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
All the mandatory fields are specified.
Request::

	http -v -a admin:admin123 --json POST http://127.0.0.1:8000/api/contacts/contact-types/ name="Shared Enterprise"  creation_user=1 effective_user=1 update_user=1 site=1

Response::

	POST /api/contacts/contact-types/ HTTP/1.1
	Accept: application/json
	Accept-Encoding: gzip, deflate
	Authorization: Basic YWRtaW46YWRtaW4xMjM=
	Connection: keep-alive
	Content-Length: 107
	Content-Type: application/json
	Host: 127.0.0.1:8000
	User-Agent: HTTPie/0.9.3
	
	{
	    "creation_user": "1",
	    "effective_user": "1",
	    "name": "Shared Enterprise",
	    "site": "1",
	    "update_user": "1"
	}
	
	HTTP/1.0 201 Created
	Allow: GET, POST, HEAD, OPTIONS
	Content-Type: application/json
	Date: Sun, 26 Jun 2016 23:09:59 GMT
	Server: WSGIServer/0.2 CPython/3.5.1
	Vary: Accept, Cookie
	X-Frame-Options: SAMEORIGIN
	
	{
	    "alias": null,
	    "creation_time": "2016-06-26T23:09:59.802011Z",
	    "creation_user": 1,
	    "deleted": false,
	    "description": null,
	    "effective_user": 1,
	    "enabled": true,
	    "id": 3,
	    "name": "Shared Enterprise",
	    "site": 1,
	    "update_time": "2016-06-26T23:09:59.802067Z",
	    "update_user": 1,
	    "uuid": "3088cb1d-40e5-4563-af77-be036b1c3d0d",
	    "version": 1
	}



Delete (ContactType) with basic authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Request::

	http -v -a admin:admin123 --json DELETE http://127.0.0.1:8000/api/contacts/contact-types/3/

Response::

	DELETE /api/contacts/contact-types/3/ HTTP/1.1
	Accept: application/json
	Accept-Encoding: gzip, deflate
	Authorization: Basic YWRtaW46YWRtaW4xMjM=
	Connection: keep-alive
	Content-Length: 0
	Content-Type: application/json
	Host: 127.0.0.1:8000
	User-Agent: HTTPie/0.9.3
	
	
	
	HTTP/1.0 204 No Content
	Allow: GET, PUT, DELETE, HEAD, OPTIONS
	Content-Length: 0
	Date: Sun, 26 Jun 2016 23:17:49 GMT
	Server: WSGIServer/0.2 CPython/3.5.1
	Vary: Accept, Cookie
	X-Frame-Options: SAMEORIGIN

Create (ContactType) providing specific api version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If the api version is not provided, a default value of the current version is used.

Request::

	http -v -a admin:admin123 --json POST http://127.0.0.1:8000/api/contacts/contact-types/ name="Shared Enterprise"  creation_user=1 effective_user=1 update_user=1 site=1 'Accept: application/json; version=1.0'


Response::


	POST /api/contacts/contact-types/ HTTP/1.1
	Accept:  application/json; version=1.0
	Accept-Encoding: gzip, deflate
	Authorization: Basic YWRtaW46YWRtaW4xMjM=
	Connection: keep-alive
	Content-Length: 107
	Content-Type: application/json
	Host: 127.0.0.1:8000
	User-Agent: HTTPie/0.9.3
	
	{
	    "creation_user": "1",
	    "effective_user": "1",
	    "name": "Shared Enterprise",
	    "site": "1",
	    "update_user": "1"
	}
	
	HTTP/1.0 201 Created
	Allow: GET, POST, HEAD, OPTIONS
	Content-Type: application/json; version=1.0
	Date: Sun, 26 Jun 2016 23:24:36 GMT
	Server: WSGIServer/0.2 CPython/3.5.1
	Vary: Accept, Cookie
	X-Frame-Options: SAMEORIGIN
	
	{
	    "alias": null,
	    "creation_time": "2016-06-26T23:24:36.796795Z",
	    "creation_user": 1,
	    "deleted": false,
	    "description": null,
	    "effective_user": 1,
	    "enabled": true,
	    "id": 4,
	    "name": "Shared Enterprise",
	    "site": 1,
	    "update_time": "2016-06-26T23:24:36.796841Z",
	    "update_user": 1,
	    "uuid": "99cdc9d4-1f65-4c2b-9a1a-00a199b024e7",
	    "version": 1
	}


Update (ContactType) providing subset of fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Only the  fields required to validate the instance are required.  Further implementation work is required
to simplify the approach.

Request::

	http -v -a admin:admin123 --json PUT http://127.0.0.1:8000/api/contacts/contact-types/4/ name="Shared Enterprise"  alias="Shared"

Response::

	PUT /api/contacts/contact-types/4/ HTTP/1.1
	Accept: application/json
	Accept-Encoding: gzip, deflate
	Authorization: Basic YWRtaW46YWRtaW4xMjM=
	Connection: keep-alive
	Content-Length: 48
	Content-Type: application/json
	Host: 127.0.0.1:8000
	User-Agent: HTTPie/0.9.3
	
	{
	    "alias": "Shared",
	    "name": "Shared Enterprise"
	}
	
	HTTP/1.0 200 OK
	Allow: GET, PUT, DELETE, HEAD, OPTIONS
	Content-Type: application/json
	Date: Sun, 26 Jun 2016 23:28:08 GMT
	Server: WSGIServer/0.2 CPython/3.5.1
	Vary: Accept, Cookie
	X-Frame-Options: SAMEORIGIN
	
	{
	    "alias": "Shared",
	    "creation_time": "2016-06-26T23:24:36.796795Z",
	    "creation_user": 1,
	    "deleted": false,
	    "description": null,
	    "effective_user": 2,
	    "enabled": true,
	    "id": 4,
	    "name": "Shared Enterprise",
	    "site": 1,
	    "update_time": "2016-06-26T23:28:08.351774Z",
	    "update_user": 2,
	    "uuid": "99cdc9d4-1f65-4c2b-9a1a-00a199b024e7",
	    "version": 2
	}


Create (ContactType) providing subset of fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specify minimal set of required fields while the remainder are derived from the request context

Request::

	http -v -a admin:admin123 --json POST http://127.0.0.1:8000/api/contacts/contact-types/ name="Shared Individual" 'Accept: application/json; version=1.0'

Response::

	POST /api/contacts/contact-types/ HTTP/1.1
	Accept:  application/json; version=1.0
	Accept-Encoding: gzip, deflate
	Authorization: Basic YWRtaW46YWRtaW4xMjM=
	Connection: keep-alive
	Content-Length: 29
	Content-Type: application/json
	Host: 127.0.0.1:8000
	User-Agent: HTTPie/0.9.3
	
	{
	    "name": "Shared Individual"
	}
	
	HTTP/1.0 201 Created
	Allow: GET, POST, HEAD, OPTIONS
	Content-Type: application/json; version=1.0
	Date: Sun, 26 Jun 2016 23:31:29 GMT
	Server: WSGIServer/0.2 CPython/3.5.1
	Vary: Accept, Cookie
	X-Frame-Options: SAMEORIGIN
	
	{
	    "alias": null,
	    "creation_time": "2016-06-26T23:31:29.164140Z",
	    "creation_user": 2,
	    "deleted": false,
	    "description": null,
	    "effective_user": 2,
	    "enabled": true,
	    "id": 5,
	    "name": "Shared Individual",
	    "site": 1,
	    "update_time": "2016-06-26T23:31:29.164187Z",
	    "update_user": 2,
	    "uuid": "80cf11bf-2551-4b7d-8b29-b67c65dba5ac",
	    "version": 1
	}

Get all instances (ContactType)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Request::

	http -v -a admin:admin123 --json GET http://127.0.0.1:8000/api/contacts/contact-types/

Response::

	GET /api/contacts/contact-types/ HTTP/1.1
	Accept: application/json
	Accept-Encoding: gzip, deflate
	Authorization: Basic YWRtaW46YWRtaW4xMjM=
	Connection: keep-alive
	Content-Type: application/json
	Host: 127.0.0.1:8000
	User-Agent: HTTPie/0.9.3
	
	
	
	HTTP/1.0 200 OK
	Allow: GET, POST, HEAD, OPTIONS
	Content-Type: application/json
	Date: Sun, 26 Jun 2016 23:42:25 GMT
	Server: WSGIServer/0.2 CPython/3.5.1
	Vary: Accept, Cookie
	X-Frame-Options: SAMEORIGIN
	
	[
	    {
	        "alias": "",
	        "creation_time": "2016-06-05T22:50:50.641807Z",
	        "creation_user": 2,
	        "deleted": false,
	        "description": "",
	        "effective_user": 2,
	        "enabled": true,
	        "id": 2,
	        "name": "Organization",
	        "site": 1,
	        "update_time": "2016-06-05T22:50:50.642022Z",
	        "update_user": 2,
	        "uuid": "cde5f16e-cc50-4e3b-976e-c505b4ca8888",
	        "version": 1
	    },
	    {
	        "alias": "",
	        "creation_time": "2016-05-30T21:24:59.951750Z",
	        "creation_user": 2,
	        "deleted": false,
	        "description": "",
	        "effective_user": 2,
	        "enabled": true,
	        "id": 1,
	        "name": "Private",
	        "site": 1,
	        "update_time": "2016-05-30T21:24:59.952078Z",
	        "update_user": 2,
	        "uuid": "dc615ecf-583f-48bc-bdc9-5944de684c9f",
	        "version": 1
	    },
	    {
	        "alias": "Shared",
	        "creation_time": "2016-06-26T23:24:36.796795Z",
	        "creation_user": 1,
	        "deleted": false,
	        "description": null,
	        "effective_user": 2,
	        "enabled": true,
	        "id": 4,
	        "name": "Shared Enterprise",
	        "site": 1,
	        "update_time": "2016-06-26T23:28:08.351774Z",
	        "update_user": 2,
	        "uuid": "99cdc9d4-1f65-4c2b-9a1a-00a199b024e7",
	        "version": 2
	    },
	    {
	        "alias": null,
	        "creation_time": "2016-06-26T23:31:29.164140Z",
	        "creation_user": 2,
	        "deleted": false,
	        "description": null,
	        "effective_user": 2,
	        "enabled": true,
	        "id": 5,
	        "name": "Shared Individual",
	        "site": 1,
	        "update_time": "2016-06-26T23:31:29.164187Z",
	        "update_user": 2,
	        "uuid": "80cf11bf-2551-4b7d-8b29-b67c65dba5ac",
	        "version": 1
	    }
	]


Browser scenarios
^^^^^^^^^^^^^^^^^
These scenarios were executed using a browser navigating Django Rest Framework urls.

Show list of end points
~~~~~~~~~~~~~~~~~~~~~~~
Request::

	http://127.0.0.1:8000/api/root/end-points/
	
Response::

	Api Root
	GET /api/root/end-points/
	HTTP 200 OK
	Allow: OPTIONS, GET
	Content-Type: application/json
	Vary: Accept
	
	{
	    "address-types": "http://127.0.0.1:8000/api/locations/address-types/",
	    "addresses": "http://127.0.0.1:8000/api/locations/addresses/",
	    "ages": "http://127.0.0.1:8000/api/demographics/ages/",
	    "annotations": "http://127.0.0.1:8000/api/core-models/annotations/",
	    "categories": "http://127.0.0.1:8000/api/core-models/categories/",
	    "child-count": "http://127.0.0.1:8000/api/demographics/child-count/",
	    "cities": "http://127.0.0.1:8000/api/locations/cities/",
	    "contact-relationship-types": "http://127.0.0.1:8000/api/contacts/contact-relationship-types/",
	    "contact-types": "http://127.0.0.1:8000/api/contacts/contact-types/",
	    "contacts": "http://127.0.0.1:8000/api/contacts/contacts/",
	    "countries": "http://127.0.0.1:8000/api/locations/countries/",
	    "currencies": "http://127.0.0.1:8000/api/core-models/currencies/",
	    "demographic-regions": "http://127.0.0.1:8000/api/demographics/demographic-regions/",
	    "distance-units": "http://127.0.0.1:8000/api/locations/distance-units/",
	    "document-orientations": "http://127.0.0.1:8000/api/images/document-orientations/",
	    "education-levels": "http://127.0.0.1:8000/api/demographics/education-levels/",
	    "email-types": "http://127.0.0.1:8000/api/social-media/email-types/",
	    "ethnicities": "http://127.0.0.1:8000/api/demographics/ethnicities/",
	    "formatted-names": "http://127.0.0.1:8000/api/social-media/formatted-names/",
	    "gender": "http://127.0.0.1:8000/api/demographics/gender/",
	    "geographic-location": "http://127.0.0.1:8000/api/locations/geographic-locations/",
	    "geographic-location-types": "http://127.0.0.1:8000/api/locations/geographic-location-types/",
	    "groups": "http://127.0.0.1:8000/api/social-media/groups/",
	    "household-size": "http://127.0.0.1:8000/api/demographics/household-size/",
	    "image-formats": "http://127.0.0.1:8000/api/images/image-formats/",
	    "images": "http://127.0.0.1:8000/api/images/images/",
	    "incomes": "http://127.0.0.1:8000/api/demographics/incomes/",
	    "instant-messaging-types": "http://127.0.0.1:8000/api/social-media/instant-messaging-types/",
	    "language-types": "http://127.0.0.1:8000/api/locations/language-types/",
	    "languages": "http://127.0.0.1:8000/api/locations/languages/",
	    "logo-types": "http://127.0.0.1:8000/api/social-media/logo-types/",
	    "names": "http://127.0.0.1:8000/api/social-media/names/",
	    "nickname-types": "http://127.0.0.1:8000/api/social-media/nickname-types/",
	    "organization-types": "http://127.0.0.1:8000/api/organizations/organization-types/",
	    "organization-units": "http://127.0.0.1:8000/api/organizations/organization-units/",
	    "organizations": "http://127.0.0.1:8000/api/organizations/organizations/",
	    "phone-types": "http://127.0.0.1:8000/api/social-media/phone-types/",
	    "photo-types": "http://127.0.0.1:8000/api/social-media/photo-types/",
	    "provinces": "http://127.0.0.1:8000/api/locations/proninces/",
	    "roles": "http://127.0.0.1:8000/api/organizations/roles/",
	    "states": "http://127.0.0.1:8000/api/locations/states/",
	    "timezone-types": "http://127.0.0.1:8000/api/locations/timezone-types/",
	    "timezones": "http://127.0.0.1:8000/api/locations/timezones/",
	    "titles": "http://127.0.0.1:8000/api/organizations/titles/",
	    "url-types": "http://127.0.0.1:8000/api/social-media/url-types/",
	    "users": "http://127.0.0.1:8000/api/root/users/"
	}
	
Show list of ContactTypes
~~~~~~~~~~~~~~~~~~~~~~~~~
Request::

	http://127.0.0.1:8000/api/contacts/contact-types/
	
Response::

	GET /api/contacts/contact-types/
	HTTP 200 OK
	Allow: GET, POST, HEAD, OPTIONS
	Content-Type: application/json
	Vary: Accept
	
	[
	    {
	        "id": 2,
	        "uuid": "cde5f16e-cc50-4e3b-976e-c505b4ca8888",
	        "version": 1,
	        "enabled": true,
	        "deleted": false,
	        "creation_time": "2016-06-05T22:50:50.641807Z",
	        "update_time": "2016-06-05T22:50:50.642022Z",
	        "creation_user": 2,
	        "update_user": 2,
	        "effective_user": 2,
	        "site": 1,
	        "name": "Organization",
	        "alias": "",
	        "description": ""
	    },
	    {
	        "id": 1,
	        "uuid": "dc615ecf-583f-48bc-bdc9-5944de684c9f",
	        "version": 1,
	        "enabled": true,
	        "deleted": false,
	        "creation_time": "2016-05-30T21:24:59.951750Z",
	        "update_time": "2016-05-30T21:24:59.952078Z",
	        "creation_user": 2,
	        "update_user": 2,
	        "effective_user": 2,
	        "site": 1,
	        "name": "Private",
	        "alias": "",
	        "description": ""
	    },
	    {
	        "id": 4,
	        "uuid": "99cdc9d4-1f65-4c2b-9a1a-00a199b024e7",
	        "version": 2,
	        "enabled": true,
	        "deleted": false,
	        "creation_time": "2016-06-26T23:24:36.796795Z",
	        "update_time": "2016-06-26T23:28:08.351774Z",
	        "creation_user": 1,
	        "update_user": 2,
	        "effective_user": 2,
	        "site": 1,
	        "name": "Shared Enterprise",
	        "alias": "Shared",
	        "description": null
	    },
	    {
	        "id": 5,
	        "uuid": "80cf11bf-2551-4b7d-8b29-b67c65dba5ac",
	        "version": 1,
	        "enabled": true,
	        "deleted": false,
	        "creation_time": "2016-06-26T23:31:29.164140Z",
	        "update_time": "2016-06-26T23:31:29.164187Z",
	        "creation_user": 2,
	        "update_user": 2,
	        "effective_user": 2,
	        "site": 1,
	        "name": "Shared Individual",
	        "alias": null,
	        "description": null
	    }
	]

Docker unit test execution
--------------------------
To run unit tests in docker environment:

* sqlite: `docker-compose -f docker-sqlite-compose-test.yml up --abort-on-container-exit` .
* postgres: `docker-compose -f docker-postgres-compose-test.yml up --abort-on-container-exit` .
* mysql: `docker-compose -f docker-mysql-compose-test.yml up --abort-on-container-exit` .

Docker container execution
--------------------------
To run browser against a docker container:

* sqlite: `docker-compose -f docker-sqlite-compose.yml up -d` .
* postgres: `docker-compose -f docker-postgres-compose.yml up -d` .
* mysql: `docker-compose -f docker-mysql-compose.yml up -d`.

Set the browser address to the ip address returned from `docker-machine ip`.
For example: `http://192.168.99.100:8000/`

Docker notes
------------

* In order to configure command line docker environment:

    #. docker-machine restart default
    #. eval $(docker-machine env default)


* To remove all containers: `docker rm $(docker ps -a -q)`
* To remove all images: `docker rmi -f $(docker images -q)`



Other
-----

* pandoc may be used to convert from .rst to .md:

  ``pandoc -f rst -t markdown_github -o README.md README.rst``
  
* check-manifest was run from the command line.  Could not get it
  to work from within tox.  There was an error in handling '~'
  with gitconfig when running:
  
  ``git ls-files -z``    
  
* To create admin super user: `create_super_user.py`

To do
-----
* Generate sphinix and/or markup documentation.



.. _djangorestframework: http://www.django-rest-framework.org/
.. _django-core-utils: https://github.com/ajaniv/django-core-utils/
.. _django-core-models: https://github.com/ajaniv/django-core-models/
.. _python-core-utils: https://github.com/ajaniv/python-core-utils/
.. _django-guardian:  https://github.com/django-guardian/django-guardian/