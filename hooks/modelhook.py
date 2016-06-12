# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from django.db import models


logger = logging.getLogger('django')


def _is_abstract_model_check(klass):
    if not issubclass(klass, models.Model):
        raise ValueError(
            "{} must inherit from {}"
            .format(klass.__name__, models.Model.__name__))

    if not klass._meta.abstract:
        raise ValueError(
            "{} must be abstract"
            .format(klass.__name__))


class ModelHook(object):

    def __init__(self):
        self._registry = []

    @property
    def plugins(self):
        """
        Create a new class dynamically,\
        inheriting all registered plugins.

        This is similar to::

            class MyAppModel(*plugins, ...):

        Except that's not a valid syntax in Python 2.7

        :return: A new model inheriting from\
        all registered plugins
        """
        class DummyBase(object):
            """"""

        class Plugins(DummyBase):
            class Meta:
                abstract = True

        return type(
            Plugins.__name__,
            tuple(self._registry) + (models.Model, ),  # bases
            dict(Plugins.__dict__))

    def register(self, model_class):
        _is_abstract_model_check(model_class)

        if model_class in self._registry:
            return

        self._registry.append(model_class)
