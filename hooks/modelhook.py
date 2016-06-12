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
            .format(klass.__name__, models.Model.__name__))


class ModelHook(object):

    def __init__(self):
        self._registry = []

    @property
    def plugins(self):
        return self._registry

    def register(self, model_class):
        _is_abstract_model_check(model_class)

        if model_class in self._registry:
            return

        self._registry.append(model_class)

