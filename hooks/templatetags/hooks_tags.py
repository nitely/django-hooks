# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template
from django.utils.html import format_html_join

from hooks.templatehook import hook


register = template.Library()


@register.simple_tag(name="hook", takes_context=True)
def hook_tag(context, name, *args, **kwargs):
    responses = ((response, ) for response in hook(name, context, *args, **kwargs))
    return format_html_join("\n", "{}", responses)


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
        return ""

    responses = ((response, ) for response in templatehook(*args, **kwargs))
    return format_html_join("\n", "{}", responses)