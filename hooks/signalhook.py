#-*- coding: utf-8 -*-

from django.dispatch import Signal


__all__ = ['hook', ]


class Hook(object):
    """
    A dynamic-signal dispatcher.

    thread-safety: it's not thread safe, this may change
    in the future if a RLock is added around _registry operations.
    In the meanwhile, you should register/connect/disconnect
    at import time (global scope) to ensure thread-safety,
    models.py and urls.py are good places (django<=1.6)
    or do it in the AppConfig.ready() method (django>=1.7).
    """
    def __init__(self):
        self._registry = {}

    def register(self, name):
        """
        Registers a new hook. Not required (see connect method).

        @name: the hook name.
        """
        signal = Signal(providing_args=['args', 'kwargs'])
        self._registry[name] = signal
        return signal

    def connect(self, name, func, sender=None, dispatch_uid=None):
        """
        Connects a function to a hook. Creates the hook-name if it does not exists.

        @name: the hook name.
        @func: a function reference, must return a string.
        @sender: optional sender __class__ to which this func should respond. Default will match all.
        @dispatch_uid: optional unique id, see django Signals for more info.
        """
        try:
            signal = self._registry[name]
        except KeyError:
            signal = self.register(name)

        signal.connect(func, sender=sender, dispatch_uid=dispatch_uid)

    def disconnect(self, name, func, dispatch_uid=None):
        """
        Disconnects a function from a hook.

        @name: the hook name.
        @func: a function reference.
        @dispatch_uid: optional unique id, see django Signals for more info.
        """
        try:
            signal = self._registry[name]
        except KeyError:
            return

        signal.disconnect(func, dispatch_uid=dispatch_uid)

    def send(self, name, sender=None, **kwargs):
        """
        Sends the signal. Returns every function response
        that was hooked to hook-name as a list: [(func, response), ].

        @name: the hook name.
        @sender: optional sender __class__, see connect method.
        """
        try:
            signal = self._registry[name]
        except KeyError:
            return []

        return signal.send(sender=sender, **kwargs)

hook = Hook()