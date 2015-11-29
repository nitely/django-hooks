# django-hooks

[![Build Status](https://img.shields.io/travis/nitely/django-hooks.svg?style=flat-square)](https://travis-ci.org/nitely/django-hooks)
[![Coverage Status](https://img.shields.io/coveralls/nitely/django-hooks.svg?style=flat-square)](https://coveralls.io/r/nitely/django-hooks)
[![pypi](https://img.shields.io/pypi/v/django-hooks.svg?style=flat-square)](https://pypi.python.org/pypi/django-hooks)
[![licence](https://img.shields.io/pypi/l/django-hooks.svg?style=flat-square)](https://raw.githubusercontent.com/nitely/django-hooks/master/LICENSE)

A modular plugin system for django apps.

There are 3 kinds of hooks:

* TemplateHook: Third-party apps will be able to insert their own code (text/html) into an app template.
* FormHook: Third-party apps will be able to insert Forms in an app view.
* ~~ViewHook~~: This is deprecated in favor of `FormHook`
* SignalHook: Connect or emit a signal by its name/id. This is the same as Django signals
except that they don't need to be pre-defined.

## Why?

Let's say we want to render contextual information beside a record allocated in `my_main_app`.
This extra information can be provided by some third-party application: Notes, Attachments,
Comments, Followers, etc.

Adding an `{% include %}` tag to our `my_record.html` is not possible because we don't know what
to render beforehand (a note? a list of comments?) or even if any of those applications are
installed for our case/customer/project.

We can create a *TemplateHook* `{% hook 'my_contextual_info' %}` where we delegate the rendering and
content retrieval to the hooked app(s). By doing so, `my_record.html` doesn't need to be touched anymore,
no need to add more templatetags to `{% load %}` and we also make it easily reusable.

## Compatibility

* Django 1.8 LTS; Python 2.7, 3.4 or 3.5

## Documentation

[Read The Docs](http://django-hooks.readthedocs.org/en/latest/)

## License

MIT
