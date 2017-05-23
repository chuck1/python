# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climb', '0002_auto_20150611_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wall',
            name='area',
            field=models.ForeignKey(to='climb.Area', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wall',
            name='location',
            field=models.ForeignKey(to='climb.Location', null=True),
            preserve_default=True,
        ),
    ]
