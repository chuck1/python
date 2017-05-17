# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='area',
            field=models.ForeignKey(to='climb.Area', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='route',
            name='location',
            field=models.ForeignKey(to='climb.Location', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='route',
            name='wall',
            field=models.ForeignKey(to='climb.Wall', null=True),
            preserve_default=True,
        ),
    ]
