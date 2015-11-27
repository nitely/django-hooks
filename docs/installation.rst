.. _installation:

Installation
============

Pip
---

Latest django-hooks can be installed via pip::

    $ pip install django-hooks

Django Project
--------------

To load the templatetags add ``hooks`` into ``settings.INSTALLED_APPS``.

Example::

    # settings.py

    INSTALLED_APPS = [
        # ...

        'hooks'
    ]
