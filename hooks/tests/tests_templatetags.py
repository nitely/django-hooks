#-*- coding: utf-8 -*-

from django.test import TestCase
from django.template import Template, Context

from hooks.templatehook import hook
from hooks.templatetags.hooks_tags import template_hook_collect
from . import utils_hooks


class HookTagTest(TestCase):

    def setUp(self):
        pass

    def test_hook_tag(self):
        def func(context, *args, **kwargs):
            self.assertEqual(args, ("foobar", ))
            self.assertEqual(kwargs, {'bar': "bar", })
            self.assertEqual(context['foo'], "foo")
            return "hello"

        hook.register('myhook', func)

        out = Template(
            "{% load hooks_tags %}"
            "{% hook 'myhook' 'foobar' bar='bar' %}"
        ).render(Context({"foo": "foo", }))
        self.assertEqual(out, u"hello")

    def test_template_hook_collect(self):
        def func(context, *args, **kwargs):
            self.assertEqual(context, "context")
            self.assertEqual(args, ("foo", ))
            self.assertEqual(kwargs, {'extra': "bar", })
            return "hello"

        utils_hooks.myhook.register(func)
        res = template_hook_collect(utils_hooks, 'myhook', "context", "foo", extra="bar")
        self.assertEqual(res, u"hello")

        res = template_hook_collect(utils_hooks, 'badhook')
        self.assertEqual(res, u"")