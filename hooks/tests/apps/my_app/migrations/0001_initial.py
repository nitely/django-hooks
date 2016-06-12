# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyAppModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('my_plugin_subtitle', models.CharField(max_length=75)),
                ('my_plugin_description', models.CharField(max_length=75)),
                ('title', models.CharField(max_length=75)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
