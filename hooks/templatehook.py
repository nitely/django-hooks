#-*- coding: utf-8 -*-


__all__ = ['hook', 'TemplateHook']


class TemplateHook(object):
    """
    A hook for templates. This can be used directly or through the Hook dispatcher.
    """
    def __init__(self, providing_args=None):
        """
        @providing_args: A list of the arguments this hook can pass along in a __call__.
        """
        self.providing_args = providing_args or []
        self._registry = []

    def __call__(self, *args, **kwargs):
        """
        Collect all callbacks responses for this template hook.
        Returns a list of responses.
        """
        return [func(*args, **kwargs) for func in self._registry]

    def register(self, func):
        """
        Register a new callback.
        @func: a func reference (callback).
        """
        assert callable(func), \
            "Callback func must be a callable"

        self._registry.append(func)

    def unregister(self, func):
        """
        Unregister a previously registered callback.
        @hook: a func reference (callback).
        """
        try:
            self._registry.remove(func)
        except ValueError:
            pass


class Hook(object):
    """
    Dynamic dispatcher for template hooks.
    """
    def __init__(self):
        self._registry = {}

    def __call__(self, name, *args, **kwargs):
        """
        Collect all callbacks responses for this template hook.
        @name: hook name.
        Returns a list of responses.
        """
        try:
            templatehook = self._registry[name]
        except KeyError:
            return []

        return templatehook(*args, **kwargs)

    def _register(self, name):
        templatehook = TemplateHook()
        self._registry[name] = templatehook
        return templatehook

    def register(self, name, func):
        """
        Register a new callback.
        @name: hook name.
        @func: a func reference (callback).
        """
        try:
            templatehook = self._registry[name]
        except KeyError:
            templatehook = self._register(name)

        templatehook.register(func)

    def unregister(self, name, func):
        """
        Unregister a callback.
        @name: hook name.
        @func: a func reference (callback).
        """
        try:
            templatehook = self._registry[name]
        except KeyError:
            return

        templatehook.unregister(func)


hook = Hook()