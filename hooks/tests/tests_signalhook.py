#-*- coding: utf-8 -*-

from django.test import TestCase

from django.dispatch import Signal
from hooks.signalhook import hook


class MockSignal:
    def __init__(self, providing_args=None):
        self.providing_args = providing_args

    def connect(self, func, sender=None, dispatch_uid=None):
        self.func = func
        self.sender = sender
        self.dispatch_uid = dispatch_uid

    def disconnect(self, func, dispatch_uid=None):
        self.func = func
        self.dispatch_uid = dispatch_uid

    def send(self, sender=None, **kwargs):
        self.sender = sender
        self.kwargs = kwargs


class FakeHook:
    """"""


class SignalHookTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        hook._registry.clear()

    def test_register(self):
        signal = hook.register("foo-hook")
        self.assertIsInstance(signal, Signal)

    def test_connect(self):
        def func():
            pass

        mocksignal = MockSignal()
        hook._registry["foo-hook"] = mocksignal

        hook.connect("foo-hook", func, sender=FakeHook, dispatch_uid="foo")
        self.assertEqual([mocksignal.func, mocksignal.sender, mocksignal.dispatch_uid],
                         [func, FakeHook, "foo"])

    def test_disconnect(self):
        def func():
            pass

        mocksignal = MockSignal()
        hook._registry["foo-hook"] = mocksignal

        hook.disconnect("foo-hook", func, dispatch_uid="foo")
        self.assertEqual([mocksignal.func, mocksignal.dispatch_uid],
                         [func, "foo"])

    def test_send(self):
        mocksignal = MockSignal()
        hook._registry["foo-hook"] = mocksignal

        hook.send("foo-hook", sender=FakeHook, extra="foobar")
        self.assertEqual([mocksignal.sender, mocksignal.kwargs],
                         [FakeHook, {'extra': "foobar", }])

    def test_connect_and_send(self):
        """
        Integration test
        """
        def func_a(signal, sender, **kwargs):
            self._kwargs_a = kwargs

        def func_b(signal, sender, extra, **kwargs):
            self._extra_b = extra

        def func_c(sender, extra, **kwargs):
            self._extra_c = extra

        def func_d(extra, **kwargs):
            # kwargs will contain *sender* and *signal*
            self._extra_d = extra

        hook.connect("foo-hook", func_a, sender=FakeHook)
        hook.connect("foo-hook", func_b, sender=FakeHook)
        hook.connect("foo-hook", func_c, sender=FakeHook)
        hook.connect("foo-hook", func_d, sender=FakeHook)
        hook.send("foo-hook", sender=FakeHook, extra="foobar")
        self.assertDictEqual(self._kwargs_a, {'extra': "foobar", })
        self.assertEqual(self._extra_b, "foobar")
        self.assertEqual(self._extra_c, "foobar")
        self.assertEqual(self._extra_d, "foobar")