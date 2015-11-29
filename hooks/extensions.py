# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os


__all__ = [
    'autodiscover',
    'apps',
    'urls'
]

apps = []
urls = []


def autodiscover(import_path, app_config='Extension'):
    # Relative path to the extension's package in
    # dot notation such as 'my_app.extensions'

    global apps, urls

    extensions_dir = os.path.join(os.getcwd(), *import_path.split('.'))
    apps_ = []
    urls_ = []

    for app in os.listdir(extensions_dir):
        app_import_path = '.'.join((import_path, app))

        if not os.path.isfile(os.path.join(extensions_dir, app, 'apps.py')):
            continue

        apps_.append(
            '.'.join((app_import_path, 'apps', app_config))
        )

        if not os.path.isfile(os.path.join(extensions_dir, app, 'urls.py')):
            continue

        urls_.append(
            '.'.join((app_import_path, 'urls'))
        )

    apps = apps_
    urls = urls_
