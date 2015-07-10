#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
import logging

import django

try:
    from django.test.runner import DiscoverRunner
except ImportError:
    from discover_runner import DiscoverRunner


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_test_runner'


def log_warnings():
    logger = logging.getLogger('py.warnings')
    handler = logging.StreamHandler()
    logger.addHandler(handler)


def run_tests():
    test_runner = DiscoverRunner()
    failures = test_runner.run_tests(["hooks", ])
    sys.exit(failures)


def start():
    django.setup()
    log_warnings()
    run_tests()


if __name__ == "__main__":
    start()
