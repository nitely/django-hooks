# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import warnings


class RemovedInNextMajorVersionWarning(DeprecationWarning):
    """"""


def warn(message):
    warnings.warn(message, RemovedInNextMajorVersionWarning)


warnings.simplefilter("default", RemovedInNextMajorVersionWarning)
