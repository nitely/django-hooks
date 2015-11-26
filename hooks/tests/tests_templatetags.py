# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase
from django.template import Template, Context
from django.utils.html import mark_safe

from hooks.templatehook import hook
from hooks.templatetags.hooks_tags import template_hook_collect
from . import utils_hooks


class HookTagTest(TestCase):

    def setUp(self):
        self.hook_name = 'myhook'
        hook.unregister_all(self.hook_name)
        utils_hooks.myhook.unregister_all()

    def test_hook_tag(self):
        def func(context, *args, **kwargs):
            self.assertEqual(args, ("foobar", ))
            self.assertEqual(kwargs, {'bar': "bar", })
            self.assertEqual(context['foo'], "foo")
            return "hello"

        hook.register(self.hook_name, func)

        out = Template(
            "{% load hooks_tags %}"
            "{% hook hook_name 'foobar' bar='bar' %}"
        ).render(Context({"hook_name": self.hook_name, "foo": "foo", }))
        self.assertEqual(out, u"hello")

    def test_hook_tag_many(self):
        """
        Should join multiple responses
        """
        def func_a(*args, **kwargs):
            return "hello"

        def func_b(*args, **kwargs):
            return "goodbye"

        hook.register(self.hook_name, func_a)
        hook.register(self.hook_name, func_b)

        out = Template(
            "{% load hooks_tags %}"
            "{% hook hook_name 'foobar' %}"
        ).render(Context({"hook_name": self.hook_name, }))

        self.assertEqual(out, "hello\ngoodbye")

    def test_hook_tag_escaped(self):
        """
        Should escape responses (if they are not marked as safe)
        """
        def func(*args, **kwargs):
            return "<span>hello</span>"

        hook.register(self.hook_name, func)

        out = Template(
            "{% load hooks_tags %}"
            "{% hook hook_name 'foobar' %}"
        ).render(Context({"hook_name": self.hook_name, }))

        self.assertEqual(out, "&lt;span&gt;hello&lt;/span&gt;")

    def test_hook_tag_mark_safe(self):
        """
        Should not escape safe strings
        """
        def func(*args, **kwargs):
            return mark_safe("<span>hello</span>")

        hook.register(self.hook_name, func)

        out = Template(
            "{% load hooks_tags %}"
            "{% hook hook_name 'foobar' %}"
        ).render(Context({"hook_name": self.hook_name, }))

        self.assertEqual(out, "<span>hello</span>")

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

    def test_template_hook_collect_escaped(self):
        def func(*args, **kwargs):
            return "<span>hello</span>"

        utils_hooks.myhook.register(func)
        res = template_hook_collect(utils_hooks, 'myhook', "context", "foo", extra="bar")
        self.assertEqual(res, "&lt;span&gt;hello&lt;/span&gt;")
