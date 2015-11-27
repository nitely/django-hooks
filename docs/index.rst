.. django-hooks documentation master file, created by
   sphinx-quickstart on Thu Nov 26 21:02:20 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-hooks
=======================

A modular plugin system for django apps.

There are 3 kinds of hooks:

* TemplateHook: Third-party apps will be able to insert their own code (text/html) into an app template.
* FormHook: Third-party apps will be able to insert Forms in an app view.
* ViewHook: This is deprecated in favor of FormHook
* SignalHook: Connect or emit a signal by its name/id.
  This is the same as Django signals except that they don't need to be pre-defined.

This documentation is divided into different parts.
I recommend that you get started with the Installation and then head over to the Usage.

User’s Guide
------------

.. toctree::
   :maxdepth: 2

   installation
   hooks

API Reference
-------------

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Additional Notes
----------------

Design notes, legal information and changelog are here for the interested.

.. toctree::
   :maxdepth: 2

   changelog
   license
