# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig


class MyAppConfig(AppConfig):

    name = 'hooks.tests.apps.my_app'
    verbose_name = "Hooks My App"
    label = 'hooks_my_app'

