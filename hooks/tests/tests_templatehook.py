#-*- coding: utf-8 -*-

from django.test import TestCase

from hooks.templatehook import TemplateHook, hook


class TemplateHookTest(TestCase):

    def setUp(self):
        pass

    def test_instance(self):
        myhook = TemplateHook(providing_args=["foo", "bar"])
        self.assertListEqual(myhook.providing_args, ["foo", "bar"])

    def test_register(self):
        def func():
            pass

        myhook = TemplateHook()
        myhook.register(func)
        self.assertListEqual(myhook._registry, [func, ])

        # try to register a non callable
        self.assertRaises(AssertionError, myhook.register, "foo")

    def test_unregister(self):
        def func():
            pass

        # register new callback
        myhook = TemplateHook()
        myhook.register(func)
        self.assertListEqual(myhook._registry, [func, ])

        # unregister callback
        myhook.unregister(func)
        self.assertListEqual(myhook._registry, [])

        # try to unregister twice should do nothing
        myhook.unregister(func)
        self.assertListEqual(myhook._registry, [])

    def test_call(self):
        def func_a(*args, **kwargs):
            self._args_a = args
            self._kwargs_a = kwargs
            return "im func_a"

        def func_b(*args, **kwargs):
            self._args_b = args
            self._kwargs_b = kwargs
            return "im func_b"

        # initial hook should not have registered callbacks
        myhook = TemplateHook()
        self.assertListEqual(myhook(), [])

        # calling hook should return a list of callback responses
        myhook.register(func_a)
        myhook.register(func_b)
        self.assertListEqual(myhook(), ["im func_a", "im func_b"])

        # passing arguments to callbacks should be ok
        myhook("foo", extra="bar")
        self.assertEqual(self._args_a, ("foo", ))
        self.assertDictEqual(self._kwargs_a, {'extra': "bar", })

        self.assertEqual(self._args_b, ("foo", ))
        self.assertDictEqual(self._kwargs_b, {'extra': "bar", })


class HookTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        hook._registry.clear()

    def test_register(self):
        def func_a():
            pass

        def func_b():
            pass

        hook.register("foo-hook", func_a)
        self.assertIsInstance(hook._registry["foo-hook"], TemplateHook)
        self.assertListEqual(hook._registry["foo-hook"]._registry, [func_a, ])

        hook.register("foo-hook", func_b)
        self.assertListEqual(hook._registry["foo-hook"]._registry, [func_a, func_b])

    def test_unregister(self):
        def func():
            pass

        hook.register("foo-hook", func)
        hook.unregister("foo-hook", func)
        self.assertListEqual(hook._registry["foo-hook"]._registry, [])

    def test_call(self):
        def template_hock_mock(*args, **kwargs):
            self._args = args
            self._kwargs = kwargs
            return "ok"

        # empty hook
        self.assertListEqual(hook("foo-hook"), [])

        hook._registry["foo-hook"] = template_hock_mock
        response = hook("foo-hook", "foo", extra="bar")
        self.assertEqual(response, "ok")
        self.assertEqual(self._args, ("foo", ))
        self.assertDictEqual(self._kwargs, {'extra': "bar", })