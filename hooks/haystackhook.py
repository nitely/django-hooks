# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from haystack import indexes


logger = logging.getLogger('django')


def hook(*klasses):
    class SearchIndexHook(*klasses, indexes.Indexable):
        """"""

    return SearchIndexHook


class HaystackHook(object):

    def __init__(self):
        self._registry = []

    def register(self, search_class):
        assert not issubclass(
            search_class,
            (indexes.SearchIndex, indexes.Indexable)
        ), "Registered class can not inherit from SearchIndex or Indexable"

        self._registry.append(search_class)

    def build_search_index(self, base_class):
        assert issubclass(base_class, indexes.SearchIndex), \
            "base_class must inherit from SearchIndex"

        logger.info("Building search index with {}".format(self._registry))
        return hook(base_class, *self._registry)
