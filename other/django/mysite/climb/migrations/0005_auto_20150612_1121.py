# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climb', '0004_auto_20150611_1128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='area',
        ),
        migrations.RemoveField(
            model_name='route',
            name='location',
        ),
        migrations.RemoveField(
            model_name='wall',
            name='location',
        ),
    ]
