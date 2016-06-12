# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models

from ..my_app.hooks import MyModelHook


class MyPlugin(models.Model):

    my_plugin_subtitle = models.CharField(max_length=75)

    class Meta:
        abstract = True


class MyPluginB(models.Model):

    my_plugin_description = models.CharField(max_length=75)

    class Meta:
        abstract = True


MyModelHook.register(MyPlugin)
MyModelHook.register(MyPluginB)
