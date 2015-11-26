# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from django.test import TestCase
from django.forms import Form

from hooks.formhook import Hook


class FormMock(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def save(self, *args, **kwargs):
        return self

    def is_valid(self):
        return True


class FormHookTest(TestCase):

    def test_instance(self):
        myhook = Hook(providing_args=["foo", "bar"])
        self.assertListEqual(myhook.providing_args, ["foo", "bar"])

    def test_register(self):
        myhook = Hook()
        myhook.register(FormMock)
        self.assertListEqual(myhook._registry, [FormMock, ])

        # try to register a non callable
        self.assertRaises(AssertionError, myhook.register, "foo")

    def test_unregister(self):
        # register new callback
        myhook = Hook()
        myhook.register(FormMock)
        self.assertListEqual(myhook._registry, [FormMock, ])

        # unregister callback
        myhook.unregister(FormMock)
        self.assertListEqual(myhook._registry, [])

        # try to unregister twice should do nothing
        myhook.unregister(FormMock)
        self.assertListEqual(myhook._registry, [])

    def test_call(self):
        class MyForm(FormMock):
            """"""

        class MyForm2(FormMock):
            """"""

        myhook = Hook()
        myhook.register(MyForm)
        myhook.register(MyForm2)
        self.assertTrue(all(
            isinstance(f, FormMock)
            for f in myhook()
        ))

    def test_call_args(self):
        myhook = Hook()
        myhook.register(FormMock)
        forms = myhook('foo', bar='bar')
        self.assertListEqual(
            [(f.args, f.kwargs) for f in forms],
            [(('foo',), {'bar': 'bar', 'prefix': 'hook0'})]
        )

    def test_call_django_form(self):
        myhook = Hook()
        myhook.register(Form)
        forms = myhook({'data': 'foo'}, initial={'initial': 'bar'})
        self.assertListEqual(
            [(f.data, f.initial, f.prefix) for f in forms],
            [({'data': 'foo'}, {'initial': 'bar'}, 'hook0')]
        )

    def test_call_args_prefix(self):
        myhook = Hook()
        myhook.register(FormMock)
        myhook.register(FormMock)
        forms = myhook(prefix='foo_%d')
        self.assertListEqual(
            [f.kwargs for f in forms],
            [{'prefix': 'foo_0'}, {'prefix': 'foo_1'}]
        )

    def test_is_valid(self):
        myhook = Hook()
        myhook.register(FormMock)
        forms = myhook()
        self.assertTrue(forms.is_valid())

    def test_is_valid_many(self):
        class MyForm(FormMock):
            call_count = []

            def is_valid(self):
                self.call_count.append(True)
                return False

        myhook = Hook()
        myhook.register(MyForm)
        myhook.register(MyForm)
        forms = myhook()
        self.assertFalse(forms.is_valid())
        self.assertEqual(len(MyForm.call_count), 2)

    def test_is_save(self):
        class MyForm(FormMock):
            def save(self, *args, **kwargs):
                return args, kwargs

        myhook = Hook()
        myhook.register(MyForm)
        forms = myhook()
        self.assertEqual(
            forms.save('foo', bar='bar'),
            [(('foo',), {'bar': 'bar'}), ]
        )
