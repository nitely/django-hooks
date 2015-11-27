# -*- coding: utf-8 -*-

from __future__ import unicode_literals


__all__ = ['Hook']


class HookFactory(object):
    """
    Hook factory, provide some short-cuts\
    to make a sequence of forms behave as a single form.\
    This is used by :py:class:`Hook`

    :param list instances: Sequence of callables,\
    usually :py:class:`django.forms.Form` or\
    :py:class:`django.forms.ModelForm`
    """
    def __init__(self, instances):
        self.instances = instances

    def __iter__(self):
        """
        Forms iterator

        :yield: Form instance
        """
        for form in self.instances:
            yield form

    def is_valid(self):
        """
        Validate all the forms

        :return: The result of validating all the forms
        :rtype: bool
        """
        # Avoid short-circuit evaluation
        return all([form.is_valid() for form in self.instances])

    def save(self, *args, **kwargs):
        """
        Save all the forms

        :param \*args: Positional arguments passed to the forms
        :param \*\*kwargs: Keyword arguments passed to the forms
        :return: Sequence of returned values by all the forms as tuples of (instance, result)
        :rtype: list
        """
        return [
            (form, form.save(*args, **kwargs))
            for form in self.instances
        ]


class Hook(object):
    """
    Container of forms

    :param list providing_args: A list of the arguments\
    this hook can pass along in a :py:func:`.__call__`
    """
    def __init__(self, providing_args=None):
        self.providing_args = providing_args or []
        self._registry = []

    def __call__(self, *args, **kwargs):
        """
        Call all registered forms

        :param str prefix: Prefix for the forms to avoid clashing of fields,\
        it must be of the form ``text_%d``. Defaults to ``hook%d``
        :param \*args: Positional arguments passed to the forms
        :param \*\*kwargs: Keyword arguments passed to the forms
        :return: Factory to handle all the forms as they were one
        :rtype: :py:class:`HookFactory`
        """
        prefix = kwargs.pop('prefix', 'hook%d')

        return HookFactory(
            instances=[
                form(prefix=self._prefix(prefix, i), *args, **kwargs)  # todo: update kwargs is cleaner
                for i, form in enumerate(self._registry)
            ]
        )

    @staticmethod
    def _prefix(prefix, i):
        return prefix % i

    def register(self, form):
        """
        Register form

        :param callable form: The form, usually\
        :py:class:`django.forms.Form` or\
        :py:class:`django.forms.ModelForm`
        """
        assert callable(form), \
            "Form must be callable"

        self._registry.append(form)

    def unregister(self, form):
        """
        Remove form from registry

        :param callable form: The previously registered form
        """
        try:
            self._registry.remove(form)
        except ValueError:
            pass
