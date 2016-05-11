django-contacts
===============

The *django-contacts* project objectives are to address the following primary use cases:

-   Capture a contact definition inspired by [VCARD RFC6350](https://tools.ietf.org/html/rfc6350/).
-   Organize contacts by groups (i.e builders, dentists) , contact type (i.e. individual, corporate), and category (i.e. friends, vendors, family).
-   A contact may belong to one or more contact groups and contact categories.
-   Defined relationships between contacts such as parent, child, co-worker.
-   Contacts can be both private to an individual owner as well as shared by multiple users and groups.
-   Changes to a contact can be made only by authorized user/users.
-   Register interest to receive notifications when changes are made to contact/contacts.
-   Import/export from iPhone, Android, other sources using multiple formats including VCARD.
-   Export/import to/from email.

It was developed using Django 1.9.4 for python 2.7, python 3.5, sqlite, MySql and Postgres. *tox*, *Travis*, *Docker* and *coverage* are used for unit test execution. The unit tests are also executed under Django 1.8.

Detailed documentation may be found in the "docs" directory.

Contact ownership
-----------------

-   Private contact is one that only its creator can update and read. Creator can designate users, user groups as being able to have read or read/write access
-   Shared contact is one to which several user, user groups have read or read/write access
-   Contact permission is a relationship:

    > -   contact -&gt;user
    > -   contact-&gt;user group
    > -   contact-&gt;permissions(read/write)

Individual using shared site
----------------------------

-   Registers to web site
-   Uploads contacts
-   Each contact that is uploaded has default permissions of private.
-   Individual may grant others access to contact.
-   User has default profile with default owner permissions

Corporate site
--------------

-   As for individual using shared site except that each contract created by default has shared access to user, groups as per profile.

Connected contacts
------------------

-   Further analysis is required to determine what it means to have 'connected-contacts'.

Build Status
------------

[![image](https://travis-ci.org/ajaniv/django-core-models.svg?branch=master)](https://travis-ci.org/ajaniv/django-core-models)

Attributes
----------

Minimal attributes required to define a contact are either name or formatted\_name.

-   addresses
-   anniversary
-   annotations
-   birth\_date
-   categories
-   contact\_type
-   emails
-   formatted\_name
-   formatted\_names
-   gender
-   geographic\_locations
-   groups
-   instant\_messaging
-   languages
-   logos
-   name
-   names
-   nicknames
-   organizations
-   phones
-   photos
-   related\_contacts
-   roles
-   timezones
-   titles
-   urls

Quick start
-----------

1.  Add the relevant applications to your INSTALLED\_APPS setting like this:

        INSTALLED_APPS = [
            ...
            contacts.apps.ContactsConfig',


        ]

Dependencies
------------

### Development/Runtime

-   [djangorestframework](http://www.django-rest-framework.org/).
-   [django-core-models](https://github.com/ajaniv/django-core-models/).
-   [django-core-utils](https://github.com/ajaniv/django-core-utils/).
-   [python-core-utils](https://github.com/ajaniv/python-core-utils/).

### Testing

-   [django-core-utils-tests](https://github.com/ajaniv/django-core-utils-tests/).

### Development

-   coverage
-   flake8
-   tox
-   virtualenv

Docker unit test execution
--------------------------

To run unit tests in docker environment:

-   sqlite: docker-compose -f docker-sqlite-compose-test.yml up --abort-on-container-exit .
-   postgres: docker-compose -f docker-postgres-compose-test.yml up --abort-on-container-exit .
-   mysql: docker-compose -f docker-mysql-compose-test.yml up --abort-on-container-exit .

Docker container execution
--------------------------

To run browser against a docker container:

-   sqlite: docker-compose -f docker-sqlite-compose.yml up -d .
-   postgres: docker-compose -f docker-postgres-compose.yml up -d .
-   mysql: docker-compose -f docker-mysql-compose.yml up -d.

Set the browser address to the ip address returned from docker-machine ip. For example: http://192.168.99.100:8000/

Docker notes
------------

-   In order to configure command line docker environment:

    > 1.  docker-machine restart default
    > 2.  eval $(docker-machine env default)

-   To remove all containers: docker rm $(docker ps -a -q)
-   To remove all images: docker rmi -f $(docker images -q)

Other
-----

-   pandoc was used to convert from .rst to .md:

    `pandoc -f rst -t markdown_github -o README.md README.rst`

-   check-manifest was run from the command line. Could not get it to work from within tox. There was an error in handling '~' with gitconfig when running:

    `git ls-files -z`

-   To create admin super user: create\_super\_user.py

To do
-----

-   Generate sphinix and/or markup documentation.

