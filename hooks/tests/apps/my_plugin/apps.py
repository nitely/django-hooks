# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig


class MyPluginConfig(AppConfig):

    name = 'hooks.tests.apps.my_plugin'
    verbose_name = "Hooks My Plugin"
    label = 'hooks_my_plugin'

