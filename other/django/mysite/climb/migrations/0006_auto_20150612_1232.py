# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climb', '0005_auto_20150612_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='location',
            field=models.ForeignKey(default=None, to='climb.Location'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='route',
            name='wall',
            field=models.ForeignKey(default=None, to='climb.Wall'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wall',
            name='area',
            field=models.ForeignKey(default=None, to='climb.Area'),
            preserve_default=False,
        ),
    ]
