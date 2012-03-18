Integration of Soundcloud in Plone
==================================

!!! work in progress !!!

WRITE ME

Installation
============

Just depend in your buildout on the egg ``collective.soundcloud``. ZCML is
loaded automagically with z3c.autoinclude.

Follow the steps needed to get `plone.app.async <http://pypi.python.org/pypi/plone.app.async>`_
to work.

Install it as an addon in Plone control-panel or portal_setup.

This package is written for Plone 4.1 or later.

Configuration
=============

Soundcloud only gives authentication credentials for domains it can resolve.
If you are on your local machine, create a dns entry like "local.yourdomain.com" 
that points to "127.0.0.1"

- Register your app at http://soundcloud.com/you/apps/new
   - Fill in a name for your app
   - add http://local.yourdomain.com:8080/Plone/soundcloud_redirect_handler 
     as your "Redirect URI"

In the soundcloud controlpanel:
- Enter your client id
- Enter your client secret

Source Code and Contributions
=============================

If you want to help with the development (improvement, update, bug-fixing, ...)
of ``collective.soundcloud`` this is a great idea!

The code is located in the
`github collective <https://github.com/collective/collective.soundcloud>`_.

You can clone it or `get access to the github-collective
<http://collective.github.com/>`_ and work directly on the project.

Maintainers are Jens Klein, Peter Holzer and the BlueDynamics Alliance
developer team. We appreciate any contribution and if a release is needed
to be done on pypi, please just contact one of us
`dev@bluedynamics dot com <mailto:dev@bluedynamics.com>`_

Contributors
============

- Jens W. Klein <jens@bluedynamics.com>

- Peter Holzer <hpeter@agitator.com>

