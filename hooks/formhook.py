# -*- coding: utf-8 -*-

from __future__ import unicode_literals


__all__ = ['Hook']


class HookFactory(object):

    def __init__(self, instances):
        self.instances = instances

    def __iter__(self):
        for form in self.instances:
            yield form

    def is_valid(self):
        # Avoid short-circuit evaluation
        return all([form.is_valid() for form in self.instances])

    def save(self, *args, **kwargs):
        return [form.save(*args, **kwargs) for form in self.instances]


class Hook(object):

    def __init__(self, providing_args=None):
        self.providing_args = providing_args or []
        self._registry = []

    def __call__(self, *args, **kwargs):
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
        assert callable(form), \
            "Form must be callable"

        self._registry.append(form)

    def unregister(self, form):
        try:
            self._registry.remove(form)
        except ValueError:
            pass
