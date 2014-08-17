#-*- coding: utf-8 -*-

import mock

from django.test import TestCase

from hooks.viewhook import HookBase, HookProxy, Hook


class HookBaseTest(TestCase):

    def setUp(self):
        pass

    def test_instance(self):
        hook = HookBase("request", "foo", extra="bar")
        self.assertEqual(hook.request, "request")
        self.assertEqual(hook.args, ("foo", ))
        self.assertDictEqual(hook.kwargs, {'extra': "bar", })
        self.assertDictEqual(hook.context, {})

    def test_methods(self):
        hook = HookBase("request")
        self.assertIsNone(hook.dispatch("foo", extra="bar"))
        self.assertIsNone(hook.get("foo", extra="bar"))
        self.assertIsNone(hook.post("foo", extra="bar"))
        self.assertTrue(hook.is_valid())
        self.assertIsNone(hook.save("foo", extra="bar"))


def test_proxy_method(func_name):
    hook_a = mock.MagicMock()
    hook_b = mock.MagicMock()
    proxy = HookProxy([])
    proxy._hooks = [hook_a, hook_b]

    func = getattr(proxy, func_name)
    func("foo", extra="bar")

    mocked = getattr(hook_a, func_name)
    mocked.assert_called_once_with("foo", extra="bar")

    mocked = getattr(hook_b, func_name)
    mocked.assert_called_once_with("foo", extra="bar")


class HookProxyTest(TestCase):

    def setUp(self):
        pass

    def test_instance(self):
        hook_a = mock.MagicMock()
        hook_b = mock.MagicMock()
        proxy = HookProxy([hook_a, hook_b], "request", "foo", extra="bar")
        hook_a.assert_called_once_with("request", "foo", extra="bar")
        hook_b.assert_called_once_with("request", "foo", extra="bar")

    def test_methods(self):
        test_proxy_method("dispatch")
        test_proxy_method("get")
        test_proxy_method("post")
        test_proxy_method("save")
        self.assertRaises(AttributeError, test_proxy_method, "foo")

    def test_is_valid(self):
        hook_a = mock.MagicMock()
        hook_b = mock.MagicMock()
        hook_a.is_valid.return_value = True
        hook_b.is_valid.return_value = True
        proxy = HookProxy([])
        proxy._hooks = [hook_a, hook_b]
        self.assertTrue(proxy.is_valid())
        hook_a.is_valid.assert_called_once_with()
        hook_b.is_valid.assert_called_once_with()

        hook_a.is_valid.return_value = False
        hook_b.is_valid.return_value = True
        hook_a.reset_mock()
        hook_b.reset_mock()
        self.assertFalse(proxy.is_valid())
        hook_a.is_valid.assert_called_once_with()
        hook_b.is_valid.assert_called_once_with()

        hook_a.is_valid.return_value = True
        hook_b.is_valid.return_value = False
        hook_a.reset_mock()
        hook_b.reset_mock()
        self.assertFalse(proxy.is_valid())
        hook_a.is_valid.assert_called_once_with()
        hook_b.is_valid.assert_called_once_with()

        hook_a.is_valid.return_value = False
        hook_b.is_valid.return_value = False
        hook_a.reset_mock()
        hook_b.reset_mock()
        self.assertFalse(proxy.is_valid())
        hook_a.is_valid.assert_called_once_with()
        hook_b.is_valid.assert_called_once_with()

        # if there are no hooks registered, should be valid
        proxy2 = HookProxy([])
        self.assertTrue(proxy2.is_valid())

    def test_context(self):
        hook_a = mock.MagicMock()
        hook_b = mock.MagicMock()
        hook_a.context = {"hook_a": "foo", }
        hook_b.context = {"hook_b": "foo", }
        proxy = HookProxy([])
        proxy._hooks = [hook_a, hook_b]
        self.assertDictEqual(proxy.context, {"hook_a": "foo", "hook_b": "foo"})


class HookTest(TestCase):

    def setUp(self):
        pass

    def test_register(self):
        class BadHook:
            """"""

        class GoodHook(HookBase):
            """"""

        hook = Hook()
        self.assertRaises(AssertionError, hook.register, BadHook)
        self.assertRaises(AssertionError, hook.register, GoodHook("req"))

        hook.register(GoodHook)
        self.assertListEqual(hook._registry, [GoodHook, ])

    def test_unregister(self):
        class GoodHook(HookBase):
            """"""

        hook = Hook()
        hook.register(GoodHook)
        self.assertListEqual(hook._registry, [GoodHook, ])
        hook.unregister(GoodHook)
        self.assertListEqual(hook._registry, [])

        # calling unregister again should do nothing
        hook.unregister(GoodHook)
        self.assertListEqual(hook._registry, [])

    def test_call(self):
        hook = Hook()

        with mock.patch.object(HookProxy, '__init__') as mock_init:
            mock_init.return_value = None
            proxy = hook("foo", extra="bar")
            mock_init.assert_called_once_with(hook._registry, "foo", extra="bar")
            self.assertIsInstance(proxy, HookProxy)