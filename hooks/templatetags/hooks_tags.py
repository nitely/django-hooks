#-*- coding: utf-8 -*-

from django import template

from hooks.templatehook import hook


register = template.Library()


@register.simple_tag(name="hook", takes_context=True)
def hook_tag(context, name, *args, **kwargs):
    return u"\n".join(hook(name, context, *args, **kwargs))


def template_hook_collect(module, hook_name, *args, **kwargs):
    """
    Helper to include in your own templatetag, for static TemplateHooks.

    example:
    import myhooks
    from hooks.templatetags import template_hook_collect

    @register.simple_tag(takes_context=True)
    def hook(context, name, *args, **kwargs):
        return template_hook_collect(myhooks, name, context, *args, **kwargs)
    """
    try:
        templatehook = getattr(module, hook_name)
    except AttributeError:
        return u""

    responses = templatehook(*args, **kwargs)
    return u"\n".join(responses)