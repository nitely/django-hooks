# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from .hooks import MyModelHook


class MyAppModel(*MyModelHook.plugins, models.Model):

    title = models.CharField(max_length=75)

