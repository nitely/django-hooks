# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.dispatch import Signal


__all__ = ['hook', ]


class Hook(object):
    """
    A dynamic-signal dispatcher.\
    Should be used through :py:data:`hook`

    thread-safety: it's not thread safe, this may change\
    in the future if a RLock is added around _registry operations.\
    In the meanwhile, you should register/connect/disconnect\
    at import time (global scope) to ensure thread-safety,\
    doing it in the AppConfig.ready() method is safe
    """
    def __init__(self):
        self._registry = {}

    def register(self, name):
        """
        Register a new hook. Not required (see :py:func:`.connect` method)

        :param str name: The hook name
        :return: Django signal
        :rtype: :py:class:`django.dispatch.Signal`
        """
        signal = Signal(providing_args=['args', 'kwargs'])
        self._registry[name] = signal
        return signal

    def connect(self, name, func, sender=None, dispatch_uid=None):
        """
        Connects a function to a hook.\
        Creates the hook (name) if it does not exists

        :param str name: The hook name
        :param callable func: A function reference used as a callback
        :param class sender: Optional sender __class__ to which the\
        func should respond. Default will match all
        :param str dispatch_uid: Optional unique id,\
        see :py:class:`django.dispatch.Signal` for more info
        """
        try:
            signal = self._registry[name]
        except KeyError:
            signal = self.register(name)

        signal.connect(func, sender=sender, dispatch_uid=dispatch_uid)

    def disconnect(self, name, func, dispatch_uid=None):
        """
        Disconnects a function from a hook

        :param str name: The hook name
        :param callable func: A function reference registered previously
        :param str dispatch_uid: optional unique id,\
        see :py:class:`django.dispatch.Signal` for more info.
        """
        try:
            signal = self._registry[name]
        except KeyError:
            return

        signal.disconnect(func, dispatch_uid=dispatch_uid)

    def send(self, name, sender=None, **kwargs):
        """
        Sends the signal. Return every function response\
        that was hooked to hook-name as a list: [(func, response), ]

        :param str name: The hook name
        :param class sender: Optional sender __class__ to which\
        registered callback should match (see :py:func:`.connect` method)
        :return: Signal responses as a sequence of tuples (func, response)
        :rtype: list
        """
        try:
            signal = self._registry[name]
        except KeyError:
            return []

        return signal.send(sender=sender, **kwargs)

hook = Hook()
