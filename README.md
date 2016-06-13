# django-hooks

[![Build Status](https://img.shields.io/travis/nitely/django-hooks.svg?style=flat-square)](https://travis-ci.org/nitely/django-hooks)
[![Coverage Status](https://img.shields.io/coveralls/nitely/django-hooks.svg?style=flat-square)](https://coveralls.io/r/nitely/django-hooks)
[![pypi](https://img.shields.io/pypi/v/django-hooks.svg?style=flat-square)](https://pypi.python.org/pypi/django-hooks)
[![licence](https://img.shields.io/pypi/l/django-hooks.svg?style=flat-square)](https://raw.githubusercontent.com/nitely/django-hooks/master/LICENSE)

A modular plugin system for django apps.

There are 4 kinds of hooks:

* TemplateHook: Third-party apps will be able to insert their own code (text/html) into a template.
* ModelHook: Third-party apps will be able to add fields and methods to a model.
* FormHook: Third-party apps will be able to insert Forms in a view.
* ~~ViewHook~~: This is deprecated in favor of FormHook
* SignalHook: Connect or emit a signal by its name/id.
  This is the same as Django signals except that they don't need to be pre-defined.

## Why?

* The app does not have to be built to support plugins from the grown up.
  `django-hooks` can be added as an afterthought.
* It's modular, use the hooks your app needs.
* It's is explicit, there is no magical or surprising behaviour.

## Compatibility

* Django 1.8 LTS; Python 2.7, 3.4 or 3.5

## Documentation

[Read The Docs](http://django-hooks.readthedocs.org/en/latest/)

## License

MIT
