#-*- coding: utf-8 -*-

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_test_runner'

try:
    from django.test.runner import DiscoverRunner
except ImportError:
    from discover_runner import DiscoverRunner


def run_tests():
    test_runner = DiscoverRunner()
    failures = test_runner.run_tests(["hooks", ])
    sys.exit(failures)


if __name__ == "__main__":
    run_tests()