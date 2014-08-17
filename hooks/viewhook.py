#-*- coding: utf-8 -*-

"""
API example

# app/hooks.py
myview = Hook()

# app/views.py
def myview(request):
    ...
    hook = hooks.myview(request)
    hook.dispatch()

    if is_post:
        ...
        hook.post()

        if hook.is_valid() and ...:
            ...
            hook.save()
            redirect('/')
    else:
        ...
        hook.get()

    context = {'foo': foobar, }
    context.update(hook.context)

    return response(context)
"""

__all__ = ["Hook", "HookBase"]


class HookBase(object):
    """
    View hooks should subclass this.
    """
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.context = {}

    def dispatch(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        """
        Should get call on GET request.
        Returns None.
        """
        pass

    def post(self, *args, **kwargs):
        """
        Should get call on POST request.
        You should define all your form here,
        add forms to kwargs so you can validate them later.
        Returns None.
        """
        pass

    def is_valid(self):
        """
        Should get call on validate forms.
        Returns True if valid or False otherwise.
        """
        return True

    def save(self, *args, **kwargs):
        """
        Save forms.
        Returns None.
        """
        pass


class HookProxy(object):

    def __init__(self, registry, *args, **kwargs):
        self._hooks = [hook(*args, **kwargs) for hook in registry]

    def dispatch(self, *args, **kwargs):
        for hook in self._hooks:
            hook.dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        for hook in self._hooks:
            hook.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        for hook in self._hooks:
            hook.post(*args, **kwargs)

    def is_valid(self):
        # Validate all so errors are attached
        return all([hook.is_valid() for hook in self._hooks])

    def save(self, *args, **kwargs):
        for hook in self._hooks:
            hook.save(*args, **kwargs)

    @property
    def context(self):
        context = {}

        for hook in self._hooks:
            context.update(hook.context)

        return context


class Hook(object):

    def __init__(self):
        self._registry = []

    def __call__(self, *args, **kwargs):
        return HookProxy(self._registry, *args, **kwargs)

    def register(self, hook):
        """
        Register a hook.

        @hook: a HookBase subclass reference.
        """
        assert callable(hook), \
            "Hook must be a callable"
        assert issubclass(hook, HookBase), \
            "The hook does not inherit from HookBase"

        self._registry.append(hook)

    def unregister(self, hook):
        """
        Unregister a hook.

        @hook: a HookBase subclass reference.
        """
        try:
            self._registry.remove(hook)
        except ValueError:
            pass